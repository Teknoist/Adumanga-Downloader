import os
import time
import requests
import threading
import zipfile
import customtkinter as ctk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from PIL import Image

# UI tema karanlık
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

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
        return chapters[::-1]  # Listeyi ters çevir
    else:
        print(f"HTML içeriği alınamadı. HTTP Durum Kodu: {response.status_code}")
        return []

def fetch_image_urls(url):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(30)

    try:
        driver.get(url)
        time.sleep(10)
    except Exception as e:
        print(f"Sayfa yüklenirken hata oluştu: {url}, {e}")
        driver.quit()
        return []

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    image_elements = soup.select('img.ts-main-image')
    image_urls = [img['src'] for img in image_elements if 'src' in img.attrs]

    driver.quit()
    return image_urls

def download_image(url, path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return True
    except Exception as e:
        print(f"{url} indirilirken hata: {e}")
    return False

def create_cbz(image_paths, output_path):
    with zipfile.ZipFile(output_path, 'w') as cbz:
        for image in image_paths:
            cbz.write(image, arcname=os.path.basename(image))
    for img in image_paths:
        os.remove(img)

def start_download():
    def download():
        manga_url = entry_url.get()
        manga_name = manga_url.strip('/').split('/')[-1]
        manga_dir = os.path.join(os.getcwd(), manga_name)
        os.makedirs(manga_dir, exist_ok=True)

        chapters = fetch_chapter_links(manga_url)
        if not chapters:
            messagebox.showerror("Hata", "Bölüm alınamadı.")
            return

        from_chapter = float(entry_from.get())
        to_chapter = float(entry_to.get())

        for line in chapters:
            title, url = line.strip().split(': ')
            chapter_str = title.split()[1]
            try:
                chapter_num = float(chapter_str.replace('-', '.'))
            except:
                continue
            if from_chapter <= chapter_num <= to_chapter:
                clean_title = title.replace(' ', '_').replace(':', '').replace('"', '')
                output_cbz = os.path.join(manga_dir, f'{clean_title}.cbz')
                if os.path.exists(output_cbz):
                    label_status.configure(text=f"Atlanıyor (zaten var): {clean_title}")
                    continue
                label_status.configure(text=f"İndiriliyor: {clean_title}")
                image_urls = fetch_image_urls(url.strip('"'))
                if not image_urls:
                    continue
                image_paths = []
                for i, img_url in enumerate(image_urls):
                    image_path = os.path.join(manga_dir, f"{clean_title}_{i}.jpg")
                    if download_image(img_url, image_path):
                        image_paths.append(image_path)
                if image_paths:
                    create_cbz(image_paths, output_cbz)
                    label_status.configure(text=f"CBZ oluşturuldu: {clean_title}")
        messagebox.showinfo("Tamamlandı", "İndirme işlemi tamamlandı!")

    threading.Thread(target=download).start()

# UI Oluşturma
app = ctk.CTk()
app.title("Manga Downloader (CBZ)")

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=60, fill="both", expand=True)

ctk.CTkLabel(master=frame, text="Manga URL:").pack(pady=5)
entry_url = ctk.CTkEntry(master=frame, width=400)
entry_url.pack(pady=5)

ctk.CTkLabel(master=frame, text="Başlangıç Bölümü:").pack(pady=5)
entry_from = ctk.CTkEntry(master=frame, width=100)
entry_from.pack(pady=5)

ctk.CTkLabel(master=frame, text="Bitiş Bölümü:").pack(pady=5)
entry_to = ctk.CTkEntry(master=frame, width=100)
entry_to.pack(pady=5)

button_download = ctk.CTkButton(master=frame, text="İndir (CBZ)", command=start_download)
button_download.pack(pady=20)

label_status = ctk.CTkLabel(master=frame, text="Durum: Bekleniyor...")
label_status.pack(pady=10)

app.mainloop()
