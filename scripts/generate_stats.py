#!/usr/bin/env python3
"""Refresh The Living Archive from the public GitHub API.

The script refuses to invent a figure. If a request fails, it exits before
replacing the previous snapshot. Forks are excluded from language share and
star totals because a forked upstream would drown the record. The public
repository count is reported both ways.

Streak rule: walk backward from the latest day in the window. If that day is
today and it is still empty, start from yesterday, because the day is not
over. The count is public contributions only.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from svgtext import text_path

ROOT = Path(__file__).resolve().parents[1]
STATS = ROOT / "assets" / "stats"
README = ROOT / "README.md"
LOGIN = os.environ.get("ARCHIVE_LOGIN", "itsananyaaa")

OBSIDIAN = "#080809"
NEAR = "#111014"
CRIMSON = "#8B0000"
BURGUNDY = "#4A0710"
GOLD = "#C5A46D"
PARCHMENT = "#D8C8B0"
EMPTY = "#161418"
CINZEL = "cinzel-semibold.ttf"
MONO = "plex.ttf"

START = "<!-- living-archive:start -->"
END = "<!-- living-archive:end -->"


def token() -> str:
    for key in ("GITHUB_TOKEN", "GH_TOKEN"):
        if os.environ.get(key):
            return os.environ[key]
    return subprocess.check_output(["gh", "auth", "token"], text=True).strip()


def graphql(query: str, variables: dict, auth: str) -> dict:
    payload = json.dumps({"query": query, "variables": variables}).encode()
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"Bearer {auth}",
            "Content-Type": "application/json",
            "User-Agent": "crimson-archive-stats",
        },
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        body = json.loads(response.read().decode())
    if body.get("errors"):
        raise RuntimeError(json.dumps(body["errors"], indent=2))
    return body["data"]


def fetch(auth: str) -> dict:
    counts = graphql(
        """
        query($login: String!) {
          user(login: $login) {
            all: repositories(privacy: PUBLIC, ownerAffiliations: OWNER) { totalCount }
            own: repositories(privacy: PUBLIC, ownerAffiliations: OWNER, isFork: false) { totalCount }
          }
        }
        """,
        {"login": LOGIN},
        auth,
    )["user"]

    languages: dict[str, int] = defaultdict(int)
    stars = 0
    repos = []
    cursor = None
    while True:
        data = graphql(
            """
            query($login: String!, $cursor: String) {
              user(login: $login) {
                repositories(
                  first: 40
                  privacy: PUBLIC
                  ownerAffiliations: OWNER
                  isFork: false
                  after: $cursor
                ) {
                  pageInfo { hasNextPage endCursor }
                  nodes {
                    name
                    stargazerCount
                    languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
                      edges { size node { name } }
                    }
                  }
                }
              }
            }
            """,
            {"login": LOGIN, "cursor": cursor},
            auth,
        )["user"]["repositories"]
        for repo in data["nodes"]:
            repos.append(repo["name"])
            stars += repo["stargazerCount"]
            for edge in repo["languages"]["edges"]:
                languages[edge["node"]["name"]] += edge["size"]
        if not data["pageInfo"]["hasNextPage"]:
            break
        cursor = data["pageInfo"]["endCursor"]

    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=364)
    by_date: dict[str, int] = {}
    cursor_day = start
    while cursor_day <= end:
        chunk_end = min(cursor_day + timedelta(days=90), end)
        weeks = graphql(
            """
            query($login: String!, $from: DateTime!, $to: DateTime!) {
              user(login: $login) {
                contributionsCollection(from: $from, to: $to) {
                  contributionCalendar {
                    weeks { contributionDays { date contributionCount } }
                  }
                }
              }
            }
            """,
            {
                "login": LOGIN,
                "from": f"{cursor_day.isoformat()}T00:00:00Z",
                "to": f"{chunk_end.isoformat()}T23:59:59Z",
            },
            auth,
        )["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
        for week in weeks:
            for day in week["contributionDays"]:
                if start.isoformat() <= day["date"] <= end.isoformat():
                    by_date[day["date"]] = day["contributionCount"]
        cursor_day = chunk_end + timedelta(days=1)

    ordered = []
    day = start
    while day <= end:
        key = day.isoformat()
        ordered.append({"date": key, "count": by_date.get(key, 0)})
        day += timedelta(days=1)

    total = sum(item["count"] for item in ordered)
    longest = current = run = 0
    for item in ordered:
        if item["count"] > 0:
            run += 1
            longest = max(longest, run)
        else:
            run = 0
    probe = len(ordered) - 1
    if ordered and ordered[-1]["date"] == end.isoformat() and ordered[-1]["count"] == 0:
        probe -= 1
    while probe >= 0 and ordered[probe]["count"] > 0:
        current += 1
        probe -= 1

    ranked = sorted(languages.items(), key=lambda item: item[1], reverse=True)
    byte_total = sum(languages.values()) or 1
    return {
        "login": LOGIN,
        "fetched_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "window": {"from": start.isoformat(), "to": end.isoformat()},
        "public_repositories": counts["all"]["totalCount"],
        "non_fork_repositories": counts["own"]["totalCount"],
        "non_fork_stars": stars,
        "non_fork_names": repos,
        "contributions": total,
        "current_streak_days": current,
        "longest_streak_days": longest,
        "days": ordered,
        "languages": [
            {"name": name, "bytes": size, "share": round(size / byte_total, 4)}
            for name, size in ranked
        ],
    }


def cell_color(count: int) -> str:
    if count <= 0:
        return EMPTY
    if count <= 2:
        return BURGUNDY
    if count <= 6:
        return CRIMSON
    return GOLD


def svg(body: str, width: int, height: int) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img">\n'
        f'<rect width="{width}" height="{height}" fill="{OBSIDIAN}"/>\n'
        f"{body}\n</svg>\n"
    )


def calendar_svg(record: dict) -> str:
    days = record["days"]
    first = date.fromisoformat(days[0]["date"])
    pad = (first.weekday() + 1) % 7  # Sunday = 0
    cells = [{"date": "", "count": 0} for _ in range(pad)] + days
    while len(cells) % 7 != 0:
        cells.append({"date": "", "count": 0})
    weeks = [cells[i : i + 7] for i in range(0, len(cells), 7)]
    size, gap = 11, 3
    origin_x, origin_y = 46, 58
    parts = [
        text_path(CINZEL, "PUBLIC CONTRIBUTIONS", 36, 32, 18, PARCHMENT, "start", 0.08),
    ]
    months_seen: set[tuple[int, int]] = set()
    for column, week in enumerate(weeks):
        for row, item in enumerate(week):
            if not item["date"]:
                continue
            x = origin_x + column * (size + gap)
            y = origin_y + row * (size + gap)
            parts.append(
                f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="1.5" fill="{cell_color(item["count"])}"/>'
            )
            current = date.fromisoformat(item["date"])
            key = (current.year, current.month)
            if current.day <= 7 and key not in months_seen:
                months_seen.add(key)
                parts.append(
                    text_path(MONO, current.strftime("%b").upper(), x, origin_y - 8, 10, PARCHMENT, "start", 0.04)
                )
    legend_y = origin_y + 7 * (size + gap) + 28
    parts.append(text_path(MONO, "NONE", 46, legend_y, 11, PARCHMENT, "start", 0.06))
    swatches = [(92, EMPTY), (112, BURGUNDY), (132, CRIMSON), (152, GOLD)]
    for x, color in swatches:
        parts.append(f'<rect x="{x}" y="{legend_y - 10}" width="12" height="12" fill="{color}"/>')
    parts.append(text_path(MONO, "MORE", 172, legend_y, 11, PARCHMENT, "start", 0.06))
    width = origin_x + len(weeks) * (size + gap) + 24
    return svg("\n".join(parts), width, legend_y + 24)


def languages_svg(record: dict) -> str:
    top = [item for item in record["languages"] if item["bytes"] > 0][:6]
    parts = [
        text_path(CINZEL, "LANGUAGES BY BYTES", 32, 40, 18, PARCHMENT, "start", 0.08),
        text_path(MONO, "PUBLIC REPOSITORIES THAT ARE NOT FORKS", 32, 64, 12, GOLD, "start", 0.06),
    ]
    if not top:
        parts.append(text_path(MONO, "NO LANGUAGE DATA RETURNED", 32, 110, 14, PARCHMENT, "start"))
        return svg("\n".join(parts), 880, 160)
    max_share = top[0]["share"] or 1
    y = 108
    for item in top:
        bar = 36 + (item["share"] / max_share) * 520
        parts.append(text_path(MONO, item["name"].upper(), 32, y, 13, PARCHMENT, "start", 0.04))
        parts.append(f'<rect x="250" y="{y - 12}" width="540" height="8" fill="{NEAR}"/>')
        parts.append(f'<rect x="250" y="{y - 12}" width="{bar:.1f}" height="8" fill="{CRIMSON}"/>')
        parts.append(
            text_path(MONO, f"{item['share'] * 100:.1f}%", 810, y, 13, GOLD, "end", 0.04)
        )
        y += 36
    return svg("\n".join(parts), 880, y + 8)


def summary_svg(record: dict) -> str:
    figures = [
        (str(record["public_repositories"]), "PUBLIC REPOS"),
        (str(record["non_fork_repositories"]), "NOT FORKS"),
        (str(record["non_fork_stars"]), "STARS"),
        (str(record["contributions"]), "CONTRIBUTIONS"),
        (str(record["current_streak_days"]), "STREAK"),
        (str(record["longest_streak_days"]), "LONGEST"),
    ]
    parts = [
        text_path(CINZEL, "THE LIVING ARCHIVE", 440, 42, 20, PARCHMENT, "middle", 0.1),
        text_path(MONO, record["fetched_at"], 440, 68, 12, GOLD, "middle", 0.08),
    ]
    for index, (value, label) in enumerate(figures):
        x = 80 + (index % 6) * 140
        parts.append(text_path(CINZEL, value, x, 130, 28, PARCHMENT, "middle"))
        parts.append(text_path(MONO, label, x, 156, 10, GOLD, "middle", 0.06))
    return svg("\n".join(parts), 880, 190)


def fragment(record: dict) -> str:
    jupyter_note = ""
    if record["languages"] and record["languages"][0]["name"] == "Jupyter Notebook" and record["languages"][0]["share"] > 0.5:
        jupyter_note = (
            "Jupyter Notebook leads the byte count because a notebook file stores outputs as well as source. "
            "Read that share as file weight, not as hours spent.\n\n"
        )
    language_rows = "\n".join(
        f"| {item['name']} | {item['bytes']:,} | {item['share'] * 100:.1f}% |"
        for item in record["languages"][:6]
    ) or "| — | 0 | 0% |"
    return f"""{START}
Public GitHub record for `{record['login']}`, fetched {record['fetched_at']}. Contribution counts are the public calendar from {record['window']['from']} to {record['window']['to']}. Language share and stars exclude forks, so an upstream copy cannot dominate the shelf. The streak counts backward from the latest day; if that day is today and still empty, it starts from yesterday.

| Record | Figure |
| --- | ---: |
| Public repositories | {record['public_repositories']} |
| Public repositories that are not forks | {record['non_fork_repositories']} |
| Stars on those non-fork repositories | {record['non_fork_stars']} |
| Public contributions in the window | {record['contributions']} |
| Current public streak | {record['current_streak_days']} days |
| Longest public streak in the window | {record['longest_streak_days']} days |

| Language | Bytes | Share |
| --- | ---: | ---: |
{language_rows}

{jupyter_note}The same figures are drawn in `assets/stats/`. A failed refresh leaves this snapshot in place.
{END}"""


def update_readme(block: str) -> None:
    if not README.exists():
        return
    text = README.read_text()
    if START not in text or END not in text:
        print("README has no living-archive markers; fragment not inserted.", file=sys.stderr)
        return
    before, rest = text.split(START, 1)
    _, after = rest.split(END, 1)
    README.write_text(before + block + after)


def main() -> None:
    auth = token()
    record = fetch(auth)
    STATS.mkdir(parents=True, exist_ok=True)
    # Write beside the live files first, then replace, so a crash keeps the old snapshot.
    staging = STATS / ".staging"
    if staging.exists():
        for child in staging.iterdir():
            child.unlink()
    else:
        staging.mkdir()
    (staging / "manifest.json").write_text(json.dumps(record, indent=2) + "\n")
    (staging / "calendar.svg").write_text(calendar_svg(record))
    (staging / "languages.svg").write_text(languages_svg(record))
    (staging / "summary.svg").write_text(summary_svg(record))
    for name in ("manifest.json", "calendar.svg", "languages.svg", "summary.svg"):
        destination = STATS / name
        destination.write_text((staging / name).read_text())
        (staging / name).unlink()
    staging.rmdir()
    update_readme(fragment(record))
    print(
        f"snapshot {record['fetched_at']}: "
        f"{record['contributions']} contributions, "
        f"{record['non_fork_repositories']} non-fork repos"
    )


if __name__ == "__main__":
    main()
