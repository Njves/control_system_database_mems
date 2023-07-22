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


class Compress:
    ref_size = 300, 300

    def compress(self, link: str):
        """
        Функция принимающая на вход ширину и высоту и ссылку
        картинки которую нужно сжать
        """
        image = Image.open(link)
        width, height = image.size
        if width > 1024 or height > 1024:
            image = image.resize((1024, 1024), Image.ANTIALIAS)
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


class Query:
    def get_memes(self, current_id, query, sort_name):
        if current_id:
            memes_query = Mem.query.filter_by(owner_id=current_id).order_by(Mem.date.asc())
        else:
            memes_query = Mem.query.filter_by(status=1)
        all_memes = memes_query.all()
        sort_various = {'by_title': memes_query.order_by(asc(Mem.name)),
                        'by_likes': memes_query.order_by(desc(Mem.likes)),
                        'by_view': memes_query.order_by(desc(Mem.view))}
        found_tagged_mem = []
        if query:
            memes_query = memes_query.filter(Mem.name.like("%" + query + "%"))
            for current_mem in all_memes:
                for tag in current_mem.tags:
                    print(tag, tag.name.startswith(query))
                    if tag.name.startswith(query):
                        found_tagged_mem.append(current_mem)

        if sort_name:
            memes_query = sort_various.get(sort_name, '')
        memes = memes_query.all()
        for i in found_tagged_mem:
            if i not in memes:
                memes.append(i)
        return memes

