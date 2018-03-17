#coding=UTF-8
import os
import hashlib
import sys
import time
import difflib
import random
def fun10(_Time):
    if _Time<10:
        _Time="0"+str(_Time)
    else:
        _Time=str(_Time)
    return _Time

def pathComFun(A,B,comFileList,comFileListLost,isF_S):
    for i in A[1]:
        n=0
        for j in B[1]:
            if i.split(A[0])[1].split("/") == j.split(B[0])[1].split("/"):
                n= -1
                break
            else:
                n = n+1
        if n == -1:
            if isF_S == "F":
                comFileList.append(returnLineFun(i, j, "ok", "ok"))
            else:
                pass
        else:
            if isF_S == "F":
                comFileListLost.append(returnLineFun(i, j, "wrong", "second"))
            else:
                comFileListLost.append(returnLineFun(j, i, "wrong", "first"))
    return comFileList,comFileListLost
def returnLineFun(path1,path2,ok_wrong,isNull):
    if ok_wrong == "wrong":
        if isNull == "ok":
            return "wrong" + "##" + path1 + "##" + path2
        elif isNull == "first":
            return "wrong" + "##" + "null" + "##" + path2
        elif isNull == "second":
            return "wrong" + "##" + path1 + "##" + "null"
        else:
            pass
    else:
        return "ok" + "##" + path1 + "##" + path2
def creComFileFun(A,B):
    comFileList=[]
    comFileListLost=[]
    if os.path.isfile(A[0]) and os.path.isfile(B[0]):
        if A[0].split("/")[-1] == B[0].split("/")[-1]:
            comFileList.append(returnLineFun(path1, path2, "ok", "ok"))
        else:
            comFileList.append(returnLineFun(path1, path2, "wrong", "ok"))
    elif os.path.isdir(A[0]) and os.path.isdir(B[0]):
        comFileList,comFileListLost = pathComFun(A,B,comFileList,comFileListLost,"F")
        comFileList,comFileListLost = pathComFun(B,A,comFileList,comFileListLost,"S")
        comFileList = comFileList + comFileListLost
    else:
        pass
    return comFileList

def md5Fun(path):
    path=path.split("\n")[0]
    md5file=open(path)
    data=md5file.read()
    m=hashlib.md5()
    m.update(data)
    md5=m.hexdigest()
    md5file.close()
    return md5

def isMd5TheSame(path1,path2):
    if md5Fun(path1) == md5Fun(path2):
        return "same"
    else:
        return "deffrent"
    
def readFile(filepath):
    filepath=filepath.split("\n")[0]
    fileHandle = open(filepath)
    fileData = fileHandle.read().splitlines()
    fileHandle.close()
    return fileData

def diffHtmlFun(path1,path2,comListDirPath):
    fileName = nowTimefun("ms") + "_" +path1.split("/")[-1]
    path1Data = readFile(path1)
    path2Data = readFile(path2)
    d = difflib.HtmlDiff()
    comHtmlData=d.make_file(path1Data,path2Data)
    comResultHtmlPath=comListDirPath + "/" +fileName +".html"
    fileOpen = open(comResultHtmlPath,'w')
    fileOpen.write(comHtmlData)
    fileOpen.close()
    

def diffFun(line,comListDirPath):
    lineList=line.split("##")
    if lineList[0] == "wrong":
        return "wrong"
    elif lineList[0] == "ok":
        if os.path.isdir(lineList[1]) == True:
            return "same"
        elif os.path.isfile(lineList[1]) == True:
            if isMd5TheSame(lineList[1],lineList[2]) =="same":
                return "same"
            else:
                diffHtmlFun(lineList[1],lineList[2],comListDirPath)
                return "deffrent"
        else:
            pass
    else:
        pass

def diffHtmlCreFun(comListDirPath,comListFilepath):
    diffResultStr = ""
    diffResultStrDe = ""
    diffResultStrWr = ""
    comData=open(comListFilepath)
    for line in comData.readlines():
        diffResult = diffFun(line,comListDirPath)
        if diffResult == "same":
            diffResultStr = diffResultStr + "same" + "##" +line 
        elif diffResult == "deffrent":
            diffResultStrDe = diffResultStrDe + "deffrent" + "##" +line 
        elif diffResult == "wrong":
            diffResultStrWr = diffResultStrWr + "wrong" + "##" +line 
        else:
            pass
    diffResultStr = diffResultStr + "\n" + diffResultStrDe + "\n" + diffResultStrWr
    if not diffResultStr:
        diffResultStr = " All the Same"
    else:
        pass
    comResultFilePath= comListDirPath + "/" +"comResult.txt"
    fileOpen = open(comResultFilePath,'w')
    fileOpen.write(diffResultStr)
    fileOpen.close()
    print "End   ###################   End"

def nowTimefun(sms):
    _nowTime = time.localtime()
    if sms == "s":
        sNowTime = fun10(_nowTime.tm_year)+"年"+fun10(_nowTime.tm_mon)+"月"+fun10(_nowTime.tm_mday)+"日"+fun10(_nowTime.tm_hour)+"时"+fun10(_nowTime.tm_min)+"分"+fun10(_nowTime.tm_sec)+"秒"
    elif sms == "ms":
        sNowTime = fun10(_nowTime.tm_year)+fun10(_nowTime.tm_mon)+fun10(_nowTime.tm_mday)+fun10(_nowTime.tm_hour)+fun10(_nowTime.tm_min)+fun10(_nowTime.tm_sec)+"_" +str(random.randint(10, 99))              
    else:
        pass
    return sNowTime
def fileDiffResultFun(tuple1,tuple2):
    comFileList = creComFileFun(tuple1, tuple2)
    comList = ""
    nowTime=nowTimefun("s")
    whereiSMe=os.path.split( os.path.realpath( sys.argv[0] ) )[0]
    comListDirPath = whereiSMe + "/" +nowTime
    comListFilepath =  whereiSMe + "/" +nowTime + "/" +"comList" + ".txt"
    os.mkdir(comListDirPath)
    for i in comFileList:
        comList= comList + i + "\n"
    fileOpen = open(comListFilepath,'w')
    fileOpen.write(comList)
    fileOpen.close()
    diffHtmlCreFun(comListDirPath,comListFilepath)
    
    
    

def creFileListFun(path):
    fileList = [ ]
    if os.path.isfile(path)==True:
        fileList.append(path)
    elif os.path.isdir(path) == True:
        for i in os.walk(path):
            for k in i[1]:
                fileList.append( i[0]+"/" +k)
            for j in i[2]:
                fileList.append(i[0]+"/" +j)
    return fileList
def isFileExistFun(path):
    if os.path.exists(path)==True:
        return "True"
    else:
        print "your input is : \"%s\",input wrong,Please input gain"%(path)
        return "False"

if __name__=="__main__":
    print "Please input your two comparing file"
    print "The first file path is:"
    path1 = raw_input()
    if isFileExistFun(path1) == "True":
        print "The second file path is:"
        path2 = raw_input()
        if isFileExistFun(path2) == "True":
            if((os.path.isfile(path1) and os.path.isfile(path2)) or (os.path.isdir(path1) and os.path.isdir(path2))):
                path_list1 = creFileListFun(path1)
                path_list2 = creFileListFun(path2)
                tuple_1 = (path1,path_list1)
                tuple_2 = (path2,path_list2)
                fileDiffResultFun(tuple_1,tuple_2)
            else:
                print "The kind of your two input is diffrent,Please input again"
            
        else:
            pass
    else:
        pass
