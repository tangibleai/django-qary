# import json

# from django.db import models
# from django.conf import settings
# from django.utils.translation import ugettext, ugettext_lazy as _

# from six import python_2_unicode_compatible


# # Create your models here.

# class Article(models.Model):
#     index = models.CharField(max_length=264)
#     page_id = models.BigIntegerField(100000000)
#     source = models.URLField(max_length=264)
#     title = models.CharField(max_length=264)
#     text = models.TextField()

# # class Index(models.Model):
# #     index = models.CharField(max_length=264)
    
# #     def __str__(self):
# #         return self.index

# # class PageId(models.Model):
# #     page_id = models.BigIntegerField(100000000)
    
# #     def __str__(self):
# #         return self.page_id


# # class Source(models.Model):
# #     source = models.URLField(max_length=264)
    
# #     def __str__(self):
# #         return self.source

# # class Title(models.Model):
# #     title = models.CharField(max_length=264)
    
# #     def __str__(self):
# #         return self.title

# # class Text(models.Model):
# #     text = models.TextField()
    
# #     def __str__(self):
# #         return self.text

    

# # # Create your models here.
# # class Article(models.Model):
# #     title = Title
# #     source = Source
# #     text = Text
# #     page_id = PageId
# #     index = Index


# #     def __str__(self):
# #         return self.source, self.page_id, self, self.title, self.text
