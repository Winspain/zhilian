# -*- coding: utf-8 -*-
# @Time    : 2018/4/6 13:08
# @Author  : Winspain
# @File    : findJob.py
# @Software: PyCharm
import requests
import re
import xlwt

def get_JobUrl():
    urls = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%9D%AD%E5%B7%9E&kw=crc&sm=0&p=1'
    #urls = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%9D%AD%E5%B7%9E&kw=%E6%B5%8B%E8%AF%95&p=1&isadv=0'
    # jobDetalUrls = 'http://jobs.zhaopin.com/263940938257473.htm?ssidkey=y&ss=201&ff=03&sg=96fe6a13f5144b4187610cb4fd28450f&so=3'
    #jl:杭州 kw:crc sm:0 p:1
    response = requests.get(urls).text
    data = re.findall(r'par=(.*)</a>',response)
    for lines in data:
        getHref = re.findall(r'href=\"(.*)" target="_blank">',str(lines))
        geTail = str(re.findall(r'\"(.*)\" href',lines)).replace(';','').replace('amp','')
        wholeUrl = (str(getHref) + '?' + str(geTail)).replace('\'][\'','').replace('\']','').replace('[\'','')
        with open('jobUrl.txt','a') as f:
            f.writelines(wholeUrl + '\n')

def jobDetal():
    with open('jobUrl.txt','r') as f:
        wb = xlwt.Workbook()
        sh = wb.add_sheet('智联招聘',cell_overwrite_ok=True)
        count = 1
        for lines in f.readlines():
            response = requests.get(lines.strip()).text
            salary = re.findall(r'月薪：</span><strong>(.*)/月', response)
            jobNums = re.findall(r'招聘人数：</span><strong>(.*)人', response)
            workAddress = re.findall(r'<h2>(.*)</h2>', response)
            workAddress = re.findall(r'[\u4e00-\u9fa5]+',str(workAddress))
            compName = re.findall(r'Str_CompName = "(.*)";', response)
            description = re.findall(r'SWSStringCutStart -->(.*)<!-- SWSStringCutEnd', response, re.S | re.M)
            description = str(re.findall(r'[\u4e00-\u9fa5]+', str(description))).replace(',', ' ').replace('\'', '')
            '''创建excel'''
            sh.write(0, 0, '公司名称')
            sh.write(0, 1, '招聘人数')
            sh.write(0, 2, '薪水')
            sh.write(0, 3, '工作地点')
            sh.write(0, 4, '工作要求')
            '''写入信息'''
            sh.write(count, 0, compName)
            sh.write(count, 1, jobNums)
            sh.write(count, 2, salary)
            sh.write(count, 3, workAddress)
            sh.write(count, 4, description)
            count+=1
        wb.save('临床协调员.xls')
        


if __name__ == '__main__':
    jobDetal()



