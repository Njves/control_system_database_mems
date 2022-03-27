import uuid

from werkzeug.datastructures import FileStorage


class Service:
    def __init__(self):
        pass


class ImageService(Service):
    IMG_PATH = 'app/static/images/'

    def save(self, file: FileStorage) -> str:
        name = str(uuid.uuid4())
        if file.mimetype.split('/')[0] == 'image':
            filename = f"{name.split('-')[0]}.{file.mimetype.split('/')[1]}"
            file.save(dst=self.IMG_PATH + filename)
            return filename
        return ''
