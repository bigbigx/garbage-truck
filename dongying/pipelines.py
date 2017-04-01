# -*- coding: utf-8 -*-

# Define your item pipelines here
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import MEDIUMBLOB

class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
engine = create_engine('mysql://root:19981012@localhost:3306/spider?charset=utf8',echo=True)
DBSession = sessionmaker(bind=engine)
Base = declarative_base()

class A(Base):
    __tablename__ = 'mm'

    id = Column(Integer, primary_key=True,autoincrement=True)
    title = Column(String(255))
    url = Column(String(255))
    path = Column(String(255))
    image = Column(MEDIUMBLOB)

metadata = Base.metadata
metadata.create_all(engine)

class DongyingPipeline(object):
    def open_spider(self, spider):
        self.session = DBSession()

    def process_item(self, item, spider):
        a = A(title=item["titles"],
              url=item["urls"],
              path=item["image_paths"][0],
              image= open("/home/dongying/dongying/"+item["image_paths"][0], "rb").read())
        self.session.add(a)
        self.session.commit()

    def close_spider(self, spider):
        self.session.close()
