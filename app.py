from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def categorize_transaction(description):
    description = description.lower()
    if "mcdonald" in description or "restaurant" in description:
        return "Food"
    elif "bus" in description or "train" in description:
        return "Transport"
    elif "amazon" in description or "shop" in description:
        return "Shopping"
    elif "salary" in description:
        return "Income"
    else:
        return "Other"

@app.route("/", methods=["GET", "POST"])
def home():
    transactions = []

    if request.method == "POST":
        file = request.files["file"]

        if file:
            data = file.read().decode("utf-8").splitlines()
            reader = csv.reader(data)

            for i, row in enumerate(reader):
                if i == 0:
                    row.append("Category")  # Add header
                else:
                    category = categorize_transaction(row[1])  # Description is in the second column
                    row.append(category)

                transactions.append(row)
    return render_template("index.html", transactions=transactions)

if __name__ == "__main__":
    app.run(debug=True)