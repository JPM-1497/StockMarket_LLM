from .base_class import Base

# Import all models here to register them for Alembic migrations
import models.user
import models.strategy
import models.stock
import models.historical_price
import models.news_article
