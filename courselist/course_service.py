from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 
    'postgresql://course_user:course_pass@db:5432/course_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Course Model
class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50))
    level = db.Column(db.String(50))
    image_url = db.Column(db.String(500))
    category = db.Column(db.String(100))
    is_borrowed = db.Column(db.Boolean, default=False)
    borrowed_by = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

# Initialize courses
def init_courses():
    courses_data = [
        {
            'name': 'DevOps Multi-Cloud (AWS & Azure)',
            'description': 'Master DevOps practices across AWS and Azure cloud platforms. Learn CI/CD pipelines, Infrastructure as Code (Terraform), Kubernetes, Docker, and cloud architecture. Hands-on projects with real-world scenarios.',
            'duration': '8 Weeks',
            'level': 'Intermediate',
            'image_url': 'devops.jpg',
            'category': 'Cloud Computing'
        },
        {
            'name': 'Data Analytics',
            'description': 'Learn data analysis techniques, statistics, and visualization tools. Master Python (Pandas, NumPy), SQL, Power BI, and Tableau to extract insights from complex datasets and make data-driven decisions.',
            'duration': '6 Weeks',
            'level': 'Beginner',
            'image_url': 'data-analytics.jpg',
            'category': 'Data Science'
        },
        {
            'name': 'Data Engineering',
            'description': 'Build scalable data pipelines, ETL processes, and data warehouses. Learn Apache Spark, Kafka, Airflow, and cloud-based data solutions for enterprise-grade data processing and storage.',
            'duration': '10 Weeks',
            'level': 'Advanced',
            'image_url': 'data-engineering.jpg',
            'category': 'Data Science'
        },
        {
            'name': 'Generative AI (Gen AI)',
            'description': 'Explore large language models (LLMs), transformers, and AI-powered content generation. Learn RAG, fine-tuning, prompt engineering, and building AI applications with OpenAI, LangChain, and Hugging Face.',
            'duration': '6 Weeks',
            'level': 'Intermediate',
            'image_url': 'gen-ai.jpg',
            'category': 'Artificial Intelligence'
        },
        {
            'name': 'Prompt Engineering',
            'description': 'Master the art of crafting effective prompts for AI models to get optimal results. Learn techniques for ChatGPT, Claude, and other LLMs. Build advanced AI applications with proper prompt design and optimization.',
            'duration': '4 Weeks',
            'level': 'Beginner',
            'image_url': 'prompt-engineering.jpg',
            'category': 'Artificial Intelligence'
        },
        {
            'name': 'JAVA Fullstack',
            'description': 'Build complete web applications using Java, Spring Boot, Hibernate, and modern frontend frameworks like Angular/React. Master REST APIs, Microservices, and enterprise Java development.',
            'duration': '10 Weeks',
            'level': 'Intermediate',
            'image_url': 'java-fullstack.jpg',
            'category': 'Web Development'
        },
        {
            'name': 'Python Fullstack',
            'description': 'Develop full-stack web applications using Python, Django/Flask, PostgreSQL, and frontend technologies (HTML, CSS, JavaScript, React). Learn API development, authentication, and deployment.',
            'duration': '8 Weeks',
            'level': 'Intermediate',
            'image_url': 'python-fullstack.jpg',
            'category': 'Web Development'
        },
        {
            'name': 'SQL (Basics to Professional)',
            'description': 'Complete SQL course from basic queries to advanced database management. Master joins, subqueries, window functions, performance optimization, and database design for real-world applications.',
            'duration': '6 Weeks',
            'level': 'Beginner to Advanced',
            'image_url': 'sql.jpg',
            'category': 'Database'
        }
    ]
    
    for data in courses_data:
        if not Course.query.filter_by(name=data['name']).first():
            course = Course(**data)
            db.session.add(course)
    db.session.commit()
    print("✅ 8 Courses initialized successfully!")

@app.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description[:200] + '...' if len(c.description) > 200 else c.description,
        'duration': c.duration,
        'level': c.level,
        'category': c.category,
        'is_borrowed': c.is_borrowed,
        'borrowed_by': c.borrowed_by
    } for c in courses])

@app.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    return jsonify({
        'id': course.id,
        'name': course.name,
        'description': course.description,
        'duration': course.duration,
        'level': course.level,
        'category': course.category,
        'is_borrowed': course.is_borrowed
    })

@app.route('/courses/<int:course_id>/borrow', methods=['PUT'])
def borrow_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    data = request.json
    user_id = data.get('user_id')
    
    if course.is_borrowed:
        return jsonify({'error': 'Course already borrowed'}), 400
    
    course.is_borrowed = True
    course.borrowed_by = user_id
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Course borrowed successfully',
        'course': {
            'id': course.id,
            'name': course.name,
            'is_borrowed': course.is_borrowed,
            'borrowed_by': course.borrowed_by
        }
    })

@app.route('/courses/<int:course_id>/return', methods=['PUT'])
def return_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    if not course.is_borrowed:
        return jsonify({'error': 'Course is not borrowed'}), 400
    
    course.is_borrowed = False
    course.borrowed_by = None
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Course returned successfully',
        'course': {
            'id': course.id,
            'name': course.name,
            'is_borrowed': course.is_borrowed
        }
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_courses()  # This will add the 8 courses
    print("🚀 Course Service running on port 5002...")
    app.run(debug=True, host='0.0.0.0', port=5002)
