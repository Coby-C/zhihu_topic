from itertools import cycle
#构造请求需要的信息，若cookies失效则替换新的cookies_text
Accept='text/html, application/xhtml+xml, image/jxr, */*'
Accept_Encoding='gzip, deflate'
Accept_Language='zh-Hans-CN, zh-Hans; q=0.5'
Connection='Keep-Alive'
Referer='https://www.zhihu.com/topic'
User_Agent=cycle(['Baiduspider+(+http://www.baidu.com/search/spider.htm)','Googlebot/2.1 (+http://www.googlebot.com/bot.html)','Mozilla/5.0 (compatible; Yahoo! Slurp China; http://misc.yahoo.com.cn/help.html")','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'])
cookies_text='__utmc=51854390; l_n_c=1; q_c1=691e59ea9dfd457ab3e754363f907fc3|1483932514000|1483932514000; l_cap_id=OWYwOTIwNGYxZWRiNGE5NDg0MmViYmU3NmVlODlmYzA=|1483933508|926369a90d949398502551fc355f13359550e0d2; cap_id=ZDBlNjdmZTdiZmRmNDgxZWJjNWY1ZjExNTE0Zjg1Yjk=|1483933508|60f057513fe385108930b28ffefdc397349ddc37; r_cap_id=NDllYmM0YzQxOWZlNDFhOGFlMWM3Mjg0ZTMyYTIzZTA=|1483932517|43d396014dda42630d6aa8c707d8c6132e2ab90b; __utma=51854390.553956168.1482239411.1482714756.1483930975.3; __utmz=51854390.1483930975.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; d_c0=ABDCV1gpBwuPTrLrHSSbIINXIl49ZYhxyrM=|1482239161; _zap=409a310a-8069-4a99-bb65-395818fb2b4f; __utmv=51854390.100--|2=registration_date=20150731=1^3=entry_date=20150731=1; login=OWU2ODUyN2Y5MGY0NDg1MmExMzc3NDU2YTEzNGZhZTI=|1483933535|5923a31e83fee3d378021a9b8139871a0b04b657; __utmb=51854390.0.10.1483930975; z_c0=Mi4wQUJDTTg0cldlQWdBRU1KWFdDa0hDeGNBQUFCaEFsVk54WldhV0FEMmI4UTM1dk13LVhxRk5yN2QzZkhveGNqTUtB|1483933949|ea6ed27cf664476750674e1d253805cc4af29e91; unlock_ticket=QUJDTTg0cldlQWdYQUFBQVlRSlZUYzBQYzFnNVBwZEJLN3paSnkzRzlDaXNSUDlsZkNkR0VnPT0=|1483933893|8f80e21aa10b0ed6e2287b305e3119834fdf88ef; aliyungf_tc=AQAAAGe9UT47jAEADZvY3fTcud1oBLgp; _xsrf=e0a8d10c9ee95127a2e1619a15880753'

headers={'Accept':Accept,
        'Accept-Encoding':Accept_Encoding,
        'Accept-Language':Accept_Language,
        'Connection':Connection,
        'Referer':Referer,}
def get_headers():
    global headers,User_Agent
    headers['User-Agent']=next(User_Agent)
#    print(headers)
    return headers

cookies_dict={}
for line in cookies_text.split(';'):
    name,value=line.strip().split('=',1)
    cookies_dict[name]=value


api_key={'_xsrf':cookies_dict['_xsrf']}

