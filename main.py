from generator import generator_password
from checker import check_strength
import json
import datetime

def save_history(password, strength):
    data = {
        "password": password,
        "strength": strength,
        "timestamp": datetime.datetime.now().isoformat()
    }
    try:
        with open("history.json", "r+") as file:
            history = json.load(file)
            history.append(data)
            file.seek(0)
            json.dump(history, file, indent=4)
    except FileNotFoundError:
        with open("history.json", "w") as file:
            json.dump([data], file, indent=4)

if __name__ == "__main__":
    print("Password Generator + Strength Checker")
    length = int(input("Masukkan panjang password: "))
    password = generator_password(length)
    print(f"password: {password}")

    strength = check_strength(password)
    print(f"Kekuaran: {strength}")

    save_history(password, strength)
    print("Password disimpan ke history.json")