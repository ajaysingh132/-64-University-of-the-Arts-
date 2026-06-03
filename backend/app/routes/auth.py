from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserRegister, UserLogin, TokenResponse, TwoFactorSetup, TwoFactorVerify
from app.services.auth_service import AuthService
from datetime import timedelta

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    
    # Create new user
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=AuthService.hash_password(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create tokens
    access_token = AuthService.create_access_token(
        data={"sub": new_user.id, "role": str(new_user.role)}
    )
    
    return TokenResponse(
        access_token=access_token,
        user=new_user
    )

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    User login
    """
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not AuthService.verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify 2FA if enabled
    if user.two_factor_enabled:
        if not credentials.totp_code:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="2FA code required"
            )
        
        if not AuthService.verify_2fa_code(user.two_factor_secret, credentials.totp_code):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid 2FA code"
            )
    
    # Create token
    access_token = AuthService.create_access_token(
        data={"sub": user.id, "role": str(user.role)}
    )
    
    return TokenResponse(
        access_token=access_token,
        user=user
    )

@router.post("/2fa/setup", response_model=TwoFactorSetup)
async def setup_2fa(user_id: str, db: Session = Depends(get_db)):
    """
    Setup 2FA for user
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    secret = AuthService.generate_2fa_secret()
    qr_code_url = AuthService.get_2fa_qr_code(secret, user.username)
    
    return TwoFactorSetup(
        secret=secret,
        qr_code_url=qr_code_url
    )

@router.post("/2fa/verify")
async def verify_2fa(user_id: str, data: TwoFactorVerify, db: Session = Depends(get_db)):
    """
    Verify and enable 2FA
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # This assumes the secret was stored temporarily
    # In production, you'd have a pending 2FA secret stored
    if AuthService.verify_2fa_code(user.two_factor_secret, data.code):
        user.two_factor_enabled = True
        db.commit()
        return {"message": "2FA enabled successfully"}
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid code"
    )

@router.get("/me")
async def get_current_user(user_id: str, db: Session = Depends(get_db)):
    """
    Get current user profile
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
