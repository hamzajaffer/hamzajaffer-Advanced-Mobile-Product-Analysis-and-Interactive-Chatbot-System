from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the CSV file into a DataFrame
data = pd.read_csv('proj2.csv')
data['Price'] = pd.to_numeric(data['Price'], errors='coerce')
data['Rating'] = pd.to_numeric(data['Rating'], errors='coerce')
data.dropna(subset=['Price', 'Rating'], inplace=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    # When the form is submitted
    if request.method == 'POST':
        # This will be a string like "best phone under 30000" or "best phone rating 4.5"
        user_query = request.form['user_query']
        # Call the appropriate function based on the user query
        if 'rating' in user_query.lower():
            try:
                # Assuming the user types something like "phones with rating above 4"
                desired_rating = float(user_query.split()[-1])
                result = find_best_phones_by_rating(desired_rating)
            except ValueError:
                result = "Invalid rating value. Please enter a numeric rating."
        else:
            try:
                # Assuming the user types something like "best phone under 30000"
                max_price = float(user_query.split()[-1])
                result = find_best_phones_under(max_price)
            except ValueError:
                result = "Invalid price value. Please enter a numeric price."

        return render_template('index.html', result=result)
    else:
        # Initial page load
        return render_template('index.html')

def find_best_phones_by_rating(desired_rating):
    # Filter the phones by rating
    top_rated_phones = data[data['Rating'] >= desired_rating].sort_values(by='Rating', ascending=False)
    # If there are no phones with such a high rating
    if top_rated_phones.empty:
        return "No phones found with the rating of {} or above.".format(desired_rating)
    return top_rated_phones[['Name', 'Brand', 'Price', 'Rating']].to_html(classes='table table-striped')

def find_best_phones_under(max_price):
    # Filter the phones by price
    affordable_phones = data[data['Price'] <= max_price].sort_values(by='Rating', ascending=False)
    return affordable_phones[['Name', 'Brand', 'Price', 'Rating']].to_html(classes='table table-striped')

if __name__ == '__main__':
    app.run(debug=True)