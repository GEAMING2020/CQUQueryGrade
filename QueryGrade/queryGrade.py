from requests.api import head
from encrypt import Encrypt
from encrypt import randomWord
from bs4 import BeautifulSoup
import requests
import json
import time
import re
import prettytable as pt
from queryCourse import getCourseInfoById
#待填的信息
username=""
password=""

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
}
def current_milli_time():
    return int(round(time.time() * 1000))

#连接my.cqu.edu.cn的统一认证链接
url='http://authserver.cqu.edu.cn/authserver/login?service=http%3A%2F%2Fmy.cqu.edu.cn%2Fauthserver%2Fauthentication%2Fcas'
s=requests.session()#建立一个session对话
before_url='http://authserver.cqu.edu.cn/authserver/needCaptcha.html?'+'username='+str(username)+'&pwdEncrypt2=pwdEncryptSalt&_='+str(current_milli_time())
need_catch_img=s.get(url=before_url,headers=headers)
req_get1 = s.get(url=url,headers=headers,timeout=10)
#寻找post需要的参数
html = req_get1.content
soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
lt = soup.find("input", {"name": "lt"})['value']
dllt = soup.find("input", {"name": "dllt"})['value']
execution = soup.find("input", {"name": "execution"})['value']
_eventId = soup.find("input", {"name": "_eventId"})['value']
rmShown = soup.find("input", {"name": "rmShown"})['value']
default = soup.find("script", {"type": "text/javascript"}).string
catch_Img=soup.find("img",{"id":"captchaImg"})
salt = default[57:-3]#获取盐，被用来加密
key = salt
iv = randomWord(16)
#参数使用Encrypt加密
a = Encrypt(key=key, iv=iv)
passwordEncrypt = a.aes_encrypt(randomWord(64)+str(password))
#传入数据进行统一认证登录
data = {
    'username': str(username),
    'password': passwordEncrypt,
    'lt': lt,
    'dllt': dllt,
    'execution': execution,
    '_eventId': _eventId,
    'rmShown': rmShown
}
#因为跳转后会重定位所以需要禁止重定位来获取Response
req_post1=s.post(url=url,data=data,headers=headers,allow_redirects=False)
#通过重定位链接发送get请求
req_get2=s.get(url=req_post1.headers['Location'],headers=headers,allow_redirects=False)
#发送这个请求是为了获取后续的code
req_get3=s.get(url="http://my.cqu.edu.cn/authserver/oauth/authorize?client_id=enroll-prod&response_type=code&scope=all&state=&redirect_uri=http://my.cqu.edu.cn/enroll/token-index",allow_redirects=False)
#后续的code会隐藏在Location里面
codeValue=req_get3.headers['Location']
#采用正则表达式搜索=开始&结尾的字符串，并通过切片获得code内容
codeValue=re.search(pattern=r'=.*?&',string=str(codeValue))
codeValue=codeValue.group()[1:-1]
#构造formdata，除了code其它都是不变的
token_data={
    'client_id':'enroll-prod',
    'client_secret':'app-a-1234',
    'code':str(codeValue),
    'redirect_uri': 'http://my.cqu.edu.cn/enroll/token-index',
    'grant_type': 'authorization_code'

}
#发送post请求获取到token
access_token=s.post(url="http://my.cqu.edu.cn/authserver/oauth/token",data=token_data)
token_response=json.loads(access_token.content)
TOKEN=token_response['access_token']
#下面是获取个人信息，可以不用这一步，不过这个链接可以用来统一认证
final=s.get(url='http://my.cqu.edu.cn/authserver/simple-user',headers=headers)
json_text=json.loads(final.text)
json_item=json_text.items()
res_dic={}
for key,value in json_item:
    if(key=='krimPermTDTOS'):
        break
    res_dic[key]=value
# print(res_dic)
#构造查询寻成绩是个人认证的Authorization
headers['Authorization']="Bearer "+TOKEN
s.get(url="http://my.cqu.edu.cn/resource-api/session/info-detail",headers=headers)
score=s.get(url="http://my.cqu.edu.cn/sam-api/score/student/score",headers=headers)
grades=json.loads(score.text)

course_dic=[]#课程成绩，学分
total_credits=0#总学分
for key,items in grades['data'].items():
    print("学期--{}".format(key))
    table=pt.PrettyTable(['课程名称','课程性质','成绩','修读性质','课程代码','学分'])
    for item in items:
        Course_Info=getCourseInfoById(item['courseCode'],username,password)#查询课程学分
        table.add_row([item['courseName'],item['courseNature'],item['effectiveScoreShow'],item['studyNature'],item['courseCode'],Course_Info['学分']])
        course_dic.append({"成绩":item['effectiveScoreShow'],"学分":Course_Info['学分']})
        total_credits=total_credits+int(Course_Info['学分'])
    #打印成绩
    print(table)

five_credits=0
four_credits=0
avarage_score=0
for item in course_dic:
    score = eval(item["成绩"])
    avarage_score+=score*eval(item["学分"])
    if score < 60:
        five_credits += 0
        four_credits += 0
    else:
        five_credits += eval(item["学分"]) * (1 + (score-60)/10)
        if score > 90:
            score = 90
        four_credits += eval(item["学分"]) * (1 + (score-60)/10)
avarage_score/=total_credits
five_credits /= total_credits
four_credits /= total_credits
credits_table=pt.PrettyTable(["总学分","平均分","5分制绩点","4分制绩点"])
credits_table.add_row([total_credits,avarage_score,five_credits,four_credits])
print(credits_table)
