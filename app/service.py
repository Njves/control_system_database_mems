"""
Module contain model data processing services
and interaction with the external environment of the application
"""
import os
import uuid
from typing import List

from PIL import Image
from sqlalchemy import asc, desc
from werkzeug.datastructures import FileStorage

from app import db
from app.models import Tag, Mem


class ImageService:
    IMG_PATH_DIR = 'app/static/images/'
    IMG_PATH = 'static/images/'
    IMG_AVATAR_PATH_DIR = 'app/static/images/avatars/'
    IMG_AVATAR_PATH = 'static/images/avatars/'

    def save(self, file: FileStorage) -> str:
        """
        The method saves image to file system
        Save path app/static/images/
        FileStorage it's flask wrapper over http files
        """
        name = str(uuid.uuid4())
        if file.mimetype.split('/')[0] == 'image':
            filename = f"{name.split('-')[0]}.{file.mimetype.split('/')[1]}"
            file.save(dst=self.IMG_PATH_DIR + filename)
            Compress().compress(self.IMG_PATH_DIR + filename)
            return filename
        return ''

    def save_avatar(self, file: FileStorage):
        """
        The method saves image to file system
        Save path app/static/images/
        FileStorage it's flask wrapper over http files
        """
        name = str(uuid.uuid4())
        # checks mime-type if it's image, save else return blank string
        if file.mimetype.split('/')[0] == 'image':
            filename = f"{name.split('-')[0]}.{file.mimetype.split('/')[1]}"
            file.save(dst=self.IMG_AVATAR_PATH_DIR + filename)
            Compress.convert_picture(self.IMG_AVATAR_PATH_DIR + filename)
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

    @staticmethod
    def avatar_is_exist(link):
        files = os.listdir(ImageService.IMG_AVATAR_PATH_DIR)
        for filename in files:
            if link.split('/')[-1] == filename.split('/')[-1]:
                return True
        return False




class TagService:
    """
    Tag service need to processing with tag
    """

    def parse_tag(self, tags_dict: list) -> List[Tag]:
        """
        example raw_str: cats, woman, anime
        result: [cats, woman, anime]
        """

        tags = []
        for i in tags_dict:
            for key, name in i.items():
                exist_tag = Tag.query.filter_by(name=name).first()
                if not exist_tag:
                    tag = Tag(name=name)
                    db.session.add(tag)
                    tags.append(tag)
                else:
                    tags.append(exist_tag)
        db.session.commit()
        return tags


class Compress:
    ref_size = 300, 300

    def compress(self, link: str):
        """
        Функция принимающая на вход ширину и высоту и ссылку
        картинки которую нужно сжать
        """
        image = Image.open(link)
        width, height = image.size
        ratio = width/height
        if width > 1024 or height > 1024:
            if width > height:
                image = image.resize((1024, int(1024//ratio)), Image.ANTIALIAS)
            else:
                image = image.resize((int(1024*ratio), 1024), Image.ANTIALIAS)
        image.save(link)

    @staticmethod
    def convert_picture(link: str):
        ref_size = 150
        image = Image.open(link)
        width, height = image.size
        if width > height:
            new_height = (height * ref_size) // width
            image = image.resize((ref_size, new_height), Image.ANTIALIAS)
        else:
            new_width = (width * ref_size) // height
            image = image.resize((new_width, ref_size), Image.ANTIALIAS)
        image.save(link)

