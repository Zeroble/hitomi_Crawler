from urllib.request import urlopen
import urllib.request
import requests
import zipfile
import os
import shutil
from bs4 import BeautifulSoup

def count():
    
    global page
    global page100
    global page10
    global page1
    
    page+=1
    page1+=1
    if(page1 == 10):
        page10+=1
        page1 = 0
    if(page10 == 10):
        page100+=1
        page10=0
        
def url_slice(URL):
    URL = URL[28:]
    URL = URL[:-5]
    return URL

baseURL = "https://hitomi.la/reader/"

while(1):
    page = 1
    page100 = 0
    page10 = 0
    page1 = 1

    curPath = "./"
    aftPath = "./"

    print("(0입력시 종료) 히또미 링크를 넣어주세요.\n예) https://hitomi.la/galleries/1070435.html\n입력 : ",end="")
    URL = str(input())
    if(URL == "0"):
        break
    number = url_slice(URL)
    print(number)
    aftPath = aftPath+number+"/"

    URL = baseURL+number+".html"
    print(URL)
    print("")

    check = 0
    req = requests.get(URL)
    html = req.text
    soup = BeautifulSoup(html, "html.parser")
    myUrls = soup.select('div.img-url')
    
    while(1):
        try:
            if not os.path.exists(number):
                os.makedirs(number)
            
            for j in myUrls:
                print("https://ba{0}".format(j.get_text()[3:]))
                filename = number+"-"+str(page100)+str(page10)+str(page1)+j.get_text()[-4:]
                print("filename : {0}".format(filename))
                print("start downloading : {0}% ({1}/{2})".format(int(page/len(myUrls)*100),page,len(myUrls)))
                urllib.request.urlretrieve("https://ba"+j.get_text()[3:],filename)
                print("move file "+filename+" : "+curPath+filename+" -> "+aftPath+filename+"\n")
                shutil.move(curPath+filename,aftPath+filename)
                count()
            check = 15
        except:
             print("ERROR \n")
             check += 1
        finally:
            if(check == 15):
                break
            elif(check >= 5):
                break
        
        if(check != 15):
            break

    
    if(page == 1):
        print("잘못된 형식의 링크같습니다.\n")

    h_zip = zipfile.ZipFile('./'+number+'.zip', 'w')
    print("start zipping files...\n")
    for folder, subfolders, files in os.walk('./'+number+"/"):
        for file in files:
            if (file.endswith('.jpg') or file.endswith('.png')):
                h_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), './'+number+"/"), compress_type = zipfile.ZIP_DEFLATED)
    h_zip.close()
    print("finish zipping files...\n")

    shutil.rmtree(aftPath)
    print("deleting "+aftPath+" finish\n")

'''
page100 = 0
page10 = 0
page1 = 1

for i in range(1,page):
    j = myUrls[i-1]
    count()
    print("remove : {2}-{3}{4}{5}{6} {0}/{1}".format(i,page-1,number,str(page100),str(page10),str(page1),j.get_text()[-4:]))
    os.remove(".\\"+number+"-"+str(page100)+str(page10)+str(page1)+j.get_text()[-4:])
'''
#https://ba.hitomi.la/galleries/
#urllib.request.urlretrieve(ImageUrl,name)
#https://hitomi.la/galleries/1070321.html
#https://hitomi.la/galleries/1070796.html
