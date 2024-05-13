import yaml
import time
import subprocess
from watchdog.observers import Observer # type: ignore
from watchdog.events import FileSystemEventHandler  # type: ignore

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
            if 'zh_CN' not in data['locale_data']['available_locales']:
                data['locale_data']['available_locales'].append(self.locale_code)
            # Update patcher locales
            data['locale_data']['default_locale'] = self.locale_code
            data['settings']['locale'] = self.locale_code
            with open(self.filename, 'w') as f:
                yaml.dump(data, f)
        except Exception as e:
            print(f"Error updating YAML file: {e}")
        #try:
            # Run the other executable with the specified locale code argument
            #subprocess.Popen([self.client_exe_path, "--locale", self.locale_code])
        #except Exception as e:
            #print(f"Error updating client locale code: {e}")

class YamlWatcher:
    def __init__(self, filename, locale_code, client_exe_path):
        self.filename = filename
        self.locale_code = locale_code
        self.client_path = client_exe_path
        self.observer = Observer()

    def start_watching(self):
        event_handler = YamlHandler(self.filename, self.locale_code,self.client_path)
        observer = Observer()
        observer.schedule(event_handler, path='.', recursive=False)
        observer.start()
        
        try:
            while True:
                current_timestamp = str(time.localtime().tm_year) + "." + str(time.localtime().tm_mon) +"."+str(time.localtime().tm_mday) + " " + str(time.localtime().tm_hour) + ":" + str(time.localtime().tm_min) + ":" + str(time.localtime().tm_sec)
                print("[",current_timestamp,"] YAML file modified. ","At:",self.filename, "Updating locale to:", self.locale_code)
                event_handler.update_locale()  # Update locale
                time.sleep(5)  # Wait for 5 seconds
        except KeyboardInterrupt:
            observer.stop()
        observer.join()