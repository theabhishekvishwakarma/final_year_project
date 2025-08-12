from flask import Flask, render_template, request, redirect, url_for, session, flash
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "abhisehek123456789"  # Change this to a secure key

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")  # Replace with your JSON key file
firebase_admin.initialize_app(cred)

# Firestore database instance
db = firestore.client()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/dash-board.html')
def dashboard():
    if 'user' in session:
        user_id = session['user']
        user_doc = db.collection('users').document(user_id).get()
        user_data = user_doc.to_dict() if user_doc.exists else None
        return render_template('dash-board.html', user=user_data)
    flash("Please log in first.", "warning")
    return redirect(url_for('login'))

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.get_user_by_email(email)
            session['user'] = user.uid
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        except:
            flash("Login failed! Check credentials.", "danger")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.create_user(email=email, password=password)
            db.collection('users').document(user.uid).set({
                'name': name,
                'email': email
            })
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for('login'))
        except:
            flash("Error creating account. Try again.", "danger")
            return redirect(url_for('signup'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
