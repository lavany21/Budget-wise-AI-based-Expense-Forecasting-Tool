from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Transaction
from datetime import datetime
import re
import pandas as pd
from datetime import timedelta
from categorizer import categorize_transaction
from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies
)
def generate_category_summary(expenses):

    data = [{
        "amount": e.amount,
        "category": e.category,
        "type": e.type,
        "date": e.date
    } for e in expenses]

    df = pd.DataFrame(data)

    if df.empty:
     return {}, {}, {"income": 0, "expense": 0}

    # Spending by category
    category_summary = df[df["type"] == "expense"].groupby("category")["amount"].sum().to_dict()

    # Monthly spending
    df["date"] = pd.to_datetime(df["date"])

    monthly_summary = (
       df.groupby(df["date"].dt.to_period("M"))["amount"]
       .sum()
       .to_dict()
)

# convert Period keys to string
    monthly_summary = {str(k): float(v) for k, v in monthly_summary.items()}

    income_total = df[df["type"] == "income"]["amount"].sum()
    expense_total = df[df["type"] == "expense"]["amount"].sum()

    income_vs_expense = {
        "income": float(income_total),
        "expense": float(expense_total)
    }

    return category_summary, monthly_summary, income_vs_expense
app = Flask(__name__)

# REQUIRED FOR FLASH + SESSION
app.config["SECRET_KEY"] = "budgetwise_super_secret_key_2026"

app.config["JWT_SECRET_KEY"] = "super-secret-key"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
jwt = JWTManager(app)
db.init_app(app)

# -----------------------
# HOME
# -----------------------

@app.route("/")
def home():
    return render_template("index.html")
# -----------------------
# REGISTER
# -----------------------
@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    email = request.form.get("email").lower()
    password = request.form.get("password")

    if User.query.filter_by(email=email).first():
        flash("Email already registered. Please login.")
        return redirect("/")

    if len(password) < 8:
        flash("Password must be at least 8 characters")
        return redirect("/")

    if not re.search(r"[A-Z]", password):
        flash("Password must contain at least one uppercase letter")
        return redirect("/")

    if not re.search(r"[0-9]", password):
        flash("Password must contain at least one number")
        return redirect("/")

    if not re.search(r"[!@#$%^&*]", password):
        flash("Password must contain at least one special character")
        return redirect("/")

    hashed_password = generate_password_hash(password)

    new_user = User(
        name=name,
        email=email,
        password_hash=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()
    from flask_jwt_extended import set_access_cookies

    access_token = create_access_token(identity=str(new_user.id))

    response = redirect("/dashboard")
    set_access_cookies(response, access_token)

    return response


# -----------------------
# LOGIN
# -----------------------
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email").lower()
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        flash("Invalid credentials")
        return redirect("/")
    access_token = create_access_token(identity=str(user.id))

    response = redirect("/dashboard")
    set_access_cookies(response, access_token)

    return response
# -----------------------
@app.route("/add_expense", methods=["POST"])
@jwt_required()
def add_expense():

    user_id = int(get_jwt_identity())

    amount = float(request.form.get("amount"))
    category = request.form.get("category")
    note = request.form.get("note") or ""

    if not category or category == "" or category == "Auto Detect":
     category = categorize_transaction(note)

    date_str = request.form.get("date")
    expense_date = datetime.strptime(date_str, "%Y-%m-%d")

    type_value = request.form.get("type")

    if type_value not in ["income", "expense"]:
        flash("Invalid transaction type")
        return redirect("/dashboard")

    new_expense = Transaction(
        amount=amount,
        category=category,
        note=note,
        date=expense_date,
        user_id=user_id,
        type=type_value
    )

    db.session.add(new_expense)
    db.session.commit()

    return redirect("/dashboard")


# -----------------------
# LOGOUT
# -----------------------
@app.route("/logout")
def logout():
    response = redirect("/")
    unset_jwt_cookies(response)
    return response

# -----------------------
# COMPLETE PROFILE
# -----------------------
@app.route("/save_profile", methods=["POST"])
@jwt_required()
def save_profile():
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)

    user.age = int(request.form.get("age"))
    user.gender = request.form.get("gender")
    user.profession = request.form.get("profession")

    if user.profession in ["Student", "Unemployed"]:
        user.income_type = "Pocket Money"
    else:
        user.income_type = "Salary"

    user.budget_cycle_start = int(request.form.get("budget_cycle_start"))
    user.monthly_income = float(request.form.get("monthly_income"))

    user.budget_start_date = datetime.strptime(
        request.form.get("budget_start"),
        "%Y-%m-%d"
    )

    user.budget_fixed = request.form.get("budget_fixed") == "yes"

    if user.budget_fixed:
        user.budget_edit_limit = 0
    else:
        user.budget_edit_limit = int(request.form.get("edit_limit") or 0)
    categories = request.form.getlist("categories")
    user.preferred_categories = ",".join(categories)

    user.profile_completed = True

    db.session.commit()

    return redirect("/dashboard")
# -----------------------
# EDIT PROFILE PAGE
# -----------------------
# -----------------------
# EDIT PROFILE PAGE
# -----------------------
@app.route("/edit_profile")
@jwt_required()
def edit_profile():
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)

    if not user:
        return redirect("/")

    return render_template("edit_profile.html", user=user)


# -----------------------
# RESET PASSWORD PAGE
# -----------------------
@app.route("/reset_password")
@jwt_required()
def reset_password():
    return render_template("reset_password.html")


# -----------------------
# SETTINGS PAGE
# -----------------------
@app.route("/settings")
@jwt_required()
def settings():
    return render_template("settings.html")


# -----------------------
# BUDGET HISTORY PAGE
@app.route("/profile")
@jwt_required()
def profile():
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)

    if not user:
        return redirect("/")

    return render_template("profile.html", user=user)

from collections import defaultdict

@app.route("/history")
@jwt_required()
def history():

    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)

    selected_month = request.args.get("month")

    query = Transaction.query.filter_by(user_id=user.id)

    if selected_month:
        year, month = map(int, selected_month.split("-"))
        query = query.filter(
            db.extract("year", Transaction.date) == year,
            db.extract("month", Transaction.date) == month
        )

    expenses = query.order_by(Transaction.date.desc()).all()

    total_spent = sum(e.amount for e in expenses)

    monthly_budget = user.monthly_budget or 0
    remaining = monthly_budget - total_spent

    category_summary, monthly_summary, income_vs_expense = generate_category_summary(expenses)

    return render_template(
        "history.html",
        user=user,
        expenses=expenses,
        monthly_budget=monthly_budget,
        total_spent=total_spent,
        remaining=remaining,
        category_summary=category_summary,
        selected_month=selected_month
    )
@app.route("/save_budget", methods=["POST"])
@jwt_required()
def save_budget():
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    user.savings_goal = float(request.form.get("savings_goal") or 0)
    if not user:
        return redirect("/")

    budget = float(request.form.get("monthly_budget") or 0)

    if budget < 0:
        flash("Budget cannot be negative")
        return redirect("/dashboard")

    user.monthly_budget = budget
    db.session.commit()

    return redirect("/dashboard")
@app.route("/delete_expense/<int:expense_id>", methods=["POST"])
@jwt_required()
def delete_expense(expense_id):

    user_id = int(get_jwt_identity())
    expense = Transaction.query.get_or_404(expense_id)

    if expense.user_id != user_id:
        return redirect("/dashboard")

    db.session.delete(expense)
    db.session.commit()

    return redirect("/dashboard")
@app.route("/edit_expense/<int:expense_id>")
@jwt_required()
def edit_expense(expense_id):
    user_id = int(get_jwt_identity())
    expense = Transaction.query.get_or_404(expense_id)

    if expense.user_id != user_id:
     return redirect("/dashboard")

    return render_template("edit_expense.html", expense=expense)

@app.route("/update_expense/<int:expense_id>", methods=["POST"])
@jwt_required()
def update_expense(expense_id):
    user_id = int(get_jwt_identity())
    expense = Transaction.query.get_or_404(expense_id)

    if expense.user_id != user_id:
        return redirect("/dashboard")

    expense.amount = float(request.form.get("amount"))
    expense.category = request.form.get("category")
    expense.note = request.form.get("note")
    expense.date = datetime.strptime(
        request.form.get("date"),
        "%Y-%m-%d"
    )

    db.session.commit()

    return redirect("/dashboard")
@app.route("/dashboard")
@jwt_required()
def dashboard():

    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)

    expenses = Transaction.query.filter_by(
        user_id=user.id
    ).order_by(Transaction.date.desc()).all()

    category_summary, monthly_summary, income_vs_expense = generate_category_summary(expenses)

    monthly_budget = user.monthly_budget or 0
    total_expense = income_vs_expense.get("expense", 0)

    remaining = monthly_budget - total_expense

    return render_template(
    "dashboard.html",
    user=user,
    expenses=expenses,
    total_spent=total_expense,
    monthly_budget=monthly_budget,
    remaining=remaining,
    category_summary=category_summary,
    monthly_summary=monthly_summary,
    income_vs_expense=income_vs_expense
)
# -----------------------
# RUN
# -----------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
