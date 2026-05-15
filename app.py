import os
import secrets
import smtplib
from fastapi import FastAPI, Depends, Request, Form, Header, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from database import engine, Base, SessionLocal
from models import User, OTPRecord, EmailSettings
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from starlette import status

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def authenticate_api(x_api_key: str, db:Session):
    user = db.query(User).filter(User.api_key == x_api_key).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail='invalid API key'
        )
    return user

load_dotenv(dotenv_path=".env")

Base.metadata.create_all(bind=engine)

app = FastAPI(title='OTP service')

templates = Jinja2Templates(directory="frontend/templates")

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')

class OTPRequest(BaseModel):
    email: str

class VerifyRequest(BaseModel):
    email: str
    otp: str

def send_email(rec_email, otp, settings=None):
    org_name = "OTP SaaS"
    email_subject = "OTP Verification"
    support_email = EMAIL_USER
    footer_text = "Secure OTP Service"
    if settings:
        org_name = settings.org_name
        email_subject = settings.email_subject
        support_email = settings.support_email
        footer_text = settings.footer_text
    html_content = f"""
    <div style="
        font-family: Arial;
        max-width: 600px;
        margin: auto;
        padding: 30px;
        border-radius: 12px;
        background: #0f172a;
        color: white;
    ">
        <h1>{org_name}</h1>
        <p>Your OTP code is:</p>

        <div style="
            font-size: 36px;
            font-weight: bold;
            letter-spacing: 8px;
            margin: 30px 0;
            color: #38bdf8;
        ">
            {otp}
        </div>
        <p>This OTP expires in 5 minutes.</p>
        <hr>
        <small>
            Support: {support_email}
        </small>
        <br>
        <small>{footer_text}</small>
    </div>
    """
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = rec_email
    msg['Subject'] = email_subject
    msg.attach(MIMEText(html_content, 'html'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(
            EMAIL_USER,
            rec_email,
            msg.as_string()
        )
        server.quit()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail='email sending failed'
        )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def home(request:Request):
    user_id = request.cookies.get('user_id')
    return templates.TemplateResponse('home.html', {
        'request': request,
        'logged_in': bool(user_id)
    })

@app.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get('user_id')
    if not user_id:
        return RedirectResponse('/login')
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        return RedirectResponse("/login")
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "api_key": user.api_key,
        'name': user.name
    })

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request
    })

@app.post('/login')
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return templates.TemplateResponse('login.html', {
            'request': request,
            'msg': 'invalid credentials'
        })
    response = RedirectResponse(url='/dashboard', status_code=status.HTTP_302_FOUND)
    response.set_cookie(key='user_id', value = str(user.id))
    return response

@app.get('/logout')
def logout():
    response = RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key='user_id')
    return response

@app.get('/register')
def register_page(request: Request):
    return templates.TemplateResponse('register.html',{
        'request': request,
        'msg': 'registered successfully'
    })

@app.post("/register")
def register_user(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "User already exists"
        })
    new_user = User(
        name = name,
        email = email,
        password = hash_password(password),
        api_key = secrets.token_urlsafe(32)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="user_id", value=str(new_user.id), httponly=True)
    return response

@app.get('/settings')
def get_settings(request: Request, db: Session=Depends(get_db)):
    user_id = request.cookies.get('user_id')
    if not user_id:
        return RedirectResponse('/login')
    settings = db.query(EmailSettings).filter(EmailSettings.user_id == int(user_id)).first()

    return templates.TemplateResponse('settings.html', {
        'request': request,
        'settings': settings
    })

@app.post('/settings')
def save_settings(request: Request, org_name: str = Form(...), email_subject: str = Form(...), support_email: str = Form(...), footer_text: str = Form(...), db: Session = Depends(get_db)):
    user_id = request.cookies.get('user_id')
    if not user_id:
        return RedirectResponse('/login')
    settings = db.query(EmailSettings).filter(EmailSettings.user_id == int(user_id)).first()
    if settings:
        settings.org_name = org_name
        settings.email_subject = email_subject
        settings.support_email = support_email
        settings.footer_text = footer_text
    else:
        settings = EmailSettings(
            user_id=int(user_id),
            org_name=org_name,
            email_subject=email_subject,
            support_email=support_email,
            footer_text=footer_text
        )
        db.add(settings)
    db.commit()
    return RedirectResponse('/dashboard', status_code=302)
    
@app.post('/send-otp')
def send_otp(data: OTPRequest, x_api_key: str = Header(...), db:Session=Depends(get_db)):
    user = authenticate_api(x_api_key, db)
    email = data.email
    otp_num = str(secrets.randbelow(900000) + 100000)
    existing = db.query(OTPRecord).filter(OTPRecord.email == email, OTPRecord.user_id == user.id).first()
    if existing:
        existing.otp = otp_num
        existing.verified = False
    else:
        row = OTPRecord(
            user_id = user.id,
            email = email,
            otp = otp_num,
            verified = False
        )
        db.add(row)
    db.commit()
    settings = db.query(EmailSettings).filter(EmailSettings.user_id == user.id).first()
    send_email(email, otp_num, settings)
    return {
        'success' : True,
        'message': 'otp generated successfully'
    }

@app.post('/verify')
def verify(data: VerifyRequest, x_api_key:str = Header(...), db:Session=Depends(get_db)):
    user = authenticate_api(x_api_key, db)
    user_email = data.email
    user_otp = data.otp
    row = db.query(OTPRecord).filter(OTPRecord.email == user_email, OTPRecord.user_id == user.id).first()
    if not row:
        return {
            'success': False,
            'message': 'user not found'
        }
    if row.otp == user_otp:
        row.verified = True
        db.delete(row)
        db.commit()
        return {
            'success': True,
            'message': 'otp verified'
        }
    return {
        "success": False,
        "message": "invalid otp"
    }


