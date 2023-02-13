import subprocess
import tkinter as tk
from tkinter import ttk
import psutil
import webbrowser

PROCESS_LIST = [
    "LeagueCrashHandler.exe",
    "LeagueClientUxRender.exe",
    "LeagueClientUx.exe",
    "LeagueClient.exe",
]

# language = "en_US"


def find_lol_path_windows():
    """
    Return either Riot Client or League of Legends

    Example:
    E:\Riot Games\League of Legends\
    E:\Riot Games\Riot Client\

    """

    for process in psutil.process_iter():
        try:
            if process.name() in PROCESS_LIST:
                return process.exe()
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass

    return None


def quit_lol_client():
    # Check if the process is running
    for process in psutil.process_iter():
        if process.name() in PROCESS_LIST:
            # Terminate the process
            process.kill()
            print(f"{process.name()} has been terminated.")


def start_lol_mac():
    """
    The command for mac is
    open /Applications/League\ of\ Legends.app/Contents/LoL/LeagueClient.app –args –locale= XXXXX
    """
    # TODO


def start_lol_windows():
    """
    The command for Windows is
    "E:\Riot Games\League of Legends\LeagueClient.exe" --locale=ko_KR
    """

    path = find_lol_path_windows()

    if path is None:
        label_status.config(text="Please open LOL Client first ^3^")
        return

    print("Found LOL at", path)
    label_status.config(text="Doing the magic >:3")

    quit_lol_client()

    # Change target to
    # "E:\Riot Games\League of Legends\LeagueClient.exe" --locale=ko_KR
    path = path.split('\\')
    path[-1] = "LeagueClient.exe"
    path = '\\'.join(path)
    argument = "--locale=" + get_selected_language()

    # Start LOL with new language
    try:
        result = subprocess.run([path, argument], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    except Exception:
        label_status.config(text="Oops, something went wrong")

    # Printing the output
    print(result.stdout)

    label_status.config(text="LOL will start shortly >3<")



# Define the options
LANGUAGE_OPTIONS = {
    "English": "en_US",
    "Vietnamese": "vi_VN",
    "Japanese": "ja_JP",
    "Korean": "ko_KR",
    "Chinese": "zh_CN",
    "Taiwanese": "zh_TW",
    "Spanish (Spain)": "es_ES",
    "Spanish (Latin America)": "es_MX",
    "French": "fr_FR",
    "German": "de_DE",
    "Italian": "it_IT",
    "Polish": "pl_PL",
    "Romanian": "ro_RO",
    "Greek": "el_GR",
    "Portuguese": "pt_BR",
    "Hungarian": "hu_HU",
    "Russian": "ru_RU",
    "Turkish": "tr_TR",
}


def get_selected_language():
    return LANGUAGE_OPTIONS.get(combobox_language.get(), combobox_language.get())


def on_change_language(*arg):
    print("Selected language:", get_selected_language())


def on_click_change():
    start_lol_windows()


# Create the window
root = tk.Tk()
root.title("LOL Language Changer 0.1")
width = 310
height = 170
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(False, False)

combobox_language = ttk.Combobox(root, values=list(LANGUAGE_OPTIONS.keys()))
combobox_language.pack(side=tk.LEFT)
combobox_language.current(0)
combobox_language.bind("<<ComboboxSelected>>", on_change_language)
combobox_language.place(x=15, y=10, width=168, height=30)

button_change = tk.Button(root, text="Change", command=on_click_change)
button_change.place(x=195, y=10, width=90, height=30)

label_status = tk.Label(root, text="UwU", fg="red")
label_status.place(x=10, y=45, width=302, height=35)

label_info = tk.Label(root, text="""Instruction:\n1. Open League Client.\n2. Select or enter a language code. Eg: vi_VN\n*Note: Changing language will restart your Client""")
label_info["justify"] = "left"
label_info.place(x=10, y=70, width=302, height=75)

label_info2 = tk.Label(root, text="""@TheDuckNiceRight""", fg="darkviolet", cursor="hand2")
label_info2.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/ducviet321/LOL-Language-Changer/"))
label_info2.place(x=10, y=140, width=302, height=30)

if __name__ == "__main__":
    root.mainloop()
