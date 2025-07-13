# Giriş

Bu repo İstanbul Teknik Üniversitesi Tanıtım Komisyonu tarafından hazırlanan mezun video editleri için kullanılan altyazı editleme araçlarını içermektedir. Bu repoda, herhangi bir video/ses dosyasındaki konuşmaları zaman etiketli altyazı dosyalarına (`*.srt`) dönüştüren python betik dosyası `srt.py` ve bu altyazı dosyasını kullanarak son stil düzenlemeleri yapan `srt2ass.py` dosyası bulunmaktadır.

# Ön gereksinimler

- Python 3.x

- `whisper` kütüphanesi: Ses dosyalarındaki konuşmaları metne dönüştürmek için kullanılır. Kurmak için terminalde şu komutu çalıştırabilirsiniz:
    ```bash
    pip install whisper-openai
    ```
- `pysubs2` kütüphanesi: Altyazı dosyalarını düzenlemek için kullanılır. Kurmak için terminalde şu komutu çalıştırabilirsiniz:
    ```bash
    pip install pysubs2
    ```
- `ffmpeg`: Video ve ses dosyalarını işlemek için kullanılır. Kurmak için terminalde şu komutu çalıştırabilirsiniz:
    
    1) <a href="https://github.com/BtbN/FFmpeg-Builds/releases" target="_blank">Buradan</a> işletim sisteminize uygun FFmpeg sürümünü indirip kurabilirsiniz.
    2) İndirilen FFmpeg klasörünün `bin` dizinini sistem PATH'ine ekleyin. Bu, terminalden `ffmpeg` komutunu kullanabilmenizi ve betiklerin doğru şekilde çalışmasını sağlar.


# Kullanım

## 1. Altyazı dosyası oluşturma
- `srt.py` dosyasını kullanarak bir video veya ses dosyasından altyazı dosyası (`*.srt`) oluşturabilirsiniz. Terminalde şu komutu çalıştırın:

    ```bash
    python srt.py <video_dosyası.mp4>
    ```

## 2. Altyazı dosyasının imla kontrolü

## 3. Altyazı okunabilirliğini artırma

## 4. Altyazı stilini düzenleme

## 5. Altyazıların videoya gömülmesi


