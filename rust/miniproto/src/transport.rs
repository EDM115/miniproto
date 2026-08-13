use pyo3::IntoPyObjectExt;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyModule};
use pyo3::wrap_pyfunction;
use sha2::{Digest, Sha256};

const ABRIDGED_LONG_MARKER: u8 = 0x7f;
const QUICK_ACK_MASK: u32 = 0x8000_0000;
const PADDED_QUICK_ACK_MARKER: [u8; 4] = [0xff; 4];
const MAX_TRANSPORT_PADDING: usize = 15;
const RETAINED_BUFFER_LIMIT: usize = 1024 * 1024;
type PythonFrameEvent = (u8, Vec<u8>, i64, bool);

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<TransportCodec>()?;
    m.add_function(wrap_pyfunction!(quick_ack_token, m)?)?;
    Ok(())
}

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

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum TransportMode {
    Abridged,
    Intermediate,
    PaddedIntermediate,
}

impl TransportMode {
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

#[derive(Debug, Eq, PartialEq)]
enum FrameEvent {
    Payload {
        payload: Vec<u8>,
        quick_ack_requested: bool,
    },
    QuickAck(u32),
    TransportError(i32),
}

#[pyclass(module = "miniproto._native")]
struct TransportCodec {
    pump: FramePump,
}

#[pymethods]
impl TransportCodec {
    #[new]
    #[pyo3(signature = (mode, max_payload_size, server_side=false))]
    fn new(mode: &str, max_payload_size: usize, server_side: bool) -> PyResult<Self> {
        Ok(Self {
            pump: FramePump::new(TransportMode::parse(mode)?, max_payload_size, server_side)?,
        })
    }

    #[pyo3(signature = (payload, quick_ack=false))]
    fn encode_packet(&self, payload: &[u8], quick_ack: bool) -> PyResult<Vec<u8>> {
        self.pump.encode_packet(payload, quick_ack)
    }

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

struct FramePump {
    mode: TransportMode,
    max_payload_size: usize,
    server_side: bool,
    buffer: Vec<u8>,
    offset: usize,
}

impl FramePump {
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

    fn parse_one(&self) -> PyResult<Option<(FrameEvent, usize)>> {
        match self.mode {
            TransportMode::Abridged => self.parse_abridged(),
            TransportMode::Intermediate => self.parse_intermediate(false),
            TransportMode::PaddedIntermediate => self.parse_intermediate(true),
        }
    }

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

    fn read_slice(&self, offset: usize, length: usize) -> PyResult<&[u8]> {
        let end = offset
            .checked_add(length)
            .ok_or_else(|| PyValueError::new_err("transport frame offset overflow"))?;
        self.buffer
            .get(offset..end)
            .ok_or_else(|| PyValueError::new_err("transport frame ended unexpectedly"))
    }

    fn read_fixed<const N: usize>(&self, offset: usize) -> PyResult<[u8; N]> {
        to_fixed(self.read_slice(offset, N)?)
    }

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

fn to_fixed<const N: usize>(data: &[u8]) -> PyResult<[u8; N]> {
    data.try_into()
        .map_err(|_| PyValueError::new_err("transport frame ended unexpectedly"))
}

#[cfg(test)]
mod tests {
    use super::*;

    const PAYLOAD: [u8; 40] = [7; 40];

    #[test]
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
    fn rejects_oversized_frame_at_header() {
        let mut decoder = FramePump::new(TransportMode::Intermediate, 4, false).unwrap();
        let error = decoder.feed_data(&8_u32.to_le_bytes()).unwrap_err();
        assert!(error.to_string().contains("exceeds configured maximum"));
    }

    #[test]
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
    fn quick_ack_token_matches_published_sha256_vector() {
        let auth_key: Vec<u8> = (0_u8..=255).collect();
        let mut packet = vec![0x11; 8];
        packet.extend_from_slice(&[0x22; 16]);
        packet.extend(0_u8..64);
        assert_eq!(quick_ack_token(&auth_key, &packet).unwrap(), 0xd796_fd18);
    }
}
