from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Course, Chapter, Lesson, Enrollment, User
from app.schemas import CourseCreate, CourseResponse, ChapterCreate, ChapterResponse, EnrollmentResponse

router = APIRouter(prefix="/api/v1/courses", tags=["courses"])

@router.get("", response_model=list[CourseResponse])
async def list_courses(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """
    List all courses
    """
    courses = db.query(Course).offset(skip).limit(limit).all()
    return courses

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: str, db: Session = Depends(get_db)):
    """
    Get course by ID
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("", response_model=CourseResponse)
async def create_course(course_data: CourseCreate, teacher_id: str, db: Session = Depends(get_db)):
    """
    Create a new course (Teacher only)
    """
    # Verify teacher exists
    teacher = db.query(User).filter(User.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    new_course = Course(
        title=course_data.title,
        description=course_data.description,
        category=course_data.category,
        teacher_id=teacher_id,
        syllabus=course_data.syllabus,
        start_date=course_data.start_date,
        end_date=course_data.end_date
    )
    
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    
    return new_course

@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(course_id: str, course_data: CourseCreate, db: Session = Depends(get_db)):
    """
    Update course
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    for key, value in course_data.dict(exclude_unset=True).items():
        setattr(course, key, value)
    
    db.commit()
    db.refresh(course)
    
    return course

@router.post("/{course_id}/chapters", response_model=ChapterResponse)
async def create_chapter(course_id: str, chapter_data: ChapterCreate, db: Session = Depends(get_db)):
    """
    Add chapter to course
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    new_chapter = Chapter(
        course_id=course_id,
        title=chapter_data.title,
        description=chapter_data.description,
        content=chapter_data.content,
        order=chapter_data.order
    )
    
    db.add(new_chapter)
    db.commit()
    db.refresh(new_chapter)
    
    return new_chapter

@router.get("/{course_id}/chapters", response_model=list[ChapterResponse])
async def get_chapters(course_id: str, db: Session = Depends(get_db)):
    """
    Get all chapters for a course
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return course.chapters

@router.post("/{course_id}/enroll")
async def enroll_course(course_id: str, student_id: str, db: Session = Depends(get_db)):
    """
    Enroll student in course
    """
    # Check if already enrolled
    existing = db.query(Enrollment).filter(
        (Enrollment.student_id == student_id) & (Enrollment.course_id == course_id)
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled")
    
    enrollment = Enrollment(
        student_id=student_id,
        course_id=course_id
    )
    
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    
    return enrollment

@router.get("/student/{student_id}/enrollments", response_model=list[EnrollmentResponse])
async def get_enrollments(student_id: str, db: Session = Depends(get_db)):
    """
    Get all enrollments for a student
    """
    enrollments = db.query(Enrollment).filter(Enrollment.student_id == student_id).all()
    return enrollments
