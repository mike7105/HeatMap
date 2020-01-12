# -*- coding: utf-8 -*-
"""HeatMap GUI"""
import os
import queue
import threading
import time
import tkinter as tk
import tkinter.colorchooser as tkColor
import tkinter.filedialog as tkFD
import tkinter.messagebox as msgbox
import tkinter.ttk as ttk
import pandas as pd
from PIL import Image, ImageTk, ImageDraw


class Application(ttk.Frame):
    """класс для отрисовки HeatMap"""
    def __init__(self, master=None, version=""):
        super().__init__(master)
        self.master = master
        self.version = version
        self.grid_params = {"padx": 5, "pady": 5}
        self.grid(row=0, column=0, columnspan=2, sticky="wnse", **self.grid_params)

        # Button
        self.btn_exit = ttk.Button(text="Выход", command=self.master.destroy)
        self.btn_exit.grid(row=1, column=1, sticky="es", **self.grid_params)

        # ProgressBar
        self.var_pb = tk.IntVar()
        self.pgb = ttk.Progressbar(maximum=100, variable=self.var_pb)
        self.var_pb.set(0)
        self.pgb.grid(row=1, column=0, sticky="we")

        # LabelStatus
        self.var_status = tk.StringVar()
        self.var_status.set("")
        self.lbl_status = ttk.Label(textvariable=self.var_status, relief=tk.RIDGE)
        self.lbl_status.grid(row=2, column=0, sticky="wes")

        # Sizegrip
        self.sgp = ttk.Sizegrip()
        self.sgp.grid(row=2, column=1, sticky="es")

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.master.title("HeatMap")
        self.master.minsize(width=300, height=400)

        self.create_menu()
        self.create_widgets()

        # #####STYLE#######
        self.style = ttk.Style()

    def create_menu(self):
        """Создание меню"""
        # Создаем само главное меню и назначаем его окну приложения
        window = self.master
        self.mainmenu = tk.Menu(window, tearoff=False)
        window["menu"] = self.mainmenu

        # Создаем подменю Файл
        self.filemenu = tk.Menu(self.mainmenu, tearoff=False)

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Выход", accelerator="Ctrl+Q", command=self.master.destroy)
        self.bind_all("<Control-KeyPress-q>", lambda evt: self.btn_exit.invoke())

        self.mainmenu.add_cascade(label="Файл", menu=self.filemenu)

        # Добавляем меню Настройки в главное меню
        self.thememenu = tk.Menu(self.mainmenu, tearoff=False)

        self.them = tk.StringVar()
        self.them.set("vista")
        self.tharr = ["default", "winnative", "clam", "alt", "classic", "vista", "xpnative"]

        for style in self.tharr:
            self.thememenu.add_radiobutton(
                label=style, variable=self.them, value=style, command=self.change_theme)
        self.mainmenu.add_cascade(label="Темы", menu=self.thememenu)

        # Создаем подменю Справка
        self.helpmenu = tk.Menu(self.mainmenu, tearoff=False)
        self.helpmenu.add_command(label="О программе...", command=self.show_info)
        self.mainmenu.add_cascade(label="Справка", menu=self.helpmenu)

        # Контекстное меню
        self.contextmenu = tk.Menu(self, tearoff=False)
        self.contextmenu.add_command(label="Скопировать", command=self.copy)

    def create_widgets(self):
        """создает компненты GUI"""
        # список элементов, которые нужно блокировать
        self.elems = []

        # LabelImg
        self.lbl_img = ttk.Label(self, text="Choose image:")
        self.lbl_img.grid(row=0, column=0, columnspan=2, sticky="we", **self.grid_params)

        # EntryImg
        self.var_img = tk.StringVar()
        self.var_img.set("")
        self.ent_img = ttk.Entry(self, textvariable=self.var_img)
        self.ent_img.state(["disabled"])
        self.ent_img.bind("<Button-3>", lambda evt, obj=self.var_img: self.show_menu(evt, obj))
        self.ent_img.grid(row=1, column=0, sticky="we", **self.grid_params)

        # ButtonImg
        self.btn_img = ttk.Button(self, text="Choose...", command=self.open_img)
        self.btn_img.grid(row=1, column=1, sticky="w", **self.grid_params)
        self.elems.append(self.btn_img)

        # LabelData
        self.lbl_data = ttk.Label(self, text="Choose data:")
        self.lbl_data.grid(row=2, column=0, columnspan=2, sticky="we", **self.grid_params)

        # EntryData
        self.var_data = tk.StringVar()
        self.var_data.set("")
        self.ent_data = ttk.Entry(self, textvariable=self.var_data)
        self.ent_data.state(["disabled"])
        self.ent_data.bind("<Button-3>", lambda evt, obj=self.var_data: self.show_menu(evt, obj))
        self.ent_data.grid(row=3, column=0, sticky="we", **self.grid_params)

        # ButtonData
        self.btn_data = ttk.Button(self, text="Choose...", command=self.open_data)
        self.btn_data.grid(row=3, column=1, sticky="w", **self.grid_params)
        self.elems.append(self.btn_data)

        # Canvas
        self.canvas = tk.Canvas(self, width=300, height=300, bg='white')
        self.canvas.grid(row=4, column=0, columnspan=2, rowspan=4, sticky="wn", **self.grid_params)

        # Frame
        self.frm2 = ttk.Frame(self)

        # LabelRadius
        self.lbl_radius = ttk.Label(self.frm2, text="Entry radius in px:")
        self.lbl_radius.grid(row=0, column=0, sticky="w", **self.grid_params)

        # Spinbox
        self.var_radius = tk.IntVar()
        self.var_radius.set(1)
        self.spn_number = tk.Spinbox(
            self.frm2, from_=1, to=10, increment=1, exportselection=0, textvariable=self.var_radius)
        self.spn_number.grid(row=1, column=0, sticky="w", **self.grid_params)
        self.elems.append(self.spn_number)

        # ButtonColor
        self.btn_color = ttk.Button(self.frm2, text="Change color:", command=self.open_color)
        self.btn_color.grid(row=2, column=0, sticky="w", **self.grid_params)
        self.elems.append(self.btn_color)

        # LabelColor
        self.lbl_color = ttk.Label(self.frm2, background="#ff0000", width=-20)
        self.color = ((255, 0, 0), "#ff0000")
        self.lbl_color.grid(row=3, column=0, sticky="w", **self.grid_params)

        # LabelOpacity
        self.lbl_opacity = ttk.Label(self.frm2, text="Entry opacity (0 - 100%):")
        self.lbl_opacity.grid(row=4, column=0, sticky="w", **self.grid_params)

        # SpinboxOpacity
        self.var_opacity = tk.IntVar()
        self.var_opacity.set(50)
        self.spn_opacity = tk.Spinbox(
            self.frm2, from_=0, to=100, increment=10, exportselection=0, textvariable=self.var_opacity)
        self.spn_opacity.grid(row=5, column=0, sticky="w", **self.grid_params)
        self.elems.append(self.spn_opacity)

        # LabelDataImg
        self.lbl_dataimg = ttk.Label(self.frm2, text="Choose Data image and question:")
        self.lbl_dataimg.grid(row=6, column=0, sticky="w", **self.grid_params)

        # TreeView
        self.trw2 = ttk.Treeview(self.frm2, columns=("ConcQst", "Countdots"), displaycolumns=(0, 1), show="headings")
        self.trw2.heading("ConcQst", text="Image - QST")
        self.trw2.heading("Countdots", text="Count dots", anchor="center")
        self.trw2.grid(row=10, column=0, sticky="w", **self.grid_params)
        self.elems.append(self.trw2)

        # Scrollbar
        self.hor_scr = ttk.Scrollbar(self.frm2, orient=tk.HORIZONTAL, command=self.trw2.xview)
        self.hor_scr.grid(row=11, column=0, sticky="we")
        self.ver_scr = ttk.Scrollbar(self.frm2, command=self.trw2.yview)
        self.ver_scr.grid(row=10, column=1, sticky="ns")
        self.trw2.config(yscrollcommand=self.ver_scr.set, xscrollcommand=self.hor_scr.set)

        # ButtonDraw
        self.btn_draw = ttk.Button(self.frm2, text="Draw", command=self.drawdots)
        self.btn_draw.grid(row=12, column=0, sticky="w", **self.grid_params)
        self.elems.append(self.btn_draw)

        # ButtonSave
        self.btn_save = ttk.Button(self.frm2, text="Save", command=self.save_img)
        self.btn_save.grid(row=13, column=0, sticky="w", **self.grid_params)
        self.elems.append(self.btn_save)

        self.frm2.grid(row=0, column=2, rowspan=5, **self.grid_params)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=2)

    def drawdots(self):
        """Проход по координатам и отрисовка"""
        self.change_state(False)
        self.var_status.set("")
        if self.validate():
            # фильтрация нужных данных
            self.df2 = self.df.query('(X <= @self.img.size[0]) and (Y <= @self.img.size[1])')

            self.concqst = self.trw2.selection()[0].split(' - ')
            self.df2.query('(CONC == @self.concqst[0]) and (QST == @self.concqst[1])', inplace=True)

            # насчитываю координаты квадрата, куда вписывать точку ответа
            self.df2.eval('LEFT = X - @self.var_radius.get()', inplace=True)
            self.df2.eval('TOP = Y - @self.var_radius.get()', inplace=True)
            self.df2.eval('RIGHT = X + @self.var_radius.get()', inplace=True)
            self.df2.eval('BOTTOM = Y + @self.var_radius.get()', inplace=True)

            # цвет точки
            self.fillrgba = (int(self.color[0][0]), int(self.color[0][1]), 
                             int(self.color[0][2]), int(self.var_opacity.get() * 2.55))

            # точка для canvas
            self.pim = Image.new('RGBA', (self.var_radius.get() * 2 + 1, self.var_radius.get() * 2 + 1), (0, 0, 0, 0))
            self.draw = ImageDraw.Draw(self.pim, "RGBA")
            self.draw.ellipse((0, 0, self.pim.size[0], self.pim.size[1]), fill=self.fillrgba)
            self.photo = ImageTk.PhotoImage(self.pim)

            # картинка для сохранения
            self.photo2 = Image.open(self.var_img.get()).convert('RGBA')

            self.pgb["maximum"] = self.df2.shape[0]
            self.time_start = time.time()

            self.lock = threading.Lock()
            self.queue = queue.Queue()
            for i in range(self.df2.shape[0]):
                self.queue.put(i)

            threads = []
            quant_bariers = 10 ** (len(str(self.df2.shape[0])) // 2)
            quant_bariers = 100 if quant_bariers > 100 else quant_bariers
            self.barrier = threading.Barrier(quant_bariers)
            for i in range(0, quant_bariers - 1):
                thr = threading.Thread(target=self.draw_dots_thr)
                threads.append(thr)
                thr.start()
            thr = threading.Thread(target=self.thread_end)
            threads.append(thr)
            thr.start()

    def draw_dots_thr(self):
        """Рисует точки с использованием многопоточности"""
        local = threading.local()
        while not self.queue.empty():
            local.i = self.queue.get()
            # точка на canvas
            self.canvas.create_image(*self.df2.iloc[local.i, -4:-2:].to_list(), anchor=tk.NW,
                                     image=self.photo, tag="dot")

            # точка на картинке дял сохранения
            local.circle = Image.new('RGBA', self.photo2.size, (0, 0, 0, 0))
            local.d = ImageDraw.Draw(local.circle)
            local.d.ellipse(tuple(self.df2.iloc[local.i, -4::].to_list()), fill=self.fillrgba)

            with self.lock:
                self.photo2 = Image.alpha_composite(self.photo2, local.circle)
                self.var_status.set("dots: {0} from {1}".format(str(self.var_pb.get() + 1), str(self.df2.shape[0])))
                self.pgb.step()

            self.queue.task_done()

        self.barrier.wait()

    def thread_end(self):
        """Функция для завершающего потока"""
        self.barrier.wait()
        self.time_end = time.time()
        self.duration = self.time_end - self.time_start
        print(self.duration)
        self.change_state(True)

    def save_img(self):
        """сохранение изображения"""
        if self.validate():
            filename = tkFD.asksaveasfilename(
                title="Save heatmap", filetypes=[("Image PNG", ".png"), ("Image JPG", ".jpg")], defaultextension='.png')
            if filename:
                if str.lower(os.path.splitext(filename)[1]) == ".jpg":
                    self.photo2 = self.photo2.convert("RGB")
                else:
                    self.photo2 = self.photo2.convert("RGBA")

                self.photo2.save(filename, quality=100)
                self.var_status.set("Image was saved as {0}".format(filename))
            else:
                msgbox.showerror("Save heatmap", "File wasn't chosen!")
                self.var_status.set("")

    def open_img(self):
        """Выбор картинки"""
        self.var_status.set("")
        filename = tkFD.askopenfilename(
            title="Choose image", filetypes=(("Image JPG", "JPG"), ("Image PNG", "PNG")), defaultextension=".jpg")
        if filename:
            self.var_img.set(filename)
            self.img = Image.open(filename)
            self.tatras = ImageTk.PhotoImage(self.img)
            self.canvas.configure(width=self.img.size[0], height=self.img.size[1])
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tatras)
        else:
            msgbox.showerror("Choose image", "File wasn't chosen!")

    def open_data(self):
        """Выбор данных"""
        self.var_status.set("")
        filename = tkFD.askopenfilename(
            title="Choose data", filetypes=(("Data CSV", "CSV"), ("Data SPSS", "SAV")), defaultextension=".csv")
        if filename:
            self.var_data.set(filename)
            if str.lower(os.path.splitext(filename)[1]) == ".csv":
                self.df = pd.read_csv(filename)
            else:
                self.df = pd.read_spss(filename)

            self.df.columns = [str.upper(i) for i in self.df.columns]
            self.df.dropna(how='any', inplace=True)
            self.df.query('(X >= 0) and (Y >= 0)', inplace=True)

            # считаю статистику кликов
            stat = self.df.pivot_table(['X', 'Y'], index=['CONC', 'QST'], aggfunc='count')

            # добавляю статистику и CONC QST в TreeView
            self.trw2.delete(*self.trw2.get_children())
            for row in list(stat.index):
                self.trw2.insert("", "end", " - ".join(map(str, row)),
                                 values=(" - ".join(row), str(stat.loc[row, 'X'])))

        else:
            msgbox.showerror("Choose data", "File wasn't chosen!")

    def open_color(self):
        """Выбор цвета"""
        self.var_status.set("")
        self.color = tkColor.askcolor(self.lbl_color["background"])
        if self.color != (None, None):
            self.lbl_color["background"] = self.color[1]

    def show_info(self):
        """Показ информации"""
        msgbox.showinfo("О программе...", """{0}
        © Михаил Чесноков, 2019 г.
        mailto: Mihail.Chesnokov@ipsos.com""".format(self.version), parent=self)

    def show_menu(self, evt, obj):
        """Показывает контекстное меню"""
        self.to_copy = obj.get()
        self.contextmenu.post(evt.x_root, evt.y_root)

    def copy(self):
        """Копирует содержимое путей"""
        # print(self.to_copy)
        self.clipboard_clear()
        self.clipboard_append(self.to_copy)

    def change_theme(self):
        """меняет внешний вид при выборе встроенных тем"""
        self.style.theme_use(self.them.get())

    def validate(self) -> bool:
        """проверка введенных значений"""
        res = ""
        if not self.var_img.get():
            res = "Choose image!"
        if not hasattr(self, "df"):
            res = res + " Choose data!"
        if self.trw2.selection() == ():
            res = res + " Choose Data image - question!"
        if res:
            msgbox.showerror("Validation fail", res)
            return False
        return True

    def change_state(self, is_visible):
        """меняет активность элементов"""
        for elem in self.elems:
            if is_visible:
                if hasattr(elem, 'state'):
                    elem.state(["!disabled"])
                else:
                    elem.config(state="normal")
            else:
                if hasattr(elem, 'state'):
                    elem.state(["disabled"])
                else:
                    elem.config(state="disabled")


if __name__ == "__main__":
    pass
