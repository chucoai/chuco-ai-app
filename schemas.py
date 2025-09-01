"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from models import InquiryStatus, ServiceType


class ContactFormBase(BaseModel):
    """Base schema for contact form"""

    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    company_name: Optional[str] = Field(
        None, max_length=255, description="Company name"
    )
    company_website: Optional[str] = Field(
        None, max_length=255, description="Company website"
    )
    message: str = Field(
        ..., min_length=10, max_length=5000, description="Inquiry message"
    )

    @validator("phone")
    def validate_phone(cls, v):
        if v:
            # Remove common formatting characters
            cleaned = "".join(filter(str.isdigit, v))
            if len(cleaned) < 10 or len(cleaned) > 15:
                raise ValueError("Invalid phone number")
        return v

    @validator("company_website")
    def validate_website(cls, v):
        if v and not (v.startswith("http://") or v.startswith("https://")):
            v = f"https://{v}"
        return v


class ContactFormCreate(ContactFormBase):
    """Schema for creating a new contact inquiry"""

    company_size: Optional[str] = Field(None, description="Company size range")
    industry: Optional[str] = Field(None, max_length=100, description="Industry")
    annual_revenue: Optional[str] = Field(None, description="Annual revenue range")
    service_interested: Optional[ServiceType] = Field(
        ServiceType.OTHER, description="Service interested in"
    )
    project_timeline: Optional[str] = Field(None, description="Project timeline")
    budget_range: Optional[str] = Field(None, description="Budget range")
    preferred_contact_method: Optional[str] = Field(
        "email", description="Preferred contact method"
    )
    best_time_to_contact: Optional[str] = Field(
        None, description="Best time to contact"
    )

    # Hidden fields for tracking
    lead_source: Optional[str] = Field(None, description="Lead source")
    utm_source: Optional[str] = Field(None, description="UTM source parameter")
    utm_medium: Optional[str] = Field(None, description="UTM medium parameter")
    utm_campaign: Optional[str] = Field(None, description="UTM campaign parameter")

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@company.com",
                "phone": "(915) 555-0123",
                "company_name": "ABC Corporation",
                "company_website": "www.abccorp.com",
                "company_size": "10-50",
                "industry": "E-commerce",
                "annual_revenue": "$1M-$5M",
                "service_interested": "chatbot_llm",
                "message": "We're interested in implementing an AI chatbot for customer service.",
                "project_timeline": "1-3 months",
                "budget_range": "$10k-$25k",
                "preferred_contact_method": "email",
            }
        }


class ContactFormResponse(ContactFormBase):
    """Schema for contact inquiry response"""

    id: int
    status: InquiryStatus
    lead_score: float
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ContactFormListResponse(BaseModel):
    """Schema for listing contact inquiries"""

    total: int
    inquiries: List[ContactFormResponse]


class InquiryUpdateStatus(BaseModel):
    """Schema for updating inquiry status"""

    status: InquiryStatus
    internal_notes: Optional[str] = Field(
        None, description="Internal notes about the inquiry"
    )
    assigned_to: Optional[str] = Field(
        None, description="Team member assigned to this inquiry"
    )


class EmailNotificationRequest(BaseModel):
    """Schema for email notification requests"""

    recipient_email: EmailStr
    recipient_name: str
    subject: str
    template: str = Field(..., description="Email template to use")
    context: dict = Field(
        default_factory=dict, description="Context variables for template"
    )


class SuccessResponse(BaseModel):
    """Generic success response"""

    success: bool = True
    message: str
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    """Generic error response"""

    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[dict] = None


class HealthCheckResponse(BaseModel):
    """Health check response"""

    status: str
    message: str
    timestamp: datetime
    version: str
    database_connected: bool = False
