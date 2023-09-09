import keyboard
from desktop_app import GUIThread

if __name__ == "__main__":
    gui_thread = GUIThread()
    gui_thread.start()

    keyboard.add_hotkey('ctrl+shift+f', gui_thread.activate_and_translate)

    try:
        print("Program działa w tle...")
        keyboard.wait('esc')  # Czekanie na naciśnięcie klawisza 'esc' w celu zakończenia programu
    except KeyboardInterrupt:
        print("Zakończono program.")
        keyboard.unhook_all()  # Usunięcie aktywnego skrótu