import cv2
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, filedialog
from scipy.ndimage import median_filter

# Filtre fonksiyonlarını tanımlıyoruz formül vs varsa buraya açıklayabilirsiniz
def ortalama_filtresi(goruntu, kernel_size=(5, 5)):
    return cv2.blur(goruntu, kernel_size)

def gaussian_filtresi(goruntu, kernel_size=(5, 5), sigma=1):
    return cv2.GaussianBlur(goruntu, kernel_size, sigma)

def medyan_filtresi(goruntu, kernel_size=5):
    return median_filter(goruntu, size=kernel_size)

def sobel_filtresi(goruntu):
    sobel_x = cv2.Sobel(goruntu, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(goruntu, cv2.CV_64F, 0, 1, ksize=3)
    return cv2.magnitude(sobel_x, sobel_y)

def laplace_filtresi(goruntu):
    return cv2.Laplacian(goruntu, cv2.CV_64F, ksize=3)

def spatial_correlation(goruntu):
    kernel = np.array([[1, 1, 1],
                       [1, 1, 1],
                       [1, 1, 1]], dtype=np.float32) / 9
    return cv2.filter2D(goruntu, -1, kernel)

# Filtreleri  uygulama fonksiyonlarımız yazdığım kod dizini
def apply_filter():
    selected_filter = filter_var.get()

    if not image_path.get():
        messagebox.showerror("Hata", "Lütfen önce bir görüntü seçin!")
        return

    goruntu = cv2.imread(image_path.get(), cv2.IMREAD_GRAYSCALE)
    if goruntu is None:
        messagebox.showerror("Hata", "Görüntü yüklenemedi!")
        return
    
    if selected_filter == "Ortalama":
        filtered_image = ortalama_filtresi(goruntu)
    elif selected_filter == "Gaussian":
        filtered_image = gaussian_filtresi(goruntu)
    elif selected_filter == "Medyan":
        filtered_image = medyan_filtresi(goruntu)
    elif selected_filter == "Sobel":
        filtered_image = sobel_filtresi(goruntu)
    elif selected_filter == "Laplace":
        filtered_image = laplace_filtresi(goruntu)
    elif selected_filter == "Lineer Spatial":
        filtered_image = spatial_correlation(goruntu)
    else:
        messagebox.showerror("Hata", "Geçersiz filtre seçimi!")
        return
    
    show_results(goruntu, filtered_image, selected_filter)

def show_results(original, filtered, filter_name):
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1), plt.imshow(original, cmap='gray'), plt.title('Orijinal')
    plt.axis('off')
    
    plt.subplot(1, 2, 2), plt.imshow(filtered, cmap='gray'), plt.title(f'{filter_name} Filtrelenmiş')
    plt.axis('off')
    
    plt.show()

def select_image():
    file_path = filedialog.askopenfilename(title="Bir resim seçin", filetypes=[("Image files", "*.jpg;*.png;*.tif")])
    if file_path:
        image_path.set(file_path)
        messagebox.showinfo("Başarılı", f"{file_path} başarıyla yüklendi.")

# Basit BİR Arayüzü oluşturalım
root = tk.Tk()
root.title("Görüntü Filtre Uygulama")

filter_frame = tk.Frame(root)
filter_frame.pack()

filter_var = tk.StringVar(value="Ortalama")

filters = ["Ortalama", "Gaussian", "Medyan", "Sobel", "Laplace", "Lineer Spatial"]
for i, filter_name in enumerate(filters):
    tk.Radiobutton(filter_frame, text=filter_name, variable=filter_var, value=filter_name).grid(row=i, column=0, sticky="w")

select_button = tk.Button(root, text="Fotoğraf Seç", command=select_image)
select_button.pack(pady=10)

image_path = tk.StringVar()

apply_button = tk.Button(root, text="Filtreyi Uygula", command=apply_filter)
apply_button.pack()

root.mainloop()
