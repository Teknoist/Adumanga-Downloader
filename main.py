import os
import time
import requests
import threading
import customtkinter as ctk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from fpdf import FPDF
from PIL import Image

def fetch_chapter_links(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        chapter_list = soup.find("div", {"class": "eplister"}).find_all("li")
        chapters = []
        for chapter in chapter_list:
            link = chapter.find("a")["href"]
            chapter_num = chapter.find("span", {"class": "chapternum"}).text.strip()
            chapters.append(f'{chapter_num}: "{link}"')
        return chapters[::-1]  # Listeyi tersine çevir
    else:
        print(f"HTML içeriği alınamadı. HTTP Durum Kodu: {response.status_code}")
        return []

def save_chapters_to_file(chapters, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(chapters))
    print(f"Bölüm listesi '{file_path}' dosyasına yazıldı.")

def fetch_image_urls(url):
    options = Options()
    options.add_argument('--headless')  # Tarayıcıyı başlık olmadan çalıştır

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(30)  # Sayfa yüklenme zaman aşımını 30 saniye olarak ayarla

    try:
        driver.get(url)
        time.sleep(10)  # Sayfanın tamamen yüklenmesi için bekleyin
    except Exception as e:
        print(f"Error loading page: {url}, {e}")
        driver.quit()
        return []

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    image_elements = soup.select('img.ts-main-image')
    image_urls = [img['src'] for img in image_elements]

    driver.quit()
    return image_urls

def download_image(url, path):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Downloaded: {path}")
                return True
            else:
                print(f"Failed to download image: {url} (Attempt {attempt+1}/{max_retries})")
        except Exception as e:
            print(f"An error occurred while downloading {url}: {e} (Attempt {attempt+1}/{max_retries})")
    return False

def is_valid_jpeg(filepath):
    try:
        with open(filepath, 'rb') as f:
            f.seek(0)
            if f.read(2) != b'\xff\xd8':
                return False
            f.seek(-2, os.SEEK_END)
            if f.read() != b'\xff\xd9':
                return False
        return True
    except:
        return False

def convert_to_png(image_path):
    try:
        im = Image.open(image_path)
        png_path = os.path.splitext(image_path)[0] + ".png"
        im.save(png_path, 'PNG')
        return png_path
    except Exception as e:
        print(f"An error occurred while converting to PNG: {e}")
        return None
def create_pdf(image_paths, output_path):
    pdf = FPDF()
    for image_path in image_paths:
        if os.path.exists(image_path):
            pdf.add_page()
            pdf.image(image_path, x = 10, y = 10, w = 180)
    pdf.output(output_path, "F")
    delete_images(image_paths)  # Resim dosyalarını sil

def delete_images(image_paths):
    for image_path in image_paths:
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"Deleted: {image_path}")

def clean_temp_files():
    if os.path.exists('output.txt'):
        os.remove('output.txt')
    if os.path.exists('temp'):
        for filename in os.listdir('temp'):
            file_path = os.path.join('temp', filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        os.rmdir('temp')

def fetch_chapters():
    manga_url = entry_url.get()
    manga_name = manga_url.strip('/').split('/')[-1]
    manga_dir = os.path.join(os.getcwd(), manga_name)

    if not os.path.exists(manga_dir):
        os.makedirs(manga_dir)

    chapters = fetch_chapter_links(manga_url)
    if not chapters:
        messagebox.showerror("Hata", "Bölüm listesi alınamadı.")
        return

    save_chapters_to_file(chapters, 'output.txt')

    total_chapters = len(chapters)
    label_chapters_count.configure(text=f"Toplam Bölüm Sayısı: {total_chapters}")

def stop_download():
    global stop_flag
    stop_flag = True

def start_download():
    global stop_flag
    stop_flag = False

    def download():
        manga_url = entry_url.get()
        manga_name = manga_url.strip('/').split('/')[-1]
        manga_dir = os.path.join(os.getcwd(), manga_name)

        # Kod çalışmaya başlamadan önce temp klasörünü ve output.txt dosyasını sil
        clean_temp_files()

        if not os.path.exists(manga_dir):
            os.makedirs(manga_dir)

        # Bölüm linklerini içeren dosyanın varlığını kontrol et ve oluştur
        if not os.path.exists('output.txt'):
            fetch_chapters()

        # Kullanıcıdan bölüm aralığını alma
        from_chapter = int(entry_from.get())
        to_chapter = int(entry_to.get())

        with open('output.txt', 'r', encoding='utf-8') as file:
            urls = file.readlines()

        selected_urls = []
        for line in urls:
            title, url = line.strip().split(': ')
            chapter_num = title.split()[1].split('-')[0]
            if from_chapter <= int(chapter_num) <= to_chapter:
                if '-' in title.split()[1]:
                    part_num = title.split()[1].split('-')[1]
                    title = f"Bölüm {chapter_num}-p{part_num}"
                else:
                    title = f"Bölüm {chapter_num}"
                selected_urls.append(f"{title}: {url}")

        button_download.configure(state="disabled")
        progress_bar.start()

        if not os.path.exists('temp'):
            os.makedirs('temp')

        for i, line in enumerate(selected_urls, start=1):
            if stop_flag:
                break
            title, url = line.strip().split(': ')
            title = title.replace('Bölüm ', 'Bolum_').replace(' ', '_').replace(':', '').replace('"', '')
            output_pdf = os.path.join(manga_dir, f'{title}.pdf')
            temp_dir = 'temp'

            if os.path.exists(output_pdf):
                label_status.configure(text=f"{i}. PDF zaten var, atlanıyor: {output_pdf}")
                print(f"PDF already exists, skipping: {output_pdf}")
                continue

            label_status.configure(text=f"İndiriliyor: {title}")
            print(f"Processing {url.strip()}...")
            image_urls = fetch_image_urls(url.strip('"'))
            if not image_urls:
                print(f"No images found for {url.strip()}")
                continue

            image_paths = []
            for index, image_url in enumerate(image_urls):
                image_path = os.path.join(temp_dir, f'{title}_image_{index}.jpg')
                if download_image(image_url, image_path):
                    if not is_valid_jpeg(image_path):
                        image_path = convert_to_png(image_path)
                if image_path:
                    image_paths.append(image_path)

            if image_paths:
                create_pdf(image_paths, output_pdf)
                label_status.configure(text=f"PDF oluşturuldu: {title}")
                print(f"PDF başarıyla oluşturuldu: {output_pdf}")
            else:
                print(f"No images were downloaded for {url.strip()}")

        progress_bar.stop()
        button_download.configure(state="normal")
        messagebox.showinfo("Tamamlandı", "İndirme işlemi tamamlandı!")

    download_thread = threading.Thread(target=download)
    download_thread.start()

# UI oluşturma
app = ctk.CTk()
app.title("Manga Downloader")
app.protocol("WM_DELETE_WINDOW", stop_download)  # Pencere kapatıldığında durdurmayı etkinleştir

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label_title = ctk.CTkLabel(master=frame, text="Manga İndirme Aracı")
label_title.pack(pady=12, padx=10)

label_url = ctk.CTkLabel(master=frame, text="Manga URL:")
label_url.pack(pady=5, padx=10)

entry_url = ctk.CTkEntry(master=frame, width=350)
entry_url.pack(pady=5, padx=10)

label_chapters_count = ctk.CTkLabel(master=frame, text="Toplam Bölüm Sayısı: ?")
label_chapters_count.pack(pady=5, padx=10)

button_fetch_chapters = ctk.CTkButton(master=frame, text="Bölüm Sayısını Al", command=fetch_chapters)
button_fetch_chapters.pack(pady=5, padx=10)

label_from_chapter = ctk.CTkLabel(master=frame, text="Başlangıç Bölümü:")
label_from_chapter.pack(pady=5, padx=10)

entry_from = ctk.CTkEntry(master=frame, width=50)
entry_from.pack(pady=5, padx=10)

label_to_chapter = ctk.CTkLabel(master=frame, text="Bitiş Bölümü:")
label_to_chapter.pack(pady=5, padx=10)

entry_to = ctk.CTkEntry(master=frame, width=50)
entry_to.pack(pady=5, padx=10)

button_download = ctk.CTkButton(master=frame, text="İndir", command=start_download)
button_download.pack(pady=20, padx=10)

label_status = ctk.CTkLabel(master=frame, text="")
label_status.pack(pady=5, padx=10)

progress_bar = ctk.CTkProgressBar(master=frame)
progress_bar.pack(pady=20, padx=10)

app.mainloop()
