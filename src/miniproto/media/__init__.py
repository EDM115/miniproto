"""Public media-transfer APIs for downloading, uploading, CDN decryption and range caching.

The exports intentionally group high-level download and upload helpers with the
typed results, source/destination aliases and CDN integrity errors they use.
"""

from miniproto.media.cdn import CdnError, CdnIntegrityError, CdnRedirect, decrypt_cdn_chunk
from miniproto.media.download import (
    DEFAULT_DOWNLOAD_CONCURRENCY,
    DEFAULT_DOWNLOAD_IN_FLIGHT_BYTES,
    DEFAULT_DOWNLOAD_PART_SIZE,
    DEFAULT_RANGE_CACHE_BYTES,
    MAX_DOWNLOAD_CHUNK_SIZE,
    Destination,
    DownloadRangeCache,
    MediaDownloadError,
    MediaDownloadResult,
    MediaIntegrityError,
    download_file,
    download_location_from_media,
    download_media,
    iter_download,
    iter_download_media,
    media_from_raw,
)
from miniproto.media.upload import (
    BIG_FILE_THRESHOLD,
    DEFAULT_CHUNK_SIZE,
    FileSource,
    MediaUploadError,
    MediaUploadResult,
    ProgressCallback,
    upload_file,
)

__all__ = [
    "BIG_FILE_THRESHOLD",
    "DEFAULT_CHUNK_SIZE",
    "DEFAULT_DOWNLOAD_CONCURRENCY",
    "DEFAULT_DOWNLOAD_IN_FLIGHT_BYTES",
    "DEFAULT_DOWNLOAD_PART_SIZE",
    "DEFAULT_RANGE_CACHE_BYTES",
    "MAX_DOWNLOAD_CHUNK_SIZE",
    "CdnError",
    "CdnIntegrityError",
    "CdnRedirect",
    "Destination",
    "DownloadRangeCache",
    "FileSource",
    "MediaDownloadError",
    "MediaDownloadResult",
    "MediaIntegrityError",
    "MediaUploadError",
    "MediaUploadResult",
    "ProgressCallback",
    "decrypt_cdn_chunk",
    "download_file",
    "download_location_from_media",
    "download_media",
    "iter_download",
    "iter_download_media",
    "media_from_raw",
    "upload_file",
]
