from flask import Flask, render_template, request
import csv

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    transactions = []

    if request.method == "POST":
        file = request.files["file"]

        if file:
            data = file.read().decode("utf-8").splitlines()
            reader = csv.reader(data)

            for row in reader:
                transactions.append(row)
    
    return render_template("index.html", transactions=transactions)

if __name__ == "__main__":
    app.run(debug=True)