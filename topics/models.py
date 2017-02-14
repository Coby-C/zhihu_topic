from django.db import models
from django.core.cache import cache

class Topic(models.Model):
    name=models.CharField(max_length=30,null=True)
    follower_num=models.IntegerField(null=True)
    sub_topic=models.ManyToManyField('self',symmetrical=False)
    topic_id=models.IntegerField(primary_key=True)
    description=models.CharField(max_length=300,null=True)
    is_complete=models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.topic_id)
        
