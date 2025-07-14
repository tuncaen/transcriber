# Mezun Video Altyazı Araçları

## Giriş

Bu repo İstanbul Teknik Üniversitesi Tanıtım Komisyonu tarafından hazırlanan mezun video editleri için kullanılan altyazı editleme araçlarını içermektedir. Bu repoda, herhangi bir video/ses dosyasındaki konuşmaları zaman etiketli altyazı dosyalarına (`*.srt`) dönüştüren python betik dosyası `srt.py` ve bu altyazı dosyasını kullanarak son stil düzenlemeleri yapan `srt2ass.py` dosyası bulunmaktadır.

## Ön Gereksinimler

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


## Kullanım

### 1. Altyazı dosyası oluşturma
- `srt.py` dosyasını kullanarak bir video veya ses dosyasından altyazı dosyası (`*.srt`) oluşturabilirsiniz. Terminalde şu komutu çalıştırın:

    ```bash
    python srt.py <video_dosyası.mp4>
    ```

### 2. Altyazı dosyasının imla kontrolü
- `srt.py` tarafından oluşturulan `*.srt` dosyasını bir metin
  düzenleyicisi ile açarak yazım ve noktalama hatalarını düzeltin.
  Gerekirse `config.json` dosyasında `srt_file` alanını değiştirerek
  çıktı dosyasının adını belirleyebilirsiniz.

### 3. Altyazı okunabilirliğini artırma
- `config.json` içindeki `word_options` ayarları ile satır uzunluğu ve
  satır sayısı gibi değerleri düzenleyerek altyazıların daha
  okunabilir olmasını sağlayabilirsiniz.

### 4. Altyazı stilini düzenleme
- Altyazı dosyasını ASS formatına dönüştürmek ve stil eklemek için
  `srt2ass.py` betiğini çalıştırın:
  ```bash
  python srt2ass.py
  ```
  Stil seçeneklerini ve bileşenleri yine `config.json` dosyasından
  değiştirebilirsiniz.

### 5. Altyazıların videoya gömülmesi
- Oluşturduğunuz ASS dosyasını videoya gömmek için aşağıdaki FFmpeg
  komutunu kullanabilirsiniz:
  ```bash
  ffmpeg -i <giris.mp4> -vf "ass=<dosya.adı.ass>" -c:a copy <çıkış.mp4>
  ```


## `config.json` parametreleri

Aşağıdaki başlıca alanlar `config.json` dosyası ile yapılandırılabilir:

- **audio_file**: Sadece ses içeren giriş dosyası.
- **video_file**: Video içeren giriş dosyası (audio_file yoksa kullanılır).
- **srt_file**: `srt.py` çalıştırıldığında oluşturulacak altyazı dosyası.
- **ass_file**: `srt2ass.py` tarafından üretilen ASS dosyasının adı.
- **delay_seconds**: Altyazıların ne kadar süre kaydırılacağı.
- **language**: Ses veya video dili (örneğin `tr`).
- **model**: Kullanılacak Whisper modelinin adı.
- **task**: `transcribe` ya da `translate` görevlerinden biri.
- **output_format**: Çıktı biçimi (`srt`, `vtt` vb.).
- **output_dir**: Oluşturulan dosyaların kaydedileceği klasör.
- **word_timestamps**: Her kelime için zaman etiketi oluşturulup oluşturulmayacağı.
- **word_options**: Satır uzunlukları gibi okunabilirlik ayarları.
- **mobile_style**: ASS çıktısının yazı tipi, renk ve hizalama gibi stil bilgileri.
- **components**: Videoda belirli noktalarda görünecek ek metin öğeleri.

### mobile_style
Bu nesne, tüm altyazı satırlarına uygulanacak temel ASS stilini tanımlar.

- **fontname**: Kullanılacak yazı tipi.
- **fontsize**: Yazı boyutu.
- **primarycolor** / **backcolor**: Metin ve arka plan renkleri.
- **outline**: Kenar çizgisi kalınlığı.
- **shadow**: Gölge kalınlığı.
- **alignment**: Ekrandaki hizalama kodu.
- **marginl**, **marginr**, **marginv**: Kenar boşlukları.
- **bold**: Metin kalınlığı.
- **borderstyle**: Kenarlık stili.
- **opacity**: Arka plan saydamlığı.

### components
Her bir öğe ekranda belirli zamanlarda gösterilecek metni ve stilini tanımlar.

- **text**: Görünecek yazı.
- **start_seconds** / **end_seconds**: Görünme suresi aralığı.
- Diğer stil parametreleri `mobile_style` ile aynıdır.
- **fadein** ve **fadeout**: Yazının giriş/çıkış efekt süreleri (ms).
Örnek bir yapılandırma için repodaki `config.json` dosyasını inceleyebilirsiniz.

