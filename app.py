from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import sys
from datetime import datetime

def time_calculator_in_minutes(time1, time2):
    fmt="%I:%M:%p"
    try:
        #print("before",time1,time2)
        time1 = datetime.strptime(time1,fmt)
        time2 = datetime.strptime(time2,fmt)
        period = (time2-time1).seconds/60
        #print("after")
    except:
        return 0;
    return period
    

def totaltimespent(filename):
    f = open(app.config['UPLOAD_FOLDER']+filename,'r')
    m=f.read()
    m=m.upper();
    totaltime=0;
    index=m.find("TIME LOG:");
    if index!=-1:
        m=m[index+9:]
    index=m.find('-')
    while (index!=-1):
        if m[index+1]==' ':
            m=m[:index-1]+"&"+m[index+2:];
        elif m[index-1]==' ':
            m=m[:index-2]+"&"+m[index+1:]
        else:
            m=m[:index-1]+"&"+m[index+1:];
        index = m.find("&",index-2,index+2);
        st = m.rfind(" ",0,index);
        st = m[st+1:index];
        et = m.find("M",index,index+15);
        et = m[index+1:et+1];
        st = st[:len(st)-2]+":"+st[len(st)-2:]
        et = et[:len(et)-2]+":"+et[len(et)-2:]
        totaltime=totaltime + time_calculator_in_minutes(st,et)
        #print(totaltime)
        index = m.find('-')
    return totaltime



app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/"

@app.route('/')
def upload_file():
    return render_template('index.html') 
    
@app.route('/output', methods = ['GET', 'POST'])
def parse():  
    if request.method == 'POST':
        f = request.files['input_file']        
        filename = secure_filename(f.filename)
        f.save(app.config['UPLOAD_FOLDER'] + filename)
        ti = totaltimespent(filename);
        hours = int(ti/60)
        mins = int(ti%60)
        totaltime="Total Time spent by the author is the given file is "+str(hours)+" hours "+str(mins)+" minutes";   
        return render_template('index.html',spentime=totaltime)
    return render_template('index.html')
                    

if __name__ == '__main__':
    app.run(debug = True)
