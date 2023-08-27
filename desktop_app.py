import tkinter as tk
import pystray
from googletrans import LANGUAGES
from tkinter import ttk
import clipboard
import threading
from googletrans import Translator
import json
from PIL import Image
from pystray import MenuItem as item


class GUIThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.original_text = None
        self.translated_text = None
        self.translator = Translator()
        self.languages = list(LANGUAGES.values())

    def run(self):
        self.create_gui()


    def save_settings(self, src_language, dest_language):
        to_save = {
            "src_language": src_language,
            "dest_language": dest_language
        }

        with open("Translaterra_settings.json", "w") as file:
            json.dump(to_save, file)

    def translate_clipboard(self, clipboard_text, src_language, dest_language):
        if src_language == "Auto Detect":
            detected_lang = self.translator.detect(clipboard_text).lang
            result = self.translator.translate(clipboard_text, src=detected_lang, dest=dest_language)
        else:
            result = self.translator.translate(clipboard_text, src=src_language, dest=dest_language)
        return result.text

    def translate_text(self):
        original_text = self.original_text.get("1.0", tk.END).strip()
        if len(original_text) > 0:
            self.translated_text.config(state=tk.NORMAL)
            self.translated_text.delete("1.0", tk.END)

            selected_original_language = self.original_lang_combobox.get()
            selected_translate_language = self.translated_lang_combobox.get()
            self.save_settings(selected_original_language, selected_translate_language)
            translation = self.translate_clipboard(original_text, selected_original_language, selected_translate_language)

            if translation:
                self.translated_text.insert(tk.END, translation)
            self.translated_text.config(state=tk.DISABLED)

    def activate_and_translate(self):
        clipboard_text = clipboard.paste()
        self.original_text.delete("1.0", tk.END)
        self.original_text.insert(tk.END, clipboard_text)

        self.translated_text.config(state=tk.NORMAL)
        self.translated_text.delete("1.0", tk.END)

        selected_original_language = self.original_lang_combobox.get()
        selected_translate_language = self.translated_lang_combobox.get()
        self.save_settings(selected_original_language, selected_translate_language)
        translation = self.translate_clipboard(clipboard_text, selected_original_language, selected_translate_language)
        if translation:
            self.translated_text.insert(tk.END, translation)
        self.translated_text.config(state=tk.DISABLED)
        self.create_gui.show_window()

    def translate_clipboard_text(self):
        self.original_text.delete("1.0", tk.END)
        self.translated_text.delete("1.0", tk.END)

        clipboard_text = clipboard.paste()
        self.original_text.insert(tk.END, clipboard_text)

        self.activate_and_translate()

    def create_gui(self):
        root = tk.Tk()
        root.title("Text Translator App")
        root.configure(bg="black")

        root.resizable(False, False)

        main_frame = tk.Frame(root, bg="black")
        main_frame.pack(padx=10, pady=10)

        original_frame = tk.Frame(main_frame, width=300, height=300, bg="black")
        original_frame.pack(side=tk.LEFT)

        translated_frame = tk.Frame(main_frame, width=300, height=300, bg="black")
        translated_frame.pack(side=tk.RIGHT)

        label_font = ("Helvetica", 14, "bold")
        label_bg = "black"
        label_fg = "white"

        original_label = tk.Label(original_frame, text="Original text", bg=label_bg, fg=label_fg, font=label_font)
        original_label.pack()

        translated_label = tk.Label(translated_frame, text="Translated text", bg=label_bg, fg=label_fg, font=label_font)
        translated_label.pack()

        text_font = ("Helvetica", 12)
        text_bg = "black"
        text_fg = "white"

        translate_button = tk.Button(root, text="Translate", command=self.translate_text,
                                     bg="#007ACC", fg="white", font=("Helvetica", 16, "bold"))
        translate_button.pack(pady=10)

        self.original_text = tk.Text(original_frame, wrap=tk.WORD, width=40, height=10,
                                     bg=text_bg, fg=text_fg, font=text_font, insertbackground=text_fg)
        self.original_text.pack()

        with open("Translaterra_settings.json", "r") as file:
            settings = json.load(file)

        self.original_lang_combobox = ttk.Combobox(original_frame, values=["Auto Detect"] + self.languages, state="readonly")
        self.original_lang_combobox.set(settings["src_language"])
        self.original_lang_combobox.pack()

        self.translated_text = tk.Text(translated_frame, wrap=tk.NONE, width=40, height=10, state=tk.DISABLED,
                                       bg=text_bg, fg=text_fg, font=text_font)
        self.translated_text.pack()

        self.translated_lang_combobox = ttk.Combobox(translated_frame, values=self.languages, state="readonly")
        self.translated_lang_combobox.set(settings["dest_language"])
        self.translated_lang_combobox.pack()

        def quit_window(icon, item):
            icon.stop()
            root.destroy()

        def show_window(icon, item):
            icon.stop()
            root.after(0, root.deiconify())

        def hide_window():
            root.withdraw()
            image = Image.open("icon.png")
            menu = ( item('Show', show_window), item('Quit', quit_window))
            icon = pystray.Icon("name", image, "My System Tray Icon", menu)
            icon.run()

        root.protocol('WM_DELETE_WINDOW', hide_window)

        root.mainloop()


if __name__ == "__main__":
    gui_thread = GUIThread()
    gui_thread.start()