import tkinter as tk
import clipboard
from googletrans import Translator
import threading
from tkinter import ttk


class GUIThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.original_text = None
        self.translated_text = None
        self.translator = Translator()

    def run(self):
        self.create_gui()

    def translate_clipboard(self, clipboard_text):
        print("Clipboard text:", clipboard_text)
        detected_lang = self.translator.detect(clipboard_text).lang
        target_lang = 'en' if detected_lang == 'pl' else 'pl'
        print(f"Translating from {detected_lang} to {target_lang}")
        result = self.translator.translate(clipboard_text, dest=target_lang)
        return result.text

    def translate_text(self):
        original_text = self.original_text.get("1.0", tk.END).strip()
        self.translated_text.config(state=tk.NORMAL)
        self.translated_text.delete("1.0", tk.END)  # Clear translated text area

        translation = self.translate_clipboard(original_text)
        if translation:
            self.translated_text.insert(tk.END, translation)
        self.translated_text.config(state=tk.DISABLED)

    def activate_and_translate(self):
        clipboard_text = clipboard.paste()
        self.original_text.delete("1.0", tk.END)
        self.original_text.insert(tk.END, clipboard_text)

        self.translated_text.config(state=tk.NORMAL)
        self.translated_text.delete("1.0", tk.END)  # Clear translated text area

        translation = self.translate_clipboard(clipboard_text)
        if translation:
            self.translated_text.insert(tk.END, translation)
        self.translated_text.config(state=tk.DISABLED)

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

        # Create frames with custom background colors
        original_frame = tk.Frame(root, width=300, height=300, bg="black")
        original_frame.pack(side=tk.LEFT, padx=10, pady=10)

        translated_frame = tk.Frame(root, width=300, height=300, bg="black")
        translated_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Set the font and colors for Text widgets
        text_font = ("Helvetica", 12)
        text_bg = "black"
        text_fg = "white"

        self.original_text = tk.Text(original_frame, wrap=tk.WORD, width=40, height=10,
                                     bg=text_bg, fg=text_fg, font=text_font, insertbackground=text_fg)
        self.original_text.pack()

        self.translated_text = tk.Text(translated_frame, wrap=tk.NONE, width=40, height=10, state=tk.DISABLED,
                                       bg=text_bg, fg=text_fg, font=text_font)
        self.translated_text.pack()

        # Set label fonts and colors
        label_font = ("Helvetica", 14, "bold")
        label_bg = "black"
        label_fg = "white"

        original_label = tk.Label(original_frame, text="Original text", bg=label_bg, fg=label_fg, font=label_font)
        original_label.pack()

        translated_label = tk.Label(translated_frame, text="Translated text", bg=label_bg, fg=label_fg, font=label_font)
        translated_label.pack()

        # Improve the appearance of the Translate button
        translate_button = tk.Button(root, text="Translate", command=self.translate_text,
                                     bg="#007ACC", fg="white", font=("Helvetica", 16, "bold"))
        translate_button.pack(pady=10)

        root.mainloop()

if __name__ == "__main__":
    gui_thread = GUIThread()
    gui_thread.start()