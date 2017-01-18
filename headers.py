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

_url=b'POST /topic/19776749/organize/entire HTTPS/1.1\r\nAccept: */*\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: zh-Hans-CN, zh-Hans; q:0.5\r\nCache-Control: no-cache\r\nConnection: Keep-Alive\r\nContent-Length: 38\r\nContent-Type: application/x-www-form-urlencoded; charset:utf-8\r\nCookie: __utmc:51854390; q_c1:64bb2da36fcf47d49799fb7ec91c269d|1482843077000|1482843077000; cap_id:ZDJjNTk5YjFiOWNhNGZjNDkwZjYxMmI5YmZiMDVhNWI:|1482916655|e8c5bdba019ddabe31b3761f374d3d083b95ff05; l_cap_id:OTY2MGY4MDc1NTNhNDU1NWFhZGFiMDhmYmVkMjI2MjE:|1482916655|cacdabb372a348ab803ca60ba08ca70c99db3456; d_c0:AHDC3wdJDguPTp4COum3TPYps5x8VHzkoUQ:|1482717229; r_cap_id:MDhiYjNkNmYxZWU0NGYwNDhlNzUzMGM3MzQyNjFhZGY:|1482916656|ed6a2056e5dd9b958e71eda8bf2ff1f6ad80f0eb; _zap:ed103ca3-a435-40e8-95c9-f81f7a2c2e94; __utma:51854390.460675002.1483578478.1483965135.1483965493.18; __utmz:51854390.1483965135.17.3.utmcsr:zhihu.com|utmccn:(referral)|utmcmd:referral|utmcct:/topic/19583842/organize/entire; login:MGRlMjdmN2VhNjVjNDMwMzk3NzBkZjEwZmRlYjM0NTQ:|1482917051|8a6153c4af942eae1adbdfa10629910df474dea9; z_c0:Mi4wQUFBQXRVUkFBQUFBY01MZkIwa09DeGNBQUFCaEFsVk51eEdMV0FDQk50T3Jmd3VLS09pZ19uUkxieUdtOEJDTmN3|1484027548|666e0d809550346b20f70989fb84169a5b72152c; nweb_qa:heifetz; __utmv:51854390.100-1|2:registration_date:20141113:1^3:entry_date:20141113:1; __utmb:51854390.0.10.1483965493; _xsrf:4291ad8f5fbd31fcdd4f705ab60f344e; aliyungf_tc:AQAAACT5gUhZlw0ADZvY3XzHQViK1lC0\r\nHost: www.zhihu.com\r\nReferer: https://www.zhihu.com/topic/19550994/organize/entire\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393\r\nX-Requested-With: XMLHttpRequest\r\n\r\n_xsrf:4291ad8f5fbd31fcdd4f705ab60f344e'
