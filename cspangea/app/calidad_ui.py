import base64
import urllib.request
from tkinter import Tk, PhotoImage, Label, Entry, Button
from tkinter import ttk
from tkinter.constants import W, EW
from tkinter.ttk import Combobox

from cspangea.app.calidad import Calidad
from cspangea.app.constants import APP_VIOLATION_COLOR_CODE, APP_TITLE, APP_ICO


class Ui:
    def __init__(self, calidad: Calidad):
        self.window = Tk()

        self.window.title(APP_TITLE)
        # self.window.iconbitmap('icon.ico')
        self.__set_icon()
        self.calidad = calidad
        self.init_row_infractions = 2

        self.tab_control = ttk.Notebook(self.window)

        # Tab1 Content:
        self.tab_main = None
        self.__show_main_frame()

        self.tab_control.pack(expand=1, fill='both')
        # self.window.geometry("%dx%d" % (self.window_width, self.window_height))
        self.window.geometry("")
        self.window.mainloop()

    def __set_icon(self):
        raw_data = urllib.request.urlopen(APP_ICO).read()

        b64_data = base64.encodebytes(raw_data)
        image = PhotoImage(data=b64_data)
        self.window.tk.call('wm', 'iconphoto', self.window._w, image)

    # ------------------------------------------------------------------------------------------------
    # TAB 1
    # ------------------------------------------------------------------------------------------------

    def __show_main_frame(self):
        self.tab_main = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_main, text='Buscar')

        lbl = Label(self.tab_main, text="Archivo:")
        lbl.grid(column=0, row=0, sticky=W)
        self.file = Entry(self.tab_main, width=20)
        # self.file.insert(END, 'DecisionValidaciones')
        self.file.focus()
        self.file.grid(column=1, row=0, sticky=W)

        lbl = Label(self.tab_main, text="Tipo:")
        lbl.grid(column=0, row=1, sticky=W)
        self.extension = Combobox(self.tab_main, state="readonly", values=("Java", "JavaScript", "JSP"))
        self.extension.grid(column=1, row=1, sticky=W)
        self.extension.current(0)

        self.file_found = Label(self.tab_main, font='Helvetica 8 bold')
        self.file_found.grid(column=1, row=2)

        btn = Button(self.tab_main, text="Ver Calidad", command=self.show_qa_click)
        btn.grid(column=0, row=2, sticky=W)

        self.window.bind('<Return>', self.show_qa_click)

    # ------------------------------------------------------------------------------------------------
    # TAB 2
    # ------------------------------------------------------------------------------------------------

    def show_qa(self, data: dict = None):

        if None is not data:
            tab_qa_details = ttk.Frame(self.tab_control)
            self.tab_control.add(tab_qa_details, text=str(self.file.get()))
            self.__tab_qa_details_file_path(tab_qa_details, data)
            self.__tab_qa_details_headers(tab_qa_details)
            self.__tab_qa_details_data(tab_qa_details, data)
            self.tab_control.select(len(self.tab_control.tabs()) - 1)

            last_row = self.init_row_infractions + len(data['qa_infractions']) + 1
            btn = Button(tab_qa_details, text="Cerrar", command=self.delete_tab)
            btn.grid(column=0, row=last_row, sticky=W)

            self.window.geometry("")

    @staticmethod
    def __tab_qa_details_file_path(tab_qa_details: ttk.Frame, data: dict):
        lbl2 = Label(tab_qa_details, font='Helvetica 8 bold', text='Archivo:')
        lbl2.grid(column=0, row=0, sticky=W)
        file_path = Label(tab_qa_details, text=data['file_path'])
        file_path.grid(column=0, row=1, sticky=EW)

    def __tab_qa_details_headers(self, tab_qa_details: ttk.Frame):

        lbl = Label(tab_qa_details, font='Helvetica 8 bold', text='Regla', background='#ffffff')
        lbl.grid(column=0, row=self.init_row_infractions, sticky=EW)
        lbl = Label(tab_qa_details, text='|', background='#ffffff')
        lbl.grid(column=1, row=self.init_row_infractions, sticky=EW)

        lbl = Label(tab_qa_details, font='Helvetica 8 bold', text='Descripción', background='#ffffff')
        lbl.grid(column=2, row=self.init_row_infractions, sticky=EW)
        lbl = Label(tab_qa_details, text='|', background='#ffffff')
        lbl.grid(column=3, row=self.init_row_infractions, sticky=EW)

        lbl = Label(tab_qa_details, font='Helvetica 8 bold', text='Código Fuente', background='#ffffff')
        lbl.grid(column=4, row=self.init_row_infractions, sticky=EW)
        lbl = Label(tab_qa_details, text='|', background='#ffffff')
        lbl.grid(column=5, row=self.init_row_infractions, sticky=EW)

        lbl = Label(tab_qa_details, font='Helvetica 8 bold', text='Línea', background='#ffffff')
        lbl.grid(column=6, row=self.init_row_infractions, sticky=EW)
        lbl = Label(tab_qa_details, text='|', background='#ffffff')
        lbl.grid(column=7, row=self.init_row_infractions, sticky=EW)

        lbl = Label(tab_qa_details, font='Helvetica 8 bold', text='Prioridad', background='#ffffff')
        lbl.grid(column=8, row=self.init_row_infractions, sticky=EW)

    def __tab_qa_details_data(self, tab_qa_details: ttk.Frame, data: dict):
        row = self.init_row_infractions + 1
        for quality in data['qa_infractions']:
            lbl2 = Label(tab_qa_details, text=quality["c_regla"],
                         background="#F1FAFF")
            lbl2.grid(column=0, row=row, sticky=EW)
            lbl2 = Label(tab_qa_details, text='|', background='#F1FAFF')
            lbl2.grid(column=1, row=row)

            lbl2 = Label(tab_qa_details, text=quality["descripcion"],
                         background="#F1FAFF")
            lbl2.grid(column=2, row=row, sticky=EW)
            lbl2 = Label(tab_qa_details, text='|', background='#F1FAFF')
            lbl2.grid(column=3, row=row)

            lbl2 = Label(tab_qa_details, text=quality["c_fuente"],
                         background="#F1FAFF")
            lbl2.grid(column=4, row=row, sticky=EW)
            lbl2 = Label(tab_qa_details, text='|', background='#F1FAFF')
            lbl2.grid(column=5, row=row)

            lbl2 = Label(tab_qa_details, text=quality["n_linea"],
                         background="#F1FAFF")
            lbl2.grid(column=6, row=row, sticky=EW)
            lbl2 = Label(tab_qa_details, text='|', background='#F1FAFF')
            lbl2.grid(column=7, row=row)

            lbl2 = Label(tab_qa_details, text=quality["prioridad"],
                         background=APP_VIOLATION_COLOR_CODE[quality["prioridad"]])
            lbl2.grid(column=8, row=row, sticky=EW)

            row += 1

    # ------------------------------------------------------------------------------------------------
    # UI FUNCTIONS
    # ------------------------------------------------------------------------------------------------

    def show_qa_click(self, event=None):
        file = str(self.file.get())
        extension = str(self.extension.get())
        data = self.calidad.get_data(file, extension)

        # Archivo calidad KO
        if data["file_path"] and data["qa_infractions"]:
            self.show_qa(data)
            self.file_found.config(text="")

        # Archivo calidad OK
        elif data["file_found"]:
            self.file_found.config(text="Archivo en CALIDAD OK", foreground="green")

        # Archivo No encontrado
        else:
            self.file_found.config(text="Archivo no encontrado", foreground="red")

    def delete_tab(self):
        self.tab_control.forget(self.tab_control.select())
