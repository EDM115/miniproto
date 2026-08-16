//! Stateful native codecs for Telegram TCP abridged, intermediate, and padded-intermediate frames.
//!
//! `TransportCodec` is exported to Python as `miniproto._native.TransportCodec` and mirrors the
//! Python fallback's framing contract.  It accepts arbitrary receive fragmentation, emits payload,
//! quick-ACK, and transport-error events, and returns Python exceptions for malformed or oversized
//! data rather than panicking. `FramePump` itself is Python-independent, but the PyO3 methods in
//! this module currently do not detach regular parsing or encoding work from the GIL; the GIL is
//! also required while their results are converted to Python objects.
//! Incompatible Python inputs retain PyO3's `TypeError`, `OverflowError`, or source conversion
//! exception; framing validation that runs after conversion intentionally returns `ValueError`.

use pyo3::IntoPyObjectExt;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyModule};
use pyo3::wrap_pyfunction;
use sha2::{Digest, Sha256};

/// Abridged header byte that introduces its three-byte word-length form.
const ABRIDGED_LONG_MARKER: u8 = 0x7f;
/// Wire bit that asks the peer to return a quick-ACK token.
const QUICK_ACK_MASK: u32 = 0x8000_0000;
/// Padded-intermediate payload marker identifying a quick-ACK response.
const PADDED_QUICK_ACK_MARKER: [u8; 4] = [0xff; 4];
/// Maximum random padding bytes allowed by padded-intermediate TCP framing.
const MAX_TRANSPORT_PADDING: usize = 15;
/// Largest drained receive-buffer allocation retained for later chunks.
const RETAINED_BUFFER_LIMIT: usize = 1024 * 1024;
/// Python `feed_data` event tuple: kind, payload, numeric detail, quick-ACK request flag.
type PythonFrameEvent = (u8, Vec<u8>, i64, bool);

/// Registers Python `TransportCodec` and `quick_ack_token` on `miniproto._native`.
///
/// Returns a PyO3 exception if either export cannot be installed.
///
/// # Arguments
///
/// - `m`: The Python extension module receiving the transport exports.
pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<TransportCodec>()?;
    m.add_function(wrap_pyfunction!(quick_ack_token, m)?)?;
    Ok(())
}

/// Computes the flagged quick-ACK token for Python `quick_ack_token`.
///
/// The 256-byte `auth_key` and nonempty encrypted portion of `encrypted_packet` are validated.
/// Returns the token with the quick-ACK bit set or `ValueError` for invalid packet/key input.
///
/// # Arguments
///
/// - `auth_key`: 256-byte MTProto authorization key used by the quick-ACK hash schedule.
/// - `encrypted_packet`: Full MTProto packet whose nonempty encrypted suffix is hashed.
#[pyfunction]
fn quick_ack_token(auth_key: &[u8], encrypted_packet: &[u8]) -> PyResult<u32> {
    if auth_key.len() != 256 {
        return Err(PyValueError::new_err("MTProto auth_key must be 256 bytes"));
    }
    let encrypted_portion = encrypted_packet
        .get(24..)
        .filter(|portion| !portion.is_empty())
        .ok_or_else(|| PyValueError::new_err("MTProto packet must contain an encrypted portion"))?;
    let digest = Sha256::new()
        .chain_update(&auth_key[88..120])
        .chain_update(encrypted_portion)
        .finalize();
    Ok(u32::from_le_bytes([digest[0], digest[1], digest[2], digest[3]]) | QUICK_ACK_MASK)
}

/// Supported Telegram TCP framing modes selected by their Python wire-name strings.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum TransportMode {
    /// TCP abridged framing with a word-count prefix.
    Abridged,
    /// TCP intermediate framing with a four-byte byte-count prefix.
    Intermediate,
    /// Intermediate framing with up to 15 random padding bytes.
    PaddedIntermediate,
}

impl TransportMode {
    /// Parses one Python transport mode name into its internal framing strategy.
    ///
    /// Returns `ValueError` for unsupported values.
    ///
    /// # Arguments
    ///
    /// - `value`: Python transport mode name to map to a framing variant.
    fn parse(value: &str) -> PyResult<Self> {
        match value {
            "tcp_abridged" => Ok(Self::Abridged),
            "tcp_intermediate" => Ok(Self::Intermediate),
            "tcp_padded_intermediate" => Ok(Self::PaddedIntermediate),
            _ => Err(PyValueError::new_err(format!(
                "unsupported transport mode: {value:?}"
            ))),
        }
    }
}

/// One native frame-pump result before it is converted to a Python return shape.
#[derive(Debug, Eq, PartialEq)]
enum FrameEvent {
    /// A complete MTProto payload and whether the peer requested a quick ACK.
    Payload {
        /// Complete transport payload with padding removed where relevant.
        payload: Vec<u8>,
        /// Whether the inbound header requested a quick-ACK response.
        quick_ack_requested: bool,
    },
    /// A quick-ACK token received from the peer.
    ///
    /// The contained `u32` is the wire token, including its quick-ACK mask bit.
    QuickAck(u32),
    /// A negative MTProto transport error received in its dedicated wire form.
    ///
    /// The contained `i32` is the peer-provided negative transport error code.
    TransportError(i32),
}

/// Python-visible incremental TCP framing codec, exported as `miniproto._native.TransportCodec`.
#[pyclass(module = "miniproto._native")]
struct TransportCodec {
    /// Stateful native parser and encoder backing this Python object.
    pump: FramePump,
}

#[pymethods]
impl TransportCodec {
    #[new]
    /// Creates `TransportCodec(mode, max_payload_size, server_side=False)`.
    ///
    /// `mode` must be a supported Python transport name and `max_payload_size` must be positive;
    /// otherwise this constructor raises `ValueError`.
    ///
    /// # Arguments
    ///
    /// - `mode`: One of the supported Python TCP mode names.
    /// - `max_payload_size`: Positive upper bound for decoded application payload bytes.
    /// - `server_side`: Whether inbound quick-ACK request bits remain payload metadata instead of
    ///   being interpreted as quick-ACK response frames.
    #[pyo3(signature = (mode, max_payload_size, server_side=false))]
    fn new(mode: &str, max_payload_size: usize, server_side: bool) -> PyResult<Self> {
        Ok(Self {
            pump: FramePump::new(TransportMode::parse(mode)?, max_payload_size, server_side)?,
        })
    }

    /// Encodes Python `encode_packet(payload, quick_ack=False)` into a single TCP frame.
    ///
    /// Returns `ValueError` for oversized payloads, invalid abridged alignment, length overflow,
    /// or operating-system randomness failure in padded mode.
    ///
    /// # Arguments
    ///
    /// - `payload`: Complete MTProto payload to frame.
    /// - `quick_ack`: Whether to set the outbound quick-ACK request bit where the mode supports it.
    #[pyo3(signature = (payload, quick_ack=false))]
    fn encode_packet(&self, payload: &[u8], quick_ack: bool) -> PyResult<Vec<u8>> {
        self.pump.encode_packet(payload, quick_ack)
    }

    /// Feeds Python `feed_data(data)` and returns tagged native event tuples.
    ///
    /// Tuple kinds are `0` payload, `1` quick ACK, and `2` negative transport error. It preserves
    /// incomplete trailing bytes for the next call and raises Python errors for invalid framing.
    ///
    /// # Arguments
    ///
    /// - `data`: Newly received TCP bytes to append to this codec's buffered stream.
    fn feed_data(&mut self, data: &[u8]) -> PyResult<Vec<PythonFrameEvent>> {
        self.pump.feed_data(data).map(|events| {
            events
                .into_iter()
                .map(|event| match event {
                    FrameEvent::Payload {
                        payload,
                        quick_ack_requested,
                    } => (0, payload, 0, quick_ack_requested),
                    FrameEvent::QuickAck(token) => (1, Vec::new(), i64::from(token), false),
                    FrameEvent::TransportError(code) => (2, Vec::new(), i64::from(code), false),
                })
                .collect()
        })
    }

    /// Feeds compatibility `feed_transport_data(data)` and returns bytes or integer Python events.
    ///
    /// The GIL token is used only for object conversion after native parsing; malformed framing
    /// returns a Python exception.
    ///
    /// # Arguments
    ///
    /// - `py`: The acquired GIL token used to build Python `bytes` and integer events.
    /// - `data`: Newly received TCP bytes to append to this codec's buffered stream.
    fn feed_transport_data(&mut self, py: Python<'_>, data: &[u8]) -> PyResult<Vec<Py<PyAny>>> {
        self.pump
            .feed_data(data)?
            .into_iter()
            .map(|event| match event {
                FrameEvent::Payload { payload, .. } => {
                    Ok(PyBytes::new(py, &payload).into_any().unbind())
                }
                FrameEvent::QuickAck(token) => token.into_py_any(py),
                FrameEvent::TransportError(code) => code.into_py_any(py),
            })
            .collect()
    }
}

/// GIL-free incremental parser/encoder retaining incomplete receive data between calls.
struct FramePump {
    /// Framing variant used for every operation.
    mode: TransportMode,
    /// Maximum permitted decoded MTProto payload size.
    max_payload_size: usize,
    /// Whether inbound quick-ACK request bits represent payload frames rather than ACK responses.
    server_side: bool,
    /// Accumulated unconsumed receive bytes.
    buffer: Vec<u8>,
    /// Leading consumed byte count within `buffer`.
    offset: usize,
}

impl FramePump {
    /// Creates a framed-stream pump after validating its positive payload limit.
    ///
    /// Returns `ValueError` for zero `max_payload_size`.
    ///
    /// # Arguments
    ///
    /// - `mode`: Internal TCP framing strategy for this pump.
    /// - `max_payload_size`: Positive upper bound for decoded application payload bytes.
    /// - `server_side`: Whether quick-ACK request bits are decoded as payload metadata.
    fn new(mode: TransportMode, max_payload_size: usize, server_side: bool) -> PyResult<Self> {
        if max_payload_size == 0 {
            return Err(PyValueError::new_err("max_payload_size must be positive"));
        }
        Ok(Self {
            mode,
            max_payload_size,
            server_side,
            buffer: Vec::new(),
            offset: 0,
        })
    }

    /// Encodes one payload using the pump's configured TCP transport mode.
    ///
    /// Returns `ValueError` for size/alignment violations or downstream frame construction errors.
    ///
    /// # Arguments
    ///
    /// - `payload`: Complete MTProto payload to frame.
    /// - `quick_ack`: Whether to set the outbound quick-ACK request bit where allowed.
    fn encode_packet(&self, payload: &[u8], quick_ack: bool) -> PyResult<Vec<u8>> {
        if payload.len() > self.max_payload_size {
            return Err(PyValueError::new_err(
                "transport payload exceeds configured maximum",
            ));
        }
        match self.mode {
            TransportMode::Abridged => self.encode_abridged(payload, quick_ack),
            TransportMode::Intermediate => self.encode_intermediate(payload, quick_ack),
            TransportMode::PaddedIntermediate => {
                self.encode_padded_intermediate(payload, quick_ack)
            }
        }
    }

    /// Encodes an abridged frame with a one- or four-byte word-count header.
    ///
    /// Returns `ValueError` unless `payload` is four-byte aligned and representable on the wire.
    ///
    /// # Arguments
    ///
    /// - `payload`: Four-byte-aligned MTProto payload to frame.
    /// - `quick_ack`: Whether to set abridged's quick-ACK request bit.
    fn encode_abridged(&self, payload: &[u8], quick_ack: bool) -> PyResult<Vec<u8>> {
        if !payload.len().is_multiple_of(4) {
            return Err(PyValueError::new_err(
                "tcp abridged payload length must be divisible by 4",
            ));
        }
        let length_words = payload.len() / 4;
        if length_words > 0xff_ffff {
            return Err(PyValueError::new_err("tcp abridged payload is too large"));
        }
        let header_length: usize = if length_words < usize::from(ABRIDGED_LONG_MARKER) {
            1
        } else {
            4
        };
        let total_length = header_length
            .checked_add(payload.len())
            .ok_or_else(|| PyValueError::new_err("tcp abridged frame length overflow"))?;
        let mut output = vec![0; total_length];
        if header_length == 1 {
            let length = u8::try_from(length_words)
                .map_err(|_| PyValueError::new_err("tcp abridged payload is too large"))?;
            output[0] = length | if quick_ack { 0x80 } else { 0 };
        } else {
            output[0] = if quick_ack {
                0xff
            } else {
                ABRIDGED_LONG_MARKER
            };
            let length_bytes = (length_words as u32).to_le_bytes();
            output[1..4].copy_from_slice(&length_bytes[..3]);
        }
        output[header_length..].copy_from_slice(payload);
        Ok(output)
    }

    /// Encodes an intermediate frame with a flagged four-byte byte-count header.
    ///
    /// Returns `ValueError` for unrepresentable transport lengths.
    ///
    /// # Arguments
    ///
    /// - `payload`: MTProto payload to frame.
    /// - `quick_ack`: Whether to set intermediate's quick-ACK request bit.
    fn encode_intermediate(&self, payload: &[u8], quick_ack: bool) -> PyResult<Vec<u8>> {
        let payload_length = u32::try_from(payload.len())
            .map_err(|_| PyValueError::new_err("tcp intermediate payload is too large"))?;
        if payload_length > i32::MAX as u32 {
            return Err(PyValueError::new_err(
                "tcp intermediate payload is too large",
            ));
        }
        encode_length_prefixed(payload, payload_length, quick_ack)
    }

    /// Encodes an intermediate frame with random zero-to-fifteen-byte padding.
    ///
    /// Returns `ValueError` for arithmetic, size, or operating-system randomness failures.
    ///
    /// # Arguments
    ///
    /// - `payload`: MTProto payload to frame before random transport padding.
    /// - `quick_ack`: Whether to set the intermediate quick-ACK request bit.
    fn encode_padded_intermediate(&self, payload: &[u8], quick_ack: bool) -> PyResult<Vec<u8>> {
        let mut random = [0_u8; 1];
        getrandom::fill(&mut random)
            .map_err(|error| PyValueError::new_err(format!("OS random failed: {error}")))?;
        let padding_length = usize::from(random[0] & MAX_TRANSPORT_PADDING as u8);
        let frame_length = payload.len().checked_add(padding_length).ok_or_else(|| {
            PyValueError::new_err("tcp padded intermediate frame length overflow")
        })?;
        let encoded_length = u32::try_from(frame_length)
            .map_err(|_| PyValueError::new_err("tcp padded intermediate payload is too large"))?;
        if encoded_length > i32::MAX as u32 {
            return Err(PyValueError::new_err(
                "tcp padded intermediate payload is too large",
            ));
        }
        let mut output = encode_length_prefixed(payload, encoded_length, quick_ack)?;
        let old_length = output.len();
        output.resize(old_length + padding_length, 0);
        if padding_length > 0 {
            getrandom::fill(&mut output[old_length..])
                .map_err(|error| PyValueError::new_err(format!("OS random failed: {error}")))?;
        }
        Ok(output)
    }

    /// Buffers `data`, parses every complete frame, and retains a partial suffix for later input.
    ///
    /// Returns parsed events or a Python exception for allocation, overflow, or invalid framing.
    ///
    /// # Arguments
    ///
    /// - `data`: Newly received TCP bytes to append before parsing complete frames.
    fn feed_data(&mut self, data: &[u8]) -> PyResult<Vec<FrameEvent>> {
        self.buffer
            .try_reserve(data.len())
            .map_err(|_| PyValueError::new_err("failed to allocate transport frame buffer"))?;
        self.buffer.extend_from_slice(data);
        let mut events = Vec::new();
        while let Some((event, consumed)) = self.parse_one()? {
            self.offset = self
                .offset
                .checked_add(consumed)
                .ok_or_else(|| PyValueError::new_err("transport frame offset overflow"))?;
            events.push(event);
        }
        self.compact();
        Ok(events)
    }

    /// Attempts to parse one complete frame without mutating the receive buffer.
    ///
    /// Returns `None` for an incomplete frame or a Python exception for malformed framing.
    fn parse_one(&self) -> PyResult<Option<(FrameEvent, usize)>> {
        match self.mode {
            TransportMode::Abridged => self.parse_abridged(),
            TransportMode::Intermediate => self.parse_intermediate(false),
            TransportMode::PaddedIntermediate => self.parse_intermediate(true),
        }
    }

    /// Parses one abridged frame or client-side quick-ACK response from buffered input.
    ///
    /// Returns `None` while incomplete and `ValueError` for oversized or overflowing frames.
    fn parse_abridged(&self) -> PyResult<Option<(FrameEvent, usize)>> {
        let available = self.buffer.len().saturating_sub(self.offset);
        if available < 1 {
            return Ok(None);
        }
        let mut first = self.buffer[self.offset];
        let quick_ack_requested = first & 0x80 != 0;
        if quick_ack_requested && !self.server_side {
            if available < 4 {
                return Ok(None);
            }
            let bytes = self.read_fixed::<4>(self.offset)?;
            return Ok(Some((FrameEvent::QuickAck(u32::from_be_bytes(bytes)), 4)));
        }
        if quick_ack_requested {
            first &= 0x7f;
        }
        let (header_length, payload_length): (usize, usize) = if first < ABRIDGED_LONG_MARKER {
            (1, usize::from(first) * 4)
        } else {
            if available < 4 {
                return Ok(None);
            }
            let bytes = self.read_slice(self.offset + 1, 3)?;
            let words = u32::from_le_bytes([bytes[0], bytes[1], bytes[2], 0]);
            (
                4,
                usize::try_from(words)
                    .unwrap_or(usize::MAX)
                    .saturating_mul(4),
            )
        };
        self.validate_frame_length(payload_length, false)?;
        let frame_length = header_length
            .checked_add(payload_length)
            .ok_or_else(|| PyValueError::new_err("transport frame length overflow"))?;
        if available < frame_length {
            return Ok(None);
        }
        let payload_start = self.offset + header_length;
        let payload = self.read_slice(payload_start, payload_length)?.to_vec();
        Ok(Some((
            self.payload_event(payload, false, quick_ack_requested)?,
            frame_length,
        )))
    }

    /// Parses one intermediate or padded-intermediate frame from buffered input.
    ///
    /// `padded` selects padded payload processing. Returns `None` while incomplete or `ValueError`
    /// for invalid lengths and protocol-incompatible quick-ACK forms.
    ///
    /// # Arguments
    ///
    /// - `padded`: Whether the wire payload carries padded-intermediate transport suffix bytes.
    fn parse_intermediate(&self, padded: bool) -> PyResult<Option<(FrameEvent, usize)>> {
        let available = self.buffer.len().saturating_sub(self.offset);
        if available < 4 {
            return Ok(None);
        }
        let raw_length = u32::from_le_bytes(self.read_fixed::<4>(self.offset)?);
        let has_quick_ack_bit = raw_length & QUICK_ACK_MASK != 0;
        if has_quick_ack_bit && !self.server_side {
            if padded {
                return Err(PyValueError::new_err(
                    "tcp padded intermediate server frame has the quick-ACK request bit set",
                ));
            }
            return Ok(Some((FrameEvent::QuickAck(raw_length), 4)));
        }
        let payload_length_u32 = if has_quick_ack_bit {
            raw_length & !QUICK_ACK_MASK
        } else {
            raw_length
        };
        let payload_length = usize::try_from(payload_length_u32)
            .map_err(|_| PyValueError::new_err("transport frame length overflow"))?;
        self.validate_frame_length(payload_length, padded)?;
        let frame_length = 4_usize
            .checked_add(payload_length)
            .ok_or_else(|| PyValueError::new_err("transport frame length overflow"))?;
        if available < frame_length {
            return Ok(None);
        }
        let payload = self.read_slice(self.offset + 4, payload_length)?.to_vec();
        Ok(Some((
            self.payload_event(payload, padded, has_quick_ack_bit)?,
            frame_length,
        )))
    }

    /// Converts a complete raw transport payload to an application, ACK, or error event.
    ///
    /// Removes and validates padded-intermediate suffix bytes when `padded`; returns `ValueError`
    /// for invalid encapsulated packet shape or a payload above the configured maximum.
    ///
    /// # Arguments
    ///
    /// - `payload`: Complete raw payload after its transport frame prefix.
    /// - `padded`: Whether to classify and remove padded-intermediate suffix bytes.
    /// - `quick_ack_requested`: Whether the inbound frame header requested a quick ACK.
    fn payload_event(
        &self,
        mut payload: Vec<u8>,
        padded: bool,
        quick_ack_requested: bool,
    ) -> PyResult<FrameEvent> {
        if padded {
            if (8..=16).contains(&payload.len()) && payload.starts_with(&PADDED_QUICK_ACK_MARKER) {
                let token = u32::from_le_bytes(to_fixed::<4>(&payload[4..8])?);
                return Ok(FrameEvent::QuickAck(token));
            }
            if (4..=4 + MAX_TRANSPORT_PADDING).contains(&payload.len()) {
                let code = i32::from_le_bytes(to_fixed::<4>(&payload[..4])?);
                if code < 0 {
                    return Ok(FrameEvent::TransportError(code));
                }
            }
            let packet_length = padded_packet_length(&payload)?;
            let padding_length = payload.len() - packet_length;
            if padding_length > MAX_TRANSPORT_PADDING {
                return Err(PyValueError::new_err(
                    "padded intermediate frame has too much transport padding",
                ));
            }
            if packet_length > self.max_payload_size {
                return Err(PyValueError::new_err(
                    "transport payload exceeds configured maximum",
                ));
            }
            payload.truncate(packet_length);
        } else if payload.len() == 4 {
            let code = i32::from_le_bytes(to_fixed::<4>(&payload)?);
            if code < 0 {
                return Ok(FrameEvent::TransportError(code));
            }
        }
        Ok(FrameEvent::Payload {
            payload,
            quick_ack_requested,
        })
    }

    /// Validates a declared frame payload length against this pump's configured maximum.
    ///
    /// Adds the allowed padded-mode suffix and returns `ValueError` on overflow or excess.
    ///
    /// # Arguments
    ///
    /// - `payload_length`: Declared transport payload size in bytes.
    /// - `padded`: Whether the frame may include up to `MAX_TRANSPORT_PADDING` bytes.
    fn validate_frame_length(&self, payload_length: usize, padded: bool) -> PyResult<()> {
        let maximum = self
            .max_payload_size
            .checked_add(if padded { MAX_TRANSPORT_PADDING } else { 0 })
            .ok_or_else(|| PyValueError::new_err("transport maximum frame length overflow"))?;
        if payload_length > maximum {
            return Err(PyValueError::new_err(
                "transport frame length exceeds configured maximum",
            ));
        }
        Ok(())
    }

    /// Borrows a checked range from the accumulated receive buffer.
    ///
    /// Returns `ValueError` rather than panicking on overflow or a truncated frame.
    ///
    /// # Arguments
    ///
    /// - `offset`: Absolute buffered-stream offset at which the range begins.
    /// - `length`: Number of bytes to borrow.
    fn read_slice(&self, offset: usize, length: usize) -> PyResult<&[u8]> {
        let end = offset
            .checked_add(length)
            .ok_or_else(|| PyValueError::new_err("transport frame offset overflow"))?;
        self.buffer
            .get(offset..end)
            .ok_or_else(|| PyValueError::new_err("transport frame ended unexpectedly"))
    }

    /// Reads an exactly `N`-byte receive-buffer field at `offset`.
    ///
    /// Returns `ValueError` for missing bytes.
    ///
    /// # Arguments
    ///
    /// - `N`: Compile-time field width to read.
    /// - `offset`: Absolute buffered-stream offset at which the field begins.
    fn read_fixed<const N: usize>(&self, offset: usize) -> PyResult<[u8; N]> {
        to_fixed(self.read_slice(offset, N)?)
    }

    /// Discards consumed data while retaining only bounded buffer capacity for future chunks.
    fn compact(&mut self) {
        if self.offset == 0 {
            return;
        }
        if self.offset == self.buffer.len() {
            if self.buffer.capacity() > RETAINED_BUFFER_LIMIT {
                self.buffer = Vec::new();
            } else {
                self.buffer.clear();
            }
            self.offset = 0;
            return;
        }
        if self.offset >= RETAINED_BUFFER_LIMIT || self.offset >= self.buffer.len() / 2 {
            self.buffer.drain(..self.offset);
            self.offset = 0;
        }
    }
}

/// Encodes a four-byte little-endian length prefix and payload, optionally setting quick-ACK bit.
///
/// Returns `ValueError` if header-plus-payload length overflows `usize`.
///
/// # Arguments
///
/// - `payload`: Bytes to follow the four-byte header.
/// - `payload_length`: Already validated wire length, excluding the header.
/// - `quick_ack`: Whether to set the intermediate quick-ACK request bit.
fn encode_length_prefixed(
    payload: &[u8],
    payload_length: u32,
    quick_ack: bool,
) -> PyResult<Vec<u8>> {
    let encoded_length = payload_length | if quick_ack { QUICK_ACK_MASK } else { 0 };
    let total_length = 4_usize
        .checked_add(payload.len())
        .ok_or_else(|| PyValueError::new_err("transport frame length overflow"))?;
    let mut output = vec![0; total_length];
    output[..4].copy_from_slice(&encoded_length.to_le_bytes());
    output[4..].copy_from_slice(payload);
    Ok(output)
}

/// Determines the embedded MTProto packet length within a padded-intermediate payload.
///
/// Returns `ValueError` for malformed unencrypted or encrypted packet shapes; it deliberately
/// does not treat arbitrary encrypted payload bytes as transport error indicators.
///
/// # Arguments
///
/// - `payload`: Padded-intermediate contents containing an embedded MTProto packet and suffix.
fn padded_packet_length(payload: &[u8]) -> PyResult<usize> {
    if payload.len() >= 20 && payload[..8] == [0; 8] {
        let body_length = i32::from_le_bytes(to_fixed::<4>(&payload[16..20])?);
        if body_length < 0 || body_length % 4 != 0 {
            return Err(PyValueError::new_err(
                "invalid unencrypted MTProto payload in padded intermediate frame",
            ));
        }
        let packet_length = 20_usize
            .checked_add(body_length as usize)
            .ok_or_else(|| PyValueError::new_err("unencrypted MTProto packet length overflow"))?;
        if packet_length > payload.len() {
            return Err(PyValueError::new_err(
                "invalid unencrypted MTProto payload in padded intermediate frame",
            ));
        }
        Ok(packet_length)
    } else {
        let remainder = payload.len().saturating_sub(8) % 16;
        let packet_length = payload.len().saturating_sub(remainder);
        if packet_length < 40 {
            return Err(PyValueError::new_err(
                "invalid encrypted MTProto payload in padded intermediate frame",
            ));
        }
        Ok(packet_length)
    }
}

/// Converts a slice to an exact fixed-width array for frame header decoding.
///
/// Returns `ValueError` rather than panicking on an unexpected length.
///
/// # Arguments
///
/// - `N`: Compile-time width required by the caller.
/// - `data`: Slice expected to contain exactly `N` bytes.
fn to_fixed<const N: usize>(data: &[u8]) -> PyResult<[u8; N]> {
    data.try_into()
        .map_err(|_| PyValueError::new_err("transport frame ended unexpectedly"))
}

/// Unit tests for TCP transport framing, fragmentation, and quick-ACK interpretation.
#[cfg(test)]
mod tests {
    use super::*;

    /// Four-byte-aligned payload fixture shared by framing tests.
    const PAYLOAD: [u8; 40] = [7; 40];

    #[test]
    /// Verifies fragmentation and coalescing behavior in every native TCP framing mode.
    fn all_modes_roundtrip_fragmented_and_coalesced_frames() {
        for mode in [
            TransportMode::Abridged,
            TransportMode::Intermediate,
            TransportMode::PaddedIntermediate,
        ] {
            let encoder = FramePump::new(mode, 1024, false).unwrap();
            let encoded = encoder.encode_packet(&PAYLOAD, false).unwrap();
            for split in 0..=encoded.len() {
                let mut decoder = FramePump::new(mode, 1024, false).unwrap();
                let mut events = decoder.feed_data(&encoded[..split]).unwrap();
                events.extend(decoder.feed_data(&encoded[split..]).unwrap());
                assert_eq!(
                    events,
                    vec![FrameEvent::Payload {
                        payload: PAYLOAD.to_vec(),
                        quick_ack_requested: false,
                    }]
                );
            }
            let mut decoder = FramePump::new(mode, 1024, false).unwrap();
            let coalesced = [encoded.as_slice(), encoded.as_slice()].concat();
            assert_eq!(decoder.feed_data(&coalesced).unwrap().len(), 2);
        }
    }

    #[test]
    /// Verifies server-side decoders preserve quick-ACK requests as payload metadata.
    fn server_side_decodes_quick_ack_request_bits() {
        for mode in [
            TransportMode::Abridged,
            TransportMode::Intermediate,
            TransportMode::PaddedIntermediate,
        ] {
            let encoder = FramePump::new(mode, 1024, false).unwrap();
            let encoded = encoder.encode_packet(&PAYLOAD, true).unwrap();
            let mut decoder = FramePump::new(mode, 1024, true).unwrap();
            assert_eq!(
                decoder.feed_data(&encoded).unwrap(),
                vec![FrameEvent::Payload {
                    payload: PAYLOAD.to_vec(),
                    quick_ack_requested: true,
                }]
            );
        }
    }

    #[test]
    /// Verifies client-side decoders recognize each published quick-ACK wire representation.
    fn client_side_decodes_all_quick_ack_wire_forms() {
        let token = 0x9234_5678_u32;
        let cases = [
            (TransportMode::Abridged, token.to_be_bytes().to_vec()),
            (TransportMode::Intermediate, token.to_le_bytes().to_vec()),
            (
                TransportMode::PaddedIntermediate,
                [
                    11_u32.to_le_bytes().as_slice(),
                    PADDED_QUICK_ACK_MARKER.as_slice(),
                    token.to_le_bytes().as_slice(),
                    b"pad",
                ]
                .concat(),
            ),
        ];
        for (mode, encoded) in cases {
            let mut decoder = FramePump::new(mode, 1024, false).unwrap();
            assert_eq!(
                decoder.feed_data(&encoded).unwrap(),
                vec![FrameEvent::QuickAck(token)]
            );
        }
    }

    #[test]
    /// Prevents abridged parsing from mistaking encrypted payload bytes for transport errors.
    fn abridged_does_not_peek_for_errors_inside_payload() {
        let mut payload = PAYLOAD;
        payload[..4].copy_from_slice(&(-429_i32).to_le_bytes());
        let encoder = FramePump::new(TransportMode::Abridged, 1024, false).unwrap();
        let encoded = encoder.encode_packet(&payload, false).unwrap();
        let mut decoder = FramePump::new(TransportMode::Abridged, 1024, false).unwrap();
        assert_eq!(
            decoder.feed_data(&encoded).unwrap(),
            vec![FrameEvent::Payload {
                payload: payload.to_vec(),
                quick_ack_requested: false,
            }]
        );
    }

    #[test]
    /// Ensures declared oversized frame length fails before payload accumulation.
    fn rejects_oversized_frame_at_header() {
        let mut decoder = FramePump::new(TransportMode::Intermediate, 4, false).unwrap();
        let error = decoder.feed_data(&8_u32.to_le_bytes()).unwrap_err();
        assert!(error.to_string().contains("exceeds configured maximum"));
    }

    #[test]
    /// Ensures a drained oversized receive allocation is dropped rather than retained.
    fn releases_oversized_receive_buffer_after_drain() {
        let payload = vec![7; RETAINED_BUFFER_LIMIT + 16];
        let encoder = FramePump::new(TransportMode::Intermediate, payload.len(), false).unwrap();
        let encoded = encoder.encode_packet(&payload, false).unwrap();
        let mut decoder =
            FramePump::new(TransportMode::Intermediate, payload.len(), false).unwrap();
        let events = decoder.feed_data(&encoded).unwrap();
        assert_eq!(events.len(), 1);
        assert!(decoder.buffer.is_empty());
        assert_eq!(decoder.buffer.capacity(), 0);
    }

    #[test]
    /// Locks down the published SHA-256 quick-ACK token vector.
    fn quick_ack_token_matches_published_sha256_vector() {
        let auth_key: Vec<u8> = (0_u8..=255).collect();
        let mut packet = vec![0x11; 8];
        packet.extend_from_slice(&[0x22; 16]);
        packet.extend(0_u8..64);
        assert_eq!(quick_ack_token(&auth_key, &packet).unwrap(), 0xd796_fd18);
    }
}
