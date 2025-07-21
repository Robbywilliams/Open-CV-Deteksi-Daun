import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Label, Button
from PIL import Image, ImageTk

def hitung_daun(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Gambar tidak ditemukan!")
        return 0, img

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


    lower_green = np.array([25, 30, 30])
    upper_green = np.array([90, 255, 255])


    lower_green_dark = np.array([25, 20, 20])
    upper_green_dark = np.array([85, 255, 180])


    mask1 = cv2.inRange(hsv, lower_green, upper_green)
    mask2 = cv2.inRange(hsv, lower_green_dark, upper_green_dark)

    mask = cv2.bitwise_or(mask1, mask2)


    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Debug mask (opsional)
    # cv2.imshow("Mask Debug", mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    jumlah_daun = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h
        if 0.3 < aspect_ratio < 1.7 and area > 800:
            jumlah_daun += 1
            cv2.drawContours(img, [cnt], -1, (0, 255, 0), 2)


    max_width = 400
    h, w = img.shape[:2]
    if w > max_width:
        ratio = max_width / w
        img = cv2.resize(img, (int(w * ratio), int(h * ratio)))

    return jumlah_daun, img

def pilih_gambar():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if not file_path:
        return

    jumlah, hasil_img = hitung_daun(file_path)

    hasil_img_rgb = cv2.cvtColor(hasil_img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(hasil_img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)

    label_gambar.config(image=img_tk)
    label_gambar.image = img_tk
    label_hasil.config(text=f"Jumlah daun terdeteksi: {jumlah}")

root = tk.Tk()
root.title("Program Hitung Daun")
root.geometry("700x800")
root.configure(bg="#f0f0f0")

label_judul = Label(root, text="Program Hitung Daun", bg="#f0f0f0", font=("Helvetica", 16, "bold"))
label_judul.pack(pady=10)

placeholder = Image.new("RGB", (400, 300), color=(220, 220, 220))
img_placeholder = ImageTk.PhotoImage(placeholder)

label_gambar = Label(root, image=img_placeholder, bg="#d9d9d9", bd=4, relief="ridge")
label_gambar.image = img_placeholder
label_gambar.pack(pady=20)

label_hasil = Label(root, text="", bg="#f0f0f0", font=("Helvetica", 12))
label_hasil.pack(pady=10)

button_pilih = Button(root, text="Pilih Gambar", command=pilih_gambar, font=("Helvetica", 10, "bold"))
button_pilih.pack(pady=20)

root.mainloop()
