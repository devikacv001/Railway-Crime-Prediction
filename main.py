import tkinter as tk
from tkinter import messagebox, PhotoImage, ttk
from prediction import predict_arrests_for_year, plot_yearwise_rape_cases
from prediction import plot_trend_2023_to_2030
from panic_alert import send_emergency_alert
import pandas as pd
import os

USERS = {
    "admin": "admin123",
    "1": "1"
}

# Load full state list from CSV
_PREDICTED_DIR = os.path.join(os.path.dirname(__file__), "predicted arrests")
df = pd.read_csv(os.path.join(_PREDICTED_DIR, "predicted_arrests_2030.csv"))
ALL_STATES = df["State/UT"].dropna().unique().tolist()


def run_gui():
    def login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if username in USERS and USERS[username] == password:
            login_frame.destroy()
            main_app()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def main_app():
        def on_predict():
            try:
                year_input = year_entry.get().strip()
                selected_state = state_combo.get().strip()
                year = int(year_input)
                if year <= 2022:
                    messagebox.showinfo("Info", f"No prediction needed for {year}, data already exists.")
                else:
                    predict_arrests_for_year(year)
                    messagebox.showinfo("Success", f"Prediction for {year} saved and plotted successfully!")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid year (number only).")




        def on_panic():
            send_emergency_alert()

        def on_show_trend():
            selected_state = state_combo.get().strip()
            if not selected_state:
                messagebox.showerror("Error", "Please select a state.")
                return
            plot_yearwise_rape_cases(selected_state)

        root.geometry("460x500")
        title_label = tk.Label(root, text="🔐 Railway Safety + 🆘 Panic Alert", font=("Helvetica", 14, "bold"))
        title_label.pack(pady=10)

        tk.Label(root, text="Enter Year (e.g., 2023):", font=("Helvetica", 12)).pack()
        year_entry = tk.Entry(root, font=("Helvetica", 12), justify="center")
        year_entry.pack(pady=5)

        tk.Label(root, text="Select State:", font=("Helvetica", 12)).pack()
        state_combo = ttk.Combobox(root, values=ALL_STATES, font=("Helvetica", 12))
        state_combo.pack(pady=5)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=20)

        try:
            predict_icon = PhotoImage(file="panic_icon2.png").subsample(6, 6)
            panic_icon = PhotoImage(file="panic_icon.png").subsample(6, 6)
        except Exception as e:
            predict_icon = panic_icon = None
            print("Error loading icons:", e)

        tk.Button(btn_frame, image=predict_icon, command=on_predict).grid(row=0, column=0, padx=20)
        tk.Button(btn_frame, image=panic_icon, command=on_panic).grid(row=0, column=1, padx=20)

        tk.Label(btn_frame, text="Predict", font=("Helvetica", 10)).grid(row=1, column=0)
        tk.Label(btn_frame, text="Panic", font=("Helvetica", 10)).grid(row=1, column=1)

        tk.Button(root, text="📈 Total Arrest Trend (2023–30)", font=("Helvetica", 12), command=plot_trend_2023_to_2030).pack(pady=5)
        tk.Button(root, text="📊 State Trend (2023–29)", font=("Helvetica", 12), command=on_show_trend).pack(pady=10)

        root.mainloop()

    root = tk.Tk()
    root.title("Login - Railway Safety Tool")
    root.geometry("300x250")

    login_frame = tk.Frame(root)
    login_frame.pack(pady=30)

    tk.Label(login_frame, text="Username:", font=("Helvetica", 12)).grid(row=0, column=0, pady=5)
    username_entry = tk.Entry(login_frame, font=("Helvetica", 12))
    username_entry.grid(row=0, column=1)

    tk.Label(login_frame, text="Password:", font=("Helvetica", 12)).grid(row=1, column=0, pady=5)
    password_entry = tk.Entry(login_frame, show="*", font=("Helvetica", 12))
    password_entry.grid(row=1, column=1)

    tk.Button(login_frame, text="Login", font=("Helvetica", 12), command=login).grid(row=2, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_gui()