import httpx
from config import settings
import logging

logger = logging.getLogger(__name__)

async def verify_recaptcha(token: str) -> bool:
    """Verify reCAPTCHA token with Google"""
    
    if not settings.RECAPTCHA_ENABLED:
        return True  # Skip if disabled
    
    if not token:
        return False
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data={
                    "secret": settings.RECAPTCHA_SECRET_KEY,
                    "response": token
                }
            )
            result = response.json()
            return result.get("success", False)
    except Exception as e:
        logger.error(f"reCAPTCHA verification failed: {e}")
        return False
