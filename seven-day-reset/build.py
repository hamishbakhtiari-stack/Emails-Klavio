#!/usr/bin/env python3
"""Build the 7-Day Reset emails (Day 0 to Day 7) from one master template.

Edit content.json (copy, icons, links, colours), then run:
    python3 seven-day-reset/build.py
Outputs in seven-day-reset/dist/:
    day-N.html        full email, ready to import into Klaviyo as an HTML (code) template
    day-N.block.html  the same email as one line, for a Klaviyo HTML block
"""
import html
import json
import pathlib
import re
import string

ROOT = pathlib.Path(__file__).resolve().parent
TEMPLATE = (ROOT / "template.html").read_text()
DATA = json.loads((ROOT / "content.json").read_text())
TOTAL_DAYS = 7


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def img(url: str, size: int, alt: str = "") -> str:
    return (
        f'<img src="{url}" width="{size}" height="{size}" alt="{esc(alt)}" '
        f'style="display:block;border:0;width:{size}px;height:{size}px;">'
    )


def progress_bar(day: int, c: dict) -> str:
    cells = []
    for i in range(1, TOTAL_DAYS + 1):
        bg = c["accent"] if i <= day else c["rule"]
        cells.append(
            f'<td width="14%" style="padding:0 2px;"><div style="height:6px;line-height:6px;'
            f'font-size:0;border-radius:3px;background-color:{bg};">&nbsp;</div></td>'
        )
    return "".join(cells)


def steps_html(steps, c, base) -> str:
    rows = []
    for step in steps:
        head, body, icon = step[0], step[1], step[2]
        label = (
            f'<span style="font-size:11px;line-height:15px;font-weight:700;color:{c["accent"]};'
            f'letter-spacing:0.08em;text-transform:uppercase;">{esc(step[3])}</span><br>'
            if len(step) > 3
            else ""
        )
        rows.append(f"""
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 8px 0;"><tr>
  <td valign="middle" width="58" style="background-color:{c['row_bg']};border-radius:12px 0 0 12px;padding:12px 0 12px 12px;">{img(base + icon + '.png', 42)}</td>
  <td valign="middle" style="background-color:{c['row_bg']};border-radius:0 12px 12px 0;padding:12px 14px 12px 6px;font-size:16px;line-height:23px;color:{c['ink']};">
    {label}<strong>{esc(head)}</strong><br><span style="font-size:15px;line-height:22px;color:{c['muted']};">{esc(body)}</span>
  </td>
</tr></table>""")
    return "".join(rows)


def build(day: dict) -> str:
    b = DATA["brand"]
    c = b["colors"]
    base = b["image_base"]
    n = day["day"]

    def para(text, color, bold=False, italic=False):
        if bold:
            text = f"<strong>{text}</strong>"
        if italic:
            text = f"<em>{text}</em>"
        return f'<p style="margin:0 0 12px 0;font-size:15px;line-height:22px;color:{color};">{text}</p>'

    is_video = "youtube" in day["cta_url"]
    fields = {
        **{f"c_{k}": v for k, v in c.items()},
        "brand_name": esc(b["name"]),
        "logo_url": b["logo_url"],
        "site_url": b["site_url"],
        "support_email": b["support_email"],
        "signer_name": esc(b["signer_name"]),
        "signer_role": esc(b["signer_role"]),
        "subject": esc(day["subject"]),
        "preview": esc(day["preview"]),
        "title": esc(day["title"]),
        "subtitle": esc(day["subtitle"]),
        "eyebrow": "Welcome" if n == 0 else f"Day {n} of {TOTAL_DAYS}",
        "counter": "Starts tomorrow" if n == 0 else "7-Day Reset",
        "hero_icon": base + day["hero_icon"] + ".png",
        "intro": esc(day["intro"]),
        "focus_label": esc(day["focus_label"]),
        "steps": steps_html(day["steps"], c, base),
        "progress": progress_bar(n, c),
        "cta_url": day["cta_url"],
        "cta_label": esc(day["cta_label"]),
        "cta_eyebrow": "Today's video" if is_video else "Your program page",
        "cta_icon": img(base + b["icons"]["play"] + ".png", 42) if is_video
        else img(base + b["icons"]["tip"] + ".png", 42),
        "tip": esc(day["tip"]),
        "tip_icon": base + b["icons"]["tip"] + ".png",
        "help_icon": base + b["icons"]["help"] + ".png",
        "reply_prompt": esc(day["reply_prompt"]),
        "note_block": para(esc(day["note"]), c["ink"], bold=True) if day.get("note") else "",
        "tomorrow_block": para(esc(day["tomorrow"]), c["muted"], italic=True) if day.get("tomorrow") else "",
        "finale_block": para(
            f'Want to run through it again? <a href="{b["program_url"]}" style="color:{c["accent"]};">'
            f"The full 7-Day Reset is here</a>.", c["muted"]) if day.get("finale") else "",
    }
    return string.Template(TEMPLATE).substitute(fields)


def to_block(full_html: str) -> str:
    """Body content + responsive <style>, on one line, for a Klaviyo HTML block."""
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
        imgs = full.count("<img")
        print(f"wrote {path.relative_to(ROOT.parent)}  ({path.stat().st_size // 1024} KB, {imgs} images)  subject: {day['subject']}")


if __name__ == "__main__":
    main()
