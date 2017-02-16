from django.shortcuts import render
from django.http import HttpResponse 
from django.shortcuts import render_to_response 
import os
from topics.models import Topic
import datetime
# Create your views here.

rend_dict={'PATH':os.getcwd()}

def return_home_page(request,topic_id=19776749):
    serch_topic_name=request.GET.get('topic_name','')
    if serch_topic_name:
        current_topic_list=Topic.objects.filter(name__contains=serch_topic_name).order_by('-follower_num')[:100]
    else:
        current_topic_list=Topic.objects.filter(topic_id=topic_id)
    top100_topics=Topic.objects.order_by('-follower_num')[:100]
    r_dict={'name':'ZJ','top100_topics':top100_topics,'current_topic_list':current_topic_list}
    r_dict.update(rend_dict)
    return render_to_response('homepage.html',r_dict)

