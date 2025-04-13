from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import csv
import os
from difflib import get_close_matches

app = Flask(__name__)
app.secret_key = 'your-secret-key'

chatbot_data = {}

def load_csv_data(filename):
    chatbot_data.clear()
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            question = row['Questions'].strip().lower()
            answer = row['Answers'].strip()
            chatbot_data[question] = answer

load_csv_data('college_info_qna.csv')

@app.route('/chat', methods=['POST'])
def chat():
    user_query = request.json.get('query', '').strip().lower()

    casual_responses = {
        "hello": "Hi there! How can I help you today?",
        "hi": "Hello! Feel free to ask me anything about the college.",
        "hii": "Hey! How can I assist you?",
        "hyy": "Hi! What would you like to know?",
        "hlo": "Hello! 😊",
        "hey": "Hey! What's your question?",
        "good morning": "Good morning! How can I help?",
        "good afternoon": "Good afternoon! Ask me anything about the college.",
        "good evening": "Good evening! How can I help you today?"
    }

    if user_query in casual_responses:
        return jsonify({'response': casual_responses[user_query]})
    if user_query in chatbot_data:
        return jsonify({'response': chatbot_data[user_query]})
    matches = get_close_matches(user_query, chatbot_data.keys(), n=1, cutoff=0.5)
    if matches:
        return jsonify({'response': chatbot_data[matches[0]]})
    return jsonify({'response': "Sorry, I don't have the answer to that. Please contact the administration."})

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        return render_template('admin_login.html', error="Invalid credentials.")
    return render_template('admin_login.html')

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename.endswith('.csv'):
            filepath = os.path.join(os.getcwd(), 'college_info_qna.csv')
            file.save(filepath)
            load_csv_data(filepath)
            return render_template('admin_dashboard.html', message="Dataset updated successfully.")
        return render_template('admin_dashboard.html', error="Invalid file. Please upload a CSV.")
    return render_template('admin_dashboard.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatpage')
def chat_page():
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True)
