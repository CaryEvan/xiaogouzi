from socket import *
import urllib3
import json
import struct
import time
import threading

http = urllib3.PoolManager()

#创建房间
#url = 'http://47.94.173.4/momo/v2/room/create-chat-room'
#info = {}
#info['open_id'] = 'UEx6NFowOUJnVE5uY09jYy9hb3ZyQT09'
#info['game_id'] = '8-1-10000-1-8000'
#info['room_name'] = '111'
#info['config_info'] = '{"room_config":{"room_time":15}}'
#info['version'] = '100.112'
#r = http.request('POST', url, body = json.dumps(info), headers = {'Content-Type':'application/json'})
#print r.status
#print r.data

#获取gtoken
url = 'http://47.94.173.4/byx/any-index'
info = {}
info['v'] = 'json'
msg = {}
msg['show_id'] = '2034'
msg['open_id'] = 'UEx6NFowOUJnVE5uY09jYy9hb3ZyQT09'
msg['mid'] = 'LoadGameModel'
msg['sign'] = 'caae857f57bbf5b87616990d9c027bbd'
info['m'] = json.dumps(msg)
r = http.request('POST', url, body = json.dumps(info), headers = {'Content-Type':'application/json'})
print r.status
print r.data
table = json.loads(r.data)
table_1 = json.loads(table['data'])

#获取陌陌信息
url = 'http://47.94.173.4/byx/any-index'
info = {}
info['v'] = 'json'
msg = {}
msg['open_id'] = 'UEx6NFowOUJnVE5uY09jYy9hb3ZyQT09'
msg['mid'] = 'MomoUserInfo'
msg['sign'] = 'caae857f57bbf5b87616990d9c027bbd'
info['m'] = json.dumps(msg)
info['n'] = str(table_1['g_token'])
r = http.request('POST', url, body = json.dumps(info), headers = {'Content-Type':'application/json'})
print r.status
print r.data
playerId = json.loads(json.loads(r.data)['data'])['uid']

#加入房间
url = 'http://47.94.173.4/byx/any-index'
info = {}
info['v'] = 'json'
msg = {}
msg['show_id'] = '2034'
msg['open_id'] = 'UEx6NFowOUJnVE5uY09jYy9hb3ZyQT09'
msg['mid'] = 'JoinRoom'
msg['sign'] = 'caae857f57bbf5b87616990d9c027bbd'
info['m'] = json.dumps(msg)
info['n'] = str(table_1['g_token'])
r = http.request('POST', url, body = json.dumps(info), headers = {'Content-Type':'application/json'})
print r.status
print r.data
table_2 = json.loads(r.data)
table_3 = json.loads(table_2['data'])

HOST = table_3['ip']

PORT = int(table_3['port'])

BUFFSIZE = 2048

ADDR = (HOST,PORT)

client = socket(AF_INET,SOCK_STREAM)
#client.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)

#client.setsockopt(SOL_TCP, TCP_NODELAY, 1)

client.connect(ADDR)

hertBeatData = struct.pack('=iBBi', 6, 1, 1, int(time.time()))
authData = struct.pack('=iBBi33s', 39, 1, 2, int(playerId), str(table_1['g_token']))
ret = client.send(hertBeatData)
recvData = client.recv(256)
#time.sleep(1)
ret = client.send(authData)
recvData = client.recv(2048)

#msg = [0x1f, 0x00, 0x00, 0x00,\
#       0x01, 0x02,\
#       0x01, 0x00, 0x00, 0x00,\
#       0x70, 0x6f, 0x74, 0x61, 0x74, 0x6f, 0x2c, 0x20, 0x69,\
#       0x20, 0x61, 0x6d, 0x20, 0x70, 0x61, 0x63, 0x68, 0x79, 0x72, 0x68, 0x69, 0x7a, 0x75, 0x73, 0x00]
#sendData = struct.pack("%dB"%(len(msg)),*msg)

#msg = [0x06, 0x00, 0x00, 0x00,\
#       0x01, 0x01,\
#       0x01, 0x00, 0x00, 0x00,]
#sendData = struct.pack("%dB"%(len(msg)),*msg)






def handleHertBeat():
    while True:
        hertBeatData = struct.pack('=iBBi', 6, 1, 1, int(time.time()))
        client.send(hertBeatData)
        recvData = client.recv(256)
        time.sleep(3)


if __name__ == '__main__':
    hertBeatThread = threading.Thread(target = handleHertBeat)
    hertBeatThread.setDaemon(True)
    hertBeatThread.start()
    while True:
        name = input("Please intput your action:")
        if name == 1:
            msg = {}
            msg['fun'] = 'presenterapplyseatC'
            msg['type'] = 1
            data = json.dumps(msg, separators=(',',':'))
            length = len(data)
            sendData = struct.pack('=iBBi%ds' % (length+1), length + 4 + 2 + 1, 1, 3, length + 1, data)  #这里尤其需要注意，构造消息后多留一个空字节结尾，这样才能让服务端确认收了一条完整消息并立即进行处理
            client.send(sendData)
        
        if name == 2:
            msg = {}
            msg['fun'] = 'presenterleaveseatC'
            data = json.dumps(msg, separators=(',',':'))
            length = len(data)
            sendData = struct.pack('=iBBi%ds' % (length+1), length + 4 + 2 + 1, 1, 3, length + 1, data)
            client.send(sendData)
