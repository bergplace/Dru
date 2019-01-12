import os

from web import celery_app
from web.mongo import Mongo
from .utils import auto_save_result

@celery_app.task
@auto_save_result
def get_block_by_height(height):
    block = Mongo.db(os.environ['cryptocurrency']).blocks.find_one({'height': height})
    block['_id'] = ''  # mongo ObjectID is not JSON serializable, and I dont yet have nice solution
    return block
