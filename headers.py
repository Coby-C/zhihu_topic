from itertools import cycle
#构造请求需要的信息，若cookies失效则替换新的cookies_text
Accept='text/html, application/xhtml+xml, image/jxr, */*'
Accept_Encoding='gzip, deflate'
Accept_Language='zh-Hans-CN, zh-Hans; q=0.5'
Connection='Keep-Alive'
Referer='https://www.zhihu.com/topic'
User_Agent=cycle(['Baiduspider+(+http://www.baidu.com/search/spider.htm)','Googlebot/2.1 (+http://www.googlebot.com/bot.html)','Mozilla/5.0 (compatible; Yahoo! Slurp China; http://misc.yahoo.com.cn/help.html")','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'])
cookies_text='q_c1=eb38b40993414766b08611a66a1fc5b3|1487152677000|1487152677000; l_cap_id=MmVjZTY5YmZlNWUzNDFmMWFkZDViZGFkMWNjNzNhYzg=|1487152677|1002b9a6d20d0320a808fcc0891e8fcad390021a; cap_id=YjA0NTU1MGY3NmEwNGUxZGI2ZWNmZTkzNGJhYjVmZGE=|1487152677|d9bc73dee4a4fe2922368b85bb21563623ee4eb4; d_c0=ABCCiBw0LAuPTg700etoRp0t0dVBpn3nj9g=|1484725011; r_cap_id=ZmEzZmEyOTVkNDk4NDlkZThiNTMxMmI5NWQ5ZjdjNmU=|1484725012|249ec38b8f88efb86489a1d17245716bba942955; __utma=51854390.474663210.1484725042.1487137544.1487152648.4; __utmz=51854390.1487137544.3.3.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.000--|2=registration_date=20141113=1^3=entry_date=20170215=1; login=ZTU0YmNiNDUwNTU0NDg1NDljMzQzNDIxNGY3YmZlMzc=|1487137554|63351c6d5d129e315c14bae5e724c45a7b463e1b; nweb_qa=heifetz; _zap=d717fdfd-3924-4542-a3a9-8c77f98eabcb; __utmb=51854390.0.10.1487152648; l_n_c=1; n_c=1; __utmc=51854390; _xsrf=7d0674f13ccdb33e4562bf4137d6dae0; aliyungf_tc=AQAAAFMuDRok7gkASch3e+6rbuElRKqk'

headers={'Accept':Accept,
        'Accept-Encoding':Accept_Encoding,
        'Accept-Language':Accept_Language,
        'Connection':Connection,
        'Referer':Referer,}
def get_headers():
    global headers,User_Agent
#    headers['User-Agent']=next(User_Agent)
    headers['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'
#    print(headers)
    return headers

cookies_dict={}
for line in cookies_text.split(';'):
    name,value=line.strip().split('=',1)
    cookies_dict[name]=value


api_key={'_xsrf':cookies_dict['_xsrf']}

