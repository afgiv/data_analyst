import os
from flask import Flask, redirect, render_template, request, url_for
import smtplib
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

EMAIL_ADDRESS = os.environ.get("EMAIL")
PASSKEY = os.environ.get("PASSKEY")

@app.route("/")
def index():
    # Look for ?msg_sent=true in the URL query string
    msg_sent = request.args.get("msg_sent") == "True"
    return render_template("index.html", msg_sent=msg_sent)

@app.route("/contact", methods=["GET", "POST"])
def contact():
        if request.method == "POST":
            data = request.form
            name = data.get("name")
            email = data.get("email")
            package = data.get("package")
            business = data.get("business")
            file = data.get("file")
            message = data.get("message")
            send(name, email, package, business, file, message)
            return redirect(url_for("index", msg_sent=True))
        return render_template("index.html", msg_sent=False)

def send(name, email, package, business, file, message):
    email_message = f"Subject: New Contact Form Submission\n\nName: {name}\nEmail: {email}\nPackage: {package}\nBusiness: {business}\nFile: {file}\nMessage: {message}"
    try:
        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls()
        connection.login(EMAIL_ADDRESS, PASSKEY)
        connection.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, email_message)
        connection.close()
    except Exception as e:
        print(f"Error occurred while sending email: {e}")



if __name__ == "__main__":
    app.run(debug=True)