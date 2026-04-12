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
                if len(row) < 3:
                    continue  # Skip rows that don't have enough columns
                
                if i == 0:
                    row.append("Category")  # Add header
                else:
                    category = categorize_transaction(row[1])  # Description is in the second column
                    row.append(category)

                    amount = float(row[2])

                    # Only consider expenses (negative amounts), not income
                    if amount < 0:
                        if category in category_totals:
                            category_totals[category] += abs(amount)
                        else:
                            category_totals[category] = abs(amount)

                transactions.append(row)

            # Generate insights
            if category_totals:
                total_spent = sum(category_totals.values())

                for category, amount in category_totals.items():
                    percentage = (amount / total_spent) * 100
                    insights.append(f"{percentage:.1f}% of your spending is on {category}")

                top_category = max(category_totals, key=category_totals.get)
                insights.append(f"Your highest spending is on {top_category}")


    return render_template("index.html", transactions=transactions, insights=insights, category_totals=category_totals)

if __name__ == "__main__":
    app.run(debug=True)