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
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============= CONFIGURATION =============
# Set these in environment variables or .env file for production
RECAPTCHA_ENABLED = True  # Set to True to enable reCAPTCHA
RECAPTCHA_SITE_KEY = "6LfK3LkrAAAAAOTdm__jSIA-iwQT5fvXFdaO4k66"  # Replace with your site key
RECAPTCHA_SECRET_KEY = "6LfK3LkrAAAAAPwgail8-m8eQYNFS681KrP3qwdh"  # Replace with your secret key

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
    honeypot: Optional[str] = None  # Honeypot field for spam protection


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


# ============= RECAPTCHA VERIFICATION =============

async def verify_recaptcha(token: str) -> bool:
    """Verify reCAPTCHA token with Google"""
    if not RECAPTCHA_ENABLED:
        return True  # Skip verification if disabled
    
    if not token:
        return False
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data={
                    "secret": RECAPTCHA_SECRET_KEY,
                    "response": token
                }
            )
            result = response.json()
            return result.get("success", False)
    except Exception as e:
        logger.error(f"reCAPTCHA verification error: {str(e)}")
        return False


# ============= STORAGE =============
# Simple in-memory storage for inquiries (replace with database in production)
inquiries_storage = []


# ============= PAGE ROUTES =============

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render home page"""
    context = {
        "request": request,
        "recaptcha_enabled": RECAPTCHA_ENABLED,
        "recaptcha_site_key": RECAPTCHA_SITE_KEY if RECAPTCHA_ENABLED else None
    }
    return templates.TemplateResponse("index.html", context)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Chuco AI is running",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "recaptcha_enabled": RECAPTCHA_ENABLED,
    }


# ============= API ROUTES =============

@app.post("/api/contact")
async def submit_contact_form(
    form_data: ContactForm,
    request: Request,
):
    """
    Submit a contact form inquiry with spam protection
    """
    # Get client IP for rate limiting
    client_ip = request.client.host

    # Check honeypot field (if filled, it's likely a bot)
    if form_data.honeypot:
        logger.warning(f"Honeypot triggered from IP: {client_ip}")
        # Return success to confuse bots, but don't process
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Thank you for your inquiry!",
            }
        )

    # Check rate limit (10 requests per minute)
    if not rate_limiter.is_allowed(client_ip, max_requests=10):
        raise HTTPException(
            status_code=429, 
            detail="Too many requests. Please try again later."
        )

    # Verify reCAPTCHA if enabled
    if RECAPTCHA_ENABLED:
        is_valid = await verify_recaptcha(form_data.recaptcha_token)
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail="reCAPTCHA verification failed. Please try again."
            )

    try:
        # Calculate lead score
        lead_score = calculate_lead_score(form_data)
        
        # Create inquiry record
        inquiry = {
            "id": len(inquiries_storage) + 1,
            "timestamp": datetime.now().isoformat(),
            "first_name": form_data.first_name,
            "last_name": form_data.last_name,
            "email": form_data.email,
            "phone": form_data.phone,
            "company_name": form_data.company_name,
            "company_website": form_data.company_website,
            "company_size": form_data.company_size,
            "industry": form_data.industry,
            "annual_revenue": form_data.annual_revenue,
            "service_interested": form_data.service_interested,
            "message": form_data.message,
            "project_timeline": form_data.project_timeline,
            "budget_range": form_data.budget_range,
            "preferred_contact_method": form_data.preferred_contact_method,
            "best_time_to_contact": form_data.best_time_to_contact,
            "lead_source": form_data.lead_source,
            "utm_source": form_data.utm_source,
            "utm_medium": form_data.utm_medium,
            "utm_campaign": form_data.utm_campaign,
            "lead_score": lead_score,
            "ip_address": client_ip,
            "user_agent": request.headers.get("user-agent"),
            "status": "new"
        }
        
        # Store inquiry (in production, save to database)
        inquiries_storage.append(inquiry)
        
        # Log the inquiry
        logger.info(f"New inquiry #{inquiry['id']} from {form_data.first_name} {form_data.last_name}")
        logger.info(f"Email: {form_data.email} | Phone: {form_data.phone}")
        logger.info(f"Company: {form_data.company_name} | Service: {form_data.service_interested}")
        logger.info(f"Timeline: {form_data.project_timeline} | Lead Score: {lead_score}")
        
        # TODO: In production, you would also:
        # 1. Save to database
        # 2. Send email notification to admin
        # 3. Send confirmation email to user
        # 4. Integrate with CRM (HubSpot, Salesforce, etc.)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Thank you for your inquiry! We'll be in touch within 24 hours.",
                "data": {
                    "inquiry_id": inquiry['id'],
                    "lead_score": lead_score,
                }
            }
        )

    except Exception as e:
        logger.error(f"Error submitting contact form: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request. Please try again."
        )


def calculate_lead_score(form_data: ContactForm) -> int:
    """Calculate lead score based on form data"""
    score = 50  # Base score
    
    # Company information
    if form_data.company_name:
        score += 10
    if form_data.company_website:
        score += 5
    
    # Company size scoring
    if form_data.company_size:
        if "50+" in form_data.company_size or "100+" in form_data.company_size:
            score += 15
        elif "20-49" in form_data.company_size:
            score += 10
        elif "10-19" in form_data.company_size:
            score += 5
    
    # Timeline scoring (urgency)
    if form_data.project_timeline == "Immediate (ASAP)":
        score += 25
    elif form_data.project_timeline == "1-2 months":
        score += 20
    elif form_data.project_timeline == "3-6 months":
        score += 10
    elif form_data.project_timeline == "6+ months":
        score += 5
    
    # Budget scoring
    if form_data.budget_range:
        if "$100,000+" in form_data.budget_range:
            score += 30
        elif "$50,000" in form_data.budget_range:
            score += 25
        elif "$25,000" in form_data.budget_range:
            score += 20
        elif "$10,000" in form_data.budget_range:
            score += 15
        elif "$5,000" in form_data.budget_range:
            score += 10
    
    # Service interest scoring
    if form_data.service_interested:
        high_value_services = ["Custom AI Chatbots", "Data Strategy", "Process Automation"]
        if any(service in form_data.service_interested for service in high_value_services):
            score += 10
    
    # Message quality (has detailed message)
    if form_data.message and len(form_data.message) > 100:
        score += 5
    
    # Cap score at 100
    return min(score, 100)


# ============= ADMIN ENDPOINTS =============

@app.get("/api/inquiries")
async def get_inquiries(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
):
    """
    Get list of inquiries (admin endpoint)
    Note: In production, protect with authentication
    """
    # Filter by status if provided
    filtered_inquiries = inquiries_storage
    if status:
        filtered_inquiries = [inq for inq in inquiries_storage if inq.get("status") == status]
    
    # Sort by timestamp (newest first)
    filtered_inquiries.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Apply pagination
    paginated = filtered_inquiries[offset:offset + limit]
    
    return {
        "success": True,
        "total": len(filtered_inquiries),
        "limit": limit,
        "offset": offset,
        "inquiries": paginated
    }


@app.get("/api/inquiries/{inquiry_id}")
async def get_inquiry(inquiry_id: int):
    """
    Get single inquiry by ID (admin endpoint)
    Note: In production, protect with authentication
    """
    inquiry = next((inq for inq in inquiries_storage if inq['id'] == inquiry_id), None)
    
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    
    return {
        "success": True,
        "inquiry": inquiry
    }


@app.patch("/api/inquiries/{inquiry_id}/status")
async def update_inquiry_status(
    inquiry_id: int,
    status: str
):
    """
    Update inquiry status (admin endpoint)
    Note: In production, protect with authentication
    """
    inquiry = next((inq for inq in inquiries_storage if inq['id'] == inquiry_id), None)
    
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    
    # Update status
    valid_statuses = ["new", "contacted", "qualified", "proposal_sent", "won", "lost"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
    
    inquiry["status"] = status
    inquiry["updated_at"] = datetime.now().isoformat()
    
    return {
        "success": True,
        "message": f"Inquiry status updated to {status}",
        "inquiry": inquiry
    }


@app.get("/api/stats")
async def get_stats():
    """
    Get inquiry statistics (admin endpoint)
    """
    total = len(inquiries_storage)
    today_count = sum(1 for inq in inquiries_storage 
                     if inq['timestamp'].startswith(datetime.now().strftime('%Y-%m-%d')))
    
    status_counts = {}
    for inq in inquiries_storage:
        status = inq.get('status', 'new')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    avg_lead_score = sum(inq.get('lead_score', 0) for inq in inquiries_storage) / max(total, 1)
    
    return {
        "success": True,
        "stats": {
            "total_inquiries": total,
            "today_inquiries": today_count,
            "average_lead_score": round(avg_lead_score, 1),
            "by_status": status_counts
        }
    }


# ============= ERROR HANDLERS =============

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Handle 404 errors"""
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=404, 
            content={"success": False, "message": "Endpoint not found"}
        )
    return templates.TemplateResponse("index.html", {"request": request})


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(exc)}")
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Internal server error"}
        )
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)