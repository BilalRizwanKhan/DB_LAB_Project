from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint
from database import Base

class User(Base):
    __tablename__ = "users"
    id       = Column(Integer, primary_key=True, index=True)
    name     = Column(String)
    email    = Column(String, unique=True, index=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    phone    = Column(String, nullable=True)
    city     = Column(String, nullable=True)
    bio      = Column(String, nullable=True)
    avatar   = Column(String, nullable=True)

class Property(Base):
    __tablename__ = "properties"
    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String)
    location    = Column(String)
    price       = Column(Integer)
    description = Column(String)
    owner_id    = Column(Integer)
    image_path  = Column(String, nullable=True)

class Favorite(Base):
    __tablename__ = "favorites"
    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer)
    property_id = Column(Integer)
    __table_args__ = (UniqueConstraint("user_id", "property_id", name="uq_user_property"),)

class Review(Base):
    __tablename__ = "reviews"
    id          = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer)
    user_id     = Column(Integer)
    user_name   = Column(String)
    rating      = Column(Integer)
    comment     = Column(String)
    __table_args__ = (UniqueConstraint("user_id", "property_id", name="uq_user_review"),)

class Inquiry(Base):
    __tablename__ = "inquiries"
    id          = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer)
    buyer_id    = Column(Integer)
    buyer_name  = Column(String)
    buyer_email = Column(String)
    message     = Column(String)
    status      = Column(String, default="pending")
    reply       = Column(String, nullable=True)

class Appointment(Base):
    __tablename__ = "appointments"
    id           = Column(Integer, primary_key=True, index=True)
    property_id  = Column(Integer)
    user_id      = Column(Integer)
    user_name    = Column(String)
    user_email   = Column(String)
    visit_date   = Column(String)   # e.g. "2026-06-15"
    visit_time   = Column(String)   # e.g. "10:00 AM"
    note         = Column(String, nullable=True)
    status       = Column(String, default="pending")  # pending, confirmed, cancelled
