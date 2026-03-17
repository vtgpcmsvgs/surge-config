#!/usr/bin/env python3
"""Sync selected third-party rule snapshots into rules/upstream/."""

from __future__ import annotations

import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_ROOT = ROOT / "rules" / "upstream"
USER_AGENT = "surge-config-upstream-sync/1.0"


@dataclass(frozen=True)
class UpstreamFile:
    path: Path
    url: str


UPSTREAM_FILES = (
    UpstreamFile(Path("loyalsoldier/direct.txt"), "https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/direct.txt"),
    UpstreamFile(Path("loyalsoldier/cncidr.txt"), "https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/cncidr.txt"),
    UpstreamFile(Path("loyalsoldier/gfw.txt"), "https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/gfw.txt"),
    UpstreamFile(Path("loyalsoldier/tld-not-cn.txt"), "https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/tld-not-cn.txt"),
    UpstreamFile(Path("loyalsoldier/telegramcidr.txt"), "https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/telegramcidr.txt"),
    UpstreamFile(Path("acl4ssr/bilibili.list"), "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Bilibili.list"),
    UpstreamFile(Path("acl4ssr/bilibili_hmt.list"), "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/BilibiliHMT.list"),
    UpstreamFile(Path("acl4ssr/china_domain.list"), "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ChinaDomain.list"),
    UpstreamFile(Path("acl4ssr/china_media.list"), "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ChinaMedia.list"),
    UpstreamFile(Path("acl4ssr/download.list"), "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Download.list"),
    UpstreamFile(Path("acl4ssr/google_fcm.list"), "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/GoogleFCM.list"),
    UpstreamFile(Path("acl4ssr/microsoft.list"), "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Microsoft.list"),
    UpstreamFile(Path("acl4ssr/netease_music.list"), "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/NetEaseMusic.list"),
    UpstreamFile(Path("acl4ssr/netflix.list"), "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Netflix.list"),
    UpstreamFile(Path("acl4ssr/onedrive.list"), "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/OneDrive.list"),
    UpstreamFile(Path("acl4ssr/openai.list"), "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/OpenAi.list"),
    UpstreamFile(Path("acl4ssr/proxy_gfwlist.list"), "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ProxyGFWlist.list"),
    UpstreamFile(Path("acl4ssr/proxy_media.list"), "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ProxyMedia.list"),
    UpstreamFile(Path("acl4ssr/unban.list"), "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/UnBan.list"),
    UpstreamFile(Path("acl4ssr/youtube.list"), "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/YouTube.list"),
)


def decode_text(payload: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gb18030", "latin-1"):
        try:
            return payload.decode(encoding)
        except UnicodeDecodeError:
            continue
    return payload.decode("utf-8", errors="replace")


def normalize_text(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.endswith("\n"):
        normalized += "\n"
    return normalized


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return normalize_text(decode_text(response.read()))


def read_existing(path: Path) -> str | None:
    if not path.exists():
        return None
    return normalize_text(decode_text(path.read_bytes()))


def sync_one(item: UpstreamFile) -> tuple[bool, bool]:
    destination = UPSTREAM_ROOT / item.path
    destination.parent.mkdir(parents=True, exist_ok=True)

    try:
        latest = fetch_text(item.url)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f"[WARN] {item.path.as_posix()} fetch failed: {exc}")
        return False, True

    existing = read_existing(destination)
    if existing == latest:
        print(f"[SKIP] {item.path.as_posix()}")
        return False, False

    destination.write_text(latest, encoding="utf-8")
    print(f"[UPDATE] {item.path.as_posix()}")
    return True, False


def main() -> int:
    changed = 0
    failed = 0

    for item in UPSTREAM_FILES:
        updated, fetch_failed = sync_one(item)
        changed += int(updated)
        failed += int(fetch_failed)

    print(f"[DONE] {changed} files updated, {failed} fetch failures.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
