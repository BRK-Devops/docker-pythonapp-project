from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import requests
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-12345')

# Service URLs
AUTH_SERVICE = os.environ.get('AUTH_SERVICE', 'http://auth:5001')
COURSE_SERVICE = os.environ.get('COURSE_SERVICE', 'http://courselist:5002')
BORROW_SERVICE = os.environ.get('BORROW_SERVICE', 'http://borrow:5003')

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        response = requests.post(
            f'{AUTH_SERVICE}/auth/login',
            json={'username': username, 'password': password}
        )
        
        if response.status_code == 200:
            data = response.json()
            session['user_id'] = data['user_id']
            session['username'] = data['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('signup.html')
        
        response = requests.post(
            f'{AUTH_SERVICE}/auth/signup',
            json={'username': username, 'email': email, 'password': password}
        )
        
        if response.status_code == 201:
            flash('Account created! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash(response.json().get('message', 'Signup failed'), 'danger')
    
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get courses
    courses_response = requests.get(f'{COURSE_SERVICE}/courses')
    courses = courses_response.json() if courses_response.status_code == 200 else []
    
    # Get borrowed courses
    borrow_response = requests.get(f'{BORROW_SERVICE}/borrow/user/{session["user_id"]}')
    borrowed = borrow_response.json() if borrow_response.status_code == 200 else []
    
    return render_template('dashboard.html', 
                         username=session['username'],
                         total_courses=len(courses),
                         borrowed_count=len(borrowed))

@app.route('/courses')
def courses():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    response = requests.get(f'{COURSE_SERVICE}/courses')
    courses = response.json() if response.status_code == 200 else []
    
    return render_template('courses.html', courses=courses)

@app.route('/borrow', methods=['POST'])
def borrow_course():
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401
    
    course_id = request.form.get('course_id')
    
    # Borrow in course service
    course_response = requests.put(
        f'{COURSE_SERVICE}/courses/{course_id}/borrow',
        json={'user_id': session['user_id']}
    )
    
    if course_response.status_code != 200:
        flash('Course not available for borrowing', 'danger')
        return redirect(url_for('courses'))
    
    # Create borrow record
    borrow_response = requests.post(
        f'{BORROW_SERVICE}/borrow',
        json={'user_id': session['user_id'], 'course_id': course_id}
    )
    
    flash('Course borrowed successfully!', 'success')
    return redirect(url_for('borrowed'))

@app.route('/return/<int:course_id>', methods=['POST'])
def return_course(course_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401
    
    # Return in course service
    course_response = requests.put(f'{COURSE_SERVICE}/courses/{course_id}/return')
    
    if course_response.status_code != 200:
        flash('Error returning course', 'danger')
        return redirect(url_for('borrowed'))
    
    # Update borrow record
    borrow_response = requests.post(
        f'{BORROW_SERVICE}/borrow/return',
        json={'user_id': session['user_id'], 'course_id': course_id}
    )
    
    flash('Course returned successfully!', 'success')
    return redirect(url_for('borrowed'))

@app.route('/borrowed')
def borrowed():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get borrowed courses
    borrow_response = requests.get(f'{BORROW_SERVICE}/borrow/user/{session["user_id"]}')
    borrowed_records = borrow_response.json() if borrow_response.status_code == 200 else []
    
    # Get course details for each borrowed course
    borrowed_courses = []
    for record in borrowed_records:
        course_response = requests.get(f'{COURSE_SERVICE}/courses/{record["course_id"]}')
        if course_response.status_code == 200:
            course_data = course_response.json()
            course_data['borrowed_at'] = record['borrowed_at']
            course_data['due_date'] = record['due_date']
            borrowed_courses.append(course_data)
    
    return render_template('borrowed.html', borrowed_courses=borrowed_courses)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
