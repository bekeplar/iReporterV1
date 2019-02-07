import os

class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    JSON_SORT_KEYS = False

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ENV = "Development"
    DATABASE_URI = 'postgres://postgres:bekeplar@localhost:5432/postgres'

class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = 'postgres://postgres:bekeplar@localhost:5432/postgres'

runtime_mode = "Testing"
app_config = {
    "Development": DevelopmentConfig,
    "Testing": TestingConfig,
    "Production": ProductionConfig
}

