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
    category_totals = {}
    insights = []

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

                    amount = float(row[2])  # Amount is in the third column
                    if category in category_totals:
                        category_totals[category] += amount
                    else:
                        category_totals[category] = amount

                transactions.append(row)

            if category_totals:
                total_spent = sum(abs(v) for v in category_totals.values())

                for category, amount in category_totals.items():
                    percentage = (abs(amount) / total_spent) * 100
                    insights.append(f"You spent {percentage:.2f}% on {category}.")

                top_category = max(category_totals, key=lambda x: abs(category_totals[x]))
                insights.append(f"Your highest spending is on {top_category}")


    return render_template("index.html", transactions=transactions, insights=insights)

if __name__ == "__main__":
    app.run(debug=True)