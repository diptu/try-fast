# app/db/init_db.py
"""
Async-safe initialization for database models.
"""

# Ensure all models are imported so they are registered with Base
import app.models  # noqa: F401
