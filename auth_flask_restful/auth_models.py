from datetime import datetime
from sqlalchemy import DateTime, Column, Integer, String
from flask_sqlalchemy import SQLAlchemy

authdb = SQLAlchemy()


class ApiUser(authdb.Model):
    __tablename__ = 'api_user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    description = Column(String(255))
    token = Column(String(255), unique=True)
    created_on = Column(DateTime, default=datetime.now)
