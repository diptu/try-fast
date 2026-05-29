"""
Async-safe initialization for database models.
"""

# Ensure all models are imported so they are registered with Base
import user_service.models  # noqa: F401


def import_all_models() -> None:
    """
    Ensure all SQLAlchemy models are imported before
    metadata/table creation.
    """

    import user_service.models.address  # noqa: F401
    import user_service.models.social  # noqa: F401
    import user_service.models.user  # noqa: F401
