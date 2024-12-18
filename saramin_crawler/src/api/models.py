from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 다대다 관계를 위한 연결 테이블들
job_tech_stacks = db.Table('job_tech_stacks',
    db.Column('job_id', db.Integer, db.ForeignKey('jobs.id', ondelete='CASCADE'), primary_key=True),
    db.Column('tech_stack_id', db.Integer, db.ForeignKey('tech_stacks.id', ondelete='CASCADE'), primary_key=True),
    extend_existing=True
)

resume_skills = db.Table('resume_skills',
    db.Column('resume_id', db.Integer, db.ForeignKey('resumes.id', ondelete='CASCADE'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('tech_stacks.id', ondelete='CASCADE'), primary_key=True),
    extend_existing=True
)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    # 관계 설정
    resumes = db.relationship('Resume', backref='user', lazy=True, cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='user', lazy=True, cascade='all, delete-orphan')
    bookmarks = db.relationship('Bookmark', backref='user', lazy=True, cascade='all, delete-orphan')


# 채용공고 테이블
class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary_range = db.Column(db.String(100))
    salary_min = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('job_categories.id', ondelete='SET NULL'))
    requirements = db.Column(db.JSON)  # List[str]를 JSON으로 저장
    category = db.Column(db.String(50), nullable=False)
    job_type = db.Column(db.String(50), nullable=False)
    experience_required = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 설정
    tech_requirements = db.relationship('TechStack', secondary='job_tech_requirements')
    tech_stacks = db.relationship('TechStack', secondary=job_tech_stacks, backref='jobs', lazy='dynamic')
    applications = db.relationship('Application', backref='job', lazy=True, cascade='all, delete-orphan')
    bookmarks = db.relationship('Bookmark', backref='job', lazy=True, cascade='all, delete-orphan')
    category = db.relationship('JobCategory', back_populates='jobs')
    
    # 인덱스 설정
    __table_args__ = (
        db.Index('idx_job_title', 'title'),
        db.Index('idx_job_created', 'created_at'),
        db.Index('idx_job_salary', 'salary_min', 'salary_max'),
        db.Index('idx_job_composite', 'title', 'company_id', 'category_id')
    )

    category = db.relationship('JobCategory', back_populates='jobs')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'company': self.company,
            'location': self.location,
            'salary_range': self.salary_range,
            'requirements': self.requirements,
            'category': self.category,
            'job_type': self.job_type,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    
class JobCategory(db.Model):
    __tablename__ = 'job_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 설정
    jobs = db.relationship('Job', back_populates='category')

    # 인덱스 설정
    __table_args__ = (
        db.Index('idx_category_name', 'name'),
    )


# 회사 정보 테이블
class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    industry = db.Column(db.String(50))
    employee_count = db.Column(db.Integer)
    size = db.Column(db.String(50))
    founded_year = db.Column(db.Integer)
    website = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # 관계 설정
    jobs = db.relationship('Job', backref='company', lazy=True)
    # 인덱스 설정
    __table_args__ = (
        db.Index('idx_company_name', 'name'),
        db.Index('idx_company_location', 'location'),
        db.Index('idx_company_composite', 'name', 'location', 'industry')
    )

# 기술 스택 테이블
class TechStack(db.Model):
    __tablename__ = 'tech_stacks'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 인덱스 설정
    __table_args__ = (
        db.Index('idx_tech_name', 'name'),
    )

# 채용공고-기술스택 연결 테이블
class JobTechRequirement(db.Model):
    __tablename__ = 'job_tech_requirements'
    
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), primary_key=True)
    tech_id = db.Column(db.Integer, db.ForeignKey('tech_stacks.id'), primary_key=True)
    level_required = db.Column(db.String(20))


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_id': self.job_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
    }

    # 유니크 제약조건 추가
    __table_args__ = (
        db.UniqueConstraint('user_id', 'job_id', name='unique_user_job_bookmark'),
    )

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id', ondelete='CASCADE'), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id', ondelete='SET NULL'))
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 이력서 테이블
class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    education = db.Column(db.Text)
    experience = db.Column(db.Text)
    skills = db.Column(db.Text)
    file_path = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 설정
    skills = db.relationship('TechStack', secondary=resume_skills, backref='resumes', lazy='dynamic')
    educations = db.relationship('Education', backref='resume', lazy=True, cascade='all, delete-orphan')
    experiences = db.relationship('WorkExperience', backref='resume', lazy=True, cascade='all, delete-orphan')

    # 인덱스 설정
    __table_args__ = (
        db.Index('idx_resume_user', 'user_id'),
        db.Index('idx_resume_created', 'created_at')
    )

# 알림 설정 테이블
class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'application_status', 'new_job', etc.
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class NotificationSetting(db.Model):
    __tablename__ = 'notification_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    email_notifications = db.Column(db.Boolean, default=False)
    push_notifications = db.Column(db.Boolean, default=False)
    notification_types = db.Column(db.JSON)  # List[str]를 JSON으로 저장
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'email_notifications': self.email_notifications,
            'push_notifications': self.push_notifications,
            'notification_types': self.notification_types,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
# 학력 정보 테이블
class Education(db.Model):
    __tablename__ = 'educations'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    degree = db.Column(db.String(50))
    major = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    # 경력 정보 테이블
class WorkExperience(db.Model):
    __tablename__ = 'work_experiences'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100))
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
