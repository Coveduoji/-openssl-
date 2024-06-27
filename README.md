# -基于openssl的安全聊天程序课设-
环境准备：

安装 OpenSSL。
安装必要的 Python 库：
sh
复制代码
pip install pyOpenSSL
pip install pycryptodome
生成证书和密钥：

生成 CA 私钥：
sh
复制代码
openssl genpkey -algorithm RSA -out ca.key -pkeyopt rsa_keygen_bits:2048
生成 CA 请求文件：
sh
复制代码
openssl req -new -key ca.key -out ca.csr
生成 CA 证书：
sh
复制代码
openssl x509 -req -in ca.csr -signkey ca.key -out ca.crt
生成服务器私钥：
sh
复制代码
openssl genpkey -algorithm RSA -out server.key -pkeyopt rsa_keygen_bits:2048
生成服务器请求文件：
sh
复制代码
openssl req -new -key server.key -out server.csr
生成服务器证书：
sh
复制代码
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt
生成客户端私钥：
sh
复制代码
openssl genpkey -algorithm RSA -out client.key -pkeyopt rsa_keygen_bits:2048
生成客户端请求文件：
sh
复制代码
openssl req -new -key client.key -out client.csr
生成客户端证书：
sh
复制代码
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt
