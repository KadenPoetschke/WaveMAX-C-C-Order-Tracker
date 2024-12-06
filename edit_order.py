import customtkinter as ctk
from order_class import Order

class EditOrder(ctk.CTkToplevel):
    def __init__(self, master, isNew=False, index=None):
        super().__init__(master)
        if isNew:
            self.title("Add New Order")
        else:
            self.title("Edit Order")
        self.geometry("300x200")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.after(200, lambda: self.attributes("-topmost", False))

        self.master = master
        self.index = index

        self.cents_label = ctk.CTkLabel(self, text="Cents Order:")
        self.cents_label.pack(pady=5)
        self.cents_entry = ctk.CTkEntry(self)
        self.cents_entry.pack(pady=5)

        self.cc_label = ctk.CTkLabel(self, text="CC Order:")
        self.cc_label.pack(pady=5)
        self.cc_entry = ctk.CTkEntry(self)
        self.cc_entry.pack(pady=5)

        if isNew:
            self.button_text = "Add Order"
            self.button_command = self.add_order
        else:
            self.button_text = "Edit Order"
            self.button_command = self.edit_order

        self.set_order_button = ctk.CTkButton(self, text=self.button_text, command=self.button_command)
        self.set_order_button.pack(pady=5)

    def show(self):
        self.focus()

    def add_order(self):
        order = Order(self.cents_entry.get(), self.cc_entry.get())
        self.master.add_order(order)
        self.cents_entry.delete(0, "end")
        self.cc_entry.delete(0, "end")

    def edit_order(self):
        self.master.edit_order(self.index)