import pysubs2
import json
import os
import sys

CONFIG_FILENAME = "config.json"

# -----------------------------
# Config yükle
# -----------------------------
if not os.path.exists(CONFIG_FILENAME):
    print(f"Hata: '{CONFIG_FILENAME}' bulunamadı.")
    sys.exit(1)

with open(CONFIG_FILENAME, "r", encoding="utf-8") as f:
    config = json.load(f)

srt_file = config["srt_file"]
ass_file = config.get("output_file", os.path.splitext(srt_file)[0] + ".ass")
delay_ms = int(config.get("delay_seconds", 0) * 1000)
components = config.get("components", [])

# -----------------------------
# SRT dosyasını yükle
# -----------------------------
subs = pysubs2.load(srt_file, encoding="utf-8")

# Delay uygula
for line in subs:
    line.start += delay_ms
    line.end += delay_ms

# -----------------------------
# Mobil stil
# -----------------------------
subs.styles["MobileCentered"] = pysubs2.SSAStyle(
    fontname="Helvetica",
    fontsize=16,
    primarycolor=pysubs2.Color(255, 255, 255),
    backcolor=pysubs2.Color(0, 0, 0, 192),
    outline=1.5,
    shadow=0.5,
    alignment=2,
    marginl=2,
    marginr=2,
    marginv=30,
    bold=False
)

# -----------------------------
# Component stil ve satırları ekle
# -----------------------------
for i, comp in enumerate(components):
    style_name = f"InfoBox_{i}"
    fontname = comp.get("fontname", "Helvetica")
    fontsize = comp.get("fontsize", 10)
    opacity = comp.get("opacity", 0.5)
    alignment = comp.get("alignment", 7)
    marginl = comp.get("marginl", 10)
    marginr = comp.get("marginr", 10)
    marginv = comp.get("marginv", 20)
    fadein = comp.get("fadein", 0)
    fadeout = comp.get("fadeout", 0)
    text = comp.get("text", "")
    start = int(comp.get("start_seconds", 0) * 1000 + delay_ms)
    end = int(comp.get("end_seconds", 5) * 1000 + delay_ms)

    style = pysubs2.SSAStyle(
        fontname=fontname,
        fontsize=fontsize,
        primarycolor=pysubs2.Color(255, 255, 255),
        backcolor=pysubs2.Color(0, 0, 0, int(255 * opacity)),
        outline=1.5,
        shadow=0.5,
        alignment=alignment,
        marginl=marginl,
        marginr=marginr,
        marginv=marginv,
        bold=True,
        borderstyle=4  # Sadece renkli arka planla kutulu gibi görünür
    )

    subs.styles[style_name] = style

    dialogue_text = f"{{\\fad({fadein},{fadeout})}}{text}"
    subs.append(pysubs2.SSAEvent(
        start=start,
        end=end,
        text=dialogue_text,
        style=style_name
    ))

# -----------------------------
# Mevcut tüm satırlara mobil stil ata
# -----------------------------
for line in subs:
    if line.style not in subs.styles or line.style.startswith("InfoBox"):
        continue
    line.style = "MobileCentered"

# -----------------------------
# Zaman sıralaması
# -----------------------------
subs.events.sort(key=lambda ev: ev.start)

# Kaydet
subs.save(ass_file)
print(f"[✓] '{ass_file}' başarıyla oluşturuldu.")
