import customtkinter as ctk
import logging

# Configure logging
logging.basicConfig(filename='data\order.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class LogWindow:
    def __init__(self, root):
        self.log_window = ctk.CTkToplevel(root)
        self.log_window.title("Order Log")
        self.log_window.geometry("600x500")
        self.log_window.attributes("-topmost", True)
        self.log_window.resizable(False, False)

        # Create a title label
        title_label = ctk.CTkLabel(self.log_window, text="Order Log", font=("Arial", 16))
        title_label.pack(pady=10)

        # Create a scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self.log_window, width=580, height=420)
        self.scrollable_frame.pack(pady=10, padx=10)

        # Read and display the log content
        self.display_log_content()

    def read_log_file(self):
        with open('order.log', 'r') as file:
            return file.readlines()

    def display_log_content(self):
        log_lines = self.read_log_file()
        for line in log_lines:
            label = ctk.CTkLabel(self.scrollable_frame, text=line.strip())
            label.pack(anchor='w')