# Adumanga Downloader

Bu uygulama, manga bölümlerini belirli bir URL'den indirip PDF formatında kaydetmenizi sağlar. Uygulama, bölümleri indirir, resimleri doğrular ve geçersiz JPEG dosyalarını PNG'ye dönüştürür.

## EXE Dosyası ile Kullanım

1. En son sürümü [Releases](https://github.com/Teknoist/Adumanga-Downloader/releases) kısmından indirin.
2. İndirilen EXE dosyasını çalıştırın.
3. Açılan arayüzde, manga URL'sini girin ve "Bölüm Sayısını Al" butonuna tıklayın.
4. Başlangıç ve bitiş bölümlerini belirleyin.
5. "İndir" butonuna tıklayın.
6. İndirme işlemi tamamlandığında, PDF dosyaları belirttiğiniz dizinde oluşturulacaktır.

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
