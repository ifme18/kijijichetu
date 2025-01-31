from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Community(db.Model):
    __tablename__ = 'community'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    
    users = relationship("User", back_populates="community")
    events = relationship("Event", back_populates="community")
    estates = relationship("Estate", back_populates="community")
    notifications = relationship("Notification", back_populates="community")

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    occupation = db.Column(db.String(400))
    phoneno = db.Column(db.Integer)
    houseno = db.Column(db.Integer)
    community_id = db.Column(db.Integer, ForeignKey('community.id'))
    
    community = relationship("Community", back_populates="users")
    estates = relationship("Estate", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    eventname = db.Column(db.String(100), nullable=False)
    eventdate = db.Column(db.DateTime, nullable=False)
    community_id = db.Column(db.Integer, ForeignKey('community.id'))
    
    community = relationship("Community", back_populates="events")

class Estate(db.Model):
    __tablename__ = 'estate'
    id = db.Column(db.Integer, primary_key=True)
    estatename = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    community_id = db.Column(db.Integer, ForeignKey('community.id'))
    
    user = relationship("User", back_populates="estates")
    community = relationship("Community", back_populates="estates")

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rsvp = db.Column(db.String(100))
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    community_id = db.Column(db.Integer, ForeignKey('community.id'))
    
    user = relationship("User", back_populates="notifications")
    community = relationship("Community", back_populates="notifications")
