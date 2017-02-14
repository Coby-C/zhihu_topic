from django.shortcuts import render
from django.http import HttpResponse 
from django.shortcuts import render_to_response 
import os
from topics.models import Topic
import datetime

rend_dict={'PATH':os.getcwd()}

def return_home_page(request):
    serch_topic_name=request.GET.get('topic_name','')
    if not serch_topic_name:
        serch_topic_name='根话题'
    print('这是最后的匹配检索',serch_topic_name)
    current_topic_list=Topic.objects.filter(name__contains=serch_topic_name).order_by('-follower_num')[:100]
    top100_topics=Topic.objects.order_by('-follower_num')[:100]
    r_dict={'name':'ZJ','top100_topics':top100_topics,'current_topic_list':current_topic_list}
    r_dict.update(rend_dict)
    return render_to_response('homepage.html',r_dict)

def time(request):
    return HttpResponse(str(datetime.datetime.now()))

# Create your views here.
