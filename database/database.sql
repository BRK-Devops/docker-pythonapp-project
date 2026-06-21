-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Courses Table
CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    duration VARCHAR(50),
    level VARCHAR(50),
    image_url VARCHAR(500),
    category VARCHAR(100),
    is_borrowed BOOLEAN DEFAULT FALSE,
    borrowed_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Borrowed Courses Table
CREATE TABLE IF NOT EXISTS borrowed_courses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    course_id INTEGER NOT NULL REFERENCES courses(id),
    borrowed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    returned_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'borrowed',
    due_date TIMESTAMP,
    UNIQUE(user_id, course_id, status)
);

-- Insert Default Courses
INSERT INTO courses (name, description, duration, level, category) VALUES
('DevOps Multi-Cloud (AWS & Azure)', 
 'Master DevOps practices across AWS and Azure cloud platforms. Learn CI/CD, infrastructure as code, and cloud architecture.',
 '8 Weeks', 'Intermediate', 'Cloud Computing'),
 
('Data Analytics', 
 'Learn data analysis techniques, statistics, and visualization tools to extract insights from complex datasets.',
 '6 Weeks', 'Beginner', 'Data Science'),
 
('Data Engineering', 
 'Build scalable data pipelines, ETL processes, and data warehouses for enterprise-grade data solutions.',
 '10 Weeks', 'Advanced', 'Data Science'),
 
('Generative AI (Gen AI)', 
 'Explore large language models, transformers, and AI-powered content generation techniques.',
 '6 Weeks', 'Intermediate', 'Artificial Intelligence'),
 
('Prompt Engineering', 
 'Master the art of crafting effective prompts for AI models to get optimal results in various applications.',
 '4 Weeks', 'Beginner', 'Artificial Intelligence'),
 
('JAVA Fullstack', 
 'Build complete web applications using Java, Spring Boot, and modern frontend frameworks.',
 '10 Weeks', 'Intermediate', 'Web Development'),
 
('Python Fullstack', 
 'Develop full-stack web applications using Python, Django/Flask, and frontend technologies.',
 '8 Weeks', 'Intermediate', 'Web Development'),
 
('SQL (Basics to Professional)', 
 'Complete SQL course from basic queries to advanced database management and optimization.',
 '6 Weeks', 'Beginner to Advanced', 'Database')
ON CONFLICT (name) DO NOTHING;
