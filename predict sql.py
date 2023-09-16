import tkinter as tk
from tkinter import font as tkfont
from tkcalendar import DateEntry
import subprocess
import predict
import mysql.connector
import datetime

# API key for weather data (replace with your own)
API_KEY = "7d351dc846bb20a9ddf2346acfa9d8b9"

# MySQL connection configuration
mysql_config = {
    'user': 'root',
    'password': 'Gooes@519',
    'host': 'localhost',
    'database': 'traffic'
}

def get_current_weather():
    city = "New York"  # Replace with your desired city
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather = data["weather"][0]["main"]
        temperature = data["main"]["temp"]
        return f"{weather}, {temperature}°C"
    else:
        return "Unknown"

# Function to store data in MySQL
def store_data_in_mysql(name, email, ph_number, weather, prediction_date, result):
    try:
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        # Create the table if it doesn't exist
        cursor.execute("CREATE TABLE IF NOT EXISTS traffic_analysis (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), ph_number VARCHAR(255), weather VARCHAR(255), prediction_date DATE, result VARCHAR(255))")

        # Convert the date to the desired format
        formatted_date = prediction_date.strftime("%Y-%m-%d")  # Convert date to string

        # Insert the data into the table
        query = "INSERT INTO traffic_analysis (name, email, ph_number, weather, prediction_date, result) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (name, email, ph_number, weather, formatted_date, result)
        cursor.execute(query, values)

        # Commit the changes and close the cursor and connection
        connection.commit()
        cursor.close()
        connection.close()

        return True

    except mysql.connector.Error as error:
        print("Error storing data in MySQL: {}".format(error))
        return False


def generate_summary(name, email, ph_number, weather, prediction_date):
    summary = "PREDICTED RESULTS:\n\n"
    summary += "Name: {}\n".format(name)
    summary += "Email: {}\n".format(email)
    summary += "Phone Number: {}\n".format(ph_number)
    summary += "Weather Condition: {}\n".format(weather)
    summary += "Prediction Date: {}\n".format(prediction_date)

    summary_window = tk.Toplevel()
    summary_window.title("Prediction Summary")
    summary_window.configure(bg="red")  # Set background color to red

    # Create a frame to contain the labels
    label_frame = tk.Frame(summary_window, bg="red")
    label_frame.pack(pady=20)

    # Create labels for the summary information
    summary_label = tk.Label(label_frame, text=summary, font=("Arial", 12), fg="black", bg="red", justify="left")
    summary_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    result = predict.predict_traffic(prediction_date)

    if 'text' in result:
        result_label = tk.Label(label_frame, text="Result: {}".format(result['text']), font=("Arial", 12))
        result_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Check if 'mean_correlation' key is present in the result dictionary
        if 'mean_correlation' in result:
            mean_correlation_label = tk.Label(label_frame, text="Mean Correlation: {}".format(result['mean_correlation']), font=("Arial", 12))
            mean_correlation_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

            # Print mean correlation value
            print("Mean Correlation: {}".format(result['mean_correlation']))
        
        if 'regression_value' in result:
            regression_value_label = tk.Label(label_frame, text="Regression Value: {}".format(result['regression_value']), font=("Arial", 12))
            regression_value_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

            # Print regression value
            print("Regression Value: {}".format(result['regression_value']))
        
    else:
        error_label = tk.Label(label_frame, text="Error: {}".format(result['error']), font=("Arial", 12), fg="white", bg="red")
        error_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Print error message
        print("Error: {}".format(result['error']))

    # Check if 'traffic_flow' key is present in the result dictionary
    if 'traffic_flow' in result:
        traffic_flow_label = tk.Label(label_frame, text="Traffic Flow: \n{}".format(result['traffic_flow']), font=("Arial", 12))
        traffic_flow_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

    if store_data_in_mysql(name, email, ph_number, weather, prediction_date, result['text']):
        success_label = tk.Label(label_frame, text="Data stored successfully in MySQL!", font=("Arial", 12), fg="green")
        success_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    else:
        failure_label = tk.Label(label_frame, text="Failed to store data in MySQL!", font=("Arial", 12), fg="red")
        failure_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")


def visualize_result():
    subprocess.call(["python", "pattern.py"])


def show_sample_analysis():
    subprocess.call(["python", "traffic_analysis.py"])


def validate_login(username_entry, password_entry):
    # Customize the username and password validation logic here
    if username_entry.get() == "admin" and password_entry.get() == "password":
        login_window.destroy()  # Close the login window
        create_gui()  # Create the main GUI window
    else:
        error_label = tk.Label(login_frame, text="Invalid username or password", font=("Arial", 12), fg="red")
        error_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")


def create_login():
    global login_window
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.configure(bg="light blue")

    login_title_font = tkfont.Font(family="Helvetica", size=20, weight="bold")
    login_label_font = tkfont.Font(family="Courier New", size=12, weight="bold")

    login_title_label = tk.Label(login_window, text="Login", font=login_title_font)
    login_title_label.grid(row=0, column=0, columnspan=2, pady=20)

    login_frame = tk.Frame(login_window, bg="light blue")
    login_frame.grid(row=1, column=0, pady=10, padx=20, sticky="W")

    username_label = tk.Label(login_frame, text="Username:", font=login_label_font, bg="light blue")
    username_label.grid(row=0, column=0, padx=10, pady=10, sticky="E")
    username_entry = tk.Entry(login_frame, font=login_label_font)
    username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="W")

    password_label = tk.Label(login_frame, text="Password:", font=login_label_font, bg="light blue")
    password_label.grid(row=1, column=0, padx=10, pady=10, sticky="E")
    password_entry = tk.Entry(login_frame, font=login_label_font, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="W")

    login_button = tk.Button(login_frame, text="Login", font=login_label_font, bg="green", fg="white",
                             command=lambda: validate_login(username_entry, password_entry))
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

    login_window.mainloop()


def create_gui():
    def get_weather():
        weather = weather_entry.get()
        if weather != "":
            weather_label.configure(text="Weather: {}".format(weather), fg="black")
        else:
            weather_label.configure(text="Weather: Not specified", fg="gray")

    def get_date():
        prediction_date = date_entry.get_date()
        prediction_date_label.configure(text="Prediction Date: {}".format(prediction_date.strftime("%d-%m-%Y")),
                                        fg="black")

    def predict_traffic_flow():
        name = name_entry.get()
        email = email_entry.get()
        ph_number = ph_number_entry.get()
        weather = weather_entry.get()
        prediction_date = date_entry.get_date()

        if name == "" or email == "" or ph_number == "" or prediction_date is None:
            error_label.configure(text="Please fill in all the required fields", fg="red")
        else:
            error_label.configure(text="")
            generate_summary(name, email, ph_number, weather, prediction_date)

    def clear_fields():
        name_entry.delete(0, "end")
        email_entry.delete(0, "end")
        ph_number_entry.delete(0, "end")
        weather_entry.delete(0, "end")
        date_entry.set_date(datetime.date.today())

    main_window = tk.Tk()
    main_window.title("Traffic Analysis")
    main_window.configure(bg="light blue")

    title_font = tkfont.Font(family="Helvetica", size=20, weight="bold")
    label_font = tkfont.Font(family="Courier New", size=12, weight="bold")

    title_label = tk.Label(main_window, text="Traffic Analysis", font=title_font)
    title_label.grid(row=0, column=0, columnspan=2, pady=20)

    form_frame = tk.Frame(main_window, bg="light blue")
    form_frame.grid(row=1, column=0, pady=10, padx=20, sticky="W")

    name_label = tk.Label(form_frame, text="Name:", font=label_font, bg="light blue")
    name_label.grid(row=0, column=0, padx=10, pady=10, sticky="E")
    name_entry = tk.Entry(form_frame, font=label_font)
    name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="W")

    email_label = tk.Label(form_frame, text="Email:", font=label_font, bg="light blue")
    email_label.grid(row=1, column=0, padx=10, pady=10, sticky="E")
    email_entry = tk.Entry(form_frame, font=label_font)
    email_entry.grid(row=1, column=1, padx=10, pady=10, sticky="W")

    ph_number_label = tk.Label(form_frame, text="Phone Number:", font=label_font, bg="light blue")
    ph_number_label.grid(row=2, column=0, padx=10, pady=10, sticky="E")
    ph_number_entry = tk.Entry(form_frame, font=label_font)
    ph_number_entry.grid(row=2, column=1, padx=10, pady=10, sticky="W")

    weather_label = tk.Label(form_frame, text="Weather: Not specified", font=label_font, bg="light blue", fg="gray")
    weather_label.grid(row=3, column=0, padx=10, pady=10, sticky="E")
    weather_entry = tk.Entry(form_frame, font=label_font)
    weather_entry.grid(row=3, column=1, padx=10, pady=10, sticky="W")
    weather_entry.bind("<FocusOut>", lambda event: get_weather())


    prediction_date_label = tk.Label(form_frame, text="Prediction Date:", font=label_font, bg="light blue", fg="gray")
    prediction_date_label.grid(row=4, column=0, padx=10, pady=10, sticky="E")
    date_entry = DateEntry(form_frame, width=12, background="darkblue", foreground="white", borderwidth=2,
                           font=("Arial", 12))
    date_entry.set_date(datetime.date.today())
    date_entry.grid(row=4, column=1, padx=10, pady=10, sticky="W")
    date_entry.bind("<FocusOut>", lambda event: get_date())

    button_frame = tk.Frame(main_window, bg="light blue")
    button_frame.grid(row=1, column=1, pady=10, padx=20, sticky="E")

    predict_button = tk.Button(button_frame, text="Predict", font=label_font, bg="green", fg="white",
                               command=predict_traffic_flow)
    predict_button.grid(row=0, column=0, pady=10)

    clear_button = tk.Button(button_frame, text="Clear", font=label_font, bg="gray", fg="white",
                             command=clear_fields)
    clear_button.grid(row=1, column=0, pady=10)

    summary_frame = tk.Frame(main_window, bg="light blue")
    summary_frame.grid(row=2, column=0, columnspan=2, pady=20)

    error_label = tk.Label(summary_frame, text="", font=label_font, fg="red", bg="light blue")
    error_label.pack()

    visualize_button = tk.Button(summary_frame, text="Visualize Result", font=label_font, bg="blue", fg="white",
                                 command=visualize_result)
    visualize_button.pack(side="left", padx=10)

    sample_button = tk.Button(summary_frame, text="Show Sample Analysis", font=label_font, bg="blue", fg="white",
                              command=show_sample_analysis)
    sample_button.pack(side="right", padx=10)

    main_window.mainloop()


if __name__ == "__main__":
    create_login()
