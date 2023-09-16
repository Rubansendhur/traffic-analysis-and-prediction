import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


def load_data(filename):
    """Load the data from a CSV file."""
    return pd.read_csv(filename)


def preprocess_data(data):
    """Preprocess the data."""
    data['DateTime'] = pd.to_datetime(data['DateTime'])
    data['Hour'] = data['DateTime'].dt.hour
    data['Weekday'] = data['DateTime'].dt.weekday
    return data


def train_model(features, target):
    """Train the Linear Regression model."""
    scaler = StandardScaler(copy=False)
    features_scaled = scaler.fit_transform(features)
    model = LinearRegression()
    model.fit(features_scaled, target)
    return model, scaler


def predict_traffic(prediction_date):
    """Predict the traffic for a given date."""
    try:
        # Load the data
        filename = 'traffic.csv'
        data = load_data(filename)

        # Preprocess the data
        data = preprocess_data(data)

        # Select features and target variable
        features = data[['Junction', 'Hour', 'Weekday']]
        target = data['Vehicles']

        # Train the model
        model, scaler = train_model(features, target)

        input_date = pd.to_datetime(prediction_date)
        hour = input_date.hour
        weekday = input_date.weekday()
        input_features = [[1, hour, weekday]]
        input_features_df = pd.DataFrame(input_features, columns=['Junction', 'Hour', 'Weekday'])
        features_scaled = scaler.transform(input_features_df)
        predicted_traffic = model.predict(features_scaled)

        traffic_level = ""
        if predicted_traffic <= 25:
            traffic_level = "Low"
        elif predicted_traffic <= 30:
            traffic_level = "Medium"
        else:
            traffic_level = "High"

        result = {
            'text': "Predicted traffic on {}: {} (Traffic Level: {})".format(
                prediction_date, predicted_traffic, traffic_level)
        }
        return result

    except Exception as e:
        result = {
            'error': str(e)
        }
        return result
