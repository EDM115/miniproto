"""Update-stream management, persistent cursors, duplicate tracking and handler registration."""

from __future__ import annotations

from miniproto.updates.manager import UpdateHandler, UpdateInvoker, UpdateManager, UpdateQueueOverflowPolicy
from miniproto.updates.state import DuplicateTracker, EntityReference, UpdateCursor

__all__ = [
    "DuplicateTracker",
    "EntityReference",
    "UpdateCursor",
    "UpdateHandler",
    "UpdateInvoker",
    "UpdateManager",
    "UpdateQueueOverflowPolicy",
]
