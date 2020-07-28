from socket import *
import time
import sys
import pbl2019


def SIZE(server_name, server_port,file_name):#[サイズ要求]
    s = socket(AF_INET, SOCK_STREAM)       # ソケットを作る 
    s.connect((server_name, server_port))  # サーバのソケットに接続する

    size="SIZE "+file_name+"\n"
    s.send(size.encode())
    recv_bytearray_size= bytearray()
    file_size= bytearray()
    count=0#空白文字カウント
    while 1:
        a = s.recv(1)[0]
        recv_bytearray_size.append(a)
        A=a.to_bytes(1,'big')
        
        if count == 2 :#総バイト数情報抽出
            file_size.append(a)
        
        if A == b' ' :#空白文字カウント
            count+=1
        
        if A == b'\n':
            break
    recv_str1= recv_bytearray_size.decode()
    print(recv_str1)
    
    file_size.pop()#末尾の空白を消す
    size=file_size.decode()
    size=int(size)
    return size#ファイルサイズを返す。
    s.close()
    
    
def GET(server_name, server_port,getarg,file_name):#[GET要求]
    s = socket(AF_INET, SOCK_STREAM)       # ソケットを作る 
    s.connect((server_name, server_port))
    get ="GET "+file_name+" "+getarg+" ALL\n" # キーボードから入力された文字列を受け取る
    s.send(get.encode())            # 文字列をバイト配列に変換後、送信する。    
    recv_bytearray_get = bytearray()
    while 1:
        b = s.recv(1)[0]
        recv_bytearray_get.append(b)
        B=b.to_bytes(1,'big')
        if B == b'\n':
            break
    recv_str2= recv_bytearray_get.decode()
    print(recv_str2)
    data=0
    with open(file_name, 'wb') as f:    # 'wb' は「バイナリファイルを書き込みモードで」という意味
        i=0
        while True:
            i+=1
            data = s.recv(102400)   # BUFSIZEバイトずつ受信
            print(i)
            print(len(data))
            if len(data) <= 0:  # 受信したデータがゼロなら、相手からの送信は全て終了
                break
            f.write(data)  # 受け取ったデータをファイルに書き込む
              # 最後にソケットをクローズ
    print("OK")
    s.close()

def GETP(server_name, server_port,getarg,file_name,staB,finB,g):#[GET要求]
    s = socket(AF_INET, SOCK_STREAM)       # ソケットを作る 
    s.connect((server_name, server_port))
    get ="GET "+file_name+" "+getarg+" PARTIAL "+str(staB)+" "+ str(finB)+" \n" # キーボードから入力された文字列を受け取る
    s.send(get.encode())            # 文字列をバイト配列に変換後、送信する。    
    recv_bytearray_get = bytearray()
    while 1:
        b = s.recv(1)[0]
        recv_bytearray_get.append(b)
        B=b.to_bytes(1,'big')
        if B == b'\n':
            break
    recv_str2= recv_bytearray_get.decode()
    print(recv_str2)
    if g==0:
        d='wb'
    else:
        d='ab'
    
    with open(file_name, d) as f:    # 'wb' は「バイナリファイルを書き込みモードで」という意味
        while True:
            data = s.recv(102400)   # BUFSIZEバイトずつ受信
            if len(data) <= 0:  # 受信したデータがゼロなら、相手からの送信は全て終了
                break
            f.write(data)  # 受け取ったデータをファイルに書き込む
              # 最後にソケットをクローズ
    
    s.close()
    
def REP(server_name, server_port,token_str,file_name):#[REP要求]
    s = socket(AF_INET, SOCK_STREAM)       # ソケットを作る 
    s.connect((server_name, server_port))
    rep="REP "+file_name+" "+pbl2019.repkey(token_str,file_name)+"\n"
    print("OK")
    s.send(rep.encode())
    recv_bytearray_rep= bytearray()
    while 1:
        c = s.recv(1)[0]
        recv_bytearray_rep.append(c)
        C=c.to_bytes(1,'big')
        if C == b'\n':
            break
    recv_str3= recv_bytearray_rep.decode()
    print(recv_str3)
    s.close()

if __name__ == '__main__':  
    server_name = sys.argv[1]       # サーバのホスト名あるいはIPアドレスを表す文字
    server_port = int(sys.argv[2])  # サーバのポート
    file_name=sys.argv[3]
    #token_str=sys.argv[4]
    token_str="hogehoge"
    getarg=pbl2019.genkey(token_str)     
    start=time.time()        
    
    SIZE(server_name, server_port,file_name)
<<<<<<< HEAD
  
    GET(server_name, server_port,getarg,file_name)
    #GETP(server_name, server_port,getarg,file_name,0,3)
    #GETP(server_name, server_port,getarg,file_name,4,10)
    #GETP(server_name, server_port,getarg,file_name,11,52427)
=======
    
    GET(server_name, server_port,getarg,file_name)

>>>>>>> 39671ce98782fef69fa60e435cbb896d5b8d27ae
    REP(server_name, server_port,token_str,file_name)
    
    finish=time.time()
      
    #[経過時間表示]
    print("Tile transfer finished: Transmission time:"+str(finish - start)+" sec\n")
        

