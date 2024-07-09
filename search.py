from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Load your CSV data into a DataFrame
df = pd.read_csv('C:/Users/Dell/OneDrive/Desktop/MINI PROJECT WEB/sample.csv')

# Convert numeric difficulty in CSV to string immediately after loading
difficulty_map = {0: 'easy', 1: 'medium', 2: 'hard'}
df['difficulty'] = df['difficulty'].map(difficulty_map)

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/search', methods=['GET'])
def search():
    difficulty = request.args.get('difficulty', 'all')
    year = request.args.get('year', 'all')
    subject = request.args.get('subject', 'all')
    query = request.args.get('query', '')

    # Filtering
    filtered_df = df.copy()
    if difficulty != 'all':
        filtered_df = filtered_df[filtered_df['difficulty'] == difficulty]
    if year != 'all':
        filtered_df = filtered_df[filtered_df['year'] == int(year)]
    if subject != 'all':
        filtered_df = filtered_df[filtered_df['subject'] == subject]

    # Searching
    if query:
        filtered_df = filtered_df[filtered_df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]

    # Assign question numbers
    filtered_df = filtered_df.reset_index(drop=True).reset_index()
    filtered_df.rename(columns={'index': 'Question Number'}, inplace=True)
    filtered_df['Question Number'] += 1  # start numbering from 1

    # Select only Question Number and Question columns for display
    questions = filtered_df[['Question Number', 'question']].values.tolist()

    return render_template('search.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)
