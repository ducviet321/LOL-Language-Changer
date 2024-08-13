#!/usr/bin/env python3
import subprocess
import tkinter as tk
from tkinter import ttk
import psutil
import webbrowser
import os
import platform
import argparse
from os.path import dirname
import threading
import time
import glob
import string
from ctypes import windll
import logging
from tkinter import scrolledtext
from watchdog.observers import Observer # type: ignore
from watchdog.events import FileSystemEventHandler  # type: ignore
import yaml
import time
#collections
PROCESS_LIST = [
    "LeagueCrashHandler.exe",
    "LeagueClientUxRender.exe",
    "LeagueClientUx.exe",
    "LeagueClient.exe",
]
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

path = None
# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-w", "--wineprefix", help="Path to your WINEPREFIX", default=None)
parser.add_argument('-mw', '--mac-wine', action='store_true', help="Use WINE on macOS")
args = parser.parse_args()
global log_message
WINEPREFIX = args.wineprefix
if WINEPREFIX:
    WINEPREFIX = os.path.abspath(WINEPREFIX)  # Normalize the path to an absolute path

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    return drives

def get_selected_language():
    return LANGUAGE_OPTIONS.get(combobox_language.get(), combobox_language.get())

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

def find_lol_path_windows(find_yaml=False):
    """
    Return either Riot Client or League of Legends

    Example:
    E:\Riot Games\League of Legends\
    E:\Riot Games\Riot Client\

    """
    if(not find_yaml):
        for process in psutil.process_iter():
            try:
                if process.name() in PROCESS_LIST:
                    return process.exe()
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass
    else:
        path = find_lol_live_yaml_windows()
        return path  
    return None

def find_lol_live_yaml_windows():
    finded_files = []
    base_dir = "\\ProgramData\\Riot Games\\Metadata\\league_of_legends.live"
    for drive in get_drives():
        base_dir = drive +":"+"\\ProgramData\\Riot Games\\Metadata\\league_of_legends.live"
        file_pattern = base_dir + "\\league_of_legends.live.product_settings.yaml"
        matching_files = glob.glob(file_pattern, recursive=True)
        for file_path in matching_files:
            finded_files.append(file_path)
    return finded_files[0]

def start_yaml_service(path,locale_code,client_path):
    try:
        service_thread = threading.Thread(target=start_watching_in_background(path,locale_code,client_path), daemon=True)
        service_thread.start()
        return True
    except Exception as e:
        print(f"Error starting YAML service: {e}")
        return False
    
def start_watching_in_background(path,local_code,client_path):
    watcher = YamlWatcher(path, local_code,client_path)
    watcher.start_worker()

def start_lol_windows():
    """
    The command for Windows is
    "E:\Riot Games\League of Legends\LeagueClient.exe" --locale=ko_KR
    """
    isYaml = False
    path = find_lol_path_windows(True)
    isYaml = True
    if path is None:
        print("Please open LOL Client first ^3^")
        return
    
    
    if(isYaml):
        print("Found LOL live Yaml setting file at", path)
    else:
        print("Found LOL at", path)

    #quit_lol_client()

    # Change target to
    # "E:\Riot Games\League of Legends\LeagueClient.exe" --locale=ko_KR
    client_path = find_lol_path_windows()
    client_path = client_path.split('\\')
    client_path[-1] = "LeagueClient.exe"
    client_path = '\\'.join(client_path)
    #argument = "--locale=" + get_selected_language()
    _result = None

    # Start LOL with new language
    try:
        statusCode = start_yaml_service(path,get_selected_language(),client_path)
        return statusCode
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return statusCode
    except Exception as e:
        print(f"Unexpected error: {e}")
        return statusCode
    
def start_lol_with_wine(wineprefix):
    path = find_lol_path_wine()
    env = os.environ.copy()

    if path is None:
        print(text="Please open LOL Client first ^3^")
        return

    print("Found LOL at", path)
    print(text="Doing the magic >:3")

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
        print("LOL will start shortly")
        print(_result.stdout)
        return True
    except subprocess.TimeoutExpired as e:
        print(f"Timeout error: {e}")
    except subprocess.CalledProcessError as e:
        print(text=f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return False

def start_lol_linux():
    """
    The command for Linux is
    WINEPREFIX=/path/to/your/wineprefix wine "/path/to/your/wineprefix/drive_c/Riot Games/League of Legends/LeagueClient.exe" --locale=ko_KR
    """

    return start_lol_with_wine(args.wineprefix)

def start_lol_mac_native():
    """
    The command for macOS native client is
    open "/Applications/League of Legends.app" --args "--locale=ko_KR"
    """

    path = find_lol_path_mac()

    if path is None:
        print("Please open LOL Client first ^3^")
        return

    print("Found LOL at", path)

    quit_lol_client()

    argument = "--locale=" + get_selected_language()
    _result = None

    # Start LOL with new language
    try:
        _result = subprocess.run(["open", path, "--args", argument], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 encoding='utf-8')
        print(text="LOL will start shortly >3<")
        print(_result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def start_lol_mac_wine():
    """
    The command for macOS with WINE is
    WINEPREFIX=/path/to/your/wineprefix wine "/path/to/your/wineprefix/drive_c/Riot Games/League of Legends/LeagueClient.exe" --locale=ko_KR
    """

    if WINEPREFIX is None:
        print("Please specify the WINEPREFIX path using '-w' or '--wineprefix'")
        return

    return start_lol_with_wine(args.wineprefix)
    
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
    elif os_type == "Darwin":
        if WINEPREFIX is not None:
            success = start_lol_mac_wine()
        else:
            success = start_lol_mac_native()
    else:
        print("Unsupported OS")

    if success:
        print("Language changed successfully!")
    else:
        print("Error changing language.")
        
def quit_lol_client():
    # Check if the process is running
    for process in psutil.process_iter():
        if process.name() in PROCESS_LIST:
            # Terminate the process
            process.kill()
            print(f"{process.name()} has been terminated.")

class YamlHandler(FileSystemEventHandler):
    def __init__(self, filename, locale_code, client_exe_path):
        self.filename = filename
        self.locale_code = locale_code
        self.client_exe_path = client_exe_path
    def on_modified(self, event):
        if event.src_path.endswith('.yaml'):
            print("YAML file modified. Updating locale to:", self.locale_code)
            self.update_locale()

    def update_locale(self):
        try:
            with open(self.filename, 'r') as f:
                data = yaml.safe_load(f)
            
            # Update globals locale
            if self.locale_code not in data['locale_data']['available_locales']:
                data['locale_data']['available_locales'].append(self.locale_code)
            # Update patcher locales
            data['locale_data']['default_locale'] = self.locale_code
            data['settings']['locale'] = self.locale_code
            with open(self.filename, 'w') as f:
                yaml.dump(data, f)
        except Exception as e:
            print(f"Error updating YAML file: {e}")

class YamlWatcher:
    def __init__(self, filename, locale_code, client_exe_path):
        self.filename = filename
        self.locale_code = locale_code
        self.client_path = client_exe_path
        self.observer = Observer()
        self.worker_thread = None  # To keep track of the worker thread

    def worker(self):
        # Worker function that logs messages every 5 seconds
        while True:
            current_timestamp = time.strftime("%Y.%m.%d %H:%M:%S", time.localtime())
            msg = f"[{current_timestamp}] YAML file modified. At: {self.filename} Updating locale to: {self.locale_code}"
            event_handler = YamlHandler(self.filename, self.locale_code, self.client_path)
            event_handler.update_locale()  # Update locale
            time.sleep(5)  # Wait for 5 seconds
            logging.info(msg)

    def start_worker(self):
        if self.worker_thread is None or not self.worker_thread.is_alive():
            self.worker_thread = threading.Thread(target=self.worker)
            self.worker_thread.daemon = True  # Daemonize the thread
            self.worker_thread.start()

class TextHandler(logging.Handler):
    # This class allows you to log to a Tkinter Text or ScrolledText widget
    # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tk.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)

class myGUI(tk.Frame):

    # This class defines the graphical user interface 

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.build_gui()

    def build_gui(self):
        # Create the window
        self.root.title("LOL Language Changer 1.0")
        width = 510
        height = 370
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(False, False)

        global combobox_language
        combobox_language = ttk.Combobox(self.root, values=list(LANGUAGE_OPTIONS.keys()))
        combobox_language.pack(side=tk.LEFT)
        combobox_language.current(0)
        combobox_language.bind("<<ComboboxSelected>>", on_change_language)
        combobox_language.place(x=15, y=10, width=368, height=30)

        button_change = tk.Button(self.root, text="Change", command=on_click_change)
        button_change.place(x=395, y=10, width=90, height=30)
        
        # Add text widget to display logging info
        st = scrolledtext.ScrolledText(self.root,state ='disabled', wrap= tk.WORD,font="TkFixedFont")
        st.grid(column=0, row=1, sticky='w', columnspan=4)
        # Create textLogger
        text_handler = TextHandler(st)
        st.place(x=15, y=50, width=468, height=260)
        # Logging configuration
        logging.basicConfig(filename='lol_language_changer.log',
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s - %(message)s') 
        # Add the handler to logger
        logger = logging.getLogger()        
        logger.addHandler(text_handler)
        
        label_info2 = tk.Label(self.root, text="""Original created by dcviet321""", fg="darkviolet", cursor="hand2")
        label_info2.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/ducviet321/LOL-Language-Changer/"))
        label_info2.place(x=100, y=320, width=302, height=30)
        
def main():
    root = tk.Tk()
    myGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()