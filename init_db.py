#!/usr/bin/env python
"""
Database initialization script for Chuco AI
Run this script to create all database tables
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from database import init_db, engine
from models import Base
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_tables():
    """Create all database tables"""
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully!")

        # List created tables
        from sqlalchemy import inspect

        inspector = inspect(engine)
        tables = inspector.get_table_names()

        if tables:
            logger.info(f"Created tables: {', '.join(tables)}")
        else:
            logger.warning("No tables were created. Check your models.")

    except Exception as e:
        logger.error(f"❌ Failed to create tables: {str(e)}")
        sys.exit(1)


def main():
    """Main function"""
    print("=" * 50)
    print("Chuco AI Database Initialization")
    print("=" * 50)

    # Check if .env file exists
    if not os.path.exists(".env"):
        logger.warning("⚠️  .env file not found. Using default settings.")
        logger.info("Copy .env.example to .env and update with your settings.")

    # Create tables
    create_tables()

    print("=" * 50)
    print("Database initialization complete!")
    print("You can now run the application with: python main.py")
    print("=" * 50)


if __name__ == "__main__":
    main()
