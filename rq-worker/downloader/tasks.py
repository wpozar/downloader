import os
import urllib.error
import urllib.request

from rq import Queue

from . import redis
from .downloaders import TextDownloader, ImagesDownloader


def get_website(job_type, job_url, job_hash):
    """Download website, extract text and save to file"""

    if job_type == 'text':
        text_downloader = TextDownloader(job_url=job_url, job_hash=job_hash)
        result = text_downloader.run()
        if result is False:
            redis.hset('jobs', job_hash, -1)
        else:
            redis.hset('jobs', job_hash, 2)
        return

    elif job_type == 'images':
        images_downloader = ImagesDownloader(job_url=job_url, job_hash=job_hash)
        result = images_downloader.run()
        if result is False:
            redis.hset('jobs', job_hash, -1)
            return
        else:
            images = result
            args = (job_hash, images)
            queue = Queue('tasks', connection=redis)
            queue.enqueue_call('worker.get_image', args=args)


def get_image(job_hash, images):
    """Download single image and create new task with remaining images"""

    images_count = len(images)

    # No more images to download, job finished
    if images_count == 0:
        redis.hset('jobs', job_hash, 2)
        return

    # remove last image from list
    image_url = images.pop()

    try:
        with urllib.request.urlopen(image_url) as response:
            file_extension = image_url.split('.')[-1].lower()
            image_path = os.path.join(
                ImagesDownloader.get_job_path(job_hash=job_hash),
                f"{images_count:03d}.{file_extension}"
            )
            with open(image_path, 'wb') as file_obj:
                file_obj.write(response.read())
    except urllib.error.HTTPError as e:
        pass
    except urllib.error.URLError as e:
        pass

    # Enqueue remaining images
    args = (job_hash, images)
    queue = Queue('tasks', connection=redis)
    queue.enqueue_call('worker.get_image', args=args)
