# Phase 0: Flask Basics (1-week learning plan)

This plan has four short lessons. Each one teaches a core Flask concept with a small finance-tracker exercise.
All practice code lives in this `learning/` folder, apart from the real app.
You write each exercise yourself first. If you get stuck, ask for help or a review.

## Setup (Day 1, ~15 min)

Run these from the project root:

```bash
python3 -m venv .venv          # a private Python install just for this project
source .venv/bin/activate      # turn it on (do this in every new terminal)
pip install -r learning/requirements.txt
```

Check that it worked:

```bash
python -c "import flask, flask_sqlalchemy; print(flask.__version__)"
```

**To run any lesson:**

```bash
cd learning/01_routes          # or whichever lesson folder
flask --app app run --debug
```

Then open http://127.0.0.1:5000 in your browser.
- `--app app` tells Flask to look for `app.py`.
- `--debug` reloads the server whenever you save, and it shows readable error pages.
- Press **Ctrl+C** to stop the server.

## Week schedule

| Day | Lesson |
|---|---|
| 1 | Setup + Lesson 1: Routes |
| 2 | Lesson 2: Templates |
| 3–4 | Lesson 3: Forms |
| 5–6 | Lesson 4: Database |
| 7 | Buffer: finish up, answer the check questions, ask for a review |

---

## Lesson 1: Routes

**Folder:** `learning/01_routes/app.py`

**Idea:** A route connects a URL to a Python function. When the browser visits `/total`, Flask runs the function tied to that URL and sends back whatever the function returns.

**Analogy:** A restaurant menu. The URL is the item number you order, the function is the cook, and the return value is the plate that comes back.

**Key pieces:**
- `app = Flask(__name__)` creates your app.
- `@app.route("/path")` goes above a function and says "run this for that URL".
- The function returns a string, and the browser displays it.
- Variable URLs such as `@app.route("/category/<name>")` pass the `<name>` part of the URL into your function as an argument.

**Exercise:** Make an app with three routes:
1. `/` returns `Welcome to my Finance Tracker`.
2. `/total` adds up a hard-coded Python list of expense amounts and returns `Total spent: $X.XX`.
3. `/category/<name>` returns `You asked about: <name>`.
   - *Bonus:* look up the amount for that category in a dict and return it, or return `Unknown category`.

**If it works:** Each URL shows plain text. For example, `/category/groceries` shows "You asked about: groceries". A URL you didn't define, like `/expenses`, shows a **404 Not Found** page.

**Check questions:**
- What does the `@app.route` decorator do?
- How does `<name>` in a URL reach your function?
- Why do you see a 404 for `/expenses` if you never defined it?

---

## Lesson 2: Templates

**Folder:** `learning/02_templates/` (with `app.py` and a `templates/` subfolder)

**Idea:** Writing HTML inside Python strings gets messy fast. Templates are separate `.html` files with placeholders. Flask uses its template engine, **Jinja2**, to fill those placeholders with your data.

**Analogy:** A form letter (mail merge). The letter is written once, and the names and amounts are filled in for each copy.

**Key pieces:**
- Template files go in a folder named `templates/` next to `app.py`.
- `render_template("expenses.html", expenses=expenses)` sends Python data into the template.
- `{{ value }}` prints a value.
- `{% for x in items %} ... {% endfor %}` and `{% if ... %} ... {% endif %}` add logic.
- `{% extends "base.html" %}` and `{% block content %}` let every page share one layout (nav bar, Bootstrap link, and so on).
- To add Bootstrap, paste the CSS `<link>` tag from https://getbootstrap.com (Docs, then Introduction, then Quick start) into `base.html`.

**Exercise:** Build an `/expenses` page from a hard-coded list of dicts. Each dict has `date`, `description`, `category`, and `amount`. The page should include:
- an HTML `<table>` with one row per expense, built with a `for` loop
- a total row at the bottom
- amounts over $100 highlighted, using `{% if %}` and a Bootstrap class like `table-warning`
- a `base.html` layout with a page title and a simple nav bar, which `expenses.html` extends

**If it works:** You see a styled Bootstrap table with your sample expenses and a total. If you view the page source (**Cmd+Option+U**), it's plain HTML with no `{{ }}` left, because Jinja filled everything in on the server.

**Check questions:**
- What's the difference between `{{ }}` and `{% %}`?
- How does data get from your Python function into the template?
- What problem do `extends` and `block` solve?

---

## Lesson 3: Forms

**Folder:** `learning/03_forms/` (start by copying your Lesson 2 code)

**Idea:** An HTML form lets the user send data to your Python code. Browsers make two main kinds of requests:
- **GET** means "show me a page". Clicking a link sends a GET.
- **POST** means "here is some data". Submitting a form sends a POST.

One route can handle both.

**Analogy:** A bank deposit slip. You fill in labeled boxes (inputs with `name=` attributes) and hand the slip to the teller (POST to a route). The teller reads each box by its label (`request.form["amount"]`).

**Key pieces:**
- `<form method="post">` contains `<input name="...">`, `<select name="...">`, and a submit `<button>`.
- `@app.route("/add", methods=["GET", "POST"])` accepts both kinds of request.
- `request.method` tells you which kind came in.
- `request.form["amount"]` reads a field. Form values always arrive as **text**, so convert them with `float(...)`.
- `redirect(url_for("expenses"))` sends the browser to another page after saving. This is called the **Post/Redirect/Get** pattern, and it stops a page refresh from submitting the form twice.

**Exercise:** Add an `/add` page with a form for description, category (a dropdown), amount, and date. On submit, append the new expense to your Python list and redirect to `/expenses`. Add a link to `/add` in your nav bar.
- *Bonus:* if the amount is empty or not a number, show the form again with an error message instead of crashing.

**If it works:** You submit the form and land on the expenses table, where your new row appears. If you restart the server, the new rows are gone. That's expected, because the list only lives in memory. Lesson 4 fixes this.

**Check questions:**
- What's the difference between GET and POST? Which one does the browser use when you click a normal link?
- What connects an `<input>` in the HTML to `request.form[...]` in Python?
- Why redirect after a POST instead of just rendering the page directly?

---

## Lesson 4: Database with SQLAlchemy + SQLite

**Folder:** `learning/04_database/` (start by copying your Lesson 3 code)

**Idea:** **SQLite** is a database stored in a single file, so your data survives restarts. **SQLAlchemy** lets you work with database rows as Python objects: you define a class, and each object is one row in a table. **Flask-SQLAlchemy** connects SQLAlchemy to Flask.

**Analogy:** A filing cabinet. The model class is the blank form, which decides which boxes (columns) exist. Each object is one filled-in form (a row). `db.session` is your desk: you put forms on it with `add()` and file them into the cabinet with `commit()`.

**Key pieces:**
- Setup:
  ```python
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///learning.db"
  db = SQLAlchemy(app)
  ```
- A model is `class Expense(db.Model):` with fields like `amount = db.Column(db.Float)`. Include:
  - `id`, the primary key (a unique number for each row)
  - `user_id`, because every table with user data has one, even before logins exist (see CLAUDE.md)
- `with app.app_context(): db.create_all()` creates the table if it doesn't exist yet.
- Read all rows: `db.session.scalars(db.select(Expense)).all()`
- Save a row: `db.session.add(expense)`, then `db.session.commit()`
- Delete a row: `expense = db.get_or_404(Expense, id)`, then `db.session.delete(expense)`, then `db.session.commit()`
- Flask-SQLAlchemy puts the `.db` file inside an `instance/` folder. Git ignores that folder.

**Exercise:** Replace the Python list with an `Expense` model. The `/expenses` page should read from the database, and the `/add` form should save to it.
- *Bonus:* add a **Delete** button on each row, using a small `<form method="post">` that goes to `/delete/<id>`.

**If it works:** Add a few expenses, stop the server (Ctrl+C), and start it again. Your expenses are still there. A file appears at `learning/04_database/instance/learning.db`. *Optional:* open it with the free [DB Browser for SQLite](https://sqlitebrowser.org/) app to see your rows as a table.

**Check questions:**
- What do a model class, an object, and `db.session.commit()` each correspond to in the database?
- What happens if you `add()` but forget to `commit()`?
- Why include `user_id` now, even without logins?

---

## Getting help

- When you're stuck or finished, ask for a review of a lesson by number (for example, "review Lesson 2"). You'll get an explanation of what caused any error, not just the fix.
- Commit to Git after each lesson works.
- Once Lesson 4 works, you've built a tiny version of Phase 1. Then you can update CLAUDE.md's status and start the real app.
