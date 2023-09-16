import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(filename):
    """Load the data from a CSV file."""
    return pd.read_csv(filename)


def convert_to_datetime(data, column):
    """Convert a column to datetime format."""
    data[column] = pd.to_datetime(data[column])
    return data


def analyze_avg_vehicles_by_date(data):
    """Analyze the average number of vehicles by date."""
    data['Date'] = data['DateTime'].dt.date
    avg_vehicles_by_date = data.groupby('Date')['Vehicles'].mean()

    plt.figure(figsize=(12, 6))
    plt.plot(avg_vehicles_by_date.index, avg_vehicles_by_date.values)
    plt.xlabel('Date')
    plt.ylabel('Average Number of Vehicles')
    plt.title('Traffic Pattern: Average Number of Vehicles by Date')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()


def analyze_avg_vehicles_by_hour(data):
    """Analyze the average number of vehicles by hour."""
    data['Hour'] = data['DateTime'].dt.hour
    avg_vehicles_by_hour = data.groupby('Hour')['Vehicles'].mean()

    plt.figure(figsize=(8, 6))
    plt.plot(avg_vehicles_by_hour.index, avg_vehicles_by_hour.values)
    plt.xlabel('Hour')
    plt.ylabel('Average Number of Vehicles')
    plt.title('Traffic Pattern: Average Number of Vehicles by Hour')
    plt.grid(True)
    plt.show()


def analyze_avg_vehicles_by_weekday(data):
    """Analyze the average number of vehicles by day of the week."""
    data['Weekday'] = data['DateTime'].dt.weekday
    weekday_names = ['Monday', 'Tuesday', 'Wednesday',
                     'Thursday', 'Friday', 'Saturday', 'Sunday']
    avg_vehicles_by_weekday = data.groupby('Weekday')['Vehicles'].mean()

    plt.figure(figsize=(8, 6))
    plt.plot(weekday_names, avg_vehicles_by_weekday.values)
    plt.xlabel('Weekday')
    plt.ylabel('Average Number of Vehicles')
    plt.title('Traffic Pattern: Average Number of Vehicles by Day of the Week')
    plt.grid(True)
    plt.show()


def analyze_avg_vehicles_by_junction(data):
    """Analyze the average number of vehicles by junction."""
    avg_vehicles_by_junction = data.groupby('Junction')['Vehicles'].mean()

    plt.figure(figsize=(8, 6))
    plt.bar(avg_vehicles_by_junction.index, avg_vehicles_by_junction.values)
    plt.xlabel('Junction')
    plt.ylabel('Average Number of Vehicles')
    plt.title('Traffic Pattern: Average Number of Vehicles by Junction')
    plt.xticks(avg_vehicles_by_junction.index)
    plt.grid(True)
    plt.show()


def compute_correlation_matrix(data):
    """Compute the correlation matrix."""
    correlation_matrix = data[['Vehicles',
                               'Hour', 'Weekday', 'Junction']].corr()
    return correlation_matrix


def visualize_correlation_matrix(correlation_matrix):
    """Visualize the correlation matrix as a heatmap."""
    plt.figure(figsize=(8, 6))
    plt.title('Correlation Matrix')
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.show()

# Main function


def main():
    filename = 'traffic.csv'

    # Load the data
    data = load_data(filename)

    # Perform data preprocessing
    data = convert_to_datetime(data, 'DateTime')

    # Perform traffic pattern analysis
    analyze_avg_vehicles_by_date(data)
    analyze_avg_vehicles_by_hour(data)
    analyze_avg_vehicles_by_weekday(data)
    analyze_avg_vehicles_by_junction(data)

    # Perform correlation analysis
    correlation_matrix = compute_correlation_matrix(data)
    visualize_correlation_matrix(correlation_matrix)


if __name__ == '__main__':
    main()
