# -*- coding:utf-8 -*-#
import lxml.html
import requests
import pymongo
import urllib
import sys
import time
import xlrd
import json
import xlwt
import multiprocessing
reload(sys)
sys.setdefaultencoding('utf-8')
import xlrd

header={
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
'host':"www.qichacha.com",
# 'cookie':'gr_user_id=3fb91e57-6122-4fe3-bf82-ec1d2c189573; _uab_collina=148895889674314578309074; UM_distinctid=15ad12a2ca737a-077df47d25d286-37637b02-100200-15ad12a2ca870; acw_tc=AQAAAAs0fXzh4w0AjKiP21atuYXboW9Z; _umdata=6AF5B463492A874D3EB74E51F3DE6ADC34752F0C042B91A3EA384C14433E2C0991A2A11F2D22753FCD43AD3E795C914C7DBBDD9F8770F9504D511C83760E19E1; PHPSESSID=ioftmj6nlm5m4ojcm0oi855fs6; gr_session_id_9c1eb7420511f8b2=87ccbb8a-bc3a-4f2c-936e-4fcd02826bd0; CNZZDATA1254842228=1858276494-1488435578-null%7C1490765826'
}

cookie_dict={
        'UM_distinctid':'15b94bd28c0532-06440fce5b87b3-3e64430f-15f900-15b94bd28c14d7',
        'gr_user_id':'2564fa5c-2962-4165-a15b-aacf48f7ffd7',
        '_uab_collina':'149284914580079253543107',
        'acw_tc':'AQAAAOnY9RXMkAEAsLgiOgm41tWhL1Go',
        '_umdata':'70CF403AFFD707DF01F447BEB8F98B0A64DE1388E1FB72C22705EF3B0690146152B13D1F2132E739CD43AD3E795C914C0C36F949192B7ECFBD84BF01696FBF96',
        'PHPSESSID':'996me3inl5ipjqc8f5iq4glva2',
        'gr_session_id_9c1eb7420511f8b2':'01968266-5b16-4ae1-8344-c843b6f84132',
        'CNZZDATA1254842228':'2025307065-1492848434-%7C1493263211',
        }
# cookie_dict={
#         'UM_distinctid':'15ad12a2ca737a-077df47d25d286-37637b02-100200-15ad12a2ca870',
#         'gr_user_id':'3fb91e57-6122-4fe3-bf82-ec1d2c189573',
#         '_uab_collina':'148895889674314578309074',
#         'acw_tc':'AQAAAAs0fXzh4w0AjKiP21atuYXboW9Z',
#         '_umdata':'6AF5B463492A874D3EB74E51F3DE6ADC34752F0C042B91A3EA384C14433E2C0991A2A11F2D22753FCD43AD3E795C914C7DBBDD9F8770F9504D511C83760E19E1',
#         'PHPSESSID':'ioftmj6nlm5m4ojcm0oi855fs6',
#         'gr_session_id_9c1eb7420511f8b2':'87ccbb8a-bc3a-4f2c-936e-4fcd02826bd0',
#         'CNZZDATA1254842228':'1858276494-1488435578-null%7C1490765826',
#         }

basic_url="http://www.qichacha.com"

conn = pymongo.MongoClient('106.75.65.56',27017,connect=False)
db = conn['CFDA']
account = db['qcc_important']
resultdict={}

#print r.content
def getText(elem):
    rc = []
    for node in elem.itertext():
        rc.append(node.strip())
    return ''.join(rc)

def test():
    url = 'http://www.qichacha.com/search?key=' + '同创伟业'
    r = requests.get(url, headers=header, cookies=cookie_dict)
    print r.content

test()


def main_search(query):
    company_name1=query
    url='http://www.qichacha.com/search?key='+query
    print url
    #进行爬取，提供header和cookies参数
    r=requests.get(url,headers=header,cookies=cookie_dict)
    #lxml库进行解析
    dom=lxml.html.document_fromstring(r.content)
    #print r.content
    #得到搜索结果的第一条记录的链接
    href=basic_url+dom.xpath('//table[@class="m_srchList"]/tbody/tr[1]/td[2]/a')[0].get('href')

    #得到搜索结果的第一条记录的公司名称
    company_name=dom.xpath('//table[@class="m_srchList"]/tbody/tr[1]/td[2]/a')[0]
    company_name=getText(company_name)
    print href
    print company_name
    resultdict[company_name1]=dict()

    resultdict[company_name1][u'公司名称']=company_name
    resultdict[company_name1][u'天眼查网址']=href

    r1=requests.get(href,headers=header,cookies=cookie_dict)
    dom1=lxml.html.document_fromstring(r1.content)
    #print r1.content
    #公司基本信息，每一个都可能不存在，需要进行判断
    info_table=dom1.xpath('//span[@class="clear m_comInfo"]')[0]
    if len(info_table.xpath('./small'))==2:
        resultdict[company_name1][u'公司电话']=info_table.xpath('./small[1]')[0].text.strip() if info_table.xpath('./small[1]')!=[] else ""
        resultdict[company_name1][u'公司邮箱']=info_table.xpath('./small[1]/a[1]')[0].text.strip() if info_table.xpath('./small[1]/a[1]')!=[] else ""
        if info_table.xpath('./small[1]/a[2]/label')!=[]:
            resultdict[company_name1][u'公司网址']=info_table.xpath('./small[1]/a[2]/label')[0].text.strip()
        else:
            resultdict[company_name1][u'公司网址']=""
        resultdict[company_name1][u'公司地址']=getText(info_table.xpath('./small[2]')[0]).strip() if info_table.xpath('./small[2]')!=[] else ""
        print resultdict[company_name1]
    elif len(info_table.xpath('./small'))==3:
        resultdict[company_name1][u'公司电话'] = info_table.xpath('./small[2]')[0].text.strip() if info_table.xpath('./small[2]')!=[] else ""
        resultdict[company_name1][u'公司邮箱'] = info_table.xpath('./small[2]/a[1]')[0].text.strip() if info_table.xpath('./small[2]/a[1]')!=[] else ""
        if info_table.xpath('./small[2]/a[2]/label') != []:
            resultdict[company_name1][u'公司网址'] = info_table.xpath('./small[2]/a[2]/label')[0].text.strip()
        else:
            resultdict[company_name1][u'公司网址'] = ""
        resultdict[company_name1][u'公司地址'] = getText(info_table.xpath('./small[3]')[0]).strip() if info_table.xpath('./small[3]')!=[] else ""
        #print resultdict[company_name]



    firm_key=href.split('_')[1][:-6]
    #print firm_key
    params={
        "unique":firm_key,
        'companyname':company_name.encode('utf-8'),
        'tab':"base"
    }
    more_info_url='http://www.qichacha.com/company_getinfos?'+urllib.urlencode(params)
    r2=requests.get(more_info_url,headers=header,cookies=cookie_dict)
    #print r2.content
    #print r2.content
    dom2=lxml.html.document_fromstring(r2.content.decode('utf-8'))

    #print r2.content
    #工商信息，由于列表固定，直接格式化提取，不需要一个一个字段进行提取
    if dom2.xpath('//table[@class="m_changeList"]')!=[]:
        info_table=dom2.xpath('//table[@class="m_changeList"]')[0]
       #print getText(dom2)
        #print info_table
        rows=len(info_table.xpath('./tr'))
        #print rows
        for i in range(rows):
            onerow=info_table.xpath('./tr')[i]
            td_count=len(onerow.xpath('./td'))
            for j in range(td_count/2):
                resultdict[company_name1][onerow.xpath('./td')[j*2].text.strip()[:-1]]=getText(onerow.xpath('./td')[j*2+1]).strip()

    #公司简介
    if dom2.xpath('//div[@class="panel-body base-black m-b"]/div')!=[]:
        resultdict[company_name1][u'公司简介']=getText(dom2.xpath('//div[@class="panel-body base-black m-b"]/div')[0])
    else:
        resultdict[company_name1][u'公司简介']=""

    #股东信息：
    resultdict[company_name1][u'股东信息']=dict()
    if dom2.xpath('//section[@id="Sockinfo"]')!=[]:
        sockinfo=dom2.xpath('//section[@id="Sockinfo"]')[0]
        sock_trs=sockinfo.xpath('./table[@class="m_changeList"]/tr') if sockinfo.xpath('./table[@class="m_changeList"]/tbody')==[] else sockinfo.xpath('./table[@class="m_changeList"]/tbody/tr')
        sock_count=len(sock_trs)
        socks=[]

        for i in range(1,sock_count):
            onesock=dict()
            onesock[u'股东']=getText(sock_trs[i].xpath('./td[1]/a')[0]).strip() if sock_trs[i].xpath('./td[1]/a')!=[] else getText(sock_trs[i].xpath('./td[1]')[0]).strip()
            onesock[u'持股比例']=getText(sock_trs[i].xpath('./td[2]/a')[0]).strip() if sock_trs[i].xpath('./td[2]/a')!=[] else getText(sock_trs[i].xpath('./td[2]')[0]).strip()
            onesock[u'认缴出资额（万元）']=getText(sock_trs[i].xpath('./td[3]/a')[0]).strip() if sock_trs[i].xpath('./td[3]/a')!=[] else getText(sock_trs[i].xpath('./td[3]')[0]).strip()
            onesock[u'认缴出资日期']=getText(sock_trs[i].xpath('./td[4]/a')[0]).strip() if sock_trs[i].xpath('./td[4]/a')!=[] else getText(sock_trs[i].xpath('./td[4]')[0]).strip()
            onesock[u'股东类型']=getText(sock_trs[i].xpath('./td[5]/a')[0]).strip() if sock_trs[i].xpath('./td[5]/a')!=[] else getText(sock_trs[i].xpath('./td[5]')[0]).strip()
            resultdict[company_name1][u'股东信息'][str(i)]=onesock
            #print onesock
    #变更信息
    resultdict[company_name1][u'变更信息']=dict()
    if dom2.xpath('//section[@id="Changelist"]')!=[]:
        changeinfo=dom2.xpath('//section[@id="Changelist"]')[0]
        change_trs=changeinfo.xpath('./table/tr')
        change_count=len(change_trs)
        print change_count
        changes=[]
        for i in range(1,change_count):
            onechange=[]
            #print i
            #for t in range(2,6):
            onechange=dict()
            onechange[u'变更日期']=getText(change_trs[i].xpath('./td[2]')[0]).strip() if change_trs[i].xpath('./td[2]/div[1]')==[] else getText(change_trs[i].xpath('./td[2]/div[1]')[0]).strip()
            onechange[u'变更项目'] =getText(change_trs[i].xpath('./td[3]')[0]).strip() if change_trs[i].xpath('./td[3]/div[1]')==[] else getText(change_trs[i].xpath('./td[3]/div[1]')[0]).strip()
            onechange[u'变更前'] =getText(change_trs[i].xpath('./td[4]')[0]).strip() if change_trs[i].xpath('./td[4]/div[1]')==[] else getText(change_trs[i].xpath('./td[4]/div[1]')[0]).strip()
            onechange[u'变更后'] =getText(change_trs[i].xpath('./td[5]')[0]).strip() if change_trs[i].xpath('./td[5]/div[1]')==[] else getText(change_trs[i].xpath('./td[5]/div[1]')[0]).strip()
                #print len(change_trs[i].xpath('./td'))
                #onechange.append([getText(change_trs[i].xpath('./td['+str(t)+']')[0]).strip() if change_trs[i].xpath('./td['+str(t)+']/div[1]')==[] else getText(change_trs[i].xpath('./td['+str(t)+']/div[1]')[0]).strip()][0])
            #changes.append('<->'.join(onechange))
            resultdict[company_name1][u'变更信息'][str(i)] = onechange


    #企业年报
    params['tab']='report'
    report_info_url = 'http://www.qichacha.com/company_getinfos?' + urllib.urlencode(params)
    r_report = requests.get(report_info_url, headers=header, cookies=cookie_dict)
    dom_report=lxml.html.document_fromstring(r_report.content.decode('utf-8'))
    report_dict=dict()
    if dom_report.xpath('//div[@class="tab-pane fade in active"]')!=[]:
        report_div=dom_report.xpath('//div[@class="tab-pane fade in active"]')[0]
        report_subtitle=report_div.xpath('./div[@class="m_header"]')
        report_tables=report_div.xpath('./table')

        subtitle_count=len(report_subtitle)
        for i in range(0,subtitle_count):
            title=getText(report_subtitle[i]).strip()
            table=report_tables[i]
            #print title
            report_dict[title]=dict()
            if title=="企业基本信息" or title=="企业资产状况信息":
                #print title
                trs = table.xpath('./tbody/tr') if table.xpath('./tbody') != [] else table.xpath('./tr')
                trs_count=len(trs)
                for tr in range(trs_count):
                    td_count = len(trs[tr].xpath('./td'))
                    for j in range(td_count / 2):
                        #print getText(trs[tr].xpath('./td')[j*2])
                        report_dict[title][getText(trs[tr].xpath('./td')[j*2])]=getText(trs[tr].xpath('./td')[j*2+1]).strip()
            else:
                trs = table.xpath('./tbody/tr') if table.xpath('./tbody')!=[] else table.xpath('./tr')
                #print len(trs)
                trs_count = len(trs)
                title_tr=trs[0]
                td_count = len(title_tr.xpath('./td'))
                tr_title=[]
                for one in range(td_count):
                    tr_title.append(getText(title_tr.xpath('./td')[one]))
                for tr in range(1,trs_count):
                    one_result=dict()


                    for one in range(td_count):
                        one_result[tr_title[one]]=getText(trs[tr].xpath('./td')[one])
                    #print one_result

                    report_dict[title][str(tr)] = one_result

        resultdict[company_name1][u'企业年报']=report_dict
    else:
        resultdict[company_name1][u'企业年报']={}




    #对外投资
    params['tab']='touzi'
    touzi_info_url = 'http://www.qichacha.com/company_getinfos?' + urllib.urlencode(params)
    r_touzi = requests.get(touzi_info_url, headers=header, cookies=cookie_dict)
    dom_touzi=lxml.html.document_fromstring(r_touzi.content.decode('utf-8'))
    if dom_touzi.xpath('//section[@id="touzilist"]')!=[]:
        touzi_div=dom_touzi.xpath('//section[@id="touzilist"]')[0]

        if touzi_div.xpath('./nav[@class="text-right m-r"]/ul/li')!=[]:
            type_len=len(touzi_div.xpath('./nav[@class="text-right m-r"]/ul/li'))
            if type_len<=6:
                pagecount=type_len-1
            elif type_len>6:
                pagecount=int(getText(touzi_div.xpath('./nav[@class="text-right m-r"]/ul/li['+str(type_len)+']/a')[0])[3:])
        else:
            pagecount=1

        touzi_companys_dict=dict()
        touzi_companys=touzi_div.xpath('./ul[1]/a')
        touzi_company_count=len(touzi_companys)
        for i in range(touzi_company_count):
            touzi_companys_dict[str(i)]=dict()
            touzi_companys_dict[str(i)][u"公司网址"]=basic_url+touzi_companys[i].get('href')
            touzi_companys_dict[str(i)][u"公司名称"]=getText(touzi_companys[i].xpath('./span[2]/span[1]')[0])

        if pagecount>1:
            for page in range(2,pagecount+1):
                touzi_info_url = 'http://www.qichacha.com/company_getinfos?' + urllib.urlencode(params)+"&p="+str(page)
                r_touzi = requests.get(touzi_info_url, headers=header, cookies=cookie_dict)
                #time.sleep(2)
                dom_touzi = lxml.html.document_fromstring(r_touzi.content.decode('utf-8'))
                if dom_touzi.xpath('//section[@id="touzilist"]')!=[]:
                    touzi_div = dom_touzi.xpath('//section[@id="touzilist"]')[0]
                    touzi_companys = touzi_div.xpath('./ul[1]/a')
                    touzi_company_count = len(touzi_companys)
                    for i in range(touzi_company_count):
                        touzi_companys_dict[str(i+page*10-10)] = dict()
                        touzi_companys_dict[str(i+page*10-10)][u"公司网址"] = basic_url+touzi_companys[i].get('href')
                        touzi_companys_dict[str(i+page*10-10)][u"公司名称"] = getText(touzi_companys[i].xpath('./span[2]/span[1]')[0])

        resultdict[company_name1][u"投资公司"]=touzi_companys_dict
    else:
        resultdict[company_name1][u"投资公司"] = {}
    # print touzi_companys_dict
    # for key,value in touzi_companys_dict.items():
    #     for key1,value1 in value.items():
    #         print key1
    #         print value1

    #知识产权
    params['tab']='assets'
    box_list={u"著作权":'zzq',u"软件著作权":'rjzzq',u"证书":'zhengshu'}
    for key,value in box_list.items():
        resultdict[company_name1][key]=dict()
        assets_info_url = 'http://www.qichacha.com/company_getinfos?' + urllib.urlencode(params)+"&p=1&box="+value
        #print assets_info_url
        #sectionid=value+"list"
        #print sectionid
        r_assets = requests.get(assets_info_url, headers=header, cookies=cookie_dict)
        time.sleep(2)
        if r_assets.content==None:
            dom_assets=lxml.html.document_fromstring(r_assets.content.decode('utf-8'))
        else:
            print value
            continue
        #section_box=dom_assets.xpath('//section[@id="'+sectionid+'"]')[0]
        section_box=dom_assets
        div_len=len(section_box.xpath('//div'))
        print div_len
        if section_box.xpath('//div')[div_len-1].xpath('./nav')!=[]:
            li_count=len(section_box.xpath('//div')[div_len-1].xpath('./nav/ul/li'))
            if li_count<=6:
                pagecount=li_count-1
            else:
                pagecount=int(getText(section_box.xpath('//div')[div_len-1].xpath('./nav/ul/li['+str(li_count)+']/a')[0])[3:])
        else:
            pagecount=1

        #print pagecount
        info_table=section_box.xpath('//table[@class="m_changeList"]')[0]
        title_tr=[]
        trs=info_table.xpath('./tbody/tr') if info_table.xpath('./tbody')!=[] else info_table.xpath('./tr')
        title_len=len(trs[0].xpath('./th'))
        for oneth in range(title_len):
            title_tr.append(getText(trs[0].xpath('./th')[oneth]))

        #print title_tr
        for ontr in range(1,len(trs)):
            newinfo=dict()
            for onetd in range(title_len):
                newinfo[title_tr[onetd]]=getText(trs[ontr].xpath('./td')[onetd]) if trs[ontr].xpath('./td')[onetd].xpath('./*')==[] else getText(trs[ontr].xpath('./td')[onetd].xpath('./*')[0])

            resultdict[company_name1][key][str(ontr)]=newinfo

        if pagecount>1:
            for page in range(2,pagecount+1):
                assets_info_url = 'http://www.qichacha.com/company_getinfos?' + urllib.urlencode(params) + "&p="+str(page)+"&box=" + value
                r_assets = requests.get(assets_info_url, headers=header, cookies=cookie_dict)
                time.sleep(2)
                dom_assets = lxml.html.document_fromstring(r_assets.content.decode('utf-8'))
                section_box = dom_assets
                #div_len = len(section_box.xpath('//div'))
                info_table = section_box.xpath('//table[@class="m_changeList"]')[0]
                title_tr = []
                trs = info_table.xpath('./tbody/tr') if info_table.xpath('./tbody') != [] else info_table.xpath('./tr')
                title_len = len(trs[0].xpath('./th'))
                for oneth in range(title_len):
                    title_tr.append(getText(trs[0].xpath('./th')[oneth]))

                #print title_tr
                for ontr in range(1, len(trs)):
                    newinfo = dict()
                    for onetd in range(title_len):
                        newinfo[title_tr[onetd]] = getText(trs[ontr].xpath('./td')[onetd]) if trs[ontr].xpath(
                            './td')[onetd].xpath('./*') == [] else getText(trs[onetd].xpath('./td')[onetd].xpath('./*')[0])

                    resultdict[company_name1][key][str(ontr+page*10-10)] = newinfo

    #print resultdict[company_name1]
    return company_name,resultdict[company_name1]


def getcompanylist():
    conn = pymongo.MongoClient('106.75.65.56', 27017)
    db=conn['CFDA']
    account = db['domestic_drug']
    company_list=[]
    print (type(account.find()))
    limit =5000
    t=0
    for item in account.find():
        if t<limit:
            if u'生产单位' in item.keys():
                company_list.append(item[u'生产单位'])
                print (item[u'生产单位'])
        else:
            break

        t+=1

    print "search end"
    return company_list

#从excel中得到企业列表
def getcompanylist_by_excel():
    book=xlrd.open_workbook('相似性标注-玉斌.xls')
    sheet=book.sheet_by_name('工作表1')
    company_list=[]
    nows=sheet.nrows
    print nows
    for i in range(1,nows):
        company_list.append(sheet.cell(i,0).value)
    print company_list
    return company_list



def process(companylist):
    for i in companylist:
        # company_name=table.cell(i,0).value
        company_name = i
        print company_name
        try:
            company, result = main_search(company_name)
        #finish_list.append(company_name)
        except:
        #     fail_list.append(company_name)
             continue
        print (type(result))
        # f=open(company+'.json','w+')
        # json.dump(result,f,ensure_ascii=False,indent=4)
        account.insert(result)


if __name__ == '__main__':
    companylist = getcompanylist_by_excel()
    splitlist=[0,len(companylist)/4,len(companylist)/4*2,len(companylist)/4*3,len(companylist)]
    # 4进程并行爬取
    for i in range(4):
        p = multiprocessing.Process(target=process, args=(companylist[splitlist[i]:splitlist[i+1]],))
        p.start()




#resultdict={}
# titlelist=[u'公司名称',u'天眼查网址',u'公司电话',u'公司邮箱',u'公司网址',u'公司地址',u'统一社会信用代码',u'注册号',u'组织机构代码',u'经营状态',u'法定代表人',
#            u'注册资本',u'公司类型',u'成立日期',u'营业期限',u'登记机关',u'核准日期',u'公司规模',u'所属行业',u'英文名',u'曾用名',u'企业地址',u'经营范围',u'公司简介',
#            u'股东信息',u'主要人员',u'变更信息']

#company_xlsx=xlrd.open_workbook('生物医药企业列表0617.xlsx')
#table=company_xlsx.sheets()[0]
#nrows=table.nrows
#print nrows
#f=open('result.csv','w+')
#f.write(','.join(titlelist).decode('utf-8').encode('gbk')+'\n')
# finish_list=[]
# fail_list=[]
# for i in companylist:
#     #company_name=table.cell(i,0).value
#     company_name=i
#     print company_name
#     #try:
#     company,result=main_search(company_name)
#     finish_list.append(company_name)
#     # except Exception,e:
#     #     print e
#     #     fail_list.append(company_name)
#     #     continue
#     print type(result)
#     #f=open(company+'.json','w+')
#     #json.dump(result,f,ensure_ascii=False,indent=4)
#     account.insert(result)
#
# print fail_list
   # except:
       # continue

    # onerow=[]
    # for i in range(len(titlelist)):
    #
    #     if titlelist[i] in resultdict[company_name].keys():
    #         onerow.append(resultdict[company_name][titlelist[i]])
    #         #print resultdict[company_name][titlelist[i]]
    #     else:
    #         onerow.append('')
    # #print ','.join(onerow).decode('utf-8').encode('gbk')
    # for i in range(len(onerow)):
    #
    #     if type(onerow[i]) !=list:
    #         onerow[i]='\''+onerow[i]
    #         onerow[i]=onerow[i].replace(',','_')
    #         onerow[i] = onerow[i].replace('\n', '')
    # #onerow=['\''+x for x in onerow if type(x)!=list]
    # #onerow=[x.replace(',','_') for x in onerow if type(x)!=list]
    #
    # try:
    #     f.write(','.join(onerow).decode('utf-8').encode('gbk') + '\n')
    # except:
    #     continue
    #





