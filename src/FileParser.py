#encoding=utf-8
#sshCrack by daige
#文件处理模块


#TODO:对大文件的处理
def fileToList(fileName):

    lineList = []

    try:
        fileParser = open(fileName,'r')
    
    except IOError as ioerr:
        print "[!] open file error: \n   " + str(ioerr)
    except:
        print "[!] can't access the file: %s " % fileName

    for line in fileParser.readlines():
        newLine = line.strip('\n').strip('\r')
        lineList.append(newLine)

    fileParser.close()

    return lineList

def appendLineToFile(line,fileName):
    filefd = open(fileName,'a')
    filefd.write(line+"\n")
    filefd.close()

