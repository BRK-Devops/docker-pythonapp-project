# 📚 CourseHub → LearnWithUs | Python DevOps Project

> A full-stack Python web application deployed using a production-grade DevOps pipeline with Docker Swarm, Jenkins CI/CD, SonarQube code quality analysis, Trivy image scanning, and PostgreSQL — iteratively evolved from **v1 (CourseHub)** to **v2 (LearnWithUs)**.

---

## 🏗️ Architecture Overview

```
GitHub → Jenkins CI/CD → SonarQube (QA) → Docker Build → Trivy Scan → Docker Hub → Docker Stack Deploy (Prod EC2)
```

**Microservices (Docker Services):**
- `auth-img` — User authentication service
- `borrow-img` — Course borrowing/returning logic
- `courselist-img` — Course listing service
- `database-img` — PostgreSQL database container
- `frontend-img` — Flask/HTML frontend

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python (Flask/Django) |
| **Database** | PostgreSQL 15 |
| **Containerization** | Docker, Docker Swarm (Stack) |
| **CI/CD** | Jenkins (Declarative Pipeline) |
| **Code Quality** | SonarQube |
| **Image Security** | Trivy |
| **Registry** | Docker Hub (`brkdockerhub/coursesite`) |
| **Infrastructure** | AWS EC2 (us-east-1) |
| **Orchestration** | Docker Stack (`compose.yml`) |

---

## 📊 Real Metrics Achieved

| Metric | Value |
|---|---|
| **SonarQube Quality Gate** | ✅ Passed — All conditions met |
| **Bugs** | 0 |
| **Vulnerabilities** | 0 |
| **Code Smells** | 4 |
| **Technical Debt** | 22 min |
| **Security Hotspots** | 18 (flagged for review) |
| **Lines to Cover** | 305 |
| **Total Lines** | 900 |
| **Docker Images Built & Pushed** | 5 images |
| **Docker Hub Repo Size** | 193.1 MB |
| **Total Courses Seeded** | 8 |
| **DB Tables** | `users`, `courses`, `borrowed_courses` |
| **Users in DB** | 1 (rohit — password hashed with PBKDF2:SHA256:600000 rounds) |

---

## 🔄 CI/CD Pipeline Stages (Jenkins)

```groovy
pipeline {
  agent { node { label 'prod' } }
  stages {
    stage("code")                    // Git clone from GitHub (main branch)
    stage("CQA with sonarqube")      // Static analysis via SonarQube scanner
    stage("Image build - Docker")    // Build 5 microservice images
    stage("Image Scan using Trivy")  // Vulnerability scan all images
    stage("Image Push to Registry")  // Push to Docker Hub (brkdockerhub/coursesite)
    stage("deployment using Stack")  // docker stack deploy -c compose.yml courselist
  }
}
```

---

## 🚀 Project Versions

### v1 — CourseHub (`54.145.63.245:5000`)

Initial release with core borrowing functionality.

#### 📸 Screenshots

**Login Page**
> 📎 `loginpage-coursehub.png` already uploaded ✅

![CourseHub - Login](loginpage-coursehub.png)

---

**Dashboard / Homepage**
> 📎 `homepage-coursehub.png` already uploaded ✅

![CourseHub - Dashboard](homepage-coursehub.png)

---

**Available Courses Page**
> 📎 `courses-coursehub.png` already uploaded ✅

![CourseHub - Available Courses](courses-coursehub.png)

---

**My Borrowed Courses**
> 📎 `borrowedcourses-coursehub.png` already uploaded ✅

![CourseHub - Borrowed Courses](borrowedcourses-coursehub.png)

---

**PostgreSQL — Database Tables**
> 📎 `db-2.png` already uploaded ✅

![DB - Database Tables](db-2.png)

#### v1 Dashboard Stats
- Total Courses: **8**
- Borrowed: **3**
- Available: **5**

---

### v2 — LearnWithUs (`52.23.201.97:5000`)

Rebranded and improved version with updated UI and shared borrowing state visible to all users.

#### Key Changes from v1 → v2
- Application title changed: `CourseHub` → `LearnWithUs`
- Courses already borrowed by a user now show **"Borrowed by someone"** badge to other users (real-time availability)
- Dashboard resets borrowed count per user session (fresh DB state)
- Improved card layout and spacing

#### 📸 Screenshots

**Login Page**
> 📎 `loginpage-learnwithus.png` already uploaded ✅

![LearnWithUs - Login](loginpage-learnwithus.png)

---

**Dashboard / Homepage**
> 📎 `homepage-learnwithus.png` already uploaded ✅

![LearnWithUs - Dashboard](homepage-learnwithus.png)

---

**My Borrowed Courses**
> 📎 `borrowedcourses-learnwithus.png` already uploaded ✅

![LearnWithUs - Borrowed](borrowedcourses-learnwithus.png)

---

**Available Courses (with "Borrowed by someone" badges)**
> 📎 `availblecourses-learnwithus.png` already uploaded ✅

![LearnWithUs - Available Courses with badges](availblecourses-learnwithus.png)

#### v2 Dashboard Stats
- Total Courses: **8**
- Borrowed: **0** (fresh state)
- Available: **8**

---

## 🔍 SonarQube Code Quality Report

> 📎 `sonarqube.png` already uploaded ✅

![SonarQube - Quality Gate Passed](sonarqube.png)

- **Quality Gate: PASSED ✅**
- Project: `myproject` | Branch: `main`
- Reliability: **A** | Security: **A** | Maintainability: **A**
- Security Review: **E** (18 hotspots unreviewed — flagged for future sprint)
- 0 Bugs | 0 Vulnerabilities | 4 Code Smells | 22 min Debt

---

## 🐳 Docker Hub Registry

> 📎 `dockerhub.png` already uploaded ✅

![Docker Hub - coursesite repository](dockerhub.png)

**Repository:** [`brkdockerhub/coursesite`](https://hub.docker.com/repository/docker/brkdockerhub/coursesite/general)

| Tag | Type | Last Pushed |
|---|---|---|
| `frontend-img` | Image (Linux) | < 1 day |
| `database-img` | Image (Linux) | < 1 day |
| `courselist-img` | Image (Linux) | < 1 day |
| `borrow-img` | Image (Linux) | < 1 day |
| `auth-img` | Image (Linux) | < 1 day |

**Total pushes:** 40 | **Repo size:** 193.1 MB

---

## 🧾 Jenkins Pipeline Script

> 📎 `pipelinescript-1.png` already uploaded ✅

![Jenkins Pipeline - Part 1](pipelinescript-1.png)

> 📎 `pipelinescript-2.png` already uploaded ✅

![Jenkins Pipeline - Part 2](pipelinescript-2.png)

```groovy
pipeline {
    agent {
        node {
            label "prod"
        }
    }
    stages {
        stage("code") {
            steps {
                git branch: 'main', url: 'https://github.com/BRK-Devops/docker-pythonapp-project.git'
            }
        }
        stage("CQA with sonarqube") {
            environment {
                scannerHome = tool name: "mysonar"
            }
            steps {
                withSonarQubeEnv("mysonar") {
                    sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=myproject"
                }
            }
        }
        stage("Image build - Docker") {
            steps {
                sh '''
                docker build -t brkdockerhub/coursesite:auth-img auth
                docker build -t brkdockerhub/coursesite:borrow-img borrow
                docker build -t brkdockerhub/coursesite:courselist-img courselist
                docker build -t brkdockerhub/coursesite:database-img database
                docker build -t brkdockerhub/coursesite:frontend-img .
                '''
            }
        }
        stage("Image Scan using Trivy") {
            steps {
                sh '''
                trivy image brkdockerhub/coursesite:auth-img
                trivy image brkdockerhub/coursesite:borrow-img
                trivy image brkdockerhub/coursesite:courselist-img
                trivy image brkdockerhub/coursesite:database-img
                trivy image brkdockerhub/coursesite:frontend-img
                '''
            }
        }
        stage("Image Push to Registry") {
            steps {
                withDockerRegistry(credentialsId: '1543663c-f9c5-426c-9f86-93cb36d5210c') {
                    sh '''
                    docker push brkdockerhub/coursesite:auth-img
                    docker push brkdockerhub/coursesite:borrow-img
                    docker push brkdockerhub/coursesite:courselist-img
                    docker push brkdockerhub/coursesite:database-img
                    docker push brkdockerhub/coursesite:frontend-img
                    '''
                }
            }
        }
        stage("deployment using Stack") {
            steps {
                sh "docker stack deploy -c compose.yml courselist"
            }
        }
    }
}
```

---

## 🗄️ Database Schema (PostgreSQL)

```sql
-- Users table
SELECT * FROM users;
-- id | username | email | password_hash | created_at | is_active

-- Courses table
SELECT * FROM courses;
-- id | name | description | duration | level | image_url | category | is_borrowed | borrowed_by | created_at

-- Borrowed courses table
SELECT * FROM borrowed_courses;
-- id | user_id | course_id | borrowed_at | returned_at | status | due_date
```

**Sample data verified via `docker exec` into the database container:**
- User `rohit` — password hashed with PBKDF2:SHA256 (600,000 rounds)
- 8 seeded courses across categories: Cloud Computing, Data Science, AI, Web Development, Database
- Borrow records with `due_date` auto-set to 30 days from borrow time

---

## 📂 Project Structure

```
docker-pythonapp-project/
├── auth/               # Authentication microservice
├── borrow/             # Borrow/return microservice
├── courselist/         # Course listing microservice
├── database/           # PostgreSQL container config & seed data
├── compose.yml         # Docker Stack compose file
├── Dockerfile          # Frontend image build
└── sonar-project.properties
```

---

## ▶️ How to Run Locally

```bash
# Clone the repository
git clone https://github.com/BRK-Devops/docker-pythonapp-project.git
cd docker-pythonapp-project

# Initialize Docker Swarm (if not already)
docker swarm init

# Deploy the stack
docker stack deploy -c compose.yml courselist

# Access the app
open http://localhost:5000
```

---

## 🧠 Experience & Skills Gained

### DevOps & CI/CD
- Built a **multi-stage Jenkins declarative pipeline** from scratch covering code checkout, QA, build, scan, push, and deploy
- Configured **SonarQube** with a custom project key and integrated it as a Jenkins environment tool (`withSonarQubeEnv`)
- Used **Trivy** to perform container image vulnerability scanning on all 5 microservice images before pushing to registry
- Managed **Docker Hub credentials** securely in Jenkins using `withDockerRegistry` and credential IDs

### Docker & Orchestration
- Designed a **microservices architecture** split across 5 Docker images (auth, borrow, courselist, database, frontend)
- Used **Docker Stack** (`docker stack deploy`) for production-grade Swarm deployment with a `compose.yml`
- Understood Docker **service naming, image tagging conventions**, and inter-service networking in Swarm mode

### Application Development
- Built a Python web app with **user authentication**, **session management**, **course borrowing/returning** logic
- Designed and queried a **PostgreSQL relational schema** with `users`, `courses`, and `borrowed_courses` tables
- Validated DB state directly via `docker exec ... psql` — confirming live data integrity end to end
- Implemented **real-time availability tracking** — courses borrowed by one user show as unavailable to others (v2 feature)

### Infrastructure & AWS
- Deployed on **AWS EC2 (us-east-1)** — managed two separate EC2 instances for v1 and v2 environments
- Understood **security group configuration** for exposing ports (5000 for app, 9000 for SonarQube, 8080 for Jenkins)

### Iterative Development
- Evolved the project across **two versions** (v1 → v2) with a rebrand, UI improvements, and a new shared-borrowing feature — demonstrating real-world iterative delivery

---

## 📸 Screenshot Upload Status

All images are uploaded to the **root** of this repo and are now live ✅

| # | Filename | Section | Status |
|---|---|---|---|
| 1 | `loginpage-coursehub.png` | v1 — CourseHub Login | ✅ Uploaded |
| 2 | `homepage-coursehub.png` | v1 — CourseHub Dashboard | ✅ Uploaded |
| 3 | `courses-coursehub.png` | v1 — Available Courses | ✅ Uploaded |
| 4 | `borrowedcourses-coursehub.png` | v1 — Borrowed Courses | ✅ Uploaded |
| 5 | `db-2.png` | PostgreSQL — Database Tables | ✅ Uploaded |
| 6 | `loginpage-learnwithus.png` | v2 — LearnWithUs Login | ✅ Uploaded |
| 7 | `homepage-learnwithus.png` | v2 — LearnWithUs Dashboard | ✅ Uploaded |
| 8 | `borrowedcourses-learnwithus.png` | v2 — Borrowed Courses | ✅ Uploaded |
| 9 | `availblecourses-learnwithus.png` | v2 — Available Courses with badges | ✅ Uploaded |
| 10 | `sonarqube.png` | SonarQube Quality Gate report | ✅ Uploaded |
| 11 | `dockerhub.png` | Docker Hub — 5 image tags | ✅ Uploaded |
| 12 | `pipelinescript-1.png` | Jenkins pipeline script (top) | ✅ Uploaded |
| 13 | `pipelinescript-2.png` | Jenkins pipeline script (bottom) | ✅ Uploaded |

---

## 🔗 Links

- **Docker Hub:** https://hub.docker.com/repository/docker/brkdockerhub/coursesite/general
- **GitHub Repo:** https://github.com/BRK-Devops/docker-pythonapp-project

---

## 👤 Author

**Rohit** | DevOps Engineer  
Built with 🐍 Python · 🐳 Docker · ⚙️ Jenkins · 🔍 SonarQube · 🛡️ Trivy · ☁️ AWS EC2
