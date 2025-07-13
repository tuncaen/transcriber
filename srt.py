import whisper
from whisper.utils import get_writer 

audio = './Haluk Coban_2.mp3'
model = whisper.load_model('large')
result = model.transcribe(audio=audio, language='tr', word_timestamps=True, task="transcribe")

# Set VTT Line and words width
word_options = {
    "highlight_words": False,
    "max_line_count": 2,
    "max_line_width": 20
}
# vtt_writer = get_writer(output_format='vtt', output_dir='./')
# vtt_writer(result, audio, word_options)
srt_writer = get_writer("srt", "./")
srt_writer(result, audio, word_options)
