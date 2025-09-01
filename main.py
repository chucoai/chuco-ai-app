"""
Main FastAPI application for Chuco AI
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Chuco AI",
    description="AI Consulting Platform for Small & Mid-Size Businesses",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")


# ============= MODELS =============


class ContactForm(BaseModel):
    """Contact form submission model"""

    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    company_name: Optional[str] = None
    company_website: Optional[str] = None
    company_size: Optional[str] = None
    industry: Optional[str] = None
    annual_revenue: Optional[str] = None
    service_interested: str
    message: Optional[str] = None
    project_timeline: str
    budget_range: Optional[str] = None
    preferred_contact_method: Optional[str] = "email"
    best_time_to_contact: Optional[str] = None
    lead_source: Optional[str] = "website"
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    recaptcha_token: Optional[str] = None


# ============= RATE LIMITING =============

from collections import defaultdict
import time


class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)

    def is_allowed(
        self, ip: str, max_requests: int = 10, window_minutes: int = 1
    ) -> bool:
        """Check if request is allowed based on rate limit"""
        now = time.time()
        window = window_minutes * 60

        # Clean old requests
        self.requests[ip] = [
            req_time for req_time in self.requests[ip] if now - req_time < window
        ]

        # Check if limit exceeded
        if len(self.requests[ip]) >= max_requests:
            return False

        # Add current request
        self.requests[ip].append(now)
        return True


rate_limiter = RateLimiter()


# ============= PAGE ROUTES =============


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render home page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Chuco AI is running",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
    }


# ============= API ROUTES =============


@app.post("/api/contact")
async def submit_contact_form(
    form_data: ContactForm,
    request: Request,
):
    """
    Submit a contact form inquiry
    """
    # Get client IP for rate limiting
    client_ip = request.client.host

    # Check rate limit (10 requests per minute)
    if not rate_limiter.is_allowed(client_ip, max_requests=10):
        raise HTTPException(
            status_code=429, detail="Too many requests. Please try again later."
        )

    try:
        # Log the inquiry (in production, save to database)
        logger.info(f"New inquiry from {form_data.first_name} {form_data.last_name}")
        logger.info(f"Email: {form_data.email}")
        logger.info(f"Phone: {form_data.phone}")
        logger.info(f"Company: {form_data.company_name}")
        logger.info(f"Service: {form_data.service_interested}")
        logger.info(f"Timeline: {form_data.project_timeline}")
        logger.info(f"Message: {form_data.message}")

        # Calculate a simple lead score
        lead_score = 50  # Base score
        if form_data.company_name:
            lead_score += 10
        if form_data.project_timeline == "Immediate (ASAP)":
            lead_score += 20
        elif form_data.project_timeline == "1-2 months":
            lead_score += 15
        elif form_data.project_timeline == "3-6 months":
            lead_score += 10

        if form_data.budget_range:
            if "$50,000+" in form_data.budget_range:
                lead_score += 25
            elif "$25,000" in form_data.budget_range:
                lead_score += 20
            elif "$10,000" in form_data.budget_range:
                lead_score += 15

        # TODO: In production, you would:
        # 1. Save to database
        # 2. Send email notification to admin
        # 3. Send confirmation email to user

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Thank you for your inquiry! We'll be in touch within 24 hours.",
                "data": {
                    "lead_score": lead_score,
                },
            },
        )

    except Exception as e:
        logger.error(f"Error submitting contact form: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request. Please try again.",
        )


# ============= ADMIN ENDPOINTS (Basic) =============

# Store inquiries in memory for now (in production, use database)
inquiries_storage = []


@app.get("/api/inquiries")
async def get_inquiries(
    limit: int = 50,
    offset: int = 0,
):
    """
    Get list of inquiries (admin endpoint)
    Note: In production, this should be protected with authentication
    """
    # Return stored inquiries (in production, query from database)
    return {
        "total": len(inquiries_storage),
        "inquiries": inquiries_storage[offset : offset + limit],
    }


# ============= ERROR HANDLERS =============


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Handle 404 errors"""
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=404, content={"success": False, "message": "Endpoint not found"}
        )
    return templates.TemplateResponse("index.html", {"request": request})


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(exc)}")
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Internal server error"},
        )
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
