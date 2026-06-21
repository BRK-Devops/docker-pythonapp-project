from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime, timedelta
import os
import time
import sys

app = Flask(__name__)

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://course_user:course_pass@db:5432/course_db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

db = SQLAlchemy(app)

# Borrowed Course Model
class BorrowedCourse(db.Model):
    __tablename__ = 'borrowed_courses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    borrowed_at = db.Column(db.DateTime, server_default=db.func.now())
    returned_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='borrowed')
    due_date = db.Column(db.DateTime, nullable=True)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        # Check database connection
        db.session.execute(text('SELECT 1'))
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/borrow', methods=['POST'])
def borrow_course():
    try:
        data = request.json
        user_id = data.get('user_id')
        course_id = data.get('course_id')
        
        if not user_id or not course_id:
            return jsonify({'error': 'user_id and course_id are required'}), 400
        
        # Check if already borrowed
        existing = BorrowedCourse.query.filter_by(
            user_id=user_id,
            course_id=course_id,
            status='borrowed'
        ).first()
        
        if existing:
            return jsonify({'error': 'Course already borrowed'}), 400
        
        # Create borrow record
        borrowed = BorrowedCourse(
            user_id=user_id,
            course_id=course_id,
            due_date=datetime.utcnow() + timedelta(days=30)
        )
        db.session.add(borrowed)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Course borrowed successfully',
            'borrowed_id': borrowed.id,
            'due_date': borrowed.due_date.isoformat() if borrowed.due_date else None
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/borrow/return', methods=['POST'])
def return_course():
    try:
        data = request.json
        user_id = data.get('user_id')
        course_id = data.get('course_id')
        
        if not user_id or not course_id:
            return jsonify({'error': 'user_id and course_id are required'}), 400
        
        borrowed = BorrowedCourse.query.filter_by(
            user_id=user_id,
            course_id=course_id,
            status='borrowed'
        ).first()
        
        if not borrowed:
            return jsonify({'error': 'Course not borrowed'}), 404
        
        borrowed.status = 'returned'
        borrowed.returned_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Course returned successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/borrow/user/<int:user_id>', methods=['GET'])
def get_user_borrowed(user_id):
    try:
        borrowed = BorrowedCourse.query.filter_by(
            user_id=user_id,
            status='borrowed'
        ).all()
        
        return jsonify([{
            'id': b.id,
            'course_id': b.course_id,
            'borrowed_at': b.borrowed_at.isoformat() if b.borrowed_at else None,
            'due_date': b.due_date.isoformat() if b.due_date else None
        } for b in borrowed])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/borrow/status/<int:user_id>/<int:course_id>', methods=['GET'])
def get_borrow_status(user_id, course_id):
    try:
        borrowed = BorrowedCourse.query.filter_by(
            user_id=user_id,
            course_id=course_id,
            status='borrowed'
        ).first()
        
        return jsonify({
            'is_borrowed': borrowed is not None,
            'borrowed_id': borrowed.id if borrowed else None,
            'due_date': borrowed.due_date.isoformat() if borrowed and borrowed.due_date else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return jsonify({'service': 'Borrow Service', 'status': 'running'})

if __name__ == '__main__':
    # Wait for database to be ready
    print("⏳ Waiting for database to be ready...")
    max_retries = 10
    for attempt in range(max_retries):
        try:
            with app.app_context():
                db.create_all()
                db.session.execute(text('SELECT 1'))
            print("✅ Database connection successful!")
            break
        except Exception as e:
            print(f"⚠️ Database connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
            else:
                print("❌ Failed to connect to database after multiple attempts")
                sys.exit(1)
    
    print("🚀 Starting Borrow Service on port 5003...")
    app.run(debug=True, host='0.0.0.0', port=5003)
