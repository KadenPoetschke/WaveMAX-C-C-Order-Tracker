import customtkinter as ctk
import logging
from new_order import NewOrderForm

# Configure logging
logging.basicConfig(filename='order.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Set the appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class OrderTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WaveMAX C&C Order Tracker")
        self.root.geometry("400x600")

        # Create a title label
        title_label = ctk.CTkLabel(self.root, text="WaveMAX C&C Order Tracker", font=("Arial", 16))
        title_label.pack(pady=10)

        # Create a scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self.root, width=380, height=580)
        self.scrollable_frame.pack(pady=10, padx=10)

        # Initialize the orders list
        self.orders = []

        # Create the form window
        self.form_window = NewOrderForm(self.root, self.add_order)

        # Initial population of the scrollable frame
        self.update_scrollable_frame()

    def add_order(self, cents_order, cc_order):
        self.orders.append([f"Cents Order #{cents_order}", f"C&C Order #{cc_order}"])
        self.update_scrollable_frame()

    def finish_order(self, index):
        logging.info(f"Order {self.orders[index]} picked up")
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