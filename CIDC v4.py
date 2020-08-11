from bs4 import BeautifulSoup
#import matplotlib.image as mpimg
import webbrowser
import re
import urllib.request
import matplotlib.pyplot as plt
datad=dict()
allcurr=list()
date1=input("Date1(YYYY-MM-DD)")
date2=input("Date2(YYYY-MM-DD)")
base=(input("Enter Source")).upper()
namel=[date1,date2]


def plotgraph(maindata,commonkeys,base,lofchange,namel):
    p=0
    
    #datawa=dict()
    for i in lofchange:
        if(i<0):
                p=p+1                       #weak
    #print("Weakened Against",p)
    weakp=p/len(commonkeys)
    plt.figure(figsize=(40, 17))

    x=[]
    y=[]
    x1=[]
    y1=[]
    for key in commonkeys:
        if(maindata[key][4]>0 and maindata[key][4]<200):
            x.append(key)
            y.append(maindata[key][4])
        elif(maindata[key][4]<0 and maindata[key][4]>-200):
            x1.append(key)
            y1.append(maindata[key][4])
    
    plt.bar(x,y,label='bars',color='g')
    plt.bar(x1,y1,label='bars',color='r')
    plt.xlabel("Currencies")
    plt.ylabel("INR change % against")
    plt.xticks(rotation=90)
    plt.title(base+" change%\n Weakened Against "+str(round(weakp*100,2))+"% of Total Currencies\n"+str(namel[0])+" to "+str(namel[1]))
    plt.savefig('myfigm')
 
   # plt.show()

    
def weakagainst(lofchange,commonkeys,base):
    p=0
    #datawa=dict()
    for i in lofchange:
        if(i<0):
                p=p+1                       #weak
    print("Weakened Against",p)
    weakp=p/len(commonkeys)
    #datawa[0]=p
    #datawa[1]=weakp
    print("% of currencies against it weakened",weakp*100,"%")
    
    table = "<table class='table table-striped table-hover'>"
    
    table += "<tr>"
    table += "<th>WeakAgainst</th>"
    table += "<th>% of currencies whom against "+str(base)+" Weakened</th>"
    table += "<th>Total Currencies</th>"
    table += "</tr>"
    table += "<tr>"
    table += "<td>" + str(p) + "</td>"
    table += "<td>" + str(weakp*100) + "</td>"
    table += "<td>" + str(len(commonkeys)) + "</td>"
    table += "</tr>"
    table += "</table>"
    return table
    
def create_table(maindata,commonkeys):
    table = "<table class='table table table-hover'>"
    table +='<col width="40">'
    table += "<tr>"
    table += "<th>CurrName</th>"
    table += "<th>Symbol</th>"
    table += "<th>"+(namel[0])+"</th>"
    table += "<th>"+(namel[1])+"</th>"
    table += "<th>% Change</th>"
    table += "<th>Power</th>"
    table += "</tr>"
    for key in commonkeys:
        table += "<tr>"
        table += "<td>" + maindata[key][0]+ "</td>"
        if(maindata[key][4]<0):
            table += '<td bgcolor="#FA8072"> ' + maindata[key][1] + "</td>"
        else:
            table += '<td bgcolor="#0fe20f"> ' + maindata[key][1] + "</td>"
        table += "<td>" + str(maindata[key][2])+ "</td>"
        table += "<td>" + str(maindata[key][3]) + "</td>"
        if(maindata[key][4]<0):
            table += '<td  bgcolor="#FA8072">' + str(maindata[key][4]) + "</td>"
        else:
            table += '<td bgcolor="#0fe20f"> ' + str(maindata[key][4]) + "</td>"
        
        if(maindata[key][4]<0):
                    table += "<td>Weakened</td>"
        elif(maindata[key][4]>0):
                    table += "<td>Strengthened</td>"
        else:
                    table += "<td>No Effect</td>"
        table += "</tr>"
    table += "</table>"
    return table

#Create a html page containing the table data for gainers and losers
def write_html(maindata,commonkeys,lofchange,base):
    html_str = """<html>
             <head>
             <title>RatesDiffcalculator</title>
             <link rel='stylesheet' href='http://netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css' />
             <script type='text/javascript' src='http://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.js'></script>
             <script type='text/javascript' src='http://netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js'></script>
             </head>
             <body>
             <ul class='nav nav-tabs'>
             <li class='active'><a href='#gainers' data-toggle='tab'><h4>Summary</h4></a></li>
             
             </ul>
             <div class='tab-pane active' id='weak'>
             {weak}
             </div>
             <ul class='nav nav-tabs'>
             <li class='active'><a href='#gainers' data-toggle='tab'><h5>RatesDiffCalc</h5></a></li>
             <li><a href='#graphplot' data-toggle='tab'><h5>Graph</h5></a></li>

             </ul>
             
            
             <div class='tab-content'>
             <div class='tab-pane active' id='gainers'>
             {gainersData}
             </div>
             <div class='tab-pane' id='graphplot'>
             <img src='C:/Users/Pandey/Desktop/Mohit/MohitPython/Coursera/myfigm.png' alt='Smiley face' >
             </div>
             
             </div> 
             </body>
             </html>""".format(gainersData = create_table(maindata,commonkeys), weak =weakagainst(lofchange,commonkeys,base))
    return html_str


maindata=dict()
lot=dict()
lot[0]=list()
lot[1]=list()
lofcurrsym=list()
lofcurrname0=dict()
lofcurrname1=dict()
valstore0=dict()
valstore1=dict()
count=0                                                                 #to know which date is being processed

for name in namel:
        print("====================================================",count)
        urlstr='https://www.xe.com/currencytables/?from='+base+'&date='+name
        html = urllib.request.urlopen(urlstr)

        soup=BeautifulSoup(html,"html.parser")
        tags = soup('tr')
        for tag in tags:
                if 300>len(str(tag))>200:
                        #print((tag))
                        p=str(tag)
                        lot[count].append(p)                            #list of tags <tr>
        print("length",len(lot[count]))
                        
        c=0                                                             #key for maindata dictionary
        

        for l in lot[count]:
            c=c+1    
            poscur=l.find("</a>")
            poscur1=l.find("</td><td class=")
            currname=l[(poscur+13):(poscur1)]                           #Currency Name
            
            currsymbol=l[(poscur-3):poscur]                             #Currency Symbol
            lofcurrsym.append(currsymbol)                               #Saving Symbol
            posvalUperBstart=str.find(l,"rateHeader")+12
            posvalUperBend=str.rfind(l,'</td><td class')
            posvalBperUstart=str.rfind(l,"rateHeader")+12
            posvalBperUend=str.rfind(l,'</td>')
            unitsperbase=float(l[posvalUperBstart:posvalUperBend])
            baseperunit=float(l[posvalBperUstart:posvalBperUend])       #Value base per units =========ThisisNeeded=========
            
            if(count==0):
                    valstore0[currsymbol]=baseperunit
                    lofcurrname0[currsymbol]=currname
                    
            elif(count==1):
                    valstore1[currsymbol]=baseperunit
                    lofcurrname1[currsymbol]=currname
        count=count+1
        
commonkeys=list()
p=0
lofchange=list()
for key in valstore0:
        for jey in valstore1:
                if(key==jey):
                        commonkeys.append(key)

for key in commonkeys:
        change=(((valstore0[key]-valstore1[key])*100))/valstore0[key]
        lofchange.append(change)
        maindata[key]=[lofcurrname0[key],key,valstore0[key],valstore1[key],change]

 

#print(maindata)



##try:
##      
html_file = open("wp.html", "w")
html_file.write(write_html(maindata,commonkeys,lofchange,base))
html_file.close()
plotgraph(maindata,commonkeys,base,lofchange,namel)
webbrowser.open_new_tab('wp.html')

##except:
##    print("Taking too long or Network error")
