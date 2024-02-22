# Import necessary libraries
import os
from flask import Flask, request, render_template
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm

# Load and preprocess your data, train your model
spam = pd.read_csv("C:\\Users\\ellij\\Desktop\\PhishingDetector\\spam.csv")
x = spam['EmailText']
y = spam['Label']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

cv = CountVectorizer()
features = cv.fit_transform(x_train)

model = svm.SVC()
model.fit(features, y_train)

# Create Flask app
app=Flask(__name__,template_folder='templates')

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    email = request.form['email']
    features = cv.transform([email])
    prediction = model.predict(features)
    return render_template('result.html', prediction=prediction)  # A HTML page to show the result

if __name__ == '__main__':
    app.run(debug=True)

print(os.path.abspath(app.template_folder))