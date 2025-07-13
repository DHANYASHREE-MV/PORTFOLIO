from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Dhanyashree Portfolio API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class ContactMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="new")

class ContactMessageCreate(BaseModel):
    name: str
    email: str
    message: str

class PortfolioStats(BaseModel):
    total_projects: int = 4
    leadership_roles: int = 2
    technologies: int = 15
    contact_messages: int = 0

# Portfolio data
portfolio_data = {
    "personal_info": {
        "name": "DHANYASHREE M V",
        "title": "AI/ML Engineering Student",
        "email": "dhanyashreem@gmail.com",
        "phone": "+91 8860769397",
        "location": "Bengaluru, Karnataka",
        "linkedin": "https://www.linkedin.com/in/dhanyashree-mv-27d/",
        "github": "https://github.com/DHANYASHREE-MV",
        "objective": "Enthusiastic AI/ML engineering student exploring roles in software development and AI, driven to build intelligent, user-focused solutions through code and creativity."
    },
    "education": [
        {
            "degree": "Bachelor of Engineering",
            "institution": "Dayananda Sagar College Of Engineering",
            "branch": "Artificial Intelligence and Machine Learning",
            "duration": "2022 - 2026"
        },
        {
            "degree": "Pre-University Course",
            "institution": "MES PU College",
            "branch": "Science PCMB",
            "duration": "2020 - 2022"
        }
    ],
    "skills": {
        "technical": ["NumPy", "Pandas", "PyTorch", "TensorFlow", "Keras", "Sklearn", "Docker", "Matlab", "Tableau"],
        "programming": ["Python", "R", "C", "JavaScript", "HTML", "CSS"],
        "soft_skills": ["Problem Solving", "Teamwork", "Adaptability", "Time Management", "Communication"]
    },
    "experience": [
        {
            "title": "Co-Lead Content Team",
            "organization": "The Central Committee - DSCE",
            "year": "2025",
            "responsibilities": [
                "Spearheaded content strategy and editorial management for consistent, impactful messaging",
                "Coordinated team efforts to deliver high-quality communications aligned with organizational goals"
            ]
        },
        {
            "title": "Event Management Volunteer",
            "organization": "E-Summit - IEDC",
            "year": "2023",
            "responsibilities": [
                "Assisted in planning and coordinating event activities for seamless execution",
                "Supported participant engagement to enhance overall event experience"
            ]
        }
    ],
    "projects": [
        {
            "name": "PURE FLOW",
            "subtitle": "IoT-Based Water Quality Monitoring System",
            "description": "Designed and implemented an Arduino ESP32 system equipped with multiple sensors to perform real-time water quality monitoring, capturing parameters like pH, turbidity, and temperature. Integrated cloud connectivity and IoT visualization by linking the system to the Blynk platform, enabling remote data access, live monitoring, and real-time alerts.",
            "technologies": ["Arduino ESP32", "IoT", "Blynk", "Sensors"]
        },
        {
            "name": "DIAGNO-GENIE",
            "subtitle": "Machine Learning Multiple Disease Prediction System",
            "description": "Built a web-based Multiple Disease Prediction System using machine learning to predict Diabetes, Heart Disease, and Parkinson's Disease from user input. Developed ML pipelines for training and evaluation, with integrated experiment tracking and artifact logging via MLflow. The application features an interactive Streamlit interface, automated model reporting, and Docker-based deployment for portability.",
            "technologies": ["Machine Learning", "Streamlit", "MLflow", "Docker", "Python"]
        },
        {
            "name": "WILD GUARD AI",
            "subtitle": "Deep Learning + Computer Vision",
            "description": "Developed a real-time wildlife monitoring system using YOLOv11 for detecting poachers, rangers, and tourists from camera images. Integrated a Streamlit-based frontend to support real-time image uploads and display detection results in an interactive, scrollable layout. Implemented automated SMS alerts via Twilio API to notify authorities instantly when poachers are detected.",
            "technologies": ["YOLOv11", "Computer Vision", "Streamlit", "Twilio API", "Deep Learning"]
        },
        {
            "name": "OZONE LEVEL FORECASTING",
            "subtitle": "Air Quality Visualization System",
            "description": "Developed a deep learning-based ozone forecasting system using LSTM models to predict monthly ozone levels from 2024 to 2027 across seven major locations in Bangalore, aimed at improving air quality insights and supporting public health awareness initiatives. The project leveraged Python, TensorFlow, Keras, Pandas, NumPy, Matplotlib, Seaborn, and Streamlit, with all data processed from structured CSV files for multi-location forecasting.",
            "technologies": ["LSTM", "TensorFlow", "Keras", "Data Visualization", "Streamlit"]
        }
    ],
    "extra_curricular": [
        "Blog Writing", "Coding", "Developing", "Dancing", "Binge-watching"
    ],
    "leadership": "Co-led the content team, overseeing strategy, creation, and quality control across multiple platforms. Collaborated with cross-functional teams to ensure consistent, engaging, and impactful communication."
}

# API Routes
@api_router.get("/")
async def root():
    return {"message": "Dhanyashree Portfolio API", "status": "active"}

@api_router.get("/portfolio")
async def get_portfolio():
    """Get complete portfolio data"""
    return portfolio_data

@api_router.get("/portfolio/stats", response_model=PortfolioStats)
async def get_portfolio_stats():
    """Get portfolio statistics"""
    try:
        # Count contact messages
        message_count = await db.contact_messages.count_documents({})
        
        stats = PortfolioStats(
            total_projects=len(portfolio_data["projects"]),
            leadership_roles=len(portfolio_data["experience"]),
            technologies=len(portfolio_data["skills"]["technical"]) + len(portfolio_data["skills"]["programming"]),
            contact_messages=message_count
        )
        return stats
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return PortfolioStats()

@api_router.post("/contact", response_model=ContactMessage)
async def create_contact_message(contact_data: ContactMessageCreate):
    """Submit a contact form message"""
    try:
        contact_dict = contact_data.dict()
        contact_obj = ContactMessage(**contact_dict)
        
        # Insert into database
        result = await db.contact_messages.insert_one(contact_obj.dict())
        
        if result.inserted_id:
            logger.info(f"Contact message received from {contact_obj.email}")
            return contact_obj
        else:
            raise HTTPException(status_code=500, detail="Failed to save contact message")
            
    except Exception as e:
        logger.error(f"Error saving contact message: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.get("/contact/messages", response_model=List[ContactMessage])
async def get_contact_messages():
    """Get all contact messages (admin endpoint)"""
    try:
        messages = await db.contact_messages.find().sort("timestamp", -1).to_list(100)
        return [ContactMessage(**message) for message in messages]
    except Exception as e:
        logger.error(f"Error retrieving contact messages: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve messages")

@api_router.get("/skills")
async def get_skills():
    """Get skills categorized by type"""
    return portfolio_data["skills"]

@api_router.get("/projects")
async def get_projects():
    """Get all projects"""
    return portfolio_data["projects"]

@api_router.get("/experience")
async def get_experience():
    """Get work experience"""
    return portfolio_data["experience"]

@api_router.get("/education")
async def get_education():
    """Get education details"""
    return portfolio_data["education"]

# Legacy routes for backward compatibility
@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}