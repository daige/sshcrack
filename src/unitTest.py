from  FileParser import *
from  SSHConnect import *
from  Banner     import *
'''
data=[]
data =fileToList("ass.txt")

print data

appendLineToFile("xxx","pass.txt")

data = fileToList("pass.txt")

print data
'''

con = SSHConnect("root",'xxxxxx',"xxxxxxxxx",22,4)

print con.userName
print con.passWord
print con.portNumber
print con.status

con.connect()
#con.exec_command('who')

print con.status

#showBanner()


