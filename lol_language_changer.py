#!/usr/bin/env python3
import subprocess
import tkinter as tk
from tkinter import ttk
import psutil
import webbrowser
import os
import platform
import argparse

PROCESS_LIST = [
    "LeagueCrashHandler.exe",
    "LeagueClientUxRender.exe",
    "LeagueClientUx.exe",
    "LeagueClient.exe",
]

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-w", "--wineprefix", help="Path to your WINEPREFIX", default=None)
parser.add_argument('-mw', '--mac-wine', action='store_true', help="Use WINE on macOS")
args = parser.parse_args()

WINEPREFIX = args.wineprefix
if WINEPREFIX:
    WINEPREFIX = os.path.abspath(WINEPREFIX)  # Normalize the path to an absolute path


def find_lol_path_wine() -> object:
    """
    Return either Riot Client or League of Legends in WINEPREFIX

    Example:
    /path/to/your/wineprefix/drive_c/Riot Games/League of Legends/
    /path/to/your/wineprefix/drive_c/Riot Games/Riot Client/

    """

    for _root, dirs, files in os.walk(WINEPREFIX):
        for file in files:
            if file == "LeagueClient.exe":
                return os.path.join(_root, file)

    return None


def start_lol_with_wine(wineprefix):
    path = find_lol_path_wine()
    env = os.environ.copy()

    if path is None:
        label_status.config(text="Please open LOL Client first ^3^")
        return

    print("Found LOL at", path)
    label_status.config(text="Doing the magic >:3")

    quit_lol_client()

    argument = "--locale=" + get_selected_language()

    if wineprefix:
        wine_command = f"WINEPREFIX={wineprefix} wine"
    else:
        wine_command = "wine"

    command = f'{wine_command} "{path}" {argument}'

    try:
        _result = subprocess.run(
            command, shell=True, timeout=120,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, encoding='utf-8'
        )
        label_status.config(text="LOL will start shortly >3<")
        print(_result.stdout)
        return True
    except subprocess.TimeoutExpired as e:
        print(f"Timeout error: {e}")
    except subprocess.CalledProcessError as e:
        label_status.config(text=f"Error: {e}")
    except Exception as e:
        label_status.config(text=f"Unexpected error: {e}")

    return False


def start_lol_linux():
    """
    The command for Linux is
    WINEPREFIX=/path/to/your/wineprefix wine "/path/to/your/wineprefix/drive_c/Riot Games/League of Legends/LeagueClient.exe" --locale=ko_KR
    """

    return start_lol_with_wine(args.wineprefix)


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


def find_lol_path_mac():
    """
    Return League of Legends.app path

    Example:
    /Applications/League of Legends.app/
    """

    search_paths = [
        "/Applications/League of Legends.app",
        os.path.expanduser("~/Applications/League of Legends.app"),
    ]

    for search_path in search_paths:
        if os.path.exists(search_path):
            return search_path

    return None


def start_lol_mac_native():
    """
    The command for macOS native client is
    open "/Applications/League of Legends.app" --args "--locale=ko_KR"
    """

    path = find_lol_path_mac()

    if path is None:
        label_status.config(text="Please open LOL Client first ^3^")
        return

    print("Found LOL at", path)
    label_status.config(text="Doing the magic >:3")

    quit_lol_client()

    argument = "--locale=" + get_selected_language()
    _result = None

    # Start LOL with new language
    try:
        _result = subprocess.run(["open", path, "--args", argument], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 encoding='utf-8')
        label_status.config(text="LOL will start shortly >3<")
        print(_result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        label_status.config(text=f"Error: {e}")
        return False
    except Exception as e:
        label_status.config(text=f"Unexpected error: {e}")
        return False


def start_lol_mac_wine():
    """
    The command for macOS with WINE is
    WINEPREFIX=/path/to/your/wineprefix wine "/path/to/your/wineprefix/drive_c/Riot Games/League of Legends/LeagueClient.exe" --locale=ko_KR
    """

    if WINEPREFIX is None:
        label_status.config(text="Please specify the WINEPREFIX path using '-w' or '--wineprefix'")
        return

    return start_lol_with_wine(args.wineprefix)


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
    _result = None

    # Start LOL with new language
    try:
        _result = subprocess.run([path, argument], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        label_status.config(text="LOL will start shortly >3<")
        print(_result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        label_status.config(text=f"Error: {e}")
        return False
    except Exception as e:
        label_status.config(text=f"Unexpected error: {e}")
        return False


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
    os_type = platform.system()
    success = None

    if os_type == "Windows":
        success = start_lol_windows()
    elif os_type == "Linux":
        if WINEPREFIX is not None:
            success = start_lol_linux()
    elif os_type == "macOS":
        if WINEPREFIX is not None:
            success = start_lol_mac_wine()
        else:
            success = start_lol_mac_native()
    else:
        label_status.config(text="Unsupported OS")

    if success:
        label_status.config(text="Language changed successfully!")
        root.after(2000, root.destroy)
        exit(0)
    else:
        label_status.config(text="Error changing language.")
        root.after(30000, root.destroy)
        exit(1)


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

label_info = tk.Label(root,
                      text="""Instruction:\n1. Open League Client.\n2. Select or enter a language code. Eg:
                      vi_VN\n*Note: Changing language will restart your Client""")
label_info["justify"] = "left"
label_info.place(x=10, y=70, width=302, height=75)

label_info2 = tk.Label(root, text="""@TheDuckNiceRight""", fg="darkviolet", cursor="hand2")
label_info2.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/ducviet321/LOL-Language-Changer/"))
label_info2.place(x=10, y=140, width=302, height=30)

if __name__ == "__main__":
    root.mainloop()
