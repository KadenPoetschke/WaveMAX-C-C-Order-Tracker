import customtkinter as ctk

class NewOrderForm:
    def __init__(self, root, add_order_callback):
        self.form_window = ctk.CTkToplevel(root)
        self.form_window.title("Add New Order")
        self.form_window.geometry("300x200")
        self.form_window.attributes("-topmost", True)
        self.form_window.resizable(False, False)

        self.cents_label = ctk.CTkLabel(self.form_window, text="Cents Order:")
        self.cents_label.pack(pady=5)
        self.cents_entry = ctk.CTkEntry(self.form_window)
        self.cents_entry.pack(pady=5)

        self.cc_label = ctk.CTkLabel(self.form_window, text="CC Order:")
        self.cc_label.pack(pady=5)
        self.cc_entry = ctk.CTkEntry(self.form_window)
        self.cc_entry.pack(pady=5)

        self.add_order_button = ctk.CTkButton(self.form_window, text="Add Order", command=lambda: add_order_callback(self.cents_entry.get(), self.cc_entry.get()))
        self.add_order_button.pack(pady=5)

    def show(self):
        self.form_window.focus()