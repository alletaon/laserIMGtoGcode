from PIL import ImageTk, Image
import tkinter as tk
import time
from tkinter import filedialog, ttk
from laser import Layer
from threading import Thread


MAX_IMG_WIDTH = 800
MAX_IMG_HIGHT = 600

class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title('BMPtoGcode')
        self.master.iconbitmap('.\\laser.ico')
        toolbar = tk.Frame(self,)
        toolbar.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        tk.Button(toolbar, text="Открыть", command=self.open).pack(side=tk.LEFT, padx=5)
        tk.Label(toolbar, text='Шаг: ').pack(side=tk.LEFT, padx=5)
        self.step = tk.DoubleVar(value=0.125)
        tk.Entry(toolbar, textvariable=self.step).pack(side=tk.LEFT, padx=5)
        tk.Label(toolbar, text='Скорость: ').pack(side=tk.LEFT, padx=5)
        self.speed = tk.IntVar(value=100)
        tk.Entry(toolbar, textvariable=self.speed).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Сгенерировать", command=self.generate).pack(side=tk.LEFT, padx=5)
        toolbar.pack(side=tk.TOP, pady=10, fill=tk.BOTH)

        self.file_path = tk.StringVar()
        tk.Label(self, textvariable=self.file_path).pack(side=tk.TOP, fill=tk.BOTH)

        self.la = tk.Label(self)
        self.la.pack(padx=5, pady=5)

        statusbar = tk.Frame(self,)
        tk.Label(statusbar, text='Статус генерации: ').pack(side=tk.LEFT, padx=5)
        self.progress = ttk.Progressbar(statusbar, orient='horizontal', mode='determinate', length=150, value=0)
        self.progress.pack(side=tk.LEFT, padx=5)
        self.time = tk.StringVar(value='00:00:00')
        tk.Entry(statusbar, textvariable=self.time, state=tk.DISABLED).pack(side=tk.RIGHT, padx=5)
        tk.Label(statusbar, text='Время выполнения: ').pack(side=tk.RIGHT, padx=5)
        statusbar.pack(side=tk.BOTTOM, pady=10, fill=tk.BOTH)

        self.pack()

    def chg_image(self):
        self.progress['value'] = 0
        self.time.set('00:00:00')
        if self.im.mode != '1':
            self.im = self.im.convert('1')
        if self.im.width > MAX_IMG_WIDTH or self.im.height > MAX_IMG_HIGHT:
            k = max(self.im.width / MAX_IMG_WIDTH, self.im.height / MAX_IMG_HIGHT)
            size = (int(self.im.width / k), int(self.im.height / k))
            self.img = ImageTk.BitmapImage(self.im.resize(size, Image.ANTIALIAS), foreground="white")
        else:
            self.img = ImageTk.BitmapImage(self.im, foreground="white")
        self.la.config(image=self.img, bg="#000000", width=self.img.width(), height=self.img.height())

    def open(self):
        filename = filedialog.askopenfilename(filetypes=(("BMP Image", '.bmp'),))
        if filename != "":
            self.im = Image.open(filename)
            self.file_path.set(filename)
            self.chg_image()

    def generate(self):
        filename = filedialog.asksaveasfilename(filetypes=(("G code", '.cnc'),))
        if filename != "":
            if not filename.endswith('.cnc'):
                filename = filename + '.cnc'
            gen_thread = Thread(target=self.set_layer, args=(filename,))
            gen_thread.start()

    def set_layer(self, filename):
        self.progress['value'] = 0
        self.layer = Layer(0, list(self.im.getdata()), self.im.width)
        self.progress['value'] = 50
        out = open(filename, 'w')
        out.writelines(self.layer.code(self.step.get(), self.speed.get()))
        out.close()
        self.progress['value'] = 100
        estimate_time = self.layer.estimate(self.speed.get(), self.step.get())
        self.time.set(time.strftime('%H:%M:%S', time.gmtime(estimate_time)))


if __name__ == "__main__":
    app = App()
    app.mainloop()
