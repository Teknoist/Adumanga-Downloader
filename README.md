# Adumanga Downloader

<img src="https://raw.githubusercontent.com/Teknoist/Adumanga-Downloader/refs/heads/main/logo.png" width="300" height="300">


Bu uygulama, manga bölümlerini belirli bir URL'den indirip PDF formatında kaydetmenizi sağlar. Uygulama, bölümleri indirir, resimleri doğrular ve geçersiz JPEG dosyalarını PNG'ye dönüştürür.

# Adumanga Downloader - Kolay Kurulum ve Kullanım

Merhaba Manga Severler!

Terminal veya komut satırı kullanmak sizin için göz korkutucu mu? Merak etmeyin, Adumanga Downloader uygulamamızı kullanmak artık çok daha kolay. Sizler için hazırladığımız hazır EXE dosyası sayesinde, terminal komutlarıyla uğraşmadan, sadece birkaç tıklama ile manga indirmenin keyfini çıkarabilirsiniz.

## Neden EXE Dosyası?

EXE dosyası, uygulamamızı Windows ortamında kolayca çalıştırmanızı sağlar. Terminal komutları ve Python kurulumlarıyla uğraşmadan, doğrudan uygulamamızı kullanabilirsiniz. İşte EXE dosyasının sağladığı bazı avantajlar:

- **Kolay Kurulum:** Python veya başka bir yazılım yüklemenize gerek yok. Tek yapmanız gereken EXE dosyasını indirip çalıştırmak.
- **Kullanım Kolaylığı:** Terminal komutlarıyla uğraşmak yerine, kullanıcı dostu arayüzümüz ile manga URL'sini girip, bölümleri indirmenin keyfini çıkarın.
- **Hızlı ve Güvenilir:** Adumanga Downloader, hızlı ve güvenilir bir şekilde manga bölümlerini indirir ve PDF formatında kaydeder.

## Adım Adım EXE Dosyası ile Kullanım

1. En son sürümü [Releases](https://github.com/Teknoist/Adumanga-Downloader/releases) kısmından indirin.
2. İndirilen EXE dosyasını çalıştırın.
3. Açılan arayüzde, manga URL'sini girin ve "Bölüm Sayısını Al" butonuna tıklayın.
4. Başlangıç ve bitiş bölümlerini belirleyin.
5. "İndir" butonuna tıklayın.
6. İndirme işlemi tamamlandığında, PDF dosyaları belirttiğiniz dizinde oluşturulacaktır.

## Ben Terminal Seven Biriyim Derseniz Buyrun Gerekli Tüm Bilgiler

Terminal veya komut satırı kullanmayı sevmiyorsanız ya da bu konuda deneyimsizseniz, EXE dosyamız tam size göre! Sadece yukarıdaki adımları takip ederek manga indirme işlemini kolay ve hızlı bir şekilde tamamlayabilirsiniz.


## Gereksinimler

Bu uygulamayı Python ile çalıştırmak için aşağıdaki araçlar ve kütüphaneler gereklidir:
- Python 3.6 veya üstü
- pip (Python package installer)

### Python Paketleri

Aşağıdaki Python paketleri gereklidir:

- requests
- selenium
- webdriver-manager
- beautifulsoup4
- fpdf
- pillow
- customtkinter

## Kurulum

### Linux ve macOS

1. Python ve pip kurulu olduğundan emin olun:

    ```sh
    python3 --version
    pip3 --version
    ```

    Python veya pip yüklü değilse, paket yöneticisini kullanarak yükleyebilirsiniz:

    ```sh
    # Ubuntu / Debian
    sudo apt update
    sudo apt install python3 python3-pip

    # macOS (Homebrew kullanarak)
    brew install python3
    ```

2. Bu projeyi klonlayın veya indirin:

    ```sh
    git clone https://github.com/Teknoist/Adumanga-Downloader.git
    cd Adumanga-Downloader
    ```

3. Gerekli Python paketlerini yükleyin:

    ```sh
    pip3 install -r requirements.txt
    ```

### Windows

1. Python ve pip kurulu olduğundan emin olun:

    ```sh
    python --version
    pip --version
    ```

    Python veya pip yüklü değilse, [Python'un resmi web sitesinden](https://www.python.org/) indirin ve yükleyin.

2. Bu projeyi aşağıdaki linkten indirin:

    [Adumanga Downloader - RAW](https://github.com/Teknoist/Adumanga-Downloader/archive/refs/heads/main.zip)

3. İndirilen ZIP dosyasını çıkarın ve `Adumanga-Downloader-main` klasörüne girin.

4. Gerekli Python paketlerini yükleyin:

    ```sh
    pip install -r requirements.txt
    ```

## Kullanım

1. Uygulamayı başlatmak için aşağıdaki komutu çalıştırın:

    ```sh
    python main.py
    ```

2. Açılan arayüzde, manga URL'sini girin ve "Bölüm Sayısını Al" butonuna tıklayın.

3. Başlangıç ve bitiş bölümlerini belirleyin.

4. "İndir" butonuna tıklayın.

5. İndirme işlemi tamamlandığında, PDF dosyaları belirttiğiniz dizinde oluşturulacaktır.

## Bilinen Sorunlar

- Geçersiz JPEG dosyaları indirilirse, bunlar otomatik olarak PNG'ye dönüştürülür.
- İndirme işlemi sırasında internet bağlantısı kesilirse, işlemi tekrar başlatmanız gerekebilir.

## Katkıda Bulunma

Katkıda bulunmak isterseniz, lütfen bir pull request gönderin veya bir sorun bildirin.

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.
