# -*- coding: utf-8 -*-
# filetrans_server.py
#
# 決められたファイルの指定されたサイズまでを転送するシステムのサーバ
#

import sys
from socket import *

BUFSIZE = 4096  # 一度に受信処理するデータサイズ

file_name = 'bigfile.dat'  # 読み書きするファイルサイズ
server_port = 50001

# クライアントとやりとりする処理
def interact_with_client(s):
    # 最大BUFSIZEバイトを受信する
    req_msg = s.recv(BUFSIZE).decode()

    # 最初の空白文字までに書かれているのがサイズなのでそれを解釈する
    send_size = int(req_msg.split()[0])  

    # ファイル全体を読み込んで、送信する
    #   with 構文を使って書いています。
    #   ファイル絡みの例外処理とクローズの処理は書く必要がありません
    with open(file_name, 'rb') as f:  # 'rb'は「バイナリファイルを読み込みモードで」の意味
        data = f.read(send_size)
        s.send(data)
    s.close()

# メインルーチン
if __name__ == '__main__':
    # 待ち受け用ソケットを作ってポートに関連付け、待ち受けを開始
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(1)
    print('The server is ready to receive')

    while True:
        # 接続されたら、そのクライアントとのソケットを作って、クライアントと通信する
        s, addr = server_socket.accept()
        interact_with_client(s)  # クライアントとの処理は別関数にて
