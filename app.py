from flask import Flask, render_template, request, redirect, url_for
import requests
import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
app = Flask(__name__)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password") 
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()

        # Check user
        cur.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cur.fetchone()

        cur.close()
        conn.close() 
        if user:
            return render_template("sales.html")   # success page
        else:
            return render_template("login.html", error="Invalid credentials")
    else: 
         return render_template("login.html")





@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password") 
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()

        # Check user
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)",(username, password))

        conn.commit()
        cur.close()
        conn.close() 
        return render_template("login.html")
        
    else: 
        return render_template("register.html")
    


@app.route("/logout")
def logout():
    return render_template("login.html")

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)