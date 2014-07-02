#encoding=utf-8
#sshcrack by daige
#ssh连接模块 使用paramiko

from sys       import exit
from threading import Thread

try:
    from paramiko import SSHClient
    from paramiko import AutoAddPolicy
except ImportError as err:
    print "[!]import error: \n  " +str(err)
    exit(0)

class SSHConnect(Thread):
    '''
    这是一个使用用户名和密码来测试连接ssh是否成功的类
    '''
    def __init__(self,userName,passWord,targetIp,portNumber,timeoutTime):

        super(SSHConnect,self).__init__()

        self.userName    = userName
        self.passWord    = passWord
        self.targetIp    = targetIp
        self.portNumber  = portNumber
        self.timeoutTime = timeoutTime
        self.status      = None
        self.connection  = None

    def __del__(self):
        pass
       # self.connection.close()

    def connect(self):
       
       sshConnection = SSHClient();
       sshConnection.set_missing_host_key_policy(AutoAddPolicy())
       
       try:
          sshConnection.connect( self.targetIp,
                                 self.portNumber,
                                 self.userName,
                                 self.passWord,
                                 timeout=self.timeoutTime,
                                 allow_agent=False,
                                 look_for_keys=False)
          self.status = True
          self.connection = sshConnection
       except:
           self.status = False
        

    def exec_command(self,command):
        stdin,stdout,stderr= self.connection.exec_command(command)
        lines=stdout.readlines()
        for line in lines:
            print line
