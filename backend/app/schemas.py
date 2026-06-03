from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

# ============ Auth Schemas ============

class RoleEnum(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    PARENT = "parent"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    phone: Optional[str] = None
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: RoleEnum = RoleEnum.STUDENT

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    totp_code: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    role: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str]
    token_type: str = "bearer"
    user: UserResponse

class TwoFactorSetup(BaseModel):
    secret: str
    qr_code_url: str

class TwoFactorVerify(BaseModel):
    code: str

# ============ Course Schemas ============

class LessonCreate(BaseModel):
    title: str
    content: Optional[str] = None
    video_url: Optional[str] = None
    resources_url: Optional[str] = None
    duration_minutes: Optional[int] = None
    order: int = 0

class LessonResponse(BaseModel):
    id: str
    title: str
    content: Optional[str]
    video_url: Optional[str]
    resources_url: Optional[str]
    duration_minutes: Optional[int]
    order: int
    
    class Config:
        from_attributes = True

class ChapterCreate(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    order: int = 0

class ChapterResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    content: Optional[str]
    order: int
    lessons: list[LessonResponse] = []
    
    class Config:
        from_attributes = True

class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    syllabus: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class CourseResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    category: Optional[str]
    teacher_id: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    created_at: datetime
    chapters: list[ChapterResponse] = []
    
    class Config:
        from_attributes = True

class EnrollmentResponse(BaseModel):
    id: str
    student_id: str
    course_id: str
    status: str
    progress: int
    enrolled_at: datetime
    
    class Config:
        from_attributes = True

# ============ Live Class Schemas ============

class LiveClassCreate(BaseModel):
    course_id: str
    title: str
    description: Optional[str] = None
    scheduled_at: datetime

class LiveClassResponse(BaseModel):
    id: str
    course_id: str
    title: str
    description: Optional[str]
    scheduled_at: datetime
    status: str
    jitsi_room_id: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class AttendanceResponse(BaseModel):
    id: str
    class_id: str
    student_id: str
    status: str
    marked_at: datetime
    
    class Config:
        from_attributes = True

# ============ AI Tutor Schemas ============

class AIQuestionRequest(BaseModel):
    question: str
    question_type: str = "text"  # text or voice

class AIAnswerResponse(BaseModel):
    id: str
    question: str
    answer: str
    answer_type: str = "text"
    created_at: datetime
    
    class Config:
        from_attributes = True

class AIChatHistoryResponse(BaseModel):
    chats: list[AIAnswerResponse]
    total: int
