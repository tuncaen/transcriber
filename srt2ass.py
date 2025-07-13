import pysubs2
import json
import os
import sys

CONFIG_FILENAME = "config.json"

# ---------------------
# Config dosyasını yükle
# ---------------------
if not os.path.exists(CONFIG_FILENAME):
    print(f"Hata: '{CONFIG_FILENAME}' bulunamadı.")
    sys.exit(1)

with open(CONFIG_FILENAME, "r", encoding="utf-8") as f:
    config = json.load(f)

srt_file = config["srt_file"]
ass_file = config.get("output_file", os.path.splitext(srt_file)[0] + ".ass")
delay_ms = int(config.get("delay_seconds", 0) * 1000)
kunye = config.get("kunye", None)

# ---------------------
# SRT dosyasını yükle
# ---------------------
subs = pysubs2.load(srt_file, encoding="utf-8")

# Zaman kayması uygula
for line in subs:
    line.start += delay_ms
    line.end += delay_ms

# ---------------------
# Mobil stil tanımı
# ---------------------
subs.styles["MobileCentered"] = pysubs2.SSAStyle(
    fontname="Helvetica",
    fontsize=16,
    primarycolor=pysubs2.Color(255, 255, 255),
    backcolor=pysubs2.Color(0, 0, 0, 192),
    outline=1.5,
    shadow=0.5,
    alignment=2,  # Alt-orta
    marginl=2,
    marginr=2,
    marginv=30,
    bold=False
)

# ---------------------
# Künye varsa stilini ve efektlerini uygula
# ---------------------
if kunye:
    style_name = "InfoBox"
    alignment = kunye.get("alignment", 7)
    opacity = kunye.get("opacity", 0.7)
    fadein_ms = int(kunye.get("fadein", 500))
    fadeout_ms = int(kunye.get("fadeout", 500))
    fontname = kunye.get("fontname", "Helvetica")
    
    subs.styles[style_name] = pysubs2.SSAStyle(
        fontname=fontname,
        fontsize=18,
        primarycolor=pysubs2.Color(255, 255, 255),
        backcolor=pysubs2.Color(0, 0, 0, int(255 * opacity)),
        outline=1.5,
        shadow=0.5,
        alignment=alignment,
        marginl=0,
        marginr=0,
        marginv=20,
        bold=True,
        borderstyle=4  # Sadece renkli arka planla kutulu gibi görünür
    )

    # Text'i stilize et (satır bazlı font boyutu ve fade efektleri)
    text_lines = kunye["text"]
    formatted_lines = []
    for line in text_lines:
        fontsize = line.get("fontsize", 18)
        content = line["text"]
        formatted_lines.append(f"{{\\fs{fontsize}}}{content}")
    text = f"{{\\fad({fadein_ms},{fadeout_ms})}}" + "\\N".join(formatted_lines)

    subs.append(
        pysubs2.SSAEvent(
            start=int(kunye["start_seconds"] * 1000) + delay_ms,
            end=int(kunye["end_seconds"] * 1000) + delay_ms,
            text=text,
            style=style_name
        )
    )

# ---------------------
# Tüm satırlara mobil stil ata
# ---------------------
for line in subs:
    if not hasattr(line, 'style') or line.style != "InfoBox":
        line.style = "MobileCentered"

# ---------------------
# Zaman etiketlerine göre sırala
# ---------------------
subs.events.sort(key=lambda e: e.start)

# Kaydet
subs.save(ass_file)
print(f"[✓] '{ass_file}' başarıyla oluşturuldu.")
