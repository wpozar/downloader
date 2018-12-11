from rq import Connection, Worker

from downloader import redis
from downloader.tasks import get_image, get_website

if __name__ == '__main__':
    with Connection(connection=redis):
        """Worker entry point"""

        w = Worker(['tasks'])
        w.work()
