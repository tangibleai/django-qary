# from django_elasticsearch_dsl import Document
# from django_elasticsearch_dsl.registries import registry
# from models import Article


# @registry.register_document
# class ArticleDocument(Document):
#     class Index:
#         # Name of the Elasticsearch index
#         index = ''
#         # See Elasticsearch Indices API reference for available settings
#         settings = {'number_of_shards': 1,
#                     'number_of_replicas': 0}

#     class Django:
#         model = Article # The model associated with this Document

#         # The fields of the model you want to be indexed in Elasticsearch
#         fields = [
#             'index',
#             'page_id',
#             'source',
#             'title',
#             'text'
#         ]

# # class ArticleDocument(Document):
# #     """Book Elasticsearch document."""

# #     id = fields.IntegerField(attr='id')

# #     title = fields.StringField(
# #         analyzer=html_strip,
# #         fields={
# #             'raw': fields.StringField(analyzer='keyword'),
# #         }
# #     )

# #     description = fields.StringField(
# #         analyzer=html_strip,
# #         fields={
# #             'raw': fields.StringField(analyzer='keyword'),
# #         }
# #     )

# #     summary = fields.StringField(
# #         analyzer=html_strip,
# #         fields={
# #             'raw': fields.StringField(analyzer='keyword'),
# #         }
# #     )

# #     publisher = fields.StringField(
# #         attr='publisher_indexing',
# #         analyzer=html_strip,
# #         fields={
# #             'raw': fields.StringField(analyzer='keyword'),
# #         }
# #     )

# #     publication_date = fields.DateField()

# #     state = fields.StringField(
# #         analyzer=html_strip,
# #         fields={
# #             'raw': fields.StringField(analyzer='keyword'),
# #         }
# #     )

# #     isbn = fields.StringField(
# #         analyzer=html_strip,
# #         fields={
# #             'raw': fields.StringField(analyzer='keyword'),
# #         }
# #     )

# #     price = fields.FloatField()

# #     pages = fields.IntegerField()

# #     stock_count = fields.IntegerField()

# #     tags = fields.StringField(
# #         attr='tags_indexing',
# #         analyzer=html_strip,
# #         fields={
# #             'raw': fields.StringField(analyzer='keyword', multi=True),
# #             'suggest': fields.CompletionField(multi=True),
# #         },
# #         multi=True
# #     )

# #     class Django(object):
# #         """Inner nested class Django."""

# #         model = Book  # The model associate with this Document