from __future__ import annotations

import argparse
import asyncio
import os
from collections.abc import Mapping, Sequence
from pathlib import Path

from miniproto import import_session_string
from miniproto.session.storage import EncryptedSQLiteSessionStorage


async def provision_sessions(*, dc_id: int, env: Mapping[str, str], root: Path = Path(".tmp")) -> tuple[str, ...]:
    """Provision missing encrypted benchmark databases from optional environment-only string sessions."""
    key = env.get("MINIPROTO_SESSION_KEY")
    candidates = {
        "user": env.get("MINIPROTO_LIVE_BENCH_USER_STRING_SESSION"),
        "bot": env.get("MINIPROTO_LIVE_BENCH_BOT_STRING_SESSION"),
    }
    if not any(candidates.values()):
        return ()
    if not key:
        raise SystemExit("MINIPROTO_SESSION_KEY is required to provision encrypted benchmark sessions")
    passphrase = env.get("MINIPROTO_LIVE_BENCH_STRING_PASSPHRASE") or None
    await asyncio.to_thread(root.mkdir, parents=True, exist_ok=True)
    provisioned: list[str] = []
    for actor, value in candidates.items():
        if not value:
            continue
        target = root / f"miniproto-live-bench-{actor}-dc{dc_id}.sqlite"
        if target.exists():
            continue
        record = import_session_string(value, passphrase=passphrase)
        if record.dc_id != dc_id:
            raise SystemExit(f"{actor} string session DC {record.dc_id} does not match requested DC {dc_id}")
        if record.user is not None and record.user.is_bot != (actor == "bot"):
            raise SystemExit(f"{actor} string session has the wrong account kind")
        storage = EncryptedSQLiteSessionStorage(target, key=key)
        await storage.save(record)
        provisioned.append(actor)
    return tuple(provisioned)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Provision optional live-benchmark string sessions")
    parser.add_argument("--dc-id", type=int, required=True)
    parser.add_argument("--root", type=Path, default=Path(".tmp"))
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    provisioned = asyncio.run(provision_sessions(dc_id=args.dc_id, env=os.environ, root=args.root))
    if provisioned:
        print(f"provisioned encrypted sessions: {', '.join(provisioned)}")
    else:
        print("no string-session provisioning required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
