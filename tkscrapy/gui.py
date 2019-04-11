# coding:utf-8
import _tkinter
import os
import subprocess
import tkinter
from threading import Thread

from tkinter import filedialog
from tkinter import messagebox
from shutil import copyfile
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from time import sleep


class App(tkinter.Tk):

    def __init__(self):
        super(App, self).__init__()

        # init windows
        self.title("Scrap to web")
        self.geometry("450x900")
        self.minsize(200, 400)
        self.resizable(False, True)
        self.config(background="#f2f2f2")

        # logo
        if "nt" == os.name:
            self.wm_iconbitmap(bitmap="icon.ico")
        else:
            self.wm_iconbitmap(bitmap="@icon.xbm")

        # //////////////////////////////////// Format frame
        self.formatframe = tkinter.LabelFrame(self, text="Format d'exportation", height=150, width=400)
        self.formatframe.pack(pady=15, ipadx=5, ipady=10)
        self.export_var = tkinter.StringVar(value="json")
        self.export_json = tkinter.Radiobutton(self.formatframe, text="JSON", value="json", variable=self.export_var)
        self.export_json.pack(side="left", anchor=tkinter.N)
        self.export_csv = tkinter.Radiobutton(self.formatframe, text="CSV", value="csv", variable=self.export_var)
        self.export_csv.pack(side="left", anchor=tkinter.N)
        self.export_xml = tkinter.Radiobutton(self.formatframe, text="XML", value="xml", variable=self.export_var)
        self.export_xml.pack(side="left", anchor=tkinter.N)

        # //////////////////////////////////// Top frame
        self.topframe = tkinter.LabelFrame(self, text="Informations", height=150)
        self.topframe.pack(pady=15, ipadx=5, ipady=10)
        # StringVars
        self.url_var = tkinter.StringVar()
        self.pagination_exemple_var = tkinter.StringVar()
        self.pagination_var = tkinter.BooleanVar(value=False)
        self.parent_selector_var = tkinter.StringVar(self.topframe)
        # widgets
        self.url_label = tkinter.Label(self.topframe, text="Url du site").pack()
        self.url_field = tkinter.Entry(self.topframe, width=50, textvariable=self.url_var)
        self.url_field.pack()
        self.parent_selector_label = tkinter.Label(self.topframe, text="Le selecteur parent (css)").pack()
        self.parent_selector = tkinter.Entry(self.topframe, width="50", textvariable=self.parent_selector_var)
        self.parent_selector.pack()
        self.selector_label = tkinter.Label(self.topframe,
                                            text="Ajouter nom_colonne | selecteurs  \n "
                                                 "ex: titre | a.product-name::text => Affiche contenu de la balise \n "
                                                 "ex: description | a.product-name => Affiche la balise HTML",
                                            font="arial 10").pack()
        self.selector_entry = tkinter.Text(self.topframe, width="50", height="12")
        self.selector_entry.pack()
        self.pagination_checkbox = tkinter.Checkbutton(self.topframe, command=self._display_pagination_entry,
                                                       onvalue=True, offvalue=False, variable=self.pagination_var)
        self.pagination_checkbox.pack(side="left")
        self.pagination = None
        self.pagination_label = tkinter.Label(self.topframe, text="Selecteur de la pagination").pack(side="left")

        # //////////////////////////////////// Output frame
        self.output = tkinter.LabelFrame(self, text="Résultat", height=200)
        self.output.pack(ipadx=5, ipady=10)

        # widgets
        self.progress = tkinter.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.output, variable=self.progress, length=250)
        self.progress_bar.pack(pady=10)
        # self.progress_bar.start(10)
        self.response_entry = ScrolledText(self.output, width="50", height="12", undo=True)
        self.response_entry.pack(expand=tkinter.TRUE, fill="both")
        # btn
        self.btn_search = tkinter.Button(self.output, text="search", width="25",
                                         command=self.call_spider_process).pack(side="top")
        self.btn_close = tkinter.Button(self.output, text="Fermer", width="25", command=self.quit).pack(side="bottom")
        self.btn_save_actived = True

    def call_spider_process(self):
        """
        Call scrapy spider process command
        :return:
        """
        self.call_subprocess_command()

    @staticmethod
    def _check_if_callable_or_transform_to_string(attr):
        """
        Check if callable or transform to string for argument command
        :param attr:
        :return:
        """
        try:
            if callable(attr.get):
                attr = attr.get()
        except (AttributeError, TypeError):
            attr = ""
        return attr

    def call_subprocess_command(self):
        """
        Call the subprocess command fo call scrapy
        :return:
        """
        # Transform Entry to string or send Entry.get()
        pagination = App._check_if_callable_or_transform_to_string(self.pagination)

        # remove all tkspider with extension
        App._clean_files("tkspider")

        if self.url_field.get() and self.parent_selector.get():
            command = "scrapy", "crawl", "tkspider", "-o", f"tkspider.{self.export_var.get()}", "-a", "url=" + self.url_field.get(), "-a", "parent_selector=" + self.parent_selector.get(), "-a", "selectors=" + self.selector_entry.get(
                1.0, tkinter.END), "-a", "pagination=" + pagination

            subprocess.run(command)  # call subprocess command

            self.display_result()  # Display result in Text
            self.create_save_btn()  # call create_save_btn method for saving file
        else:
            tkinter.messagebox.showerror("Erreur",
                                         "Vous devez renseigner \n le champ url ainsi que \n champ sélecteur parent")

    def display_result(self):
        """
        Check the result and display it in Text entry
        :return:
        """
        file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"tkspider.{self.export_var.get()}")
        # check if file existe and if not empty
        if os.path.isfile(file) and os.stat(file).st_size != 0:

            try:
                self.response_entry.delete(1.0, "end")  # reset response output
                self.response_entry.update()
            except _tkinter.TclError:
                raise

            with open(file, "r") as f:
                for line in f:
                    self.response_entry.insert(tkinter.END, line)  # Get line of file
                    self.progress_bar.step(100 / App.count_line_file(file))  # Add progress bar
                    Thread(target=sleep(0.01)).start()
                    self.progress_bar.update()
                self.progress.set(99.8)  # Set progress bar completed

    @staticmethod
    def count_line_file(file):
        """
        Count line of file
        :return: float counter
        """
        with open(file, "r") as f:
            counter = 0
            for line in f:
                counter += 1
            return counter

    def create_save_btn(self):
        """
        Create Save btn
        :return:
        """
        if self.btn_save_actived:
            btn_save = tkinter.Button(self.output, text="Sauvegarder", width="25", bg="#8ce261",
                                      command=self._save_file)
            btn_save.pack(side="top")
        self.btn_save_actived = False

    def _save_file(self):
        """
        Save file and copy the content of tkspider files
        :return:
        """
        file = filedialog.asksaveasfile(mode="w", initialdir="/home/cajoline/Bureau",
                                        defaultextension=f".{self.export_var.get()}",
                                        filetypes=(
                                            ("Json file", "*.json"), ("Excel files", "*.csv"), ("Xml file", "*.xml"),
                                            ("All files", "*.*")))

        # Copy spider file content in user choices file
        spider_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"tkspider.{self.export_var.get()}")
        copyfile(spider_file, file.name)
        os.remove(spider_file)  # remove spider file

    @classmethod
    def _clean_files(cls, filename):
        """
        Clean all file tkspider with extension
        :param filename: filename without extension
        :return:
        """
        extensions = ("json", "csv", "xml")
        dir_path = os.path.dirname(os.path.abspath(__file__))

        for ext in extensions:
            filename_ext = os.path.join(dir_path, f"{filename}.{ext}")

            if os.path.isfile(filename_ext):
                os.remove(filename_ext)

    def _display_pagination_entry(self):
        """
        Display conditional field pagination
        :return:
        """
        if self.pagination_var.get():
            self.pagination = tkinter.Entry(self.topframe, width=25, textvariable=self.pagination_exemple_var)
            self.pagination.pack(side="left")
        else:
            self.pagination.pack_forget()


if __name__ == "__main__":
    app = App()
    app.iconbitmap()
    app.mainloop()
