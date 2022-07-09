import requests
import lzma
import io
import os
from json import dumps as jdumps
from decrypt_e import decrypt_e
from xrxd_struct import dumpXrxd

def getXrxdPlainData():
    # 第一步：登录，获取 access_token
    # loginUrl = 'http://datasrv.x07.top:8043/rpc/Login/LoginInterf/loginByUsername'
    loginUrl = 'http://datasrv.x07.top:8070/rpc/Login/LoginInterf/loginByUsername'

    headers = {'client-id': '1'}
    resp = requests.post(loginUrl, json={'username': 'test', 'password': 'testtest'}, headers=headers)
    # {'code': 0, 'timestamp': 1657378292030, 'message': 'Success',
    # 'data': {
    #    'oauth': {'access_token': 'xx', 'token_type': 'token', 'expires_in': 6841378292},
    #    'user': {'userid': 1, 'username': 'xx', 'email': 'xxx',
    #        'is_active': True, 'date_joined': 1456694700000, 'nickname': '', 'is_staff': True, 'vip_time': 1574352000000}},
    # 'status_code': 200}
    jobj = resp.json()
    if resp.status_code != 200:
        resp.raise_for_status()
    access_token = jobj['data']['oauth']['access_token']
    headers['access-token'] = access_token

    # 第二步：获取 xrxd 文件（加密过的）
    xrxdUrl = 'http://stk-meta.x07.top/info-metas/SplitInfo.bin.e.xz'
    resp = requests.get(xrxdUrl)
    if resp.status_code != 200:
        resp.raise_for_status()
    with open('SplitInfo.bin.e.xz', 'wb') as fp:
        fp.write(resp.content)
    xrxdBytes = io.BytesIO(resp.content)
    data = lzma.open(xrxdBytes).read()
    print(len(data))
    with open('SplitInfo.bin.e', 'wb') as fp:
        fp.write(data)

    # 第三步：通过 xrxd 文件信息获取解密秘钥
    chipherUrl = 'http://datasrv.x07.top:8043/rpc/KlineP2/KlineP2I/getFileCipher'
    resp = requests.post(chipherUrl, json={'cipherIn': {'fileName': 'SplitInfo.bin.e', 'fileSize': len(data)}}, headers=headers)

    if resp.status_code != 200:
        resp.raise_for_status()

    cipherOut = resp.json()['data']['cipherOut']

    # 第四步：解密
    plainData = decrypt_e(data, cipherOut['fileCipher'], access_token)
    with open('SplitInfo.bin', 'wb') as fp:
        fp.write(plainData)

if not os.path.exists('SplitInfo.bin'):
    getXrxdPlainData()

with open('SplitInfo.bin', 'rb') as fp:
    dumpXrxd(fp.read())
