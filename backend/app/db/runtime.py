from app.core.config import get_settings
from app.db import models  # noqa: F401
from app.db.database import create_database, create_session_factory

settings = get_settings()
session_factory = create_session_factory(settings.database_url)
create_database(settings.database_url, session_factory)
