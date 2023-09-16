import tkinter as tk
from tkinter import font as tkfont
from tkcalendar import DateEntry
import subprocess


def run_traffic_pattern():
    subprocess.run(["python", "traffic_analysis.py"])


def run_data_preprocessing():
    subprocess.run(["python", "data_preprocessing.py"])


def visualize_results():
    # Call the pattern.py module
    process = subprocess.Popen(["python", "pattern.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = process.communicate()
    result = stdout.decode().strip()

    # Display the output in a new window
    result_window = tk.Toplevel()
    result_window.title("Pattern Analysis Results")
    result_label = tk.Label(result_window, text=result, font=("Arial", 12))
    result_label.pack(pady=20)


def predict_traffic(input_date):
    # Call the predict.py script and retrieve the predicted traffic level
    process = subprocess.Popen(["python", "predict.py", input_date], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = process.communicate()
    predicted_traffic = stdout.decode().strip()

    return predicted_traffic

def generate_summary(name, email, ph_number, weather, prediction_date):
    summary = "Summary:\n\n"
    summary += "Name: {}\n".format(name)
    summary += "Email: {}\n".format(email)
    summary += "Phone Number: {}\n".format(ph_number)
    summary += "Weather Condition: {}\n".format(weather)
    summary += "Prediction Date: {}\n".format(prediction_date)

    summary_window = tk.Toplevel()
    summary_window.title("Prediction Summary")
    summary_label = tk.Label(summary_window, text=summary, font=("Arial", 12))
    summary_label.pack(pady=20)

    # Call the predict function to retrieve the predicted traffic level
    predicted_traffic = predict_traffic(prediction_date)

    traffic_label = tk.Label(summary_window, text="Traffic Level: {}".format(predicted_traffic), font=("Arial", 12))
    traffic_label.pack(pady=10)


def create_gui():
    window = tk.Tk()
    window.title("Traffic Analysis Tool")
    window.configure(bg="lightblue")  # Set background color

    # Set custom font
    title_font = tkfont.Font(family="Helvetica", size=20, weight="bold")
    button_font = tkfont.Font(family="Arial", size=14)

    title_label = tk.Label(
        window, text="Traffic Analysis Tool", font=title_font)
    title_label.grid(row=0, column=0, columnspan=2, pady=20)

    entry_frame = tk.Frame(window)
    entry_frame.grid(row=1, column=0, columnspan=2, pady=10)

    name_label = tk.Label(entry_frame, text="Name:")
    name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    name_entry = tk.Entry(entry_frame)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    email_label = tk.Label(entry_frame, text="Email:")
    email_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    email_entry = tk.Entry(entry_frame)
    email_entry.grid(row=1, column=1, padx=10, pady=5)

    ph_number_label = tk.Label(entry_frame, text="Phone Number:")
    ph_number_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    ph_number_entry = tk.Entry(entry_frame)
    ph_number_entry.grid(row=2, column=1, padx=10, pady=5)

    weather_label = tk.Label(entry_frame, text="Weather Condition:")
    weather_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    weather_entry = tk.Entry(entry_frame)
    weather_entry.grid(row=3, column=1, padx=10, pady=5)

    prediction_frame = tk.Frame(window)
    prediction_frame.grid(row=2, column=0, columnspan=2, pady=10)

    pattern_button = tk.Button(
        window, text="Run Traffic Pattern Analysis", font=button_font, command=run_traffic_pattern)
    pattern_button.grid(row=3, column=0, columnspan=2, pady=10)

    preprocessing_button = tk.Button(
        window, text="Run Data Preprocessing", font=button_font, command=run_data_preprocessing)
    preprocessing_button.grid(row=4, column=0, columnspan=2, pady=10)

    visualize_button = tk.Button(
        window, text="Visualize Results", font=button_font, command=visualize_results)
    visualize_button.grid(row=5, column=0, columnspan=2, pady=10)

    prediction_label = tk.Label(
        prediction_frame, text="Prediction Date:", font=("Arial", 12))
    prediction_label.grid(row=0, column=0, padx=10, pady=5)
    prediction_entry = DateEntry(prediction_frame, width=12,
                                 background='darkblue', foreground='white', borderwidth=2)
    prediction_entry.grid(row=0, column=1, padx=10, pady=5)

    generate_summary_button = tk.Button(
        window, text="Generate Summary", font=button_font, command=lambda: generate_summary(
            name_entry.get(), email_entry.get(), ph_number_entry.get(),
            weather_entry.get(), prediction_entry.get_date().strftime("%m/%d/%Y"))
    )
    generate_summary_button.grid(row=6, column=0, columnspan=2, pady=10)

    # Center the window on the screen
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

    window.mainloop()


if __name__ == "__main__":
    create_gui()
