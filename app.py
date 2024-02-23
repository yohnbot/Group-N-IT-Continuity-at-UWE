from flask import Flask, render_template, request
import re

app = Flask(__name__)

def is_phishing(email):
    # Check for random inputs without "@" sign
    if "@" not in email:
        return "ERROR: Random Input Detected. This may not be a valid email address."

    # Check for suspicious sender address
    sender_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    # Example suspicious domains
    suspicious_sender_domains = ["phishing.com", "scam.net", "hackers.org"]  
    sender_match = re.search(sender_pattern, email)
    if sender_match:
        sender_domain = sender_match.group().split('@')[-1]
        if sender_domain in suspicious_sender_domains:
            return True

    # Check for suspicious content
    # Example suspicious keywords
    suspicious_keywords = ["verify", "login", "password", "urgent", "account", "update"]  
    for keyword in suspicious_keywords:
        if keyword in email.lower():
            return True

    # Check for suspicious links
    link_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    links = re.findall(link_pattern, email)
    for link in links:
        if "phishing" in link or "scam" in link:
            return True

    return False
    
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form['email']
        phishing_result = is_phishing(email)
        if phishing_result == True:
            result = "WARNING: This email is most likely a phishing attempt."
        elif phishing_result == False:
            result = "This email is legitimate :)"
        else:
            result = phishing_result
        return render_template('result.html', result=result)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
