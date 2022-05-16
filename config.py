class Config(object):
    DEBUG = False
    TESTING = False
    INIT_FIRST = False
    T_REFRESH = "refresh"
    SECRET_KEY = "xblocks2022"
    SECRET_KEY_REFRESH = "xblocks2022_reload"
    JWT_ACCESS_TOKEN_EXPIRES = 1
    JWT_REFRESH_TOKEN_EXPIRES = 30
    
class Development(Config):
    DEBUG = True
    ENV_VALUE = "Development"
    INIT_FIRST = True
    T_REFRESH = "refresh"
    SECRET_KEY = "xblocks2022"
    SECRET_KEY_REFRESH = "xblocks2022_reload"
    JWT_ACCESS_TOKEN_EXPIRES = 1
    JWT_REFRESH_TOKEN_EXPIRES = 30

class Testing(Config):
    TESTING = True
    DEBUG = True
    INIT_FIRST = False
    T_REFRESH = "refresh"
    SECRET_KEY = "xblocks2022"
    SECRET_KEY_REFRESH = "xblocks2022_reload"
    JWT_ACCESS_TOKEN_EXPIRES = 1
    JWT_REFRESH_TOKEN_EXPIRES = 30
class Production(Config):
    DEBUG = False
    INIT_FIRST = False
    T_REFRESH = "refresh"
    SECRET_KEY = "xblocks2022"
    SECRET_KEY_REFRESH = "xblocks2022_reload"
    JWT_ACCESS_TOKEN_EXPIRES = 1
    JWT_REFRESH_TOKEN_EXPIRES = 30