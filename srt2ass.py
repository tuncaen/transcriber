import pysubs2
import json
import os
import sys

CONFIG_FILENAME = "config.json"

def rgba_to_ass_color(rgba=None, opacity=None):
    r, g, b = 0, 0, 0
    a = 255
    if rgba:
        r, g, b = rgba[:3]
        if len(rgba) == 4:
            a = rgba[3]
    if opacity is not None:
        a = int((1 - opacity) * 255)
    return pysubs2.Color(r, g, b, a)

# ---------------------
# Load config
# ---------------------
if not os.path.exists(CONFIG_FILENAME):
    print(f"Hata: '{CONFIG_FILENAME}' bulunamadı.")
    sys.exit(1)

with open(CONFIG_FILENAME, "r", encoding="utf-8") as f:
    config = json.load(f)

srt_file = config["srt_file"]
ass_file = config.get("ass_file", os.path.splitext(srt_file)[0] + ".ass")
delay_ms = int(config.get("delay_seconds", 0) * 1000)
mobile_style_conf = config.get("mobile_style", {})
components = config.get("components", [])

# ---------------------
# Load SRT
# ---------------------
subs = pysubs2.load(srt_file, encoding="utf-8")

# Apply delay
for line in subs:
    line.start += delay_ms
    line.end += delay_ms

# ---------------------
# Define Mobile Style
# ---------------------
subs.styles["MobileCentered"] = pysubs2.SSAStyle(
    fontname=mobile_style_conf.get("fontname", "Helvetica"),
    fontsize=mobile_style_conf.get("fontsize", 16),
    primarycolor=rgba_to_ass_color(
        mobile_style_conf.get("primarycolor", [255, 255, 255]),
        opacity=1
    ),
    backcolor=rgba_to_ass_color(
        mobile_style_conf.get("backcolor", [0, 0, 0]),
        opacity=mobile_style_conf.get("opacity", 1)
    ),
    outline=mobile_style_conf.get("outline", 1.5),
    shadow=mobile_style_conf.get("shadow", 0.5),
    alignment=mobile_style_conf.get("alignment", 2),
    marginl=mobile_style_conf.get("marginl", 2),
    marginr=mobile_style_conf.get("marginr", 2),
    marginv=mobile_style_conf.get("marginv", 30),
    bold=int(mobile_style_conf.get("bold", False)),
    borderstyle=mobile_style_conf.get("borderstyle", 1)
)

# Apply mobile style to all lines
for line in subs:
    line.style = "MobileCentered"

# ---------------------
# Add custom components
# ---------------------
def make_style_name(index): return f"ComponentStyle{index}"

for i, comp in enumerate(components):
    start = int(comp["start_seconds"] * 1000) + delay_ms
    end = int(comp["end_seconds"] * 1000) + delay_ms
    fadein = comp.get("fadein", 0)
    fadeout = comp.get("fadeout", 0)
    text = f"{{\\fad({fadein},{fadeout})}}{comp['text']}"

    style_name = make_style_name(i)
    subs.styles[style_name] = pysubs2.SSAStyle(
        fontname=comp.get("fontname", "Helvetica"),
        fontsize=comp.get("fontsize", 10),
        primarycolor=rgba_to_ass_color(
            comp.get("primarycolor", [255, 255, 255]),
            opacity=1
            ),
        backcolor=rgba_to_ass_color(
            comp.get("backcolor", [0, 0, 0]),
            opacity=comp.get("opacity", 1)
        ),
        outline=comp.get("outline", 1.5),
        shadow=comp.get("shadow", 0.5),
        alignment=comp.get("alignment", 7),
        marginl=comp.get("marginl", 20),
        marginr=comp.get("marginr", 10),
        marginv=comp.get("marginv", 20),
        bold=int(comp.get("bold", False)),
        borderstyle=comp.get("borderstyle", 3)
    )

    subs.append(pysubs2.SSAEvent(
        start=start,
        end=end,
        text=text,
        style=style_name
    ))

# ---------------------
# Save ASS
# ---------------------
subs.sort()
subs.save(ass_file)
print(f"'{ass_file}' başarıyla oluşturuldu.")
