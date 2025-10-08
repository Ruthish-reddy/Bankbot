from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import spacy
nlp = spacy.load("bank_nlu_model")

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "replace_this_secret")

VALID_USERNAME = "Ruthish"
VALID_PASSWORD = "qwe@123"

@app.route("/")
def index():
    if session.get("logged_in"):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials. Use provided username & password.", "danger")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session.get("username"))

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    
    reply = None
    if request.method == "POST":
        user_msg = request.form.get("message", "")
        doc = nlp(user_msg)

        if "textcat" in nlp.pipe_names:
            cats = doc.cats
            intent = max(cats, key=cats.get)
        else:
            intent = "unknown"

        if intent in ("check_balance", "balance"):
            reply = "Your savings account balance is ₹50,000."

        elif intent in ("transactions", "transaction_inquiry"):
            reply = "Here are your recent transactions: Deposit ₹5000, Withdrawal ₹2000."

        elif intent in ("branch_locator", "branch_info"):
            reply = "Our nearest branch is in Bengaluru, open 9 AM – 4 PM."

        elif intent in ("loan_info", "loan_inquiry"):
            reply = "We offer personal, home, and auto loans."
            
        elif intent in ("Branches","Branch"):
            reply = "Our branches are located in Bengaluru, Mumbai, Delhi, Hyderabad, and Chennai."

        elif intent in ("greet",):
            reply = "Hello! How can I help you today?"

        elif intent in ("thanks",):
            reply = "You’re welcome! Anything else I can do?"

        elif intent in ("goodbye",):
            reply = "Goodbye! Have a great day."

        else:
            reply = "Sorry, I didn’t understand that. Please ask about balances, transactions or branches."
    
    return render_template("chat.html", reply=reply)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
