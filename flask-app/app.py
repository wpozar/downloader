import os

from api import create_app

config = {
    'ENV': os.getenv('FLASK_ENV', 'production'),
    'DEBUG': os.getenv('FLASK_DEBUG', False),
    'TESTING': os.getenv('FLASK_TESTING', False),
    'REDIS_URL': os.getenv('FLASK_REDIS_URL', 'redis://redis:6379/0')
}

app = create_app(config=config)

if __name__ == '__main__':
    app.run()
