"""
Module contain model data processing services
and interaction with the external environment of the application
"""
import uuid
import os

from PIL import Image
from werkzeug.datastructures import FileStorage

from app.models import Tag
from app import db
import itertools


class Service:
    def __init__(self):
        pass


class ImageService(Service):
    IMG_PATH_DIR = 'app/static/images/'
    IMG_PATH = 'static/images/'

    def save(self, file: FileStorage) -> str:
        """
        The method saves image to file system
        Save path app/static/images/
        FileStorage it's flask wrapper over http files
        """
        name = str(uuid.uuid4())
        # checks mime-type if it's image, save else return blank string
        if file.mimetype.split('/')[0] == 'image':
            filename = f"{name.split('-')[0]}.{file.mimetype.split('/')[1]}"
            file.save(dst=self.IMG_PATH_DIR + filename)
            Compress().compress(self.IMG_PATH_DIR + filename)
            return filename
        return ''

    def delete(self, filename: str):
        """
        The method delete image from file system
        """
        basedir = os.path.abspath(os.path.dirname(__file__))
        try:
            os.remove(os.path.join(basedir, ImageService.IMG_PATH + filename))
        except FileNotFoundError:
            print("Файла не существует")


class TagService(Service):
    """
    Tag service need to processing with tag
    """

    def parse_tag(self, tags_dict: list) -> list[Tag]:
        """
        example raw_str: cats, woman, anime
        result: [cats, woman, anime]
        """

        tags = []
        for i in tags_dict:
            for key, name in i.items():
                exist_tag = Tag.query.filter_by(name=name).first()
                if not exist_tag:
                    tag = self.add_tag(name)
                    tags.append(tag)
                else:
                    tags.append(exist_tag)
        return tags

    def add_tag(self, name: str):
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()
        return tag


class Compress(Service):
    ref_size = 300, 300

    def get_coef_compress(self, size: tuple):
        """ Функция возвращающая коэффициент сжатия
            Смотрим на отношение к эталлоному размеру и берем половину этого отношения
        """
        return (sum(size) // sum(Compress.ref_size)) // 2

    def compress(self, link: str):
        """
        Функция принимающая на вход ширину и высоту и ссылку
        картинки которую нужно сжать
        """
        # размеры к которому стремится изображение

        image = Image.open(link)
        size = image.size
        coef = self.get_coef_compress(size)
        image = image.resize((size[0] // coef, size[1] // coef), Image.ANTIALIAS)
        image.save(link)
