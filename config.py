import os

class Config:
    # Discord Configuration
    DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN', '')

    # Application Configuration
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

    # 除外するロール名のリスト
    EXCLUDED_ROLES = ['@everyone']