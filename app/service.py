import uuid
import os
from werkzeug.datastructures import FileStorage



class Service:
    def __init__(self):
        pass


class ImageService(Service):
    IMG_PATH_DIR = 'app/static/images/'
    IMG_PATH = 'static/images/'

    def save(self, file: FileStorage) -> str:
        name = str(uuid.uuid4())
        if file.mimetype.split('/')[0] == 'image':
            filename = f"{name.split('-')[0]}.{file.mimetype.split('/')[1]}"
            file.save(dst=self.IMG_PATH_DIR + filename)
            return filename
        return ''

    def delete(self, filename: str) -> bool:
        basedir = os.path.abspath(os.path.dirname(__file__))
        os.remove(os.path.join(basedir, ImageService.IMG_PATH + filename))
        return True