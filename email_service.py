"""
Email service for sending notifications
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
from datetime import datetime
import logging
from jinja2 import Template

from config import settings
from models import EmailLog, ContactInquiry
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class EmailService:
    """Service for handling email notifications"""

    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM_EMAIL
        self.from_name = settings.SMTP_FROM_NAME
        self.admin_email = settings.ADMIN_EMAIL
        self.enabled = settings.SEND_EMAIL_NOTIFICATIONS

    def send_email(
        self,
        to_email: str,
        subject: str,
        body_html: str,
        body_text: Optional[str] = None,
        reply_to: Optional[str] = None,
    ) -> bool:
        """
        Send an email using SMTP

        Args:
            to_email: Recipient email address
            subject: Email subject
            body_html: HTML body content
            body_text: Plain text body content (optional)
            reply_to: Reply-to email address (optional)

        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.enabled:
            logger.info(f"Email notifications disabled. Would send to: {to_email}")
            return True

        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = to_email

            if reply_to:
                msg["Reply-To"] = reply_to

            # Add plain text part
            if body_text:
                text_part = MIMEText(body_text, "plain")
                msg.attach(text_part)

            # Add HTML part
            html_part = MIMEText(body_html, "html")
            msg.attach(html_part)

            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                if self.smtp_user and self.smtp_password:
                    server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False

    def send_inquiry_notification_to_admin(
        self, inquiry: ContactInquiry, db: Session
    ) -> bool:
        """
        Send notification to admin about new inquiry

        Args:
            inquiry: ContactInquiry object
            db: Database session

        Returns:
            True if email sent successfully
        """
        subject = f"New Inquiry from {inquiry.get_full_name()} - {inquiry.company_name or 'Individual'}"

        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: linear-gradient(135deg, #8B5CF6 0%, #A855F7 100%); color: white; padding: 20px; border-radius: 8px 8px 0 0; }
                .content { background: #f9f9f9; padding: 20px; border-radius: 0 0 8px 8px; }
                .field { margin-bottom: 15px; }
                .label { font-weight: bold; color: #555; }
                .value { color: #333; margin-left: 10px; }
                .message-box { background: white; padding: 15px; border-left: 4px solid #8B5CF6; margin: 20px 0; }
                .lead-score { display: inline-block; padding: 5px 10px; border-radius: 20px; color: white; font-weight: bold; }
                .high-score { background: #10b981; }
                .medium-score { background: #f59e0b; }
                .low-score { background: #ef4444; }
                .cta-button { display: inline-block; padding: 10px 20px; background: #8B5CF6; color: white; text-decoration: none; border-radius: 5px; margin-top: 15px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>🎯 New Inquiry Received!</h2>
                    <p>Lead Score: <span class="lead-score {{ 'high-score' if lead_score >= 70 else 'medium-score' if lead_score >= 40 else 'low-score' }}">{{ lead_score }}%</span></p>
                </div>
                <div class="content">
                    <h3>Contact Information</h3>
                    <div class="field">
                        <span class="label">Name:</span>
                        <span class="value">{{ full_name }}</span>
                    </div>
                    <div class="field">
                        <span class="label">Email:</span>
                        <span class="value"><a href="mailto:{{ email }}">{{ email }}</a></span>
                    </div>
                    {% if phone %}
                    <div class="field">
                        <span class="label">Phone:</span>
                        <span class="value"><a href="tel:{{ phone }}">{{ phone }}</a></span>
                    </div>
                    {% endif %}
                    
                    <h3>Company Details</h3>
                    {% if company_name %}
                    <div class="field">
                        <span class="label">Company:</span>
                        <span class="value">{{ company_name }}</span>
                    </div>
                    {% endif %}
                    {% if company_website %}
                    <div class="field">
                        <span class="label">Website:</span>
                        <span class="value"><a href="{{ company_website }}">{{ company_website }}</a></span>
                    </div>
                    {% endif %}
                    {% if company_size %}
                    <div class="field">
                        <span class="label">Company Size:</span>
                        <span class="value">{{ company_size }} employees</span>
                    </div>
                    {% endif %}
                    {% if industry %}
                    <div class="field">
                        <span class="label">Industry:</span>
                        <span class="value">{{ industry }}</span>
                    </div>
                    {% endif %}
                    
                    <h3>Project Information</h3>
                    <div class="field">
                        <span class="label">Service Interested:</span>
                        <span class="value">{{ service_interested }}</span>
                    </div>
                    {% if project_timeline %}
                    <div class="field">
                        <span class="label">Timeline:</span>
                        <span class="value">{{ project_timeline }}</span>
                    </div>
                    {% endif %}
                    {% if budget_range %}
                    <div class="field">
                        <span class="label">Budget:</span>
                        <span class="value">{{ budget_range }}</span>
                    </div>
                    {% endif %}
                    
                    <h3>Message</h3>
                    <div class="message-box">
                        {{ message }}
                    </div>
                    
                    <div class="field">
                        <span class="label">Submitted:</span>
                        <span class="value">{{ submitted_at }}</span>
                    </div>
                    
                    {% if utm_source or lead_source %}
                    <h3>Attribution</h3>
                    {% if lead_source %}
                    <div class="field">
                        <span class="label">Lead Source:</span>
                        <span class="value">{{ lead_source }}</span>
                    </div>
                    {% endif %}
                    {% if utm_source %}
                    <div class="field">
                        <span class="label">Campaign:</span>
                        <span class="value">{{ utm_source }} / {{ utm_medium }} / {{ utm_campaign }}</span>
                    </div>
                    {% endif %}
                    {% endif %}
                </div>
            </div>
        </body>
        </html>
        """

        # Prepare template context
        service_names = {
            "ai_audit": "AI Opportunity Audit",
            "chatbot_llm": "Custom AI Chatbots & LLM Integration",
            "data_strategy": "Data Strategy & Architecture",
            "process_automation": "Process Automation",
            "ai_training": "AI Training & Change Management",
            "ongoing_support": "Ongoing AI Support",
            "other": "Other / General Inquiry",
        }

        context = {
            "full_name": inquiry.get_full_name(),
            "email": inquiry.email,
            "phone": inquiry.phone,
            "company_name": inquiry.company_name,
            "company_website": inquiry.company_website,
            "company_size": inquiry.company_size,
            "industry": inquiry.industry,
            "service_interested": service_names.get(
                (
                    inquiry.service_interested.value
                    if inquiry.service_interested
                    else "other"
                ),
                "Other",
            ),
            "project_timeline": inquiry.project_timeline,
            "budget_range": inquiry.budget_range,
            "message": inquiry.message,
            "lead_score": inquiry.lead_score,
            "submitted_at": inquiry.created_at.strftime("%B %d, %Y at %I:%M %p"),
            "lead_source": inquiry.lead_source,
            "utm_source": inquiry.utm_source,
            "utm_medium": inquiry.utm_medium,
            "utm_campaign": inquiry.utm_campaign,
        }

        # Render template
        template = Template(html_template)
        html_body = template.render(**context)

        # Send email
        success = self.send_email(
            to_email=self.admin_email,
            subject=subject,
            body_html=html_body,
            reply_to=inquiry.email,
        )

        # Log email
        email_log = EmailLog(
            recipient_email=self.admin_email,
            recipient_name=settings.ADMIN_NAME,
            subject=subject,
            body=html_body,
            email_type="inquiry_notification",
            inquiry_id=inquiry.id,
            sent_successfully=success,
            sent_at=datetime.now() if success else None,
        )
        db.add(email_log)
        db.commit()

        return success

    def send_inquiry_confirmation(self, inquiry: ContactInquiry, db: Session) -> bool:
        """
        Send confirmation email to the person who submitted the inquiry

        Args:
            inquiry: ContactInquiry object
            db: Database session

        Returns:
            True if email sent successfully
        """
        subject = "Thank you for contacting Chuco AI"

        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: linear-gradient(135deg, #8B5CF6 0%, #A855F7 100%); color: white; padding: 30px; border-radius: 8px 8px 0 0; text-align: center; }
                .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }
                .cta-button { display: inline-block; padding: 12px 25px; background: #8B5CF6; color: white; text-decoration: none; border-radius: 25px; margin: 20px 0; }
                .footer { text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; }
                .services-list { background: white; padding: 20px; border-radius: 8px; margin: 20px 0; }
                .service-item { padding: 10px 0; border-bottom: 1px solid #eee; }
                .service-item:last-child { border-bottom: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to Chuco AI!</h1>
                    <p>Your AI Transformation Journey Starts Here</p>
                </div>
                <div class="content">
                    <h2>Hi {{ first_name }},</h2>
                    
                    <p>Thank you for reaching out to Chuco AI! We've received your inquiry and are excited about the possibility of helping {{ company_name if company_name else 'your business' }} leverage AI to streamline operations and boost revenue.</p>
                    
                    <p><strong>What happens next?</strong></p>
                    <ul>
                        <li>Our team will review your inquiry within 24 hours</li>
                        <li>We'll reach out to schedule a free consultation call</li>
                        <li>During the call, we'll discuss your specific needs and how AI can help</li>
                        <li>You'll receive a customized proposal based on your requirements</li>
                    </ul>
                    
                    {% if service_interested and service_interested != 'other' %}
                    <p>Based on your interest in <strong>{{ service_name }}</strong>, here's a quick overview of how we can help:</p>
                    
                    <div class="services-list">
                        {% if service_interested == 'ai_audit' %}
                        <div class="service-item">
                            <strong>AI Opportunity Audit:</strong> We'll analyze your current workflows, identify automation opportunities, and create a roadmap for AI implementation tailored to your business.
                        </div>
                        {% elif service_interested == 'chatbot_llm' %}
                        <div class="service-item">
                            <strong>Custom AI Chatbots & LLM Integration:</strong> We'll build intelligent chatbots that understand your business, handle customer inquiries, and generate qualified leads 24/7.
                        </div>
                        {% elif service_interested == 'data_strategy' %}
                        <div class="service-item">
                            <strong>Data Strategy & Architecture:</strong> We'll design and implement robust data systems that make your business AI-ready and unlock insights from your data.
                        </div>
                        {% elif service_interested == 'process_automation' %}
                        <div class="service-item">
                            <strong>Process Automation:</strong> We'll automate repetitive tasks, streamline workflows, and free up your team to focus on high-value activities.
                        </div>
                        {% elif service_interested == 'ai_training' %}
                        <div class="service-item">
                            <strong>AI Training & Change Management:</strong> We'll ensure your team is equipped to leverage AI tools effectively with hands-on training and support.
                        </div>
                        {% elif service_interested == 'ongoing_support' %}
                        <div class="service-item">
                            <strong>Ongoing AI Support:</strong> We'll provide continuous optimization, maintenance, and expansion of your AI implementations to ensure long-term success.
                        </div>
                        {% endif %}
                    </div>
                    {% endif %}
                    
                    <p><strong>While you wait, here are some resources you might find helpful:</strong></p>
                    <ul>
                        <li><a href="https://chuco.ai/#services">Explore our full range of AI services</a></li>
                        <li><a href="https://chuco.ai/#about">Learn about our 15+ years of experience</a></li>
                    </ul>
                    
                    <p>If you have any immediate questions, feel free to reach out:</p>
                    <p>
                        📧 Email: <a href="mailto:yo@chuco.ai">yo@chuco.ai</a><br>
                        📞 Phone: <a href="tel:+18449152828">(844) 915-2828</a>
                    </p>
                    
                    <center>
                        <a href="https://chuco.ai" class="cta-button">Visit Our Website</a>
                    </center>
                    
                    <div class="footer">
                        <p><strong>Chuco AI</strong><br>
                        Transforming businesses through intelligent automation<br>
                        El Paso, Texas</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        # Prepare template context
        service_names = {
            "ai_audit": "AI Opportunity Audit",
            "chatbot_llm": "Custom AI Chatbots & LLM Integration",
            "data_strategy": "Data Strategy & Architecture",
            "process_automation": "Process Automation",
            "ai_training": "AI Training & Change Management",
            "ongoing_support": "Ongoing AI Support",
        }

        context = {
            "first_name": inquiry.first_name,
            "company_name": inquiry.company_name,
            "service_interested": (
                inquiry.service_interested.value if inquiry.service_interested else None
            ),
            "service_name": service_names.get(
                inquiry.service_interested.value if inquiry.service_interested else "",
                "",
            ),
        }

        # Render template
        template = Template(html_template)
        html_body = template.render(**context)

        # Send email
        success = self.send_email(
            to_email=inquiry.email, subject=subject, body_html=html_body
        )

        # Log email
        email_log = EmailLog(
            recipient_email=inquiry.email,
            recipient_name=inquiry.get_full_name(),
            subject=subject,
            body=html_body,
            email_type="inquiry_confirmation",
            inquiry_id=inquiry.id,
            sent_successfully=success,
            sent_at=datetime.now() if success else None,
        )
        db.add(email_log)
        db.commit()

        return success


# Create global email service instance
email_service = EmailService()
