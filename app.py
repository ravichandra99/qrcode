import json
from flask import Flask,jsonify,render_template,request
import pymysql as p
import time


rest=[]

app=Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    tm=time.strftime("%Y-%m-%d %H-%M-%S")
    con=p.connect(host="database-1.czejdnwyu0eq.ap-south-1.rds.amazonaws.com",user="root",password="Ivisivis5",database="QRCODE_DATA")
    cur=con.cursor()
    sql="insert into RawData(Date,Hour,Ip,Browser,Os)values(%s,%s,%s,%s,%s)"
    sqls="insert into HourWise(DATE,HOUR,VISITS,UNIQUES,BROWSER,OS,IP)values(%s,%s,%s,%s,%s,%s,%s)"
    cur.executemany("select * from HourWise where Date=%s and Hour=%s order by Date and Hour desc",[(tm[:10],tm[10:13])])
    check=cur.fetchall()
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        data={'ip': request.environ['REMOTE_ADDR'],'timestamp':tm,'browser':request.user_agent._browser, 'os':request.user_agent._platform }
        a = [tm[:10],tm[11:13],data['ip'],data['browser'],data['os']]
        cur.executemany(sql,[(a[0],a[1],a[2],a[-2],a[-1])])
        con.commit()
        if len(rest)==0 or str(rest[-1][1])!=tm[11:13]:
            v,u=1,1
            mn=[tm[:10],tm[11:13],v,u,{data['browser']:1},{data['os']:1},[data['ip']]]
            rest.append(mn)
            if len(check)==0:
                cur.executemany(sqls,[(rest[-1][0],rest[-1][1],str(rest[-1][2]),str(rest[-1][3]),str(rest[-1][-3]),str(rest[-1][-2]),str(rest[-1][-1]))])
                con.commit()

        else:
            rest[-1][2]+=1
            if a[2] not in rest[-1][-1]:
                rest[-1][3]+=1
                
                rest[-1][-1].append(a[2])
            if a[3] in rest[-1][4]:
                rest[-1][4][a[3]] += 1
            else:
                rest[-1][4][a[3]] = 1
            if a[-1] in rest[-1][-2]:
                rest[-1][-2][a[-1]] += 1
            else:
                rest[-1][-2][a[-1]] = 1
            cur.executemany("update HourWise set VISITS=%s,UNIQUES=%s,BROWSER=%s,OS=%s,IP=%s where DATE=%s and HOUR=%s order by DATE and HOUR desc limit 1",[(str(rest[-1][2]),str(rest[-1][3]),str(rest[-1][-3]),str(rest[-1][-2]),str(rest[-1][-1]),tm[:10],tm[11:13])])
            con.commit()


            
    else:
        data={'ip': request.environ['HTTP_X_FORWARDED_FOR'],'timestamp':tm,'browser':request.user_agent._browser, 'os':request.user_agent._platform }
        a = [tm[:10],tm[11:13],data['ip'],data['browser'],data['os']]
        cur.executemany(sql,[(a[0],a[1],a[2],a[-2],a[-1])])
        con.commit()
        if len(rest)==0 or str(rest[-1][1])!=tm[11:13]:
            v,u=1,1
            mn=[tm[:10],tm[11:13],v,u,{data['browser']:1},{data['os']:1},[data['ip']]]
            rest.append(mn)
            if len(check)==0:
                cur.executemany(sqls,[(rest[-1][0],rest[-1][1],str(rest[-1][2]),str(rest[-1][3]),str(rest[-1][-3]),str(rest[-1][-2]),str(rest[-1][-1]))])
                con.commit()

        else:
            rest[-1][2]+=1
            if a[2] not in rest[-1][-1]:
                rest[-1][3]+=1
                
                rest[-1][-1].append(a[2])
            if a[3] in rest[-1][4]:
                rest[-1][4][a[3]] += 1
            else:
                rest[-1][4][a[3]] = 1
            if a[-1] in rest[-1][-2]:
                rest[-1][-2][a[-1]] += 1
            else:
                rest[-1][-2][a[-1]] = 1
            cur.executemany("update HourWise set VISITS=%s,UNIQUES=%s,BROWSER=%s,OS=%s,IP=%s where DATE=%s and HOUR=%s order by DATE and HOUR desc limit 1",[(str(rest[-1][2]),str(rest[-1][3]),str(rest[-1][-3]),str(rest[-1][-2]),str(rest[-1][-1]),tm[:10],tm[11:13])])
            con.commit()



    return render_template('index.html')

@app.route('/hr/result', methods=['GET'])
def res():
    return str(rest)
    '''d={}
    for j in range(0,len(rest)):
        d.update({"HourWise Result":list({"Date":[rest[j][0]],"Hour":[rest[j][1]],"Visits":[rest[j][2]],"Unique":[rest[j][3]],"Browser":[rest[j][4]],"Os":[rest[j][5]],"IP":[rest[j][6]]})})
    return json.dumps(d,indent=4)'''


if __name__=="__main__":
    app.run()




















































'''import json
from flask import Flask,jsonify,render_template,request
import pymysql as p
from datetime import datetime
import time

str(rest),
rest=[]
app=Flask(__name__)

@app.route('/', methods=['GET'])
def index():


    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        data={'ip': request.environ['REMOTE_ADDR'],'timestamp':datetime.now(),'browser':request.user_agent._browser, 'os':request.user_agent._platform }
        tm=data['timestamp'].strftime("%Y-%m-%d %H-%M-%S")
        a = [tm[:10],tm[11:13],data['ip'],data['browser'],data['os']]
      
        if len(rest)==0:
            print("len(a)==0:",rest)
            v,u=1,1
            mn=[tm[:10],tm[11:13],v,u,{data['browser']:1},{data['os']:1},[data['ip']]]
            print(mn)
            rest.append(mn)
        
            

        else:
            print(rest)
            rest[0][2]+=1
            if a[2] not in rest[0][-1]:
                rest[0][3]+=1
                rest[0][-1].append(a[2])
            if a[3] in rest[0][4]:
                rest[0][4][a[3]] += 1
            else:
                rest[0][4][a[3]] = 1
            if a[-1] in rest[0][-2]:
                rest[0][-2][a[-1]] += 1
            else:
                rest[0][-2][a[-1]] = 1
                

    return str(rest)

@app.route('/result')
def res():
    return str(rest)

if __name__=="__main__":
    app.run()'''




'''import urllib.request
from pprint import pprint
from html_table_parser.parser import HTMLTableParser
import pandas as pd
import json
from flask import Flask,jsonify,render_template,request
import pymysql as p
from datetime import datetime
import time


app=Flask(__name__)


con=p.connect(host="database-1.czejdnwyu0eq.ap-south-1.rds.amazonaws.com",user="root",password="Ivisivis5",database="QRCODE_DATA")
cur=con.cursor()
#cur.execute("create table Hour_Wise_Data(DATE date,HOUR char(10),VISITS int(10),UNIQUES int(10),BROWSER VARCHAR(65530),OS VARCHAR(65530),IP VARCHAR(65530))")
#con.commit()


sql="insert into Raw_Data(Date,Hour,Ip,Browser,Os)values(%s,%s,%s,%s,%s)"
sqls="insert into Hour_Wise_Data(DATE,HOUR,VISITS,UNIQUES,BROWSER,OS,IP)values(%s,%s,%s,%s,%s,%s,%s)"
#upsql="update Hour_Wise_Data set VISITS=v
#create table Raw_Data(Date char(20),Hour char(10),Ip char(20),Browser char(30),Os char(30))


@app.route('/', methods=['GET'])
def index():
    v,u=1,1
    tm=time.strftime("%Y-%m-%d %H-%M-%S")
    cur.executemany("select * from Hour_Wise_Data where DATE=%s and HOUR=%s order by DATE desc",[(str(tm[:10]),str(tm[11:13]))])
    a=cur.fetchall()
    print("a:",a)
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        data={'ip': str(request.environ['REMOTE_ADDR']),'timestamp':datetime.now(),'browser':str(request.user_agent._browser), 'os':str(request.user_agent._platform)}
        tm=data['timestamp'].strftime("%Y-%m-%d %H-%M-%S")
        cur.executemany(sql,[(tm[:10],tm[11:13],data['ip'],data['browser'],data['os'])])
        con.commit()
        
        if len(a)==0:
            print("len(a)==0:",a)
            cur.executemany(sqls,[(tm[:10],tm[11:13],str(v),str(u),data['browser'],data['os'],data['ip'])])
            con.commit()
        else:
            print("if-else:len(a):",a)
            bro,os,ip=[a[0][-3]],[a[0][-2]],[a[0][-1]]
            print("bro:{}\nosu:{}\nip:{}".format(bro,os,ip))
            v,u=int(a[0][2]),int(a[0][3])
            print("v:{}\nu:{}".format(v,u))
            brd={}
            osd={}
            brl,osl=[],[]
            if a[0][-1] != data['ip']:
                bro.append(data['browser'])
                os.append(data['os'])
                ip.append(data['ip'])
                for i in bro:
                    brd.update({i:bro.count(i)})
                brl.append(brd)
                print("brl:",brl)
                for i in os:
                    osd.update({i:os.count(i)})
                osl.append(osd)
                print("osl:",osl)

            elif a[0][-1] == data['ip']:
                bro.append(data['browser'])
                os.append(data['os'])
                for i in bro:
                    brd.update({i:bro.count(i)})
                brl.append(brd)
                print("brl:",brl)
                for i in os:
                    osd.update({i:os.count(i)})
                osl.append(osd)
                print("osl:",osl)
                print("ip:",ip)
                print("vis:",str(v+1))
            cur.executemany("update Hour_Wise_Data set VISITS=%s,UNIQUES=%s,BROWSER=%s,OS=%s,IP=%s where DATE={} and HOUR={} order by DATE desc".format(tm[:10],tm[11:13]),[(str(v+1),str(u),str(brl),str(osl),str(ip))])
            con.commit()





            
        
    else:
        data={'ip': str(request.environ['HTTP_X_FORWARDED_FOR']),'timestamp':datetime.now(),'browser':str(request.user_agent._browser), 'os':str(request.user_agent._platform)}
        tm=data['timestamp'].strftime("%Y-%m-%d %H-%M-%S")
        cur.executemany(sql,[(tm[:10],tm[11:13],data['ip'],data['browser'],data['os'])])
        con.commit()
        cur.executemany(sqls,[(tm[:10],tm[11:13],str(v),str(u),data['browser'],data['os'],data['ip'])])
        con.commit()
        cur.execute("select * from Hour_Wise_Data order by DATE desc")
        b=cur.fetchall()
        print("raw:",b)
        cur.executemany("select * from Hour_Wise_Data where DATE=%s or HOUR=%s order by DATE desc",[(str(tm[:10]),str(tm[11:13]))])
        a=cur.fetchall()

        brl,osl=[],[]
        print("a:",a)
        if len(a)==0:
            print("len(a)==0:",a)
            cur.executemany(sqls,[(tm[:10],tm[11:13],str(v),str(u),data['browser'],data['os'],data['ip'])])
            con.commit()
        else:
            print("elelse:len(a):",a)
            v,u=int(a[0][2]),int(a[0][3])
            print("v:{}\nu:{}".forat(v,u))
            bro,os,ip=[a[0][-3]],[a[0][-2]],[a[0][-1]]
            print("bro:{}\nosu:{}\nip:{}".format(bro,os,ip))
            brd={}
            osd={}
            if a[0][-1] != data['ip']:
                bro.append(data['browser'])
                os.append(data['os'])
                ip.append(data['ip'])
                for i in bro:
                    brd.update({i:bro.count(i)})
                brl.append(brd)
                print("brl:",brl)
                for i in os:
                    osd.update({i:os.count(i)})
                osl.append(osd)
                print("osl:",osl)
                cur.executemany("update Hour_Wise_Data set VISITS=%s,UNIQUES=%s,BROWSER=%s,OS=%s,IP=%s where DATE={} and HOUR={} order by DATE desc".format(tm[:10],tm[11:13]),[(str(v+1),str(u+1),str(brl),str(osl),str(ip))])
                con.commit()
            elif a[0][-1] == data['ip']:
                bro.append(data['browser'])
                os.append(data['os'])
                for i in bro:
                    brd.update({i:bro.count(i)})
                brl.append(brd)
                for i in os:
                    osd.update({i:os.count(i)})
                osl.append(osd)
                cur.executemany("update Hour_Wise_Data set VISITS=%s,UNIQUES=%s,BROWSER=%s,OS=%s,IP=%s where DATE={} and HOUR={} order by DATE desc".format(tm[:10],tm[11:13]),[(str(v+1),str(u),str(brl),str(osl),str(ip))])
                con.commit()
            else:
                pass
            
    return render_template('index.html')






if __name__ == '__main__':
    app.run()'''
