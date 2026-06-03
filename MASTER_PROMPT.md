# 🎯 GBSB Digital Gurukul - Master AI System Prompt

## Project Overview

**PROJECT NAME:** GBSB Digital Gurukul AI Ecosystem

**MISSION:** एक ऐसा AI-संचालित शिक्षा प्लेटफॉर्म विकसित करना जो स्कूल प्रबंधन, ऑनलाइन शिक्षा, लाइव क्लास, AI शिक्षक, डिजिटल लाइब्रेरी, कौशल प्रशिक्षण, शोध और रोजगारोन्मुख शिक्षा को एकीकृत करे।

**CURRENT PHASE:** MVP Development (Weeks 1-12)

---

## 🎯 MVP Goals (First 3 Months)

### Core 5 Features Only:
1. **User Authentication** - Login/Registration
2. **Course Management** - Create, View, Manage Courses
3. **Live Class Studio** - Real-time Classes via Jitsi
4. **Attendance System** - QR Code + Manual Tracking
5. **AI Tutor** - Offline LLM-based Q&A

### Success Criteria:
- 1000+ users (Students/Teachers/Parents)
- 50+ courses created
- 10+ live classes per week
- 99.5% system uptime
- <3 second load time on 4G
- Works on 3-4GB RAM devices

---

## 👥 User Roles & Permissions

### 1. Student
- View courses & chapters
- Join live classes
- Take tests & submit assignments
- Ask AI Tutor questions
- View progress reports
- Download study materials

### 2. Teacher
- Create & manage courses
- Conduct live classes
- Create tests & assignments
- Mark attendance
- View student progress
- Generate reports

### 3. Parent
- View child's attendance
- Check grades & results
- View progress reports
- Communicate with teachers
- Get performance notifications

### 4. School Admin
- Manage students
- Manage teachers
- Course approval
- Fee management
- Generate school-level reports
- Dashboard & analytics

### 5. Super Admin (Optional for MVP)
- Manage all schools
- System-level analytics
- User management
- Content moderation

---

## 🛠️ Technology Stack (MVP - FREE & OPEN SOURCE)

### Frontend
```
Mobile:  Flutter
Web:     React.js + TypeScript
UI Kit:  Material Design 3
State:   Riverpod (Flutter) / Redux (React)
HTTP:    Dio (Flutter) / Axios (React)
Storage: SQLite (Offline), SharedPreferences
```

### Backend
```
Framework:    Python FastAPI
Auth:         JWT + 2FA (TOTP)
Database:     PostgreSQL (Production) / SQLite (Dev)
Cache:        Redis (Optional)
Task Queue:   Celery (Optional)
WebSocket:    FastAPI WebSockets
Validation:   Pydantic
Documentation: OpenAPI/Swagger
```

### Live Classes
```
Primary:  Jitsi Meet (Self-hosted)
Fallback: WebRTC (Direct P2P)
Chat:     WebSocket
Screen:   WebRTC Screen Capture
```

### AI & NLP
```
LLM:          Ollama (Offline) + Mistral/Llama 2
Embeddings:   HuggingFace Sentence Transformers
Vector DB:    ChromaDB (Vector Search)
Speech-to-Text: Vosk (Offline)
Text-to-Speech: Coqui TTS (Offline)
NER/Intent:   spaCy
```

### Deployment
```
Containers:   Docker
Orchestration: Docker Compose (MVP), Kubernetes (Future)
CI/CD:        GitHub Actions
Monitoring:   Prometheus + Grafana (Optional)
Logging:      ELK Stack (Optional)
```

---

## 🏗️ Architecture Design

### Backend Architecture (FastAPI)
```
┌─────────────────────────────────────────┐
│        API Gateway / Load Balancer       │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         FastAPI Application             │
├──────────────────────────────────────────┤
│  Routes Layer (User, Course, Class...)   │
├──────────────────────────────────────────┤
│  Services Layer (Business Logic)         │
├──────────────────────────────────────────┤
│  Repository Layer (Database Access)      │
├──────────────────────────────────────────┤
│  Middleware (Auth, CORS, Logging)        │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  PostgreSQL / SQLite Database            │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│  Ollama AI Service (Separate Container)  │
├──────────────────────────────────────────┤
│  - LLM Models (Mistral, Llama 2)         │
│  - ChromaDB (Vector Database)            │
│  - Embeddings Generation                 │
└──────────────────────────────────────────┘
```

### Mobile-First Approach
```
Flutter App Architecture:
├── Presentation Layer (UI Screens)
│   ├── LoginScreen
│   ├── DashboardScreen
│   ├── CourseScreen
│   ├── LiveClassScreen
│   └── AITutorScreen
├── Business Logic Layer (Services)
│   ├── AuthService
│   ├── CourseService
│   ├── ClassService
│   └── AIService
├── Data Layer
│   ├── Remote (API Client)
│   ├── Local (SQLite)
│   └── Models
└── Utils (Helpers, Constants)
```

---

## 📊 Database Schema (PostgreSQL)

### Core Tables:
```sql
-- Users Table
users (
  id, username, email, phone,
  password_hash, role, status,
  created_at, updated_at
)

-- Schools Table
schools (
  id, name, address, phone,
  email, established_year,
  admin_id, created_at
)

-- Courses Table
courses (
  id, title, description, category,
  school_id, teacher_id, syllabus,
  start_date, end_date, created_at
)

-- Chapters Table
chapters (
  id, course_id, title, content,
  order, created_at
)

-- Lessons Table
lessons (
  id, chapter_id, title, content,
  video_url, resources, order
)

-- Live Classes Table
live_classes (
  id, course_id, teacher_id,
  scheduled_at, jitsi_room_id,
  status, recording_url
)

-- Attendance Table
attendance (
  id, class_id, student_id,
  status, marked_at, qr_code
)

-- Enrollments Table
enrollments (
  id, student_id, course_id,
  enrolled_at, status
)

-- Assignments Table
assignments (
  id, course_id, title, description,
  due_date, max_marks
)

-- Submissions Table
submissions (
  id, assignment_id, student_id,
  file_url, submitted_at, marks
)
```

---

## 🌐 API Endpoints (FastAPI)

### Auth APIs
```
POST   /api/v1/auth/register       - User Registration
POST   /api/v1/auth/login          - User Login
POST   /api/v1/auth/refresh        - Refresh JWT Token
POST   /api/v1/auth/logout         - User Logout
POST   /api/v1/auth/2fa/setup      - Setup 2FA
POST   /api/v1/auth/2fa/verify     - Verify 2FA Code
```

### Course APIs
```
GET    /api/v1/courses             - List All Courses
GET    /api/v1/courses/{id}        - Get Course Details
POST   /api/v1/courses             - Create Course (Teacher)
PUT    /api/v1/courses/{id}        - Update Course (Teacher)
DELETE /api/v1/courses/{id}        - Delete Course (Teacher)
GET    /api/v1/courses/{id}/chapters - Get Chapters
```

### Live Class APIs
```
GET    /api/v1/classes             - List Classes
GET    /api/v1/classes/{id}        - Get Class Details
POST   /api/v1/classes             - Create Class (Teacher)
GET    /api/v1/classes/{id}/join   - Get Jitsi Room URL
POST   /api/v1/classes/{id}/attendance - Mark Attendance
```

### AI Tutor APIs
```
POST   /api/v1/ai/ask              - Ask Question (Text)
POST   /api/v1/ai/voice-ask        - Ask Question (Voice)
GET    /api/v1/ai/history          - Chat History
DELETE /api/v1/ai/history          - Clear History
```

### User APIs
```
GET    /api/v1/users/me            - Get Profile
PUT    /api/v1/users/me            - Update Profile
GET    /api/v1/users/progress      - Get Progress Report
```

---

## 💾 Data Models (Pydantic)

### User Schema
```python
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    phone: str
    password: str
    role: Literal["student", "teacher", "parent", "admin"]

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    totp_code: Optional[str] = None

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    role: str
    status: str
    created_at: datetime
```

### Course Schema
```python
class CourseCreate(BaseModel):
    title: str
    description: str
    category: str
    syllabus: Optional[str] = None
    start_date: date
    end_date: date

class CourseResponse(BaseModel):
    id: UUID
    title: str
    description: str
    teacher_id: UUID
    enrolled_count: int
    chapters_count: int
    created_at: datetime
```

---

## 🔐 Security Requirements

✅ **Authentication & Authorization**
- JWT Token (HS256)
- Refresh Token Rotation
- TOTP-based 2FA
- Role-Based Access Control (RBAC)
- Permission Scoping

✅ **Data Protection**
- Password Hashing (bcrypt)
- AES-256 Encryption for sensitive data
- HTTPS/TLS for all communications
- CORS Configuration
- CSRF Token Protection

✅ **API Security**
- Rate Limiting
- Input Validation & Sanitization
- SQL Injection Prevention (Parameterized Queries)
- XSS Protection
- OWASP Compliance

✅ **Audit & Monitoring**
- Audit Logs for critical actions
- API Request Logging
- Error Tracking & Monitoring
- Daily Backup
- Data Retention Policies

---

## 📱 Mobile App Features (Flutter)

### UI Screens:
1. **Splash Screen** - App Logo & Branding
2. **Login Screen** - Email/Phone + OTP
3. **Registration Screen** - Multi-step registration
4. **Dashboard Screen** - Courses, Classes, Progress
5. **Course Screen** - Chapters, Lessons, Resources
6. **Live Class Screen** - Join Class, Chat, Share
7. **Attendance Screen** - QR Scan, Status
8. **AI Tutor Screen** - Chat, Voice Q&A
9. **Profile Screen** - Edit Info, Change Password
10. **Settings Screen** - Language, Notifications, Offline Mode

### Offline Support:
- Local Database (SQLite)
- Cached Content (Courses, Chapters)
- Offline Q&A (Ollama Integration)
- Sync when online
- Progressive Web App (PWA)

### Performance:
- Fast Startup (<2s on 4G)
- Lazy Loading
- Image Compression
- Minimal Network Calls
- Battery Optimization
- Low RAM Usage (<200MB)

---

## 🌐 Web Portal Features (React)

### Admin Dashboard:
- User Analytics
- Course Statistics
- Class Attendance Charts
- Revenue Dashboard
- System Health Monitoring

### Teacher Dashboard:
- My Courses
- Create/Edit Courses
- Schedule Classes
- View Attendance
- Grade Students
- Reports

### Parent Portal:
- Child's Progress
- Attendance Records
- Marks & Grades
- Teacher Communication
- Payment Status

---

## 🤖 AI Modules Implementation

### 1. AI Tutor (Ollama)
```
Setup:
- Run Ollama locally
- Download Mistral/Llama 2 model
- Integrate with FastAPI
- ChromaDB for vector search

Flow:
1. User asks question (text/voice)
2. Convert voice to text (Vosk)
3. Search relevant context (ChromaDB)
4. Generate response (Ollama LLM)
5. Convert response to voice (Coqui TTS)
6. Send to user (text/voice)
```

### 2. Speech-to-Text (Vosk)
```
Features:
- Offline recognition
- Multiple languages
- Low latency
- Works on mobile

Setup:
- Install Vosk
- Download language models
- Integrate with Flutter/Web
```

### 3. Text-to-Speech (Coqui)
```
Features:
- Natural voice
- Multiple languages
- Offline generation
- Fast processing

Setup:
- Install Coqui TTS
- Configure voice models
- Integrate with backend
```

---

## 📦 Deployment Architecture

### Docker Compose Setup:
```yaml
services:
  # FastAPI Backend
  api:
    image: fastapi:latest
    ports: [8000:8000]
    volumes: [./backend:/app]
    environment: [DATABASE_URL, JWT_SECRET]

  # PostgreSQL Database
  db:
    image: postgres:15
    ports: [5432:5432]
    volumes: [postgres_data:/var/lib/postgresql]
    environment: [POSTGRES_PASSWORD, POSTGRES_DB]

  # Ollama AI Service
  ollama:
    image: ollama/ollama:latest
    ports: [11434:11434]
    volumes: [ollama_data:/root/.ollama]

  # Jitsi Meet (Video Conferencing)
  jitsi:
    image: jitsi/web:latest
    ports: [8080:80]
    environment: [PUBLIC_URL]

  # Redis Cache (Optional)
  redis:
    image: redis:7-alpine
    ports: [6379:6379]

  # React Web App
  web:
    image: node:18
    ports: [3000:3000]
    volumes: [./frontend/web:/app]
```

### Deployment Options:
1. **Self-Hosted** (Recommended for MVP)
   - VPS (DigitalOcean, Linode, Hetzner)
   - Docker Compose
   - GitHub Actions for CI/CD

2. **Cloud Platforms** (When scaling)
   - AWS ECS + RDS
   - Google Cloud Run
   - DigitalOcean Apps

---

## 🧪 Testing Strategy

### Unit Tests
- Backend APIs (pytest)
- Frontend Components (Jest)
- Service Logic

### Integration Tests
- Database operations
- API endpoints
- Authentication flow

### E2E Tests
- User registration
- Course creation
- Live class join
- AI tutor interaction

### Performance Tests
- API response time (<200ms)
- Database query optimization
- Mobile app startup time (<2s)

---

## 📈 Monitoring & Analytics

### Metrics to Track:
- User Engagement (DAU, MAU)
- Course Enrollment Trends
- Live Class Attendance
- System Performance
- Error Rates
- API Response Times

### Tools:
- Google Analytics (Web)
- Firebase Analytics (Mobile)
- Sentry (Error Tracking)
- Prometheus + Grafana (Infrastructure)

---

## 🚀 MVP Launch Checklist

### Week 1-4: Foundation
- [x] Project Setup
- [x] Database Schema
- [ ] Backend API Scaffolding
- [ ] Authentication System
- [ ] User Roles & Permissions

### Week 5-8: Core Features
- [ ] Course Management APIs
- [ ] Live Class Integration
- [ ] Attendance System
- [ ] Flutter App (Screens)
- [ ] React Web App (Pages)

### Week 9-12: AI & Optimization
- [ ] Ollama Integration
- [ ] AI Tutor API
- [ ] Voice Features (Vosk, Coqui)
- [ ] Mobile Optimization
- [ ] Testing & Bug Fixes
- [ ] Docker Setup
- [ ] Deployment

### Post-MVP: Phase 2
- [ ] AI Book Generator
- [ ] AI Exam Generator
- [ ] Digital Library
- [ ] Social Media Integration
- [ ] Analytics Dashboard
- [ ] Multi-school Support

---

## 💡 Development Best Practices

✅ **Code Quality**
- Clean Code Principles
- SOLID Design Patterns
- DRY (Don't Repeat Yourself)
- Type Hints & Annotations
- Comprehensive Documentation

✅ **Version Control**
- Git Flow Branching
- Meaningful Commit Messages
- Pull Request Reviews
- Code Coverage >80%

✅ **Documentation**
- API Documentation (Swagger)
- Code Comments
- Architecture Diagrams
- Setup & Deployment Guides
- User Manuals

✅ **Performance**
- Database Query Optimization
- Caching Strategies
- API Response Time <200ms
- Mobile App <3s Load Time
- Low Data Mode Support

---

## 📞 Support & Contact

- **GitHub:** https://github.com/ajaysingh132/-64-University-of-the-Arts-
- **Email:** support@digitalgurukul.com
- **Discord:** [Community Server]

---

**Last Updated:** June 3, 2026
**MVP Status:** In Development
**Version:** 1.0.0-alpha
