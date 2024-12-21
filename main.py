import tkinter
import customtkinter
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from QRDetecting import realtime_scanning, scanning

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Hackathon2024 - СyberMuziki")
        self.geometry(f"{400}x{400}")
        self.resizable(False, False)

        # configure grid layout
        self.grid_columnconfigure(1, weight=1)

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Введить параметр для поиска: ")
        self.entry.grid(row=0, column=1, padx=(20, 20), pady=(20, 10), sticky="nsew")

        self.select_file_button = customtkinter.CTkButton(self, text="Выбрать видео", command=self.select_video)
        self.select_file_button.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=2, column=1, padx=(20, 20), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Настройка:")
        self.label_radio_group.grid(row=0, column=0,  padx=20, pady=0,sticky="w")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, text="Режим реального времени",
                                                           value=0)
        self.radio_button_1.grid(row=1, column=0, pady=5, padx=20, sticky="w")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, text="Режим видео",
                                                           value=1)
        self.radio_button_2.grid(row=2, column=0, pady=5, padx=20, sticky="w")

        self.switch_1 = customtkinter.CTkSwitch(master=self.radiobutton_frame, text="Предобработка видео")
        self.switch_1.grid(row=3, column=0, pady=5, padx=20, sticky="w")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"), text = "СТАРТ!!!", command=self.on_button_click)
        self.main_button_1.grid(row=3, column=1, columnspan=2, padx=(20, 20), pady=(10, 0), sticky="nsew")

        # create label to show selected file
        self.selected_file_label = customtkinter.CTkLabel(self, text="QR-код БЭК основной найден: \n Все найденные QR-коды: \n 1 \n 2")
        self.selected_file_label.grid(row=4, column=1, padx=20, pady=10, sticky="w")


    def select_video(self):
        self.file_path = askopenfilename(title="Выберите видео файл", filetypes=[("Видео файлы", "*.mp4;*.avi;*.mov;*.mkv;*.flv")])
        if self.file_path:
            print(f"Выбранный видео файл: {self.file_path}")
        else:
            print("Видео файл не выбран")


    def on_button_click(self):
        # Проверка, был ли выбран файл
        if not hasattr(self, 'file_path') or not self.file_path:
            print("Ошибка: Видео файл не выбран!")
            return  # Прерываем выполнение, если файл не выбран

        # Получение значений параметров
        radio_value = self.radio_var.get()
        switch_value = self.switch_1.get()
        entry_value = self.entry.get()

        print(f"Параметр для поиска: {entry_value}")

        if switch_value:
            print("Предобработка видео: Включена")
        else:
            print("Предобработка видео: Отключена")
        
        if radio_value == 0:
            print("Выбранный режим: Режим реального времени")
            realtime_scanning(self.file_path, entry_value)
        else:
            print("Выбранный режим: Режим видео")
            scanning(self.file_path, entry_value, 'test_video.mp4')


if __name__ == "__main__":
    app = App()
    app.mainloop()