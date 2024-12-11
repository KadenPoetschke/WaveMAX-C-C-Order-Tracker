import customtkinter as ctk
from order_class import Order

class EditOrder(ctk.CTkToplevel):
    def __init__(self, master, isNew=False, index=None):
        super().__init__(master)
        if isNew:
            self.title("Add New Order")
            self.geometry("400x100")
            grid_rows = 2
            grid_columns = 4
        else:
            self.title("Edit Order")
            self.geometry("500x700")
            self.index = index
            self.order = master.current_orders[index][2]
            grid_rows = 9
            grid_columns = 6
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.after(200, lambda: self.attributes("-topmost", False))

        for i in range(grid_columns):
            self.grid_columnconfigure(i, weight=1)
        for i in range(grid_rows):
            self.grid_rowconfigure(i, weight=1)

        self.master = master
        self.isNew = isNew
        self.widgets = []

        self.cents_label = ctk.CTkLabel(self, text="Cents Order:")
        self.cents_label.grid(row=0, column=0, pady=(10, 5), sticky="e")
        self.cents_entry = ctk.CTkTextbox(self, height=32, width=80)
        self.cents_entry.grid(row=0, column=1, pady=(10, 5), sticky="w")
        self.widgets.append(self.cents_entry)

        self.cc_label = ctk.CTkLabel(self, text="CC Order:")
        self.cc_label.grid(row=0, column=2, pady=(10, 5), sticky="e")
        self.cc_entry = ctk.CTkTextbox(self, height=32, width=80)
        self.cc_entry.grid(row=0, column=3, pady=(10, 5), sticky="w")
        self.widgets.append(self.cc_entry)

        if isNew:
            self.button_text = "Add Order"
            self.button_command = self.add_order
        else:
            self.button_text = "Edit Order"
            self.button_command = self.edit_order
            self.cents_entry.insert("0.0", self.order.cents_order.strip())
            self.cc_entry.insert("0.0", self.order.cc_order.strip())
            self.cents_entry.configure(state="disabled", fg_color="#191919")
            self.cc_entry.configure(state="disabled", fg_color="#191919")

            self.notes_label = ctk.CTkLabel(self, text="Notes:")
            self.notes_label.grid(row=1, column=0, pady=5, sticky="e")
            self.notes_entry = ctk.CTkTextbox(self)
            self.notes_entry.grid(row=2, column=1, pady=5, columnspan=6, sticky="w")
            self.widgets.append(self.notes_entry)
            self.notes_entry.insert("0.0", self.order.notes)
            self.notes_entry.configure(state="disabled", fg_color="#191919")

            self.detergent_label = ctk.CTkLabel(self, text="Detergent:")
            self.detergent_label.grid(row=3, column=0, pady=5, sticky="e", columnspan=2)
            self.detergent_entry = ctk.CTkOptionMenu(self, values=["Regular", "Tide", "Gain", "Hypoallergenic", "FOCA", "Other - See Notes"])
            self.detergent_entry.grid(row=3, column=2, pady=5, sticky="w", columnspan=4)
            self.widgets.append(self.detergent_entry)
            self.detergent_entry.set(self.order.detergent)
            self.detergent_entry.configure(state="disabled", fg_color="#191919")

        self.set_order_button = ctk.CTkButton(self, text=self.button_text, command=self.button_command)
        self.set_order_button.grid(row=(grid_rows-1), column=0, pady=(5, 10), columnspan=grid_columns)

        for widget in self.widgets:
            widget.bind("<Tab>", lambda e, w=widget: self.tab_handler(w))
            widget.bind("<Return>", lambda e, w=widget: self.return_handler(w))

    def show(self):
        self.focus()

    def return_handler(self, widget):
        length = len(self.widgets)
        for i, w in enumerate(self.widgets):
            if w == widget:
                if i == length - 1:
                    if self.isNew:
                        self.add_order()
                    else:
                        self.apply_edits()
                else:
                    self.widgets[i + 1].focus_set()
        return "break"

    def tab_handler(self, widget):
        length = len(self.widgets)
        for i, w in enumerate(self.widgets):
            if w == widget:
                if i == length - 1:
                    self.widgets[0].focus_set()
                else:
                    self.widgets[i + 1].focus_set()
        return "break"

    def add_order(self):
        cents_order = self.cents_entry.get("0.0", "end").strip()
        cc_order = self.cc_entry.get("0.0", "end").strip()
        order = Order(cents_order, cc_order)
        self.master.add_order(order)
        self.cents_entry.delete("0.0", "end")
        self.cc_entry.delete("0.0", "end")

    def apply_edits(self):
        self.order.cents_order = self.cents_entry.get("0.0", "end").strip()
        self.order.cc_order = self.cc_entry.get("0.0", "end").strip()
        self.order.notes = self.notes_entry.get("0.0", "end").strip()
        self.order.detergent = self.detergent_entry.get()
        self.master.edit_order(self.index, self.order)
        self.destroy()
    
    def edit_order(self):
        self.cents_entry.configure(state="normal", fg_color="#323232")
        self.cc_entry.configure(state="normal", fg_color="#323232")
        self.notes_entry.configure(state="normal", fg_color="#323232")
        self.detergent_entry.configure(state="normal", fg_color="#323232")
        self.set_order_button.configure(text="Apply Edits", command=self.apply_edits)