#!/usr/bin/env python3
"""CLI tool to download the thumbnail image for a YouTube video."""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from typing import Optional
from urllib import error, parse, request

THUMBNAIL_RESOLUTIONS = [
    "maxresdefault",
    "sddefault",
    "hqdefault",
    "mqdefault",
    "default",
]


def extract_video_id(url: str) -> Optional[str]:
    """Extract a YouTube video ID from a URL or return None if unavailable."""

    url = url.strip()
    if not url:
        return None

    # If the user passed a bare video ID, accept it directly
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url):
        return url

    parsed = parse.urlparse(url)

    # https://www.youtube.com/watch?v=VIDEO_ID
    if parsed.query:
        params = parse.parse_qs(parsed.query)
        video_id = params.get("v", [None])[0]
        if video_id:
            return video_id

    # https://youtu.be/VIDEO_ID or https://www.youtube.com/embed/VIDEO_ID
    if parsed.path:
        parts = [p for p in parsed.path.split("/") if p]
        if parts:
            candidate = parts[-1]
            if re.fullmatch(r"[A-Za-z0-9_-]{11}", candidate):
                return candidate

    return None


def build_thumbnail_url(video_id: str, resolution: str) -> str:
    return f"https://img.youtube.com/vi/{video_id}/{resolution}.jpg"


def download_thumbnail(thumbnail_url: str, output_path: pathlib.Path) -> pathlib.Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    req = request.Request(thumbnail_url, headers={"User-Agent": "Mozilla/5.0"})
    with request.urlopen(req) as response:  # type: ignore[arg-type]
        data = response.read()

    output_path.write_bytes(data)
    return output_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download the thumbnail image for a YouTube video.",
    )
    parser.add_argument("url", help="YouTube video URL or video ID")
    parser.add_argument(
        "-r",
        "--resolution",
        choices=THUMBNAIL_RESOLUTIONS,
        default=THUMBNAIL_RESOLUTIONS[0],
        help="Thumbnail resolution to fetch (default: %(default)s)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=pathlib.Path,
        help="Output file path. Defaults to '<video_id>_<resolution>.jpg'",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    video_id = extract_video_id(args.url)
    if not video_id:
        print("動画IDをURLから取得できませんでした。URLを確認してください。", file=sys.stderr)
        return 1

    thumbnail_url = build_thumbnail_url(video_id, args.resolution)

    output_path = args.output or pathlib.Path(f"{video_id}_{args.resolution}.jpg")

    try:
        download_thumbnail(thumbnail_url, output_path)
    except error.HTTPError as exc:
        print(
            "サムネイルの取得に失敗しました。解像度を変更して再試行してください。",
            f"(HTTP {exc.code})",
            file=sys.stderr,
        )
        return 2
    except error.URLError as exc:
        print(f"ネットワークエラー: {exc.reason}", file=sys.stderr)
        return 3

    print(f"サムネイルを保存しました: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
