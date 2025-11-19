import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import db, create_document, get_documents
from schemas import Roadmap, Course, Lesson

app = FastAPI(title="Nazar Blog API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateRoadmapRequest(Roadmap):
    pass

class CreateCourseRequest(Course):
    pass


@app.get("/")
def root():
    return {"message": "Nazar Blog API is running"}


@app.get("/api/roadmaps", response_model=List[Roadmap])
def list_roadmaps(language: Optional[str] = None, level: Optional[str] = None):
    try:
        filter_dict = {}
        if language:
            filter_dict["language"] = language
        if level:
            filter_dict["level"] = level
        docs = get_documents("roadmap", filter_dict)
        for d in docs:
            d.pop("_id", None)
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/roadmaps", status_code=201)
def create_roadmap(payload: CreateRoadmapRequest):
    try:
        create_document("roadmap", payload)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/courses", response_model=List[Course])
def list_courses(language: Optional[str] = None, level: Optional[str] = None):
    try:
        filter_dict = {}
        if language:
            filter_dict["language"] = language
        if level:
            filter_dict["level"] = level
        docs = get_documents("course", filter_dict)
        for d in docs:
            d.pop("_id", None)
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/courses/{slug}", response_model=Course)
def get_course_by_slug(slug: str):
    try:
        docs = get_documents("course", {"slug": slug}, limit=1)
        if not docs:
            raise HTTPException(status_code=404, detail="Course not found")
        doc = docs[0]
        doc.pop("_id", None)
        return doc
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/seed")
def seed_sample_content():
    """Insert sample roadmaps and courses if they don't already exist"""
    try:
        # Seed roadmaps
        existing_rm = get_documents("roadmap", {}, limit=1)
        created = {"roadmaps": 0, "courses": 0}
        if not existing_rm:
            python_rm = Roadmap(
                language="Python",
                title="Python Developer Roadmap",
                description="A clear path from basics to building real-world Python apps.",
                level="beginner",
                steps=[
                    "Learn syntax, variables, and control flow",
                    "Work with data structures (lists, dicts, sets)",
                    "Functions, modules, and packages",
                    "OOP basics",
                    "Virtual environments & package management",
                    "Build small CLI and web projects (FastAPI)",
                ],
            )
            js_rm = Roadmap(
                language="JavaScript",
                title="JavaScript Developer Roadmap",
                description="From fundamentals to modern web apps.",
                level="beginner",
                steps=[
                    "JS fundamentals & DOM",
                    "ES6+ features",
                    "Async programming",
                    "Tooling (npm, bundlers)",
                    "React basics",
                    "Build a full-stack app",
                ],
            )
            create_document("roadmap", python_rm)
            create_document("roadmap", js_rm)
            created["roadmaps"] = 2

        # Seed courses
        if not get_documents("course", {"slug": "python-for-beginners"}, limit=1):
            py_course = Course(
                language="Python",
                title="Python for Beginners",
                slug="python-for-beginners",
                description="Start your Python journey with hands-on lessons.",
                level="beginner",
                duration="6 hours",
                lessons=[
                    Lesson(title="Introduction to Python", content="History, install, hello world", order=1),
                    Lesson(title="Variables and Types", content="Numbers, strings, lists, dicts", order=2),
                    Lesson(title="Control Flow", content="if/else, loops", order=3),
                    Lesson(title="Functions", content="Defining and using functions", order=4),
                ],
            )
            create_document("course", py_course)
            created["courses"] += 1

        if not get_documents("course", {"slug": "modern-javascript"}, limit=1):
            js_course = Course(
                language="JavaScript",
                title="Modern JavaScript",
                slug="modern-javascript",
                description="ES6+ features and building interactive pages.",
                level="beginner",
                duration="5 hours",
                lessons=[
                    Lesson(title="JS Fundamentals", content="Variables, types, operators", order=1),
                    Lesson(title="Functions & Scope", content="Function types, closures", order=2),
                    Lesson(title="Async JS", content="Promises, async/await", order=3),
                    Lesson(title="DOM", content="Selecting and manipulating elements", order=4),
                ],
            )
            create_document("course", js_course)
            created["courses"] += 1

        return {"status": "ok", "created": created}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
