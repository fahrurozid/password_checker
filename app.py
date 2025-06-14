from flask import Flask, request, render_template
from generator import generator_password
from checker import check_strength
import json
import datetime

app = Flask(__name__)
HISTORY_FILE = "history.json"

def save_to_history(password, strength):
    data = {
        "password": password,
        "strength": strength,
        "timestamp": datetime.datetime.now().isoformat()
    }
    try:
        with open(HISTORY_FILE, "r+") as file:
            history = json.load(file)
            history.append(data)
            file.seek(0)
            json.dump(history, file, indent=4)
    except FileNotFoundError:
        with open(HISTORY_FILE, "w") as file:
            json.dump([data], file, indent=4)

@app.route('/')
def index():
    return "<h1>API Password Checker Aktif!</h1><p>Buka <code>/dashboard</code> untuk menggunakan generator</p>"

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    result = None
    if request.method == 'POST':
        try:
            length = int(request.form.get('length', 12))
            password = generator_password(length)
            strength = check_strength(password)
            save_to_history(password, strength)
            result = {"password": password, "strength": strength}
        except Exception as e:
            result = {"error": f"Terjadi kesalahan saat memproses input: {str(e)}"}
    return render_template('index.html', result=result)


@app.route('/history')
def history():
    try:
        with open(HISTORY_FILE) as f:
            data = json.load(f)
        return data
    except:
        return []

if __name__ == '__main__':
    app.run(debug=True)
