import csv
import random
from flask import Flask, request, render_template

app = Flask(__name__)


# Load names from CSV file
def load_names(file_name):
    names = {"Boy": [], "Girl": [], "Unisex": []}
    with open(file_name, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            names[row["Gender"]].append(row["Name"])
    return names


# Suggest names based on user input
def suggest_names(names, gender, first_letter=None):
    filtered_names = [
        name
        for name in names[gender]
        if first_letter is None or name.startswith(first_letter.capitalize())
    ]
    return (
        random.sample(filtered_names, 5) if len(filtered_names) >= 5 else filtered_names
    )


# Load names on startup
names = load_names("names.csv")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        gender = request.form["gender"]
        first_letter = request.form.get("first_letter")
        suggestions = suggest_names(names, gender, first_letter)
        return render_template("index.html", suggestions=suggestions)
    return render_template("index.html", suggestions=[])


if __name__ == "__main__":
    app.run(debug=True)
