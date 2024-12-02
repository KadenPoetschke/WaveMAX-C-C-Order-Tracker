import requests
import shutil
import zipfile
import os
import sys
import customtkinter as ctk

# https://github.com/KadenPoetschke/WaveMAX-C-C-Order-Tracker.git

GITHUB_REPO = "KadenPoetschke/WaveMAX-C-C-Order-Tracker"  # Replace with your GitHub repo
LATEST_RELEASE_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
DOWNLOAD_DIR = "update"

class VersionChecker(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Version Checker")
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
    print(f"Response: {response}")  # Add this line to print the response object
    print(f"Status code: {response.status_code}")  # Add this line to print the status code 
    if response.status_code == 200:
        latest_release = response.json()
        latest_version = latest_release["tag_name"]
        download_url = latest_release["zipball_url"]
        current_version = "v1.0.2"  # Replace with your current version logic

        print(f"Latest version: {latest_version}")
        print(f"Current version: {current_version}")

        if latest_version != current_version:
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
    if response.status_code == 200:
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        zip_path = os.path.join(DOWNLOAD_DIR, "update.zip")
        with open(zip_path, "wb") as file:
            shutil.copyfileobj(response.raw, file)
        install_update(zip_path)
    else:
        text_response = "Failed to download the update."
        print(text_response)
        VCWindow.update_window(text_response)

def install_update(zip_path):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(DOWNLOAD_DIR)
    # Replace current files with the new ones
    for root, dirs, files in os.walk(DOWNLOAD_DIR):
        for file in files:
            if file != "update.zip":
                shutil.move(os.path.join(root, file), os.path.join(os.getcwd(), file))
    restart_application()

def restart_application():
    print("Restarting application...")
    python = sys.executable
    os.execl(python, python, *sys.argv)