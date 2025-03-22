import cv2
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from scipy.ndimage import median_filter

# Filtre fonksiyonlarını tanıtarak başlıyoruz ben görüntüyü 5*5 kernelda istedim dilerseniz değiştirebilirsiniz.
def ortalama_filtresi(goruntu, kernel_size=(5, 5)):
    """Ortalama filtresi uygulama"""
    return cv2.blur(goruntu, kernel_size)

def gaussian_filtresi(goruntu, kernel_size=(5, 5), sigma=1):
    """Gaussian filtresi uygulama"""
    return cv2.GaussianBlur(goruntu, kernel_size, sigma)

def medyan_filtresi(goruntu, kernel_size=5):
    """Medyan filtresi uygulama"""
    return median_filter(goruntu, size=kernel_size)

def sobel_filtresi(goruntu):
    """Sobel kenar tespiti uygulama"""
    sobel_x = cv2.Sobel(goruntu, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(goruntu, cv2.CV_64F, 0, 1, ksize=3)
    return cv2.magnitude(sobel_x, sobel_y)

def spatial_correlation(goruntu):
    """Lineer uzaysal korelasyon (Spatial Correlation) uygular"""
    kernel = np.array([[1, 1, 1],
                       [1, 1, 1],
                       [1, 1, 1]], dtype=np.float32) / 9  # 3x3 ortalama kernel
    return cv2.filter2D(goruntu, -1, kernel)

# Seçtiğiniz filtreyi fotoğraf üzerinde uygular
def apply_filter():
    """Seçilen filtreyi uygulama"""
    selected_filter = filter_var.get()

    # Size bilgisayardan fotoğraf seçtirerek dosya yolunu izler 
    if not image_path.get():
        messagebox.showerror("Hata", "Lütfen önce bir görüntü seçin!")
        return

    # Görüntüyü okur
    goruntu = cv2.imread(image_path.get(), cv2.IMREAD_GRAYSCALE)
    if goruntu is None:
        messagebox.showerror("Hata", "Görüntü yüklenemedi!")
        return
    
    # Burada istediğimiz Filtreyi goruntuye atadıgımız görsele uygular
    if selected_filter == "Ortalama":
        filtered_image = ortalama_filtresi(goruntu)
    elif selected_filter == "Gaussian":
        filtered_image = gaussian_filtresi(goruntu)
    elif selected_filter == "Medyan":
        filtered_image = medyan_filtresi(goruntu)
    elif selected_filter == "Sobel":
        filtered_image = sobel_filtresi(goruntu)
    elif selected_filter == "Lineer Spatial":  
        filtered_image = spatial_correlation(goruntu)
    else:
        messagebox.showerror("Hata", "Geçersiz filtre seçimi!")
        return
    
    # Sonuçları göster
    show_results(goruntu, filtered_image, selected_filter)

def show_results(original, filtered, filter_name):
    """Filtre uygulandıktan sonra sonuçları göster"""
    plt.figure(figsize=(10, 5))
    
    # 1. Orijinal Görüntü
    plt.subplot(1, 2, 1), plt.imshow(original, cmap='gray'), plt.title(f'Orijinal')
    plt.axis('off')  # Eksenleri kapat
    
    # 2. Filtrelenmiş Görüntü
    plt.subplot(1, 2, 2), plt.imshow(filtered, cmap='gray'), plt.title(f'{filter_name} Filtrelenmiş')
    plt.axis('off')  # Eksenleri kapat
    
    plt.show()

def select_image():
    """Fotoğraf seçme fonksiyonu"""
    file_path = filedialog.askopenfilename(title="Bir resim seçin", filetypes=[("Image files", "*.jpg;*.png;*.tif")])
    if file_path:
        image_path.set(file_path)
        messagebox.showinfo("Başarılı", f"{file_path} başarıyla yüklendi.")

# Ana pencereyi oluştur
root = tk.Tk()
root.title("Görüntü Filtre Uygulama")

# Filtre seçenekleri için frame oluştur
filter_frame = tk.Frame(root)
filter_frame.pack()

# Filtre seçeneklerini alt alta sıralamak için grid() fonksiyonunu kullanalım
filter_var = tk.StringVar(value="Ortalama")  # Varsayılan filtre

filters = ["Ortalama", "Gaussian", "Medyan", "Sobel", "Lineer Spatial"]  # Burada "Lineer Spatial" seçeneği var
for i, filter_name in enumerate(filters):
    tk.Radiobutton(filter_frame, text=filter_name, variable=filter_var, value=filter_name).grid(row=i, column=0, sticky="w")

# Fotoğraf seçimi için buton6
select_button = tk.Button(root, text="Fotoğraf Seç", command=select_image)
select_button.pack(pady=10)

# Fotoğraf seçimi için label
image_path = tk.StringVar()  # Seçilen fotoğrafın yolu

# Filtreyi uygulamak için buton
apply_button = tk.Button(root, text="Filtreyi Uygula", command=apply_filter)
apply_button.pack()

root.mainloop()
