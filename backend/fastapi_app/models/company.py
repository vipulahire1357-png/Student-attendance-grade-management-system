"""Company ORM model."""
from sqlalchemy import (
    Boolean, Column, Integer, String, Text, TIMESTAMP
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class Company(Base):
    __tablename__ = "companies"

    id              = Column(Integer, primary_key=True, index=True)
    email           = Column(String(255), unique=True, nullable=False, index=True)
    password_hash   = Column(Text, nullable=False)
    company_name    = Column(String(255), nullable=False)
    slug            = Column(String(100), unique=True, nullable=False, index=True)
    description     = Column(Text, nullable=True)
    logo_url        = Column(Text, nullable=True)
    website_url     = Column(Text, nullable=True)
    industry        = Column(String(255), nullable=True)
    size            = Column(String(50), nullable=True)
    founded_year    = Column(Integer, nullable=True)
    headquarters    = Column(String(255), nullable=True)
    linkedin_url    = Column(Text, nullable=True)
    is_active       = Column(Boolean, default=True)
    is_verified     = Column(Boolean, default=False)
    created_at      = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at      = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # ── Relationships ─────────────────────────────────────
    jobs        = relationship("Job", back_populates="company", cascade="all, delete-orphan")
    problems    = relationship("IndustryProblem", back_populates="company", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Company id={self.id} company_name={self.company_name!r}>"
