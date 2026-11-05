from flask import Flask

app = Flask(__name__)


@app.route("/")
def welcome():
    return "Welcome to my Finance Tracker"


@app.route("/total")
def total_expenses():
    expenses = [4, 32, 42.56, 67]
    total = sum(expenses)
    return f"Total spent: ${total:.2f}"


@app.route("/category/<name>")
def category(name):
    spent = {
        "grocerys" : 145.65,
        "entertainment" : 201.34
        }
    name = name.lower()
    if name in spent:
        #the <br> is like \n but in html b/c flask tells the browser your response is html
        return f"You asked for {name}<br>Total amount spent in {name}: ${spent[name]:.2f}"
    return "Unknown Category"
