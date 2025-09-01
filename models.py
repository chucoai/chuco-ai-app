"""
Database models for Chuco AI application
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, Enum
from sqlalchemy.sql import func
from database import Base
import enum


class InquiryStatus(str, enum.Enum):
    """Status options for inquiries"""

    NEW = "new"
    CONTACTED = "contacted"
    IN_PROGRESS = "in_progress"
    QUALIFIED = "qualified"
    NOT_QUALIFIED = "not_qualified"
    CONVERTED = "converted"
    CLOSED = "closed"


class ServiceType(str, enum.Enum):
    """Service types offered"""

    AI_AUDIT = "ai_audit"
    CHATBOT_LLM = "chatbot_llm"
    DATA_STRATEGY = "data_strategy"
    PROCESS_AUTOMATION = "process_automation"
    AI_TRAINING = "ai_training"
    ONGOING_SUPPORT = "ongoing_support"
    OTHER = "other"


class ContactInquiry(Base):
    """Model for storing contact form submissions and inquiries"""

    __tablename__ = "contact_inquiries"

    id = Column(Integer, primary_key=True, index=True)

    # Contact Information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    company_name = Column(String(255), nullable=True)
    company_website = Column(String(255), nullable=True)

    # Business Information
    company_size = Column(String(50), nullable=True)  # e.g., "5-10", "10-50", "50-100"
    industry = Column(String(100), nullable=True)
    annual_revenue = Column(String(50), nullable=True)  # Revenue range

    # Inquiry Details
    service_interested = Column(Enum(ServiceType), default=ServiceType.OTHER)
    message = Column(Text, nullable=False)
    project_timeline = Column(
        String(50), nullable=True
    )  # e.g., "immediate", "1-3 months", "3-6 months"
    budget_range = Column(String(50), nullable=True)  # e.g., "$5k-$10k", "$10k-$50k"

    # Lead Scoring
    lead_score = Column(Float, default=0.0)  # 0-100 score
    lead_source = Column(
        String(100), nullable=True
    )  # e.g., "website", "referral", "google"
    referral_source = Column(String(255), nullable=True)  # Specific referral details

    # Status and Tracking
    status = Column(Enum(InquiryStatus), default=InquiryStatus.NEW)
    assigned_to = Column(String(100), nullable=True)  # Team member assigned

    # Technical Information
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    utm_source = Column(String(100), nullable=True)
    utm_medium = Column(String(100), nullable=True)
    utm_campaign = Column(String(100), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    contacted_at = Column(DateTime(timezone=True), nullable=True)

    # Communication Preferences
    preferred_contact_method = Column(String(20), default="email")  # email, phone, text
    best_time_to_contact = Column(String(50), nullable=True)

    # Notes
    internal_notes = Column(Text, nullable=True)  # For team use only

    def __repr__(self):
        return (
            f"<ContactInquiry {self.first_name} {self.last_name} - {self.company_name}>"
        )

    def get_full_name(self):
        """Return full name of contact"""
        return f"{self.first_name} {self.last_name}"

    def calculate_lead_score(self):
        """Calculate lead score based on various factors"""
        score = 0.0

        # Company size scoring
        if self.company_size:
            if "50" in self.company_size:
                score += 20
            elif "10" in self.company_size:
                score += 15
            else:
                score += 10

        # Budget scoring
        if self.budget_range:
            if "50k" in self.budget_range or "100k" in self.budget_range:
                score += 30
            elif "25k" in self.budget_range:
                score += 20
            elif "10k" in self.budget_range:
                score += 15
            else:
                score += 5

        # Timeline scoring
        if self.project_timeline:
            if "immediate" in self.project_timeline.lower():
                score += 25
            elif "1-3" in self.project_timeline:
                score += 20
            elif "3-6" in self.project_timeline:
                score += 10
            else:
                score += 5

        # Service type scoring
        if self.service_interested in [
            ServiceType.CHATBOT_LLM,
            ServiceType.DATA_STRATEGY,
        ]:
            score += 15
        elif self.service_interested == ServiceType.AI_AUDIT:
            score += 10
        else:
            score += 5

        # Has company website
        if self.company_website:
            score += 5

        # Has phone number
        if self.phone:
            score += 5

        self.lead_score = min(score, 100)  # Cap at 100
        return self.lead_score


class EmailLog(Base):
    """Model for tracking email notifications sent"""

    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)

    # Email Details
    recipient_email = Column(String(255), nullable=False)
    recipient_name = Column(String(255), nullable=True)
    subject = Column(String(500), nullable=False)
    body = Column(Text, nullable=False)
    email_type = Column(
        String(50), nullable=False
    )  # e.g., "inquiry_notification", "inquiry_confirmation"

    # Related Inquiry
    inquiry_id = Column(Integer, nullable=True)  # Reference to ContactInquiry

    # Status
    sent_successfully = Column(Boolean, default=False)
    error_message = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    sent_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<EmailLog {self.email_type} to {self.recipient_email}>"
