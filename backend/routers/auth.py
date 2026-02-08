from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import LoginRequest, LoginResponse, UserInfo, RefreshTokenRequest, TokenResponse
from utils import success_response, error_response
from models import SysUser, UserRole
from auth import verify_password, create_access_token, create_refresh_token, decode_refresh_token, get_password_hash

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    User login endpoint
    - Validates username and password with strict data validation
    - Returns dual JWT tokens (access + refresh) and user info
    - Access token: short-lived, for API requests
    - Refresh token: long-lived, for renewing access tokens
    - Auto-upgrades legacy Bcrypt passwords to Argon2 on successful login
    """
    # Find user
    user = db.query(SysUser).filter(SysUser.username == request.username).first()
    
    if not user or not verify_password(request.password, user.password_hash):
        return error_response(msg="Invalid username or password", code=401)
    
    # Auto-upgrade legacy Bcrypt password to Argon2
    # This happens transparently when user logs in with old password
    if user.password_hash.startswith('$2b$') or user.password_hash.startswith('$2a$'):
        # User is using legacy Bcrypt password, upgrade to Argon2
        user.password_hash = get_password_hash(request.password)
        db.commit()
        print(f"✅ Auto-upgraded password for user: {user.username} (Bcrypt → Argon2)")
    
    # Create token payload
    token_data = {"sub": str(user.id), "role": user.role.value}
    
    # Create both access and refresh tokens
    access_token = create_access_token(data=token_data)
    refresh_token = create_refresh_token(data=token_data)
    
    # Prepare user info
    user_name = user.username
    if user.role == UserRole.STUDENT and user.student:
        user_name = user.student.name
    
    user_info = UserInfo(
        id=user.id,
        name=user_name,
        role=user.role
    )
    
    response_data = LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        userInfo=user_info
    )
    
    
    return success_response(data=response_data.model_dump())


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """
    Refresh access token endpoint
    - Validates refresh token
    - Issues new access token
    - Does NOT issue new refresh token (use existing one)
    """
    # Decode and validate refresh token
    payload = decode_refresh_token(request.refresh_token)
    if not payload:
        return error_response(msg="Invalid or expired refresh token", code=401)
    
    # Extract user info from token
    user_id = payload.get("sub")
    user_role = payload.get("role")
    
    if not user_id:
        return error_response(msg="Invalid token payload", code=401)
    
    # Verify user still exists and is active
    user = db.query(SysUser).filter(SysUser.id == int(user_id)).first()
    if not user:
        return error_response(msg="User not found", code=401)
    
    # Create new access token with same data
    token_data = {"sub": user_id, "role": user_role}
    new_access_token = create_access_token(data=token_data)
    
    response_data = TokenResponse(
        access_token=new_access_token,
        token_type="bearer"
    )
    
    return success_response(data=response_data.model_dump())

