from urllib.request import urlopen 
from bs4 import BeautifulSoup 
import re 
import traceback
import requests
from topics.models import Topic
import json
from django.core.cache import cache
from multiprocessing import Process
import time
from threading import Thread,Lock
import datetime
from headers import get_headers,api_key,cookies_dict
from django.conf import settings
import itchat
itchat.auto_login()

complete_list=[]
sub_list=[]
asd=[]
def get_all_topic_info():
    '''为数据库中所有的话题补充信息(关注人数，描述，话题图片)'''
    all_topic=Topic.objects.filter(description=None).iterator()
#    all_topic=Topic.objects.all().iterator()
    for topic in all_topic:
        try:
            print('开始爬取---------《{}》'.format(topic.name))
            url='https://www.zhihu.com/topic/{}/hot'.format(topic.topic_id)
            response=get_response(url,method='GET')
            bsobj=get_bs_obj(response.text)
            target_follower=bsobj.find('div',{'id':'zh-topic-side-head'})
            target_desc=bsobj.find('div',{'id':'zh-topic-desc'}).div.get_text() if bsobj.find('div',{'id':'zh-topic-desc'}) else ''
            target_img_url=bsobj.find('a',{'id':'zh-avartar-edit-form'}).img['src']
            save_img(topic.topic_id,target_img_url)
            if '还没有人关注该话题' in target_follower.get_text():
                topic.follower_num=0
            else:
                topic.follower_num=bsobj.find('div',{'id':'zh-topic-side-head'}).strong.get_text()
            topic.description=target_desc
            topic.save()
            print('话题《{}》,关注人数为{}人，描述为“{}”已经保存！'.format(topic.name,topic.follower_num,topic.description))
            itchat.send('话题《{}》,关注人数为{}人，描述为“{}”已经保存！'.format(topic.name,topic.follower_num,topic.description))
        except Exception as e:
            traceback.print_exc()
        print('\n')
             
def get_all_topic_relationship(topic_id=19776749):
    '''得到输入话题id的所有的关系模型，默认从根话题开始爬取'''
    if topic_id in complete_list:
        return
    complete_list.append(topic_id)
    url='https://www.zhihu.com/topic/{}/organize/entire'.format(topic_id)
    response=get_response(url,data=api_key,method='POST')
    relationship_list=eval(response.text)
    current_topic=Topic.objects.get_or_create(topic_id=topic_id)[0]
    sub_topic_list=[]
    for topic_ele in relationship_list['msg'][1]:
        topic=topic_ele[0]
        if topic[0]=='topic':
            if int(topic[2]) not in sub_list:
                sub_topic=Topic.objects.update_or_create(topic_id=int(topic[2]),defaults={'name':topic[1]})[0]
                current_topic.sub_topic.add(sub_topic)
                sub_list.append(int(topic[2]))
                print(datetime.datetime.now(),'话题{}，添加子话题{}！'.format(current_topic.name,sub_topic),file=f)
                sub_topic_list.append(int(topic[2]))
        elif topic[0]=='load' and topic[2] and topic[3] and topic[1]=='加载更多':
            try:
                do_load_more(current_topic,sub_topic_list,topic)
            except:
                traceback.print_exc()
        else:
            print(datetime.datetime.now(),'worning！:未识别的标签：'+topic[0],file=f)
    current_topic.is_complete=True
    current_topic.save()
    print(datetime.datetime.now(),'='*15+'话题{}，已经爬取完成！'.format(current_topic)+'='*15,file=f)
    for sub_topic_id in sub_topic_list:
        try:
            save_relationship(sub_topic_id)
        except:
            traceback.print_exc()

def do_load_more(current_topic,sub_topic_list,topic):
    '''处理《加载更多》标签'''
    while True:
        url='https://www.zhihu.com/topic/{}/organize/entire'.format(topic[3])
        params={'child':topic[2],'parent':topic[3]}
        response=get_response(url=url,params=params,data=api_key)
        relationship_list=eval(response.text)
        for topic_ele in relationship_list['msg'][1]:
            topic=topic_ele[0]
            if topic[0]=='topic':
                if int(topic[2]) not in sub_list:
                    sub_topic=Topic.objects.update_or_create(topic_id=int(topic[2]),defaults={'name':topic[1]})[0]
                    current_topic.sub_topic.add(sub_topic)
                    sub_list.append(int(topic[2]))
                    print(datetime.datetime.now(),'话题{}，添加子话题{}！'.format(current_topic.name,sub_topic),file=f)
                    sub_topic_list.append(int(topic[2]))
                else:
                    print('{}该话题已添加！'.format(topic[2]),file=f)
            elif topic[0]=='load' and topic[2] and topic[3] and topic[1]=='加载更多':
                break
            else:
                print(datetime.datetime.now(),'worning！:未识别的标签：'+topic[0],file=f)
        else:
            break
    

def get_bs_obj(html):
    '''输入str(html),返回bs对象'''
    try:
#        t1=time.time()
        bsobj = BeautifulSoup(html,'html.parser')
#        t2=time.time()
#        print('get_bs_obj,time:{}s'.format(t2-t1))
        return bsobj
    except Exception as e:
        traceback.print_exc()
        assert False,'生成bs对象发生错误！'

def get_response(url,params=[],method='POST',data={}):
    '''输入URL,返回response对象'''
#    try:
    t1=time.time()
    if method=='POST':
        response=requests.post(url,headers=get_headers(),cookies=cookies_dict,params=params,data=data)
    elif method=='GET':
        response=requests.get(url,headers=get_headers(),cookies=cookies_dict,params=params,data=data)
#            print(cookies_dict)
    if response.status_code!=200:
        assert False,'打开{}错误,返回状态码:{}'.format(url,response.status_code)
    response.encoding='unicode'
    t2=time.time()
#        print('get_response,time:{}s'.format(t2-t1))
    return response
#    except Exception as e:
#        traceback.print_exc()
#        assert False,'访问'+url+'链接时发生错误！'

def init_cache():
    all_topic_iter=Topic.objects.all().iterator()
    for topic in all_topic_iter:
        if topic.is_complete:
            cache.set(topic.topic_id,1)
        else:
            cache.set(topic.topic_id,0)

def save_img(topic_id,img_url):
    filename='{}.png'.format(topic_id)
    response=get_response(img_url,method='GET')
    with open(settings.STATICFILES_DIRS[0]+'//'+'topic_img'+'//'+filename,'wb') as f:
        f.write(response.content)
    print('话题图片保存完成'.format(topic_id))

def main():
    get_all_topic_relationship()
    get_all_topic_info()

