from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from flask import Flask
from src.api.models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_database.db'
db.init_app(app)
            
Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 관계 설정
    jobs = relationship('JobPosting', back_populates='company')

class JobPosting(Base):
    __tablename__ = 'job_postings'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'))
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    
    
    # 관계 설정
    company = relationship('Company', back_populates='jobs')
    applications = relationship('Application', back_populates='job')
    bookmarks = relationship('Bookmark', back_populates='job')

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 관계 설정
    applications = relationship('Application', back_populates='user')
    bookmarks = relationship('Bookmark', back_populates='user')

class Application(Base):
    __tablename__ = 'applications'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    job_id = Column(Integer, ForeignKey('job_postings.id'))
    status = Column(String(20), default='pending')  # pending, accepted, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 관계 설정
    user = relationship('User', back_populates='applications')
    job = relationship('JobPosting', back_populates='applications')

class Bookmark(Base):
    __tablename__ = 'bookmarks'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    job_id = Column(Integer, ForeignKey('job_postings.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 관계 설정
    user = relationship('User', back_populates='bookmarks')
    job = relationship('JobPosting', back_populates='bookmarks')
