import sys
import os

# ✅ Add /app/backend to sys.path so imports like db.base work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# ✅ Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# ✅ Import Base and models to expose metadata for Alembic
from db.base import Base
from models.user import User  # Add other models as needed

# ✅ Configure Alembic
config = context.config
fileConfig(config.config_file_name)

# ✅ Inject DB URL from .env into Alembic config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# ✅ Set target metadata
target_metadata = Base.metadata
