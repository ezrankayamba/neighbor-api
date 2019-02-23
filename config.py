# config.py


class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    # DEBUG = False
    DEBUG = True


app_config = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}
