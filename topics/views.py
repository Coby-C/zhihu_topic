from django.shortcuts import render
from django.http import HttpResponse 
from django.shortcuts import render_to_response 
import os
from topics.models import Topic
rend_dict={'PATH':os.getcwd()}
def return_home_page(request):
    top100_topics=Topic.objects.order_by('-follower_num')[:100]
    r_dict={'name':'ZJ','top100_topics':top100_topics}
    r_dict.update(rend_dict)
    return render_to_response('homepage.html',r_dict)

# Create your views here.
