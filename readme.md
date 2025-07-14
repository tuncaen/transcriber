# Altyazı Araçları

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
- `srt.py` dosyasını çalıştırarak, `config.json` dosyasında belirtilen video veya ses dosyasından otomatik olarak altyazı dosyası (`.srt`) oluşturabilirsiniz. Komut satırında dosya adı vermenize gerek yoktur, gerekli bilgiler `config.json` üzerinden okunur.
    ```bash
    python srt.py
    ```

### 1.1. Video veya ses dosyasından ses çıkarmak için örnek ffmpeg komutu:
```bash
ffmpeg -i "input.mp4" -vn "output.mp3"
```
Bu komut, video dosyasından sesi ayırıp mp3 olarak kaydeder.

### 2. Altyazı dosyasının imla kontrolü
- `srt.py` tarafından oluşturulan `*.srt` dosyasını bir metin
  düzenleyicisi ile açarak yazım ve noktalama hatalarını düzeltin.
  AI araçları kullanarak bu işlemi daha hızlı yapabilirsiniz.

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
  ffmpeg -i "input.mp4" -vf "ass=input.ass" -c:a copy "output_embedsubs.mp4"
  ```
  Bu komut, belirtilen ASS altyazı dosyasını videoya gömer ve ses parçasını değiştirmeden yeni bir video dosyası oluşturur.


## `config.json` parametreleri

Aşağıdaki başlıca alanlar `config.json` dosyası ile yapılandırılabilir:

- **audio_file**: Sadece ses içeren giriş dosyası.
- **video_file**: Video içeren giriş dosyası (audio_file yoksa kullanılır).
- **srt_file**: `srt.py` çalıştırıldığında oluşturulacak altyazı dosyası.
- **ass_file**: `srt2ass.py` tarafından üretilen ASS dosyasının adı.
- **delay_seconds**: Altyazıların ne kadar süre kaydırılacağı. (Giriş kısmı videoya eklenmeden önce srt oluşturulduğu durumda gerekli)
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

- **fontname**: Kullanılacak yazı tipi. Windows'ta yüklü bir fontun adı olmalıdır. Eğer font sistemde yoksa Arial kullanılır.
- **fontsize**: Yazı tipi boyutu (punto cinsinden).
- **primarycolor**: Altyazı metninin ana rengi. BGR (mavi-yeşil-kırmızı) formatında uzun bir tam sayı olarak belirtilir.
- **backcolor**: Altyazı kenarlığı veya gölgesi için arka plan rengi. BGR formatında.
- **outline**: Metnin etrafındaki kenarlık kalınlığı (piksel cinsinden). Sadece BorderStyle 1 ise geçerlidir.
- **shadow**: Metnin arkasındaki gölge derinliği (piksel cinsinden). Sadece BorderStyle 1 ise geçerlidir.
- **alignment**: Altyazının ekrandaki yatay ve dikey hizalamasını belirler. Numpad düzenine göre: 1-3 alt, 4-6 orta, 7-9 üst. (1=sol, 2=orta, 3=sağ; 4 eklenirse üst başlık, 8 eklenirse orta başlık)
- **marginl**, **marginr**: Kenar boşlukları. Ekranın sol ve sağ kenarından olan mesafeler (piksel cinsinden).
- **marginv** :  Altyazının dikey konumunu piksel cinsinden belirler.
    - Bir altyazı (subtitle) için, ekranın altından olan mesafeyi ifade eder.
    - Bir üst başlık (toptitle) için, ekranın üstünden olan mesafeyi ifade eder.
    - Bir orta başlık (midtitle) için, bu değer dikkate alınmaz; metin otomatik olarak dikeyde ortalanır
- **bold**: Metnin kalın olup olmadığını belirtir. -1 kalın, 0 normal.
- **borderstyle**: Kenarlık stili. 1: Kenarlık + gölge, 3: Opak kutu.
- **opacity**: Arka planın saydamlığı (ASS formatında alpha kanalı ile ayarlanır).

### components
Her bir öğe ekranda belirli zamanlarda gösterilecek metin kutusu ve stilini tanımlar.

- **text**: Görünecek yazı.
- **start_seconds** / **end_seconds**: Görünme suresi aralığı.
- Diğer stil parametreleri `mobile_style` ile aynıdır.
- **fadein** ve **fadeout**: Yazının giriş/çıkış efekt süreleri (ms).  

Örnek bir yapılandırma için repodaki `config.json` dosyasını inceleyebilirsiniz.

