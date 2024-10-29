import customtkinter as ctk
import logging
import os
import pickle
from new_order import NewOrderForm
from log_window import LogWindow

# Configure logging
logging.basicConfig(filename='data\order.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Set the appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class OrderTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WaveMAX C&C Order Tracker")
        self.root.geometry("600x800")
        self.root.resizable(False, False)

        # Create a title label
        title_label = ctk.CTkLabel(self.root, text="WaveMAX C&C Order Tracker", font=("Arial", 16))
        title_label.grid(row=0, column=0, pady=10, columnspan=2, sticky="nsew")

        # Create a button to open the NewOrderForm window
        open_form_button = ctk.CTkButton(self.root, text="New Order", command=self.open_new_order_form)
        open_form_button.grid(row=1, column=0, pady=10, padx=10, sticky="e")

        # Create a button to open the log window
        open_log_button = ctk.CTkButton(self.root, text="Order History", command=self.open_log_window)
        open_log_button.grid(row=1, column=1, pady=10, padx=10, sticky="w")

        # Create a scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self.root, width=560, height=670)
        self.scrollable_frame.grid(row=2, column=0, pady=10, padx=10, columnspan=2, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure((0, 1), weight=1)

        # Initialize the orders list
        self.orders = []

        # Load orders from file
        self.load_orders()

        # Create the form window
        self.form_window = None

        # Create the log window
        self.log_window = None

        # Initial population of the scrollable frame
        self.update_scrollable_frame()

        # Bind the save_orders method to the window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def save_orders(self):
        with open("data\orders.pkl", "wb") as f:
            pickle.dump(self.orders, f)

    def load_orders(self):
        if os.path.exists("data\orders.pkl"):
            with open("data\orders.pkl", "rb") as f:
                self.orders = pickle.load(f)

    def on_closing(self):
        self.save_orders()
        self.root.destroy()
    
    def open_new_order_form(self):
        if self.form_window is not None and self.form_window.form_window.winfo_exists():
            self.form_window.show()
        else:
            self.form_window = NewOrderForm(self.root, self.add_order)

    def open_log_window(self):
        if self.log_window is not None and self.log_window.log_window.winfo_exists():
            self.log_window.show()
        else:
            self.log_window = LogWindow(self.root)

    def add_order(self, cents_order, cc_order):
        self.orders.append([f"Cents Order #{cents_order}", f"C&C Order #{cc_order}"])
        logging.info(f"New order added: ['Cents Order #{cents_order}', 'C&C Order #{cc_order}']")
        self.update_scrollable_frame()

    def finish_order(self, index):
        logging.info(f"Order picked up: {self.orders[index]}")
        del self.orders[index]
        self.update_scrollable_frame()

    def update_scrollable_frame(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        for i, order in enumerate(self.orders):
            if order:  # Check if the order is not empty
                cents_number = ctk.CTkLabel(self.scrollable_frame, text=order[0])
                cents_number.grid(row=i, column=0, pady=5, padx=5, sticky="e")
                cc_number = ctk.CTkLabel(self.scrollable_frame, text=order[1])
                cc_number.grid(row=i, column=1, pady=5, padx=5, sticky="w")
                finish_button = ctk.CTkButton(self.scrollable_frame, text="Order Picked up", command=lambda i=i: self.finish_order(i))
                finish_button.grid(row=i, column=2, pady=5, padx=5, sticky="e")

if __name__ == "__main__":
    app = ctk.CTk()
    order_tracker_app = OrderTrackerApp(app)
    app.mainloop()