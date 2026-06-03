from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import LiveClass, Attendance, Course
from app.schemas import LiveClassCreate, LiveClassResponse, AttendanceResponse
import uuid
import qrcode
from io import BytesIO
import base64

router = APIRouter(prefix="/api/v1/classes", tags=["live-classes"])

@router.get("", response_model=list[LiveClassResponse])
async def list_classes(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """
    List all live classes
    """
    classes = db.query(LiveClass).offset(skip).limit(limit).all()
    return classes

@router.get("/{class_id}", response_model=LiveClassResponse)
async def get_class(class_id: str, db: Session = Depends(get_db)):
    """
    Get live class details
    """
    live_class = db.query(LiveClass).filter(LiveClass.id == class_id).first()
    if not live_class:
        raise HTTPException(status_code=404, detail="Class not found")
    return live_class

@router.post("", response_model=LiveClassResponse)
async def create_class(class_data: LiveClassCreate, teacher_id: str, db: Session = Depends(get_db)):
    """
    Create a new live class (Teacher only)
    """
    # Verify course exists
    course = db.query(Course).filter(Course.id == class_data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Generate Jitsi room ID
    jitsi_room_id = f"gbsb-{uuid.uuid4().hex[:12]}"
    
    new_class = LiveClass(
        course_id=class_data.course_id,
        teacher_id=teacher_id,
        title=class_data.title,
        description=class_data.description,
        scheduled_at=class_data.scheduled_at,
        jitsi_room_id=jitsi_room_id
    )
    
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    
    return new_class

@router.post("/{class_id}/start")
async def start_class(class_id: str, db: Session = Depends(get_db)):
    """
    Start a live class
    """
    live_class = db.query(LiveClass).filter(LiveClass.id == class_id).first()
    if not live_class:
        raise HTTPException(status_code=404, detail="Class not found")
    
    live_class.status = "live"
    live_class.started_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Class started", "jitsi_room": live_class.jitsi_room_id}

@router.post("/{class_id}/end")
async def end_class(class_id: str, db: Session = Depends(get_db)):
    """
    End a live class
    """
    live_class = db.query(LiveClass).filter(LiveClass.id == class_id).first()
    if not live_class:
        raise HTTPException(status_code=404, detail="Class not found")
    
    live_class.status = "completed"
    live_class.ended_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Class ended"}

@router.get("/{class_id}/qr-code")
async def get_qr_code(class_id: str, db: Session = Depends(get_db)):
    """
    Generate QR code for attendance
    """
    live_class = db.query(LiveClass).filter(LiveClass.id == class_id).first()
    if not live_class:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"attendance:{class_id}")
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return {"qr_code": f"data:image/png;base64,{img_str}"}

@router.post("/{class_id}/attendance")
async def mark_attendance(class_id: str, student_id: str, status: str = "present", db: Session = Depends(get_db)):
    """
    Mark attendance for a student
    """
    live_class = db.query(LiveClass).filter(LiveClass.id == class_id).first()
    if not live_class:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Check if already marked
    existing = db.query(Attendance).filter(
        (Attendance.class_id == class_id) & (Attendance.student_id == student_id)
    ).first()
    
    if existing:
        existing.status = status
    else:
        attendance = Attendance(
            class_id=class_id,
            student_id=student_id,
            status=status
        )
        db.add(attendance)
    
    db.commit()
    
    return {"message": f"Attendance marked as {status}"}

@router.get("/{class_id}/attendance", response_model=list[AttendanceResponse])
async def get_class_attendance(class_id: str, db: Session = Depends(get_db)):
    """
    Get attendance for a class
    """
    attendances = db.query(Attendance).filter(Attendance.class_id == class_id).all()
    return attendances
