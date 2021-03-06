# -*- coding:utf-8 -*-

import paramiko
import time

class SSHCommand(object):
    hostname = ''
    username = ''
    password = ''

    errorlogPath = ''
    errorMessage = ''

    client = ""
    connection = ''
    result = ''

    def __init__(self, hostname, username, password, errorlogPath='/var/www/html/configuration-collector/###error.log'):
        print(hostname+'開始')
        self.hostname = hostname
        self.username = username
        self.password = password
        self.errorlogPath = errorlogPath
        self.run()

    def __del__(self):
        pass

    def run(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.hostname, username=self.username, password=self.password, timeout=15.0, look_for_keys=False, allow_agent=False)
            self.connection = self.client.invoke_shell()
            self.sendCommand()

        except paramiko.ssh_exception.AuthenticationException as authException:
            self.errorMessage = 'SSH認証失敗\t' + str(authException)
        except paramiko.ssh_exception.SSHException as sshException:
            self.errorMessage = 'SSHエラー\t' + str(sshException)
        except Exception as exception:
            self.errorMessage = '一般エラー\t' + str(exception)
        finally:
            self.client.close()

        if( len(self.errorMessage) > 0 ):
            print('[' + self.hostname + ']\t' + self.errorMessage)
            try:
                file = open(self.errorlogPath,"a")
                file.write('[' + self.hostname + ']\t' + self.errorMessage + '\n')
                file.close()
            except Exception as exception:
                print(exception)


    def sendCommand(self):
        print('Override')


### Cisco Router and Catalyst Switch
class SSHCommandPattern1(SSHCommand):
    def sendCommand(self):
        time.sleep(3)
        self.connection.send('enable\n')
        time.sleep(1)
        self.connection.send('enable-password' + '\n')
        time.sleep(1)
        self.connection.send('terminal length 0\n')
        time.sleep(1)
        self.connection.recv(65535).decode('utf-8')
        self.connection.send('copy running-config startup-config\n')
        time.sleep(2)
        self.connection.send('\n')
        time.sleep(5)
        self.connection.send('show running-config\n')
        time.sleep(15)
        self.connection.send('show interface status\n')
        time.sleep(5)
        self.connection.send('show ip interface brief\n')
        time.sleep(5)
        self.connection.send('show lldp neighbors\n')
        time.sleep(5)
        self.connection.send('show cdp neighbors\n')
        time.sleep(5)
        self.connection.send('show inventory\n')
        time.sleep(10)
        self.result = self.connection.recv(65535).decode('utf-8')
        self.connection.send('exit\n')
        time.sleep(3)

        if len(self.result) > 250:
            file = ''
            try:
                file = open("/var/www/html/configuration-collector/"+self.hostname+".log","w")
                file.write(self.result)
                print("["+self.hostname+"] Getting config complete!")
            except Exception as e:
                print("["+self.hostname+"] Getting config failed")
                print(e)
            finally:
                file.close()



### Panasonic LS Networks MNO Series Switch
class SSHCommandPattern2(SSHCommand):
    def sendCommand(self):
        time.sleep(10)
        self.connection.send('c\n')
        time.sleep(3)
        self.connection.send('enable\n')
        time.sleep(3)
        self.connection.recv(65535).decode('utf-8','ignore')
        self.connection.send('copy running-config startup-config\n')
        time.sleep(5)
        self.connection.send('show running-config\n')
        time.sleep(20)
        self.connection.send('show interface info\n')
        time.sleep(10)
        self.connection.send('show vlan all\n')
        time.sleep(10)
        self.connection.send('show lldp neighbors\n')
        time.sleep(10)
        self.result = self.connection.recv(65535).decode('utf-8','ignore')
        self.connection.send('exit\n')
        time.sleep(1)
        self.connection.send('exit\n')
        time.sleep(1)
        self.connection.send('q\n')
        time.sleep(3)

        if len(self.result) > 250:
            file = ''
            try:
                file = open("/var/www/html/configuration-collector/"+self.hostname+".log","w")
                file.write(self.result)
                print("["+self.hostname+"] Getting config complete!")
            except Exception as e:
                print("["+self.hostname+"] Getting config failed")
                print(e)
            finally:
                file.close()


### A10 thunder
class SSHCommandPattern3(SSHCommand):
    def sendCommand(self):
        time.sleep(3)
        self.connection.send('enable\n')
        time.sleep(1)
        self.connection.send('enable-password' + '\n')
        time.sleep(1)
        self.connection.send('terminal length 0\n')
        time.sleep(1)
        self.connection.recv(65535).decode('utf-8')
        time.sleep(5)
        self.connection.send('show running-config\n')
        time.sleep(15)
        self.result = self.connection.recv(655350).decode('utf-8')
        self.connection.send('exit\n')
        time.sleep(3)
        self.connection.send('exit\n')
        time.sleep(3)
        self.connection.send('y')
        time.sleep(3)

        if len(self.result) > 250:
            file = ''
            try:
                file = open("/var/www/html/configuration-collector/"+self.hostname+".log","w")
                file.write(self.result)
                print("["+self.hostname+"] Getting config complete!")
            except Exception as e:
                print("["+self.hostname+"] Getting config failed")
                print(e)
            finally:
                file.close()


### Fortinet FortiGate Series
class SSHCommandPattern4(SSHCommand):
    def sendCommand(self):
        time.sleep(3)
        self.connection.send('show\n')
        time.sleep(20)
        self.result = self.connection.recv(655350).decode('utf-8')
        self.connection.send('exit\n')
        time.sleep(3)

        if len(self.result) > 250:
            file = ''
            try:
                file = open("/var/www/html/configuration-collector/"+self.hostname+".log","w")
                file.write(self.result)
                print("["+self.hostname+"] Getting config complete!")
            except Exception as e:
                print("["+self.hostname+"] Getting config failed")
                print(e)
            finally:
                file.close()


### Cisco Firepower, ASA
class SSHCommandPattern5(SSHCommand):
    def sendCommand(self):
        time.sleep(3)
        self.connection.send('enable\n')
        time.sleep(1)
        self.connection.send('enable-password' + '\n')
        time.sleep(1)
        self.connection.send('terminal pager 0\n')
        time.sleep(1)
        self.connection.recv(65535).decode('utf-8')
        self.connection.send('copy running-config startup-config\n')
        time.sleep(10)
        self.connection.send('\n')
        time.sleep(5)
        self.connection.send('show running-config\n')
        time.sleep(15)
        self.connection.send('show ip address\n')
        time.sleep(5)
        self.connection.send('show lldp neighbors\n')
        time.sleep(5)
        self.connection.send('show cdp neighbors\n')
        time.sleep(5)
        self.connection.send('show inventory\n')
        time.sleep(5)
        self.result = self.connection.recv(655350).decode('utf-8')
        self.connection.send('exit\n')
        time.sleep(3)

        if len(self.result) > 250:
            file = ''
            try:
                file = open("/var/www/html/configuration-collector/"+self.hostname+".log","w")
                file.write(self.result)
                print("["+self.hostname+"] Getting config complete!")
            except Exception as e:
                print("["+self.hostname+"] Getting config failed")
                print(e)
            finally:
                file.close()


### Mellanox Ethernet Switch
class SSHCommandPattern6(SSHCommand):
    def sendCommand(self):
        time.sleep(10)
        self.connection.send('enable\n')
        time.sleep(1)
        self.connection.send('no cli session paging enable\n')
        time.sleep(3)
        self.connection.recv(65535).decode('utf-8')
        self.connection.send('write memory\n')
        time.sleep(3)
        self.connection.send('\n')
        time.sleep(5)
        self.connection.send('show running-config\n')
        time.sleep(15)
        self.connection.send('show interface status\n')
        time.sleep(5)
        self.connection.send('show ip interface brief\n')
        time.sleep(5)
        self.connection.send('show lldp remote\n')
        time.sleep(5)
        self.connection.send('show inventory\n')
        time.sleep(10)
        self.result = self.connection.recv(65535).decode('utf-8')
        self.connection.send('exit\n')
        time.sleep(3)

        if len(self.result) > 250:
            file = ''
            try:
                file = open("/var/www/html/configuration-collector/"+self.hostname+".log","w")
                file.write(self.result)
                print("["+self.hostname+"] Getting config complete!")
            except Exception as e:
                print("["+self.hostname+"] Getting config failed")
                print(e)
            finally:
                file.close()
