# -*- coding: utf-8 -*-
import pymongo

from scrapy.exceptions import DropItem
from scrapy.conf import settings
#from scrapy import log

import logging



class DoubanmoviePipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        #Remove invalid data
        valid = True
        for data in item:
          if not data:
            valid = False
            raise DropItem("Missing %s of blogpost from %s" %(data, item['url']))
        if valid:
        #Insert data into database
            new_moive={
                "name":item['name'][0],
                "year":item['year'][0],
                "score":item['score'][0],
                "director":item['director'],
                "classification":item['classification'],
                "actor":item['actor']
            }
            self.collection.update({'name':new_moive['name']},new_moive,upsert=True)
            #self.collection.insert(new_moive)

            logger = logging.getLogger(__name__)
            logger.warning("Success Insert Into MongoDB database %s/%s" %
            (settings['MONGODB_DB'], settings['MONGODB_COLLECTION']))
        return item
