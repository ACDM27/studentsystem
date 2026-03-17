from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import LoginRequest, LoginResponse, UserInfo, RefreshTokenRequest, TokenResponse, FirstLoginRequest, ChangePasswordRequest
from utils import success_response, error_response
from models import SysUser, SysStudent, UserRole
from auth import verify_password, create_access_token, create_refresh_token, decode_refresh_token, get_password_hash
from dependencies import get_current_user

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
    # 查找用户
    user = db.query(SysUser).filter(SysUser.username == request.username).first()
    
    if not user or not verify_password(request.password, user.password_hash):
        return error_response(msg="学号或密码不正确", code=401)
    
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
    
    # 判断是否使用初始密码登录：如果密码仍为 123456，提示修改
    is_initial_password = verify_password("123456", user.password_hash)

    response_data = LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        is_first_login=is_initial_password,
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


@router.post("/first-login")
async def first_login(request: FirstLoginRequest, db: Session = Depends(get_db)):
    """
    首次登录：使用真实姓名 + 学号验证身份，无需密码。
    成功后返回临时 token，前端必须立即跳转至修改密码页。
    """
    student = db.query(SysStudent).filter(
        SysStudent.name == request.name,
        SysStudent.student_number == request.student_number
    ).first()

    if not student:
        return error_response(msg="姓名或学号不正确，请核实后重试", code=401)

    user = student.user
    if not user.is_first_login:
        return error_response(msg="该账号已完成初始化，请使用学号和密码登录", code=400)

    token_data = {"sub": str(user.id), "role": user.role.value}
    access_token = create_access_token(data=token_data)
    refresh_token = create_refresh_token(data=token_data)

    return success_response(data={
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "is_first_login": True,
        "userInfo": {"id": user.id, "name": student.name, "role": user.role.value}
    })


@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    current_user: SysUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    设置/修改密码（首次登录必须调用）。
    成功后 is_first_login 置为 False，username 更新为学号，
    后续可使用 学号 + 新密码 通过 /login 正常登录。
    """
    if request.new_password != request.confirm_password:
        return error_response(msg="两次密码输入不一致", code=400)

    current_user.password_hash = get_password_hash(request.new_password)
    current_user.is_first_login = False

    # 统一将 username 更新为学号，便于后续用学号登录
    if current_user.student:
        current_user.username = current_user.student.student_number

    db.commit()
    return success_response(msg="密码设置成功，请使用学号和新密码登录")

