import requests
import shutil
import zipfile
import os
import sys
import subprocess
import customtkinter as ctk

# Constants
from constants import APP_VERSION, LATEST_RELEASE_URL, DOWNLOAD_DIR

# https://github.com/KadenPoetschke/WaveMAX-C-C-Order-Tracker.git
# https://api.github.com/repos/KadenPoetschke/WaveMAX-C-C-Order-Tracker/releases/latest

class VersionChecker(ctk.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master = master
        self.title("Check for Updates")
        self.geometry("300x100")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        
        self.url = None
        self.text_response = "Checking for updates..."
        print(self.text_response)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self, text=self.text_response)
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.button = ctk.CTkButton(self, text="Update", command=lambda: download_update(self, self.url), state="disabled")
        self.button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    def update_window(self, text_response, update_available = False, url = None):
        self.text_response = text_response
        self.label.configure(text=self.text_response)
        if update_available:
            self.url = url
            self.button.configure(state="normal")



def check_for_updates(VCWindow):
    response = requests.get(LATEST_RELEASE_URL)
    print(f"Response: {response}")
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        latest_release = response.json()
        latest_version = latest_release["tag_name"]
        download_url = latest_release["assets"][0]["browser_download_url"]
        current_version = APP_VERSION

        print(f"Latest version: {latest_version}")
        print(f"Current version: {current_version}")
        print(f"Download URL: {download_url}")

        if latest_version != current_version and latest_version != "v1.0.1" and latest_version != "v1.0.0":
            text_response = f"New version available: {latest_version}"
            print(text_response)
            VCWindow.update_window(text_response, True, download_url)
        else:
            text_response = "You are using the latest version."
            print(text_response)
            VCWindow.update_window(text_response)
    else:
        text_response = "Failed to check for updates."
        print(text_response)
        VCWindow.update_window(text_response)

def download_update(VCWindow, url):
    VCWindow.button.configure(state="disabled")
    response = requests.get(url, stream=True)

    print(f"URL: {url}")
    print(f"Response: {response}")

    if response.status_code == 200:
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        zip_path = os.path.join(DOWNLOAD_DIR, "update.zip")
        with open(zip_path, "wb") as file:
            shutil.copyfileobj(response.raw, file)
        install_update(zip_path, VCWindow)
    else:
        text_response = "Failed to download the update."
        print(text_response)
        VCWindow.update_window(text_response)

def install_update(zip_path, VCWindow):
    print("Installing update...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(DOWNLOAD_DIR)
        print("Files Extracted...")

    # Create a batch file to replace the executable and restart the application
    script_file_path = os.path.join(DOWNLOAD_DIR, "update_script.py")
    new_executable_path = os.path.join(os.getcwd(), DOWNLOAD_DIR, 'WaveMAX C&C Order Tracker.exe')
    current_executable_path = sys.executable
    new_support_files = os.path.join(os.getcwd(), DOWNLOAD_DIR, '_internal')
    current_support_files = os.path.join(os.getcwd(), '_internal')

    with open(script_file_path, "w") as script_file:
        script_file.write(f"""
import os
import shutil
import time
import sys

time.sleep(5)
os.remove(r"{current_executable_path}")
shutil.rmtree(r"{current_support_files}")
shutil.copyfile(r"{new_executable_path}", r"{current_executable_path}")
shutil.copytree(r"{new_support_files}", r"{current_support_files}")
shutil.rmtree(r"{os.path.join(os.getcwd(), DOWNLOAD_DIR)}")
os.execv(r"{current_executable_path}", sys.argv)
""")
    
    # Ensure the script file is executable
    os.chmod(script_file_path, 0o755)

    # Run the Python script
    subprocess.Popen(['python', script_file_path])

    # Destroy the window and exit the application
    VCWindow.destroy()
    os._exit(0)