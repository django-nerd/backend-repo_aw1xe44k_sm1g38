"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (kept for reference):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Blog app schemas

class Roadmap(BaseModel):
    """
    Roadmaps for learning programming languages
    Collection name: "roadmap"
    """
    language: str = Field(..., description="Programming language name")
    title: str = Field(..., description="Roadmap title")
    description: str = Field(..., description="Short summary of the roadmap")
    level: str = Field("beginner", description="Target level: beginner/intermediate/advanced")
    steps: List[str] = Field(default_factory=list, description="Ordered list of steps to follow")

class Lesson(BaseModel):
    title: str
    content: str
    order: int = 1

class Course(BaseModel):
    """
    Courses for each programming language
    Collection name: "course"
    """
    language: str = Field(..., description="Programming language name")
    title: str = Field(..., description="Course title")
    slug: str = Field(..., description="URL-friendly unique slug for the course")
    description: str = Field(..., description="What the learner will gain")
    level: str = Field("beginner", description="Course level")
    duration: Optional[str] = Field(None, description="Estimated completion time")
    lessons: List[Lesson] = Field(default_factory=list, description="Lesson list")

# Note: The Flames database viewer can inspect these at /schema if implemented.
