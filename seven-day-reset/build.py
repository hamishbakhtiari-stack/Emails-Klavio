#!/usr/bin/env python3
"""Build the 7-Day Reset emails from one master template.

Edit content.json (copy, links, colours), then run:
    python3 seven-day-reset/build.py
Output: seven-day-reset/dist/day-1.html ... day-7.html (ready to import into Klaviyo).
"""
import html
import re
import json
import pathlib
import string

ROOT = pathlib.Path(__file__).resolve().parent
TEMPLATE = (ROOT / "template.html").read_text()
DATA = json.loads((ROOT / "content.json").read_text())
TOTAL_DAYS = 7


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def progress_bar(day: int, c: dict) -> str:
    cells = []
    for i in range(1, TOTAL_DAYS + 1):
        bg = c["accent"] if i <= day else c["rule"]
        cells.append(
            f'<td width="14%" style="padding:0 2px;"><div style="height:6px;line-height:6px;'
            f'font-size:0;border-radius:3px;background-color:{bg};">&nbsp;</div></td>'
        )
    return "".join(cells)


def steps_html(steps, c) -> str:
    rows = []
    for n, (head, body) in enumerate(steps, 1):
        rows.append(f"""
<tr>
  <td valign="top" width="40" style="padding:0 0 18px 0;">
    <div style="width:28px;height:28px;line-height:28px;border-radius:14px;background-color:{c['accent_soft']};color:{c['accent']};font-weight:700;font-size:14px;text-align:center;">{n}</div>
  </td>
  <td valign="top" style="padding:3px 0 18px 0;font-size:16px;line-height:24px;color:{c['ink']};">
    <strong>{esc(head)}</strong><br>
    <span style="color:{c['muted']};">{esc(body)}</span>
  </td>
</tr>""")
    return "".join(rows)


def build(day: dict) -> str:
    b = DATA["brand"]
    c = b["colors"]
    tomorrow = (
        f'<p style="margin:0 0 8px 0;font-size:15px;line-height:22px;color:{c["muted"]};">'
        f'<em>{esc(day["tomorrow"])}</em></p>'
        if day.get("tomorrow")
        else ""
    )
    finale = (
        f'<p style="margin:0 0 8px 0;font-size:15px;line-height:22px;color:{c["muted"]};">'
        f'Want to run through it again? <a href="{b["program_url"]}" style="color:{c["accent"]};">'
        f"The full 7-Day Reset is here</a>.</p>"
        if day.get("finale")
        else ""
    )
    note = (
        f'<p style="margin:0 0 14px 0;font-size:15px;line-height:22px;color:{c["ink"]};">'
        f'<strong>{esc(day["note"])}</strong></p>'
        if day.get("note")
        else ""
    )
    fields = {
        **{f"c_{k}": v for k, v in c.items()},
        "brand_name": esc(b["name"]),
        "logo_url": b["logo_url"],
        "site_url": b["site_url"],
        "program_url": b["program_url"],
        "support_email": b["support_email"],
        "signer_name": esc(b["signer_name"]),
        "signer_role": esc(b["signer_role"]),
        "day": day["day"],
        "total": TOTAL_DAYS,
        "subject": esc(day["subject"]),
        "preview": esc(day["preview"]),
        "title": esc(day["title"]),
        "intro": esc(day["intro"]),
        "focus_label": esc(day["focus_label"]),
        "steps": steps_html(day["steps"], c),
        "cta_url": day["cta_url"],
        "cta_label": ("&#9654;&nbsp; " if "youtube" in day["cta_url"] else "") + esc(day["cta_label"]),
        "subtitle": esc(day["subtitle"]),
        "eyebrow": "Welcome" if day["day"] == 0 else f"Day {day['day']}",
        "counter": "7-Day Reset &middot; Starts tomorrow" if day["day"] == 0 else f"7-Day Reset &middot; Day {day['day']} of {TOTAL_DAYS}",
        "tip": esc(day["tip"]),
        "reply_prompt": esc(day["reply_prompt"]),
        "tomorrow_block": tomorrow,
        "finale_block": finale,
        "note_block": note,
        "progress": progress_bar(day["day"], c),
    }
    return string.Template(TEMPLATE).substitute(fields)


def to_block(full_html: str) -> str:
    """Body content + responsive <style>, minified, for a Klaviyo drag-and-drop HTML block."""
    style = re.search(r"<style>.*?</style>", full_html, re.S).group(0)
    body = re.search(r"<body[^>]*>(.*)</body>", full_html, re.S).group(1)
    out = style + body
    out = re.sub(r"<!--.*?-->", "", out, flags=re.S)
    out = re.sub(r">\s+<", "><", out)
    out = re.sub(r"\s+", " ", out).strip()
    # single-quoted attributes so the block can be pasted into JSON without escaping
    return re.sub(r'(\s[\w-]+)="([^"\']*)"', r"\1='\2'", out)


def main():
    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    for day in DATA["days"]:
        path = out / f"day-{day['day']}.html"
        full = build(day)
        path.write_text(full)
        (out / f"day-{day['day']}.block.html").write_text(to_block(full))
        print(f"wrote {path.relative_to(ROOT.parent)}  ({path.stat().st_size // 1024} KB)  subject: {day['subject']}")


if __name__ == "__main__":
    main()
