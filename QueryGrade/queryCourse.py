from requests.api import get, head
from encrypt import Encrypt
from encrypt import randomWord
from bs4 import BeautifulSoup
import requests
import json
import time
import re
import prettytable as pt

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
}
def current_milli_time():
    return int(round(time.time() * 1000))


def formdata(course_code: str, session_id: str, form_key: str, csrf_token: str):
    return {
        "courseRangerStr": "全校",
        "selectedLineIndex": "",
        "_checked": "on",
        "searchCourseWrapperContent.courseStatus": "",
        "searchCourseWrapperContent.name": "",
        "searchCourseWrapperContent.codeR": course_code,
        "searchCourseWrapperContent.departmentId": "",
        "searchCourseWrapperContent.degree": "",
        "searchCourseWrapperContent.instNameCodeStr": "",
        "_cmCourseLookUpWrappers[0].checked": "on",
        "umsfz1p_length": "100",
        "pageId": "pageLookUpCourse",
        "viewId": "StartProposalView",
        "formKey": form_key,
        "requestedFormKey": "",
        "sessionId": session_id,
        "flowKey": "",
        "view.applyDirtyCheck": "true",
        "dirtyForm": "false",
        "renderedInDialog": "false",
        "view.singlePageView": "false",
        "view.disableBrowserCache": "true",
        "csrfToken": csrf_token,
        "methodToCall": "searchCourseByFilter",
        "ajaxReturnType": "update-page",
        "ajaxRequest": "true",
        "triggerActionId": "searchCourseCodeInputBetweenBtn",
        "focusId": "searchCourseCodeInputBetweenBtn",
        "csrfToken": csrf_token
    }
def formdata_1(formKey:str,timestap:str):
    return {
        "methodToCall": "tableJsonRetrieval",
        "updateComponentId": "LookUpCourseTableList",
        "formKey": formKey,
        "ajaxReturnType": "update-component",
        "ajaxRequest": "true",
        "sEcho": "1",
        "iColumns": "11",
        "sColumns": ",,,,,,,,,,",
        "iDisplayStart": "0",
        "iDisplayLength": "100",
        "mDataProp_0": "function",
        "sSearch_0": "",
        "bRegex_0": "false",
        "bSearchable_0": "true",
        "mDataProp_1": "function",
        "sSearch_1": "",
        "bRegex_1": "false",
        "bSearchable_1": "true",
        "mDataProp_2": "function",
        "sSearch_2": "",
        "bRegex_2": "false",
        "bSearchable_2": "true",
        "mDataProp_3": "function",
        "sSearch_3": "",
        "bRegex_3": "false",
        "bSearchable_3": "true",
        "mDataProp_4": "function",
        "sSearch_4": "",
        "bRegex_4": "false",
        "bSearchable_4": "true",
        "mDataProp_5": "function",
        "sSearch_5": "",
        "bRegex_5": "false",
        "bSearchable_5": "true",
        "mDataProp_6": "function",
        "sSearch_6": "",
        "bRegex_6": "false",
        "bSearchable_6": "true",
        "mDataProp_7": "function",
        "sSearch_7": "",
        "bRegex_7": "false",
        "bSearchable_7": "true",
        "mDataProp_8": "function",
        "sSearch_8": "",
        "bRegex_8": "false",
        "bSearchable_8": "true",
        "mDataProp_9": "function",
        "sSearch_9": "",
        "bRegex_9": "false",
        "bSearchable_9": "true",
        "mDataProp_10": "function",
        "sSearch_10": "",
        "bRegex_10": "false",
        "bSearchable_10": "true",
        "sSearch": "",
        "bRegex": "false",
        "_": timestap,
    }

def getCourseInfoById(course_id:str,username:str,password:str):

    url="http://authserver.cqu.edu.cn/authserver/login?service=http%3A%2F%2Fmy.cqu.edu.cn%2Fcm%2Fportal%2Fcourse"
    s=requests.session()
    req_get1 = s.get(url=url,headers=headers,timeout=10)
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

    req_get3=s.get(url=req_get2.headers['Location'],headers=headers,allow_redirects=False)
    homepage = s.get(url=req_get3.headers['Location'],headers=headers)

    url="http://my.cqu.edu.cn/cm/portal/course?methodToCall=getSearchCoursePage&viewId=StartProposalView"
    page=s.get(url=url,headers=headers)

    bf = BeautifulSoup(page.text, 'html.parser')
    form_key = str(bf.find("input", {"name": "formKey"})['value'])
    session_id = str(bf.find("input", {"name": "sessionId"})['value'])
    csrf_token = str(bf.find("input", {"name": "csrfToken"})['value'])

    course_page = s.post(
        url="http://my.cqu.edu.cn/cm/portal/course",
        data=formdata(course_id, session_id, form_key, csrf_token),
        headers=headers
    )


    course_page_json=s.get(
        url="http://my.cqu.edu.cn/cm/portal/course",
        params=formdata_1(form_key,str(current_milli_time())),
        headers=headers
    )
    course_info=json.loads(course_page_json.text)
    info_dic={}
    column=['课程名','课程代码','开课学院','层次','授课老师','课时','学分']
    for i in range(2,9):
        key='c{}'.format(i)
        info_dic[column[i-2]]=course_info['aaData'][0][key]['val']
    # print(info_dic)
    return info_dic

# getCourseInfoById(course_id = "STG00032",username = "20181656",password = "7509220qaz")
