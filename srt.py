import whisper
import json
import os
from whisper.utils import get_writer

CONFIG_FILENAME = "config.json"

# ---------------------
# Load config
# ---------------------
if not os.path.exists(CONFIG_FILENAME):
    print(f"Hata: '{CONFIG_FILENAME}' bulunamadı.")
    exit(1)

with open(CONFIG_FILENAME, "r", encoding="utf-8") as f:
    config = json.load(f)

# ---------------------
# Determine input media file
# ---------------------
audio_file = config.get("audio_file")
video_file = config.get("video_file")

input_file = None
if audio_file and os.path.exists(audio_file):
    input_file = audio_file
elif video_file and os.path.exists(video_file):
    input_file = video_file

if input_file is None:
    print("Hata: Tanımlı bir 'audio_file' veya 'video_file' bulunamadı ya da dosya mevcut değil.")
    exit(1)

# ---------------------
# Load model and transcribe
# ---------------------
model_name = config.get("model", "large")
model = whisper.load_model(model_name)

result = model.transcribe(
    audio=input_file,
    language=config.get("language", "tr"),
    word_timestamps=config.get("word_timestamps", True),
    task=config.get("task", "transcribe")
)

# ---------------------
# Output setup
# ---------------------
output_dir = config.get("output_dir", ".")
output_format = config.get("output_format", "srt").lower()
srt_file = config.get("srt_file")

word_options = config.get("word_options", {
    "highlight_words": False,
    "max_line_count": 2,
    "max_line_width": 20
})

writer = get_writer(output_format, output_dir)

if srt_file:
    writer(result, os.path.join(output_dir, srt_file), word_options)
    print(f"[✓] {output_format.upper()} çıktısı '{srt_file}' olarak kaydedildi.")
else:
    writer(result, input_file, word_options)
    print(f"[✓] {output_format.upper()} çıktısı varsayılan adla kaydedildi.")
