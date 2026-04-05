from fastapi import APIRouter, HTTPException
from schema.auth_schema import LoginSchema, RegisterSchema
from service.user_auth import login_user, register_user

router = APIRouter(
    prefix="/v1/api/auth",
    tags=["auth"],
)

@router.post("/login")
async def login_endpoint(req: LoginSchema):
    try:
        access_token, refresh_token, user_id = login_user(email=req.email, password=req.password)
        return {
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user_id,
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/register")
async def register_endpoint(req: RegisterSchema):
    try:
        access_token, refresh_token, user_id = register_user(email=req.email, password=req.password)
        return {
            "message": "User registered successfully",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user_id,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
