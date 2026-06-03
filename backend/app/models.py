from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from app.database import Base

# Association table for Course-Chapter
course_chapter = Table(
    'course_chapter',
    Base.metadata,
    Column('course_id', String, ForeignKey('courses.id')),
    Column('chapter_id', String, ForeignKey('chapters.id'))
)

class RoleEnum(str, enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    PARENT = "parent"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class UserStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DELETED = "deleted"

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.STUDENT)
    status = Column(Enum(UserStatusEnum), default=UserStatusEnum.ACTIVE)
    school_id = Column(String, ForeignKey('schools.id'), nullable=True)
    
    # 2FA
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    school = relationship("School", back_populates="users")
    enrollments = relationship("Enrollment", back_populates="student")
    
    def __repr__(self):
        return f"<User {self.username}>"

class School(Base):
    __tablename__ = "schools"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    established_year = Column(Integer, nullable=True)
    admin_id = Column(String, ForeignKey('users.id'))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="school")
    courses = relationship("Course", back_populates="school")
    
    def __repr__(self):
        return f"<School {self.name}>"

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True)
    school_id = Column(String, ForeignKey('schools.id'))
    teacher_id = Column(String, ForeignKey('users.id'))
    syllabus = Column(Text, nullable=True)
    thumbnail_url = Column(String, nullable=True)
    
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    school = relationship("School", back_populates="courses")
    chapters = relationship("Chapter", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")
    classes = relationship("LiveClass", back_populates="course")
    
    def __repr__(self):
        return f"<Course {self.title}>"

class Chapter(Base):
    __tablename__ = "chapters"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id = Column(String, ForeignKey('courses.id'))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    order = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course = relationship("Course", back_populates="chapters")
    lessons = relationship("Lesson", back_populates="chapter")
    
    def __repr__(self):
        return f"<Chapter {self.title}>"

class Lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    chapter_id = Column(String, ForeignKey('chapters.id'))
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    video_url = Column(String, nullable=True)
    resources_url = Column(String, nullable=True)
    order = Column(Integer, default=0)
    duration_minutes = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    chapter = relationship("Chapter", back_populates="lessons")
    
    def __repr__(self):
        return f"<Lesson {self.title}>"

class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String, ForeignKey('users.id'))
    course_id = Column(String, ForeignKey('courses.id'))
    status = Column(String, default="active")  # active, completed, dropped
    progress = Column(Integer, default=0)  # 0-100%
    
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    student = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    
    def __repr__(self):
        return f"<Enrollment {self.student_id} -> {self.course_id}>"

class LiveClass(Base):
    __tablename__ = "live_classes"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id = Column(String, ForeignKey('courses.id'))
    teacher_id = Column(String, ForeignKey('users.id'))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    
    scheduled_at = Column(DateTime, nullable=False)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    
    jitsi_room_id = Column(String, nullable=True)
    recording_url = Column(String, nullable=True)
    status = Column(String, default="scheduled")  # scheduled, live, completed
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course = relationship("Course", back_populates="classes")
    attendances = relationship("Attendance", back_populates="live_class")
    
    def __repr__(self):
        return f"<LiveClass {self.title}>"

class Attendance(Base):
    __tablename__ = "attendances"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    class_id = Column(String, ForeignKey('live_classes.id'))
    student_id = Column(String, ForeignKey('users.id'))
    status = Column(String, default="absent")  # present, absent, late
    
    marked_at = Column(DateTime, default=datetime.utcnow)
    qr_code = Column(String, nullable=True)
    
    # Relationships
    live_class = relationship("LiveClass", back_populates="attendances")
    
    def __repr__(self):
        return f"<Attendance {self.student_id}>"

class AIChat(Base):
    __tablename__ = "ai_chats"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'))
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)
    question_type = Column(String, default="text")  # text, voice
    answer_type = Column(String, default="text")  # text, voice
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<AIChat {self.user_id}>"
