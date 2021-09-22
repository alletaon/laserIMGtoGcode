from PIL import ImageTk, Image
import tkinter as tk
from tkinter import filedialog
from laser import Layer


MAX_IMG_WIDTH = 800
MAX_IMG_HIGHT = 600

class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title('BMPtoGcode')
        self.master.iconbitmap('.\\laser.ico')
        frame = tk.Frame(self,)
        frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        tk.Button(frame, text="Открыть", command=self.open).pack(side=tk.LEFT, padx=5)
        tk.Label(frame, text='Шаг: ').pack(side=tk.LEFT, padx=5)
        self.step = tk.DoubleVar(value=0.125)
        tk.Entry(frame, textvariable=self.step).pack(side=tk.LEFT, padx=5)
        tk.Label(frame, text='Скорость: ').pack(side=tk.LEFT, padx=5)
        self.speed = tk.IntVar(value=100)
        tk.Entry(frame, textvariable=self.speed).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Сгенерировать", command=self.generate).pack(side=tk.LEFT, padx=5)
        frame.pack(side=tk.TOP, pady=10, fill=tk.BOTH)

        self.file_path = tk.StringVar()
        tk.Label(self, textvariable=self.file_path).pack(side=tk.TOP, fill=tk.BOTH)

        self.la = tk.Label(self)
        self.la.pack(padx=5, pady=5)

        self.pack()

    def chg_image(self):
        if self.im.mode != '1':
            self.im = self.im.convert('1')
        if self.im.width > MAX_IMG_WIDTH or self.im.height > MAX_IMG_HIGHT:
            self.img = ImageTk.BitmapImage(self.im.resize((MAX_IMG_WIDTH, MAX_IMG_HIGHT)), foreground="white")
        else:
            self.img = ImageTk.BitmapImage(self.im, foreground="white")
        self.la.config(image=self.img, bg="#000000", width=self.img.width(), height=self.img.height())

    def open(self):
        filename = filedialog.askopenfilename()
        if filename != "":
            self.im = Image.open(filename)
            self.file_path.set(filename)
            self.chg_image()

    def generate(self):
        filename = filedialog.asksaveasfilename()
        if filename != "":
            self.set_layer(filename)

    def set_layer(self, filename):
        self.layer = Layer(0, list(self.im.getdata()), self.im.width)
        out = open(filename, 'w')
        out.write('G0X0Y0Z0\n')
        out.write(f'G90G1F{self.speed.get() * 60}\n')
        out.writelines(self.layer.code(self.step.get()))
        out.write('M30')
        out.close()


if __name__ == "__main__":
    app = App()
    app.mainloop()
