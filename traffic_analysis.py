import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def load_data(filename):
    """Load the data from a CSV file."""
    return pd.read_csv(filename)


def display_head(data):
    """Display the first few rows of the dataset."""
    return data.head()

def analyze_avg_vehicles_on_holidays(data):
    """Analyze the average number of vehicles on holidays vs. non-holidays."""
    avg_vehicles_holiday = data[data['holiday'] == 'yes']['Vehicles'].mean()
    total_vehicles_non_holiday = data[data['holiday'] == 'no']['Vehicles'].sum()
    return avg_vehicles_holiday, total_vehicles_non_holiday


def display_summary(data):
    """Display the data types and summary statistics of the dataset."""
    return data.info(), data.describe()


def analyze_avg_vehicles_by_junction(data):
    """Analyze the average number of vehicles at each junction."""
    avg_vehicles_by_junction = data.groupby('Junction')['Vehicles'].mean()
    return avg_vehicles_by_junction


def analyze_peak_traffic_hours(data):
    """Analyze the peak traffic hours."""
    data['DateTime'] = pd.to_datetime(data['DateTime'])
    data['Hour'] = data['DateTime'].dt.hour
    peak_traffic_hours = data.groupby('Hour')['Vehicles'].sum()
    return peak_traffic_hours


def analyze_avg_vehicles_on_holidays(data):
    """Analyze the average number of vehicles on holidays vs. non-holidays."""
    avg_vehicles_holiday = data[data['holiday'] == 'yes']['Vehicles'].mean()
    avg_vehicles_non_holiday = data[data['holiday'] == 'no']['Vehicles'].sum()
    return avg_vehicles_holiday, avg_vehicles_non_holiday


def compute_correlation_matrix(data):
    """Compute the correlation matrix."""
    one_hot_encoded_days = pd.get_dummies(data['day'], prefix='day')
    data = pd.concat([data, one_hot_encoded_days], axis=1)
    correlation_matrix = data[['Vehicles', 'Hour', 'day_Monday', 'day_Tuesday', 'day_Wednesday', 'day_Thursday',
                              'day_Friday', 'day_Saturday', 'day_Sunday']].corr()
    return correlation_matrix


def visualize_correlation_matrix(correlation_matrix):
    """Visualize the correlation matrix as a heatmap."""
    plt.figure(figsize=(8, 6))
    plt.title('Correlation Matrix')
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.show()


def display_results(data):
    """Display the results of exploratory data analysis."""
    result_str = ""

    head = display_head(data)
    result_str += "First few rows of the dataset:\n{}\n\n".format(head)

    info, description = display_summary(data)
    result_str += "Data types and summary statistics:\n{}\n{}\n\n".format(
        info, description)

    avg_vehicles_by_junction = analyze_avg_vehicles_by_junction(data)
    result_str += "Average number of vehicles at each junction:\n{}\n\n".format(
        avg_vehicles_by_junction)

    peak_traffic_hours = analyze_peak_traffic_hours(data)
    result_str += "Peak traffic hours:\n{}\n\n".format(peak_traffic_hours)

    avg_vehicles_holiday, avg_vehicles_non_holiday = analyze_avg_vehicles_on_holidays(
        data)
    result_str += "Average number of vehicles on holidays: {}\n".format(
        avg_vehicles_holiday)
    result_str += "Total number of vehicles on non-holidays: {}\n\n".format(
        avg_vehicles_non_holiday)

    correlation_matrix = compute_correlation_matrix(data)
    result_str += "Correlation matrix:\n{}\n".format(correlation_matrix)

    # Create a GUI window
    window = tk.Tk()
    window.title("Exploratory Data Analysis Results")

    # Create a scrollable text box to display the results
    result_text = tk.Text(window, width=80, height=30)
    result_text.pack()

    # Insert the results into the text box
    result_text.insert(tk.END, result_str)

    # Create a scrollable table to display the head of the dataset
    head_frame = tk.Frame(window)
    head_frame.pack()

    head_table = ttk.Treeview(head_frame)
    head_table["columns"] = tuple(head.columns)

    for col in head.columns:
        head_table.column(col, width=80, anchor="center")
        head_table.heading(col, text=col)

    for row in range(len(head)):
        head_table.insert("", "end", values=tuple(head.iloc[row]))

    head_table.pack(side=tk.LEFT)
    head_scrollbar = ttk.Scrollbar(
        head_frame, orient="vertical", command=head_table.yview)
    head_table.configure(yscrollcommand=head_scrollbar.set)
    head_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Show an OK button to close the window
    ok_button = tk.Button(window, text="OK", command=window.destroy)
    ok_button.pack()

    # Run the GUI event loop
    window.mainloop()


# Main function
def main():
    filename = 'traffic.csv'

    # Load the data
    data = load_data(filename)

    # Display the results of exploratory data analysis
    display_results(data)


if __name__ == '__main__':
    main()
