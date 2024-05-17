from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Initialize the Flask application
app = Flask(__name__)

# Load data from a CSV file into a Pandas DataFrame
data = pd.read_csv('Original.csv')

# Calculate some basic statistics
average_price = data['Price'].mean()
average_rating = data['Rating'].mean()

# Define a function to generate a bar chart and encode it as a base64 image
def create_and_encode_bar_chart():
    plt.figure(figsize=(10, 6))
    data.groupby('Brand')['Price'].mean().sort_values().plot(kind='barh', color='skyblue')
    plt.title('Average Price by Brand')
    plt.xlabel('Average Price')
    plt.ylabel('Brand')

    # Save the plot to a BytesIO object
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    encoded_image = base64.b64encode(img_buffer.read()).decode('utf-8')
    plt.close()
    return encoded_image

# Define a route to display the data and chart
@app.route('/')
def display_data_and_chart():
    encoded_chart = create_and_encode_bar_chart()
    return render_template('dashboard.html', average_price=average_price, average_rating=average_rating, encoded_chart=encoded_chart)

if __name__ == '__main__':
    app.run(debug=True)
