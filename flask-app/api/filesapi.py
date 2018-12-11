import base64
import mimetypes
import os
from abc import abstractmethod, ABC


class FilesApiTemplate(ABC):
    """Template for file api frameworks"""

    def __init__(self, job_hash):
        self.job_hash = job_hash
        self.job_path = self.get_job_path(job_hash=self.job_hash)
        self.data = []

    def get_data(self):
        url = self.read_file(job_path=self.job_path, file_name='url.txt')
        self.data.append({'type': 'url', 'value': url})

        # abstractmethod
        self.set_job_type()

        # abstractmethod
        self.read_data()

        return self.data

    @staticmethod
    def get_job_path(job_hash):
        # return f"/data/{job_hash[:2]}/{job_hash[2:4]}/{job_hash[4:6]}/{job_hash[6:]}"
        return f"/data/{job_hash}"

    @staticmethod
    def read_file(job_path, file_name):
        with open(os.path.join(job_path, file_name), 'r') as file_obj:
            return file_obj.read()

    @abstractmethod
    def set_job_type(self):
        pass

    @abstractmethod
    def read_data(self):
        pass


def files_api_wrapper(job_hash):
    """Wrapper that decides which file api to use (text|images)"""

    job_path = FilesApiTemplate.get_job_path(job_hash=job_hash)
    if os.path.exists(os.path.join(job_path, 'site.txt')):
        files_api = TextFilesApi(job_hash=job_hash)
    elif os.path.exists(os.path.join(job_path, 'images.txt')):
        files_api = ImagesFilesApi(job_hash=job_hash)
    else:
        return []

    return files_api.get_data()


class TextFilesApi(FilesApiTemplate):
    """File api for text jobs"""

    def set_job_type(self):
        self.data.append({'type': 'jobtype', 'value': 'text'})

    def read_data(self):
        text = self.read_file(job_path=self.job_path, file_name='site.txt')
        self.data.append({'type': 'text', 'content': text})


class ImagesFilesApi(FilesApiTemplate):
    """File api for image jobs"""

    def __init__(self, job_hash):
        super().__init__(job_hash)
        self.images = self.get_image_files(job_path=self.job_path)

    def set_job_type(self):
        self.data.append({'type': 'jobtype', 'content': 'images'})

    def read_data(self):
        for image in self.images:
            self.data.append(self.encode_file(image))

    @staticmethod
    def get_image_files(job_path):
        files = os.listdir(job_path)
        images = [
            os.path.join(job_path, file)
            for file in files
            if file.split('.')[-1] in ('png', 'gif', 'jpg', 'jpeg')
        ]
        return images

    @staticmethod
    def encode_file(image):
        content_type, _ = mimetypes.guess_type(image)
        with open(image, 'rb') as file_obj:
            encoded_file = base64.b64encode(file_obj.read()).decode("ascii")

        image_str = f"data:{content_type};base64,{encoded_file}"
        rv = {
            'type': 'image',
            'value': image_str
        }
        return rv
