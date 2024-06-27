import socket
import threading
import datetime as dt
import ssl
import pprint
import binascii
from pyDes import des, CBC, PAD_PKCS5

# DES-CBC加密
def des_encrypt(s, key='wld12345'):
    secret_key = key.encode()  # 将密钥编码为字节串
    iv = '12345678'.encode()  # 将偏移量编码为字节串
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s.encode(), padmode=PAD_PKCS5)  # 将输入字符串编码为字节串
    return binascii.b2a_hex(en)

# DES-CBC解密
def des_descrypt(s, key):
    secret_key = key.encode()  # 将密钥编码为字节串
    iv = '12345678'.encode()  # 将偏移量编码为字节串
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    return de.decode()  # 解密后的字节串转换为字符串

# 从记录文本中读取并解密信息
def read_record():
    password = input('请输入聊天记录密码\n')
    with open('record.txt', 'rb') as fp:
        record = fp.read()
        record = des_descrypt(s=record, key=password)
        print(record)

# 将聊天信息加密后写入记录文本
def write_record(s):
    with open('record.txt', 'rb') as fp:
        old_s = fp.read()
        old_s = des_descrypt(old_s, 'wld12345')
        old_s = str(old_s)
        s = old_s + '\n' + s

    with open('record.txt', 'wb') as fp:
        es = des_encrypt(s=s)
        fp.write(es)

# 与服务器建立双向验证的SSL连接
def sslConnect(serverIP, dPort):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)  # 创建一个SSL上下文，指定支持的协议版本
    context.verify_mode = ssl.CERT_REQUIRED  # 该SSL需要对方提供证书
    context.load_verify_locations('ca.crt')  # 加载可信根的证书
    context.load_cert_chain(certfile='client.crt', keyfile='client.key')  # 加载自己的证书和私钥
    
    sock = socket.socket()  # 创建一个套接字
    sslSocket = context.wrap_socket(sock, server_hostname=serverIP)  # 将套接字与SSL绑定
    sslSocket.connect((serverIP, dPort))
        
    pprint.pprint(sslSocket.getpeercert())  # 打印证书信息
    
    print('已与服务器接通，请开始聊天')
    return sslSocket

# 接收服务器的信息
def rcvInfo(sslSocket):
    if not sslSocket:
        return False
    else:
        while True:
            info = sslSocket.recv(1024).decode()
            if info == 'exit':
                print('服务器断开连接')
                sslSocket.close()
                exit()
                break
            elif len(info) > 0:
                nowtime = dt.datetime.now().strftime('%F %T')
                info = '[server at ' + nowtime + '] ' + info
                print(info)
                write_record(info)
        return True

# 向服务器发送信息
def sendInfo(sslSocket, serverIP):
    if not sslSocket:
        return False
    else:
        while True:
            sentence = input('')
            if len(sentence) > 0:
                sslSocket.send(sentence.encode())
                if sentence == 'exit':
                    exit()
                elif sentence == 'read':
                    read_record()
                else:
                    nowtime = dt.datetime.now().strftime('%F %T')
                    sentence = '[client at ' + nowtime + '] ' + sentence
                    write_record(s=sentence)

if __name__ == '__main__':
    s = 'record\n'
    s = des_encrypt(s)
    with open('record.txt', 'wb') as fp:
        fp.write(s)
    
    serverIP = '127.0.0.1'
    serverPort = 12000
    
    sslSocket = sslConnect(serverIP=serverIP, dPort=serverPort)
    
    client1_threading = threading.Thread(target=rcvInfo, args=(sslSocket,))
    client1_threading.start()
    client2_threading = threading.Thread(target=sendInfo, args=(sslSocket, serverIP,))
    client2_threading.start()
