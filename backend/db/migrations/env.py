import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# ✅ Step 1: Ensure app base and .env path are discoverable
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(BASE_DIR)

# ✅ Step 2: Load .env from root of project
from dotenv import load_dotenv
<<<<<<< HEAD
dotenv_path = os.path.join(BASE_DIR, 'db', '.env')
=======
dotenv_path = os.path.join(BASE_DIR, '.env')
>>>>>>> b8fb39c1e47ecb3da4bad163fb4f4a234c37e7be
load_dotenv(dotenv_path)

print(f"[env.py] Loading .env from: {dotenv_path}")
print(f"[env.py] DATABASE_URL = {os.getenv('DATABASE_URL')}")


# ✅ Step 3: Fail fast if env is still not loaded
db_url = os.getenv("DATABASE_URL")
if not db_url:
<<<<<<< HEAD

=======
>>>>>>> b8fb39c1e47ecb3da4bad163fb4f4a234c37e7be
    raise RuntimeError("DATABASE_URL is not set. Check your .env file or .env path in env.py")

# ✅ Step 4: Inject into Alembic config
config = context.config
fileConfig(config.config_file_name)
config.set_main_option("sqlalchemy.url", db_url)

# ✅ Step 5: Import models & metadata for autogeneration
from db.base import Base
from models.user import User
from models.strategy import Strategy
from models.historical_price import HistoricalPrice  # <- include this!

<<<<<<< HEAD

=======
>>>>>>> b8fb39c1e47ecb3da4bad163fb4f4a234c37e7be
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

