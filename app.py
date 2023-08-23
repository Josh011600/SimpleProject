from flask import Flask, render_template, request, redirect, url_for
import sqlite3


from datetime import datetime

app = Flask(__name__)

'''
I need to insert here what will i display in my dashboard.
@app.route('/')
def dashboard():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)
'''

# Function to validate user credentials and return the role

def validate_user(username_or_email, password):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    # Check if the input is an email or username
    if '@' in username_or_email:  # Assuming email addresses have '@'
        query = "SELECT username, usertype FROM employees WHERE email=? AND password=?"
    else:
        query = "SELECT username, usertype FROM employees WHERE username=? AND password=?"

    cursor.execute(query, (username_or_email, password))
    user = cursor.fetchone()

    conn.close()
    
    return user if user else None


@app.route('/')
def index_page():
    return render_template('index.html')



@app.route('/index', methods=['POST'])
def index():
    username = request.form['username']
    password = request.form['password']

    user = validate_user(username, password)
    
    if user:
        username, usertype = user
          # Access 'username' at index 2
        usertype = user[1]  # Access 'role' at index 4
        if usertype == 'admin':
            # Add the logic for admin login (e.g., session management, redirect to admin dashboard)
            return render_template('admin.html', username=username, usertype=usertype)
        elif usertype == 'employee':
            # Add the logic for user login (e.g., session management, redirect to user dashboard)
            return render_template('user.html', username=username, usertype=usertype)
        
        
    # Add the logic for failed login (e.g., display an error message)
    return render_template('index.html', login_failed=True)



@app.route('/admin.html')
def admin_dashboard():

    # Add the logic for the admin dashboard here
    username = "username"  # Replace this with the actual username retrieved from the database
    return render_template('admin.html', username=username)

@app.route('/user.html')
def user_dashboard():

    # Add the logic for the user dashboard here
    username = "username"  # Replace this with the actual username retrieved from the database
    return render_template('user.html', username=username)

@app.route('/register')
def register():
    return render_template('registeruser.html')

@app.route('/register', methods=['POST'])
def register_submit():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    name = request.form['name']
    age = int(request.form['age'])
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    dateOfBirth = request.form['date_of_birth']
    # Convert the date string to a datetime object
    dateOfBirth = datetime.strptime(dateOfBirth, '%Y-%m-%d').date()

     # Check if the username or email already exists in the database
    cursor.execute("SELECT * FROM employees WHERE username = ? OR email = ?", (username, email))
    existing_user = cursor.fetchone()

    if existing_user:
        return redirect(url_for('registration_failed', reason='Username or email already exists'))
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    # Insert the data into the 'users' table
    cursor.execute("INSERT INTO employees (name, age, email, username, password, dateOfBirth, usertype) VALUES (?, ?, ?, ?, ?, ?, 'employee')",
               (name, age, email, username, password, dateOfBirth))

    conn.commit()

    return redirect(url_for('success'))

@app.route('/success')
def success():
    

    return render_template('success.html')

@app.route('/registration_failed')
def registration_failed():
    reason = request.args.get('reason', 'Unknown error')
    return render_template('registration_failed.html', reason=reason)


if __name__ == '__main__':
    app.run(debug=True)


