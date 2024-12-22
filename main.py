import tkinter
import customtkinter
from CTkListbox import *
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
        self.geometry(f"{400}x{500}")
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

        self.label_slider_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Пропуск кадров:")
        self.label_slider_group.grid(row=4, column=0,  padx=20, pady=5,sticky="w")

        self.slider = customtkinter.CTkSlider(master=self.radiobutton_frame, from_=2, to=10, number_of_steps=8, command=self.update_label)
        self.slider.grid(row=5, column=0, padx=15, pady=5, sticky="w")
        self.slider.set(1)

        self.slider_value_label = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Значение: 2")
        self.slider_value_label.grid(row=5, column=1, padx=0, pady=0, sticky="w")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"), text = "СТАРТ!!!", command=self.on_button_click)
        self.main_button_1.grid(row=3, column=1, columnspan=2, padx=(20, 20), pady=5, sticky="nsew")

        # create label to show selected file
        self.selected_file_label = customtkinter.CTkLabel(self, text="QR-код: ")
        self.selected_file_label.grid(row=4, column=1, padx=20, pady=5, sticky="w")

        self.listbox = CTkListbox(master=self, command=self.show_value)
        self.listbox.grid(row=5, column=1, columnspan=2, padx=15, pady=5, sticky="nsew")    

    def select_video(self):
        self.file_path = askopenfilename(title="Выберите видео файл", filetypes=[("Видео файлы", "*.mp4;*.avi;*.mov;*.mkv;*.flv")])
        if self.file_path:
            print(f"Выбранный видео файл: {self.file_path}")
        else:
            print("Видео файл не выбран")

    def update_label(self, value):
        """Обновление текста в Label при изменении слайдера."""
        self.slider_value_label.configure(text=f"Значение: {int(float(value))}")
        print(f"Текущее значение слайдера: {int(float(value))}")
    
    def show_value(self, value):
        print(f"Выбранная опция: {value}")

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
        slider_value = int(self.slider.get())
        self.slider_value_label.configure(text=f"Значение: {slider_value}")
        print(slider_value)
        spisok = set()
        self.listbox.delete(0, 'end')
        self.selected_file_label.configure(text = "QR-код:")

        if switch_value:
            print("Предобработка видео: Включена")
            print(switch_value)
        else:
            print("Предобработка видео: Отключена")
            print(switch_value)
        
        if radio_value == 0:
            print("Выбранный режим: Режим реального времени")
            spisok = realtime_scanning(self.file_path, entry_value, slider_value, switch_value)

        else:
            print("Выбранный режим: Режим видео")
            spisok = scanning(self.file_path, entry_value, 'test_video.mp4', slider_value, switch_value)

        k =0
        for name in spisok:                
            self.listbox.insert(k, name)
            k+=1

        if entry_value in spisok:
            self.selected_file_label.configure(text = f"QR-код: \"{entry_value}\" Найден!!!")
        else:
            self.selected_file_label.configure(text = f"QR-код: \"{entry_value}\" Не найден!!!")


if __name__ == "__main__":
    app = App()
    app.mainloop()