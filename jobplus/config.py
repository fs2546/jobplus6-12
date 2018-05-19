class BaseConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '\xd6+@+\xc6\x03\xaa\r>o>c\xb3\x1f2z\x9c;\x8f\xbaXoo\xc9'
    INDEX_PER_PAGE = 9
    ADMIN_PER_PAGE = 15
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost:3306/jobplus?charset=utf8'
class ProductionConfig(BaseConfig):
    pass
class TestingConfig(BaseConfig):
    pass
configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
