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
f=open('log.log','w')
lock=Lock()

complete_list=[]
sub_list=[]

def save_all_follow_num():
    '''为数据库中所有的话题添加或者更新人数'''
#    all_topic=Topic.objects.filter(follower_num=None).iterator()
    all_topic=Topic.objects.all().iterator()
    for topic in all_topic:
        try:
            print(topic.topic_id)
            url='https://www.zhihu.com/topic/{}/hot'.format(topic.topic_id)
            response=get_response(url,method='GET')
            bsobj=get_bs_obj(response.text)
            bsobj_target=bsobj.find('div',{'id':'zh-topic-side-head'})
            if '还没有人关注该话题' in bsobj_target.get_text():
                topic.follower_num=0
            else:
                topic.follower_num=bsobj.find('div',{'id':'zh-topic-side-head'}).strong.get_text()
            topic.save()
            print(datetime.datetime.now(),'topic:{}，关注人数为{}人，已经保存！'.format(topic,topic.follower_num))
        except Exception as e:
            traceback.print_exc()
             
def save_relationship(topic_id=19776749):
    '''得到输入话题id的所有的关系模型，默认从根部门开始爬取'''
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
                print(datetime.datetime.now(),'话题{}，添加子话题{}！'.format(current_topic,sub_topic),file=f)
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
                    print(datetime.datetime.now(),'话题{}，添加子话题{}！'.format(current_topic,sub_topic),file=f)
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
    try:
        t1=time.time()
        if method=='POST':
            response=requests.post(url,headers=get_headers(),cookies=cookies_dict,params=params,data=data)
        elif method=='GET':
            response=requests.get(url,headers=get_headers(),cookies=cookies_dict,params=params,data=data)
#            print(cookies_dict)
        response.encoding='unicode'
        t2=time.time()
        print('get_response,time:{}s'.format(t2-t1))
        return response
    except Exception as e:
        traceback.print_exc()
        assert False,'访问'+url+'链接时发生错误！'

def init_cache():
    all_topic_iter=Topic.objects.all().iterator()
    for topic in all_topic_iter:
        if topic.is_complete:
            cache.set(topic.topic_id,1)
        else:
            cache.set(topic.topic_id,0)

def main():
    save_relationship()
    save_all_follow_num()

