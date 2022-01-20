class BaseConfig():
    DEBUG = False
    TESTING = False

class DevelopmentConfig(BaseConfig):
    FLASK_ENV = "development"
    DEBUG = True
    # Mongo URLs

class TestingConfig(BaseConfig):
    DEBUG = True
    FLASK_ENV = "testing"
    TESTING = True
    
class ProductionConfig(BaseConfig):
    FLASK_ENV = "production"
