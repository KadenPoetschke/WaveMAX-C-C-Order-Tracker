import customtkinter as ctk
import logging

# Configure logging
logging.basicConfig(filename='data\order.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class LogWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Order Log")
        self.geometry("600x500")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.after(200, lambda: self.attributes("-topmost", False))

        # Create a title label
        title_label = ctk.CTkLabel(self, text="Order Log", font=("Arial", 16))
        title_label.pack(pady=10)

        # Create a scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=580, height=420)
        self.scrollable_frame.pack(pady=10, padx=10)

        # Read and display the log content
        self.display_log_content()

    def show(self):
        self.focus()

    def read_log_file(self):
        with open('data\order.log', 'r') as file:
            return file.readlines()

    def display_log_content(self):
        log_lines = self.read_log_file()
        for line in log_lines:
            label = ctk.CTkLabel(self.scrollable_frame, text=line.strip())
            label.pack(anchor='w')