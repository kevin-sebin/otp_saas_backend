from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base

class OTPRecord(Base):
    __tablename__ = 'otp_records'
    _id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    email = Column(String(255), index=True)
    otp = Column(String(10))
    verified = Column(Boolean, default=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    api_key = Column(String(255), unique=True)

class EmailSettings(Base):
    __tablename__ = 'email_settings'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    org_name = Column(String(255))
    email_subject = Column(String(255))
    support_email = Column(String(255))
    footer_text = Column(String(500))