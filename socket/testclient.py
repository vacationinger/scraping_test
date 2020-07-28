# -*- coding: utf-8 -*-
# filetrans_client.py
#
# 決められたファイルの指定されたサイズまでを転送するシステムのクライアント

import sys
from socket import *

BUFSIZE = 4096
file_name = 'received_data.dat'
server_name = 'localhost'
server_port = 50001

def interact_with_server(s, size):
    # 要求メッセージを作る  例: '4096' ... 4096バイト要求
    req_msg = '{0:d}\n'.format(size)

    # 要求メッセージの文字列をバイト列にして送信
    s.send(req_msg.encode())

    # 書き込み用ファイルをオープンして処理
    #   with 構文を使って書いています。
    #   ファイル絡みの例外処理とクローズの処理は書く必要がありません
    with open(file_name, 'wb') as f:    # 'wb' は「バイナリファイルを書き込みモードで」という意味
        while True:
            data = s.recv(BUFSIZE)   # BUFSIZEバイトずつ受信
            if len(data) <= 0:  # 受信したデータがゼロなら、相手からの送信は全て終了
                break
            f.write(data)  # 受け取ったデータをファイルに書き込む
    s.close()  # 最後にソケットをクローズ

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Usage: {0} size_in_bytes'.format(sys.argv[0]))
    size = int(sys.argv[1])

    # ソケットを作ってサーバに接続
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((server_name, server_port))

    interact_with_server(s, size)  # サーバとのデータのやりとりは別関数に

    s.close()

