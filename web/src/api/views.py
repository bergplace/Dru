from rest_framework.decorators import api_view
from rest_framework.response import Response
from web.mongo import Mongo


@api_view(['GET'])
def last_block(request):
    block = Mongo.db('bitcoin').blocks.find().sort([('height', -1)])[0]
    block['_id'] = ''
    return Response(block)


