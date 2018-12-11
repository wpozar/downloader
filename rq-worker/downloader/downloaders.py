import os
import pathlib
import urllib.error
import urllib.parse
import urllib.request
from abc import abstractmethod, ABC

from bs4 import BeautifulSoup


class DownloaderTemplate(ABC):
    """Template for concrete downloaders"""

    def __init__(self, job_url, job_hash):

        self.REQUEST_HEADERS = {
            'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }

        self.job_url = job_url
        self.job_hash = job_hash
        self.job_html = None
        self.job_path = None
        self.error = False

        self.extracted_data = None

    def run(self):

        if self.get_website_html() is False:
            self.error = True
            return

        self.job_path = self.get_job_path(job_hash=self.job_hash)
        self.ensure_directory_structure(job_path=self.job_path)
        self.save_file(job_path=self.job_path, file_content=self.job_url, file_name='url.txt')
        self.save_file(job_path=self.job_path, file_content=self.job_html, file_name='site.html')

        # abstract methods
        self.extracted_data = self.extract_data(job_html=self.job_html)
        return self.process_data(extracted_data=self.extracted_data)

    def get_website_html(self):
        # Create request with fake headers so web servers will not reject it
        try:
            request = urllib.request.Request(
                self.job_url,
                headers=self.REQUEST_HEADERS
            )
        except ValueError as e:
            return

        try:
            with urllib.request.urlopen(request) as response:
                self.job_html = response.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            return False
        except urllib.error.URLError as e:
            return False

        return True

    @staticmethod
    def get_job_path(job_hash):
        # return f"/data/{job_hash[:2]}/{job_hash[2:4]}/{job_hash[4:6]}/{job_hash[6:]}"
        return f"/data/{job_hash}"

    @staticmethod
    def ensure_directory_structure(job_path):
        pathlib.Path(job_path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def save_file(job_path, file_content, file_name):
        with open(os.path.join(job_path, file_name), 'w') as file_obj:
            file_obj.write(file_content)

    @abstractmethod
    def extract_data(self, job_html):
        pass

    @abstractmethod
    def process_data(self, extracted_data):
        pass


class TextDownloader(DownloaderTemplate):
    """Text downloader"""

    def extract_data(self, job_html):
        soup = BeautifulSoup(job_html, 'html.parser')
        return soup.get_text()

    def process_data(self, extracted_data):
        self.save_file(job_path=self.job_path, file_content=extracted_data, file_name='site.txt')
        return True


class ImagesDownloader(DownloaderTemplate):
    """Images downloader"""

    def extract_data(self, job_html):
        parsed_url = urllib.parse.urlparse(self.job_url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}".rstrip('/')

        images = []
        soup = BeautifulSoup(job_html, 'html.parser')
        for image in soup.findAll('img'):
            image_path = image.get('src')
            file_extension = image_path.split('.')[-1].lower()
            if file_extension not in ('png', 'gif', 'jpg', 'jpeg'):
                continue
            if image_path.startswith('/'):
                image_path = f"{base_url}{image_path}"
            images.append(image_path)
        return images

    def process_data(self, extracted_data):
        images = extracted_data
        self.save_file(job_path=self.job_path, file_content='\n'.join(images), file_name='images.txt')

        return images
