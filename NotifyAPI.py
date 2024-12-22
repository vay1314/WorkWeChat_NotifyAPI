#!/usr/bin/python
# -*- encoding:utf-8 -*-

import datetime
import requests
import json
import os
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
VERSION = '20241222'
BUILDTIME = '2024-12-22 12:00'

@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    response = {
        'status': 'failed',
        'error': '',
        'version': VERSION,
        'buildtime': BUILDTIME
    }
    secret_key = os.environ.get('QYWX_SECRET_KEY', '')
    corpid = os.environ.get('QYWX_CORPID', '')
    agentid = os.environ.get('QYWX_AGENTID', '')
    secret = os.environ.get('QYWX_SECRET', '')

    try:
        if request.method == 'GET':
            num = int(request.args.get('num', '0'))
            msgtype = request.args.get('msgtype', '')
            key = request.args.get('key', '')
            touser = request.args.get('touser', '')
            title = request.args.get('title', '最新消息')
            content = request.args.get('content', '')
            redirect_url = request.args.get('redirect_url', '')
            picurl = request.args.get('picurl', '')
            media_id = request.args.get('media_id', '')
        elif request.method == 'POST':
            post_data = json.loads(request.data or '{}')
            num = int(post_data.get('num', 0))
            msgtype = post_data.get('msgtype', '')
            key = post_data.get('key', '')
            touser = post_data.get('touser', '')
            title = post_data.get('title', '最新消息')
            content = post_data.get('content', '')
            redirect_url = post_data.get('redirect_url', '')
            picurl = post_data.get('picurl', '')
            media_id = post_data.get('media_id', '')
        else:
            response['error'] = 'Invalid method'
            return jsonify(response)

        # 校验必填字段
        errors = {}
        if not key: errors['key'] = 'null'
        if not msgtype: errors['msgtype'] = 'null'
        if not corpid: errors['corpid'] = 'null'
        if not agentid: errors['agentid'] = 'null'
        if not secret: errors['secret'] = 'null'
        if not touser: errors['touser'] = 'null'
        if not content: errors['content'] = 'null'
        if msgtype == '3' and not media_id: errors['media_id'] = 'null'
        if errors:
            response['error'] = errors
            return jsonify(response)

        # 调用企业微信 API
        agentid = agentid.split(',')[num - 1]
        secret = secret.split(',')[num - 1]
        return qywx(secret_key, key, msgtype, corpid, agentid, secret, touser, title, content, redirect_url, picurl, media_id)
    except ValueError as ve:
        response['error'] = f'Invalid input: {ve}'
    except Exception as e:
        response['error'] = str(e)
    return jsonify(response)

def qywx(secret_key, key, msgtype, corpid, agentid, secret, touser, title, content, redirect_url, picurl, media_id):
    response = {
        'status': 'failed',
        'error': '',
        'version': VERSION,
        'buildtime': BUILDTIME
    }
    try:
        if key != secret_key:
            response['error'] = 'Invalid key'
            return jsonify(response)

        # 获取 access_token
        token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        token_data = {'corpid': corpid, 'corpsecret': secret}
        token_resp = requests.post(token_url, params=token_data).json()
        access_token = token_resp.get("access_token")
        if not access_token:
            response['error'] = 'Failed to get access_token'
            return jsonify(response)

        # 构建消息
        send_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        send_data = build_message(msgtype, agentid, touser, title, content, redirect_url, picurl, media_id)
        send_resp = requests.post(send_url, json=send_data).json()

        if send_resp.get('errcode') == 0:
            response['status'] = 'success'
        else:
            response['error'] = send_resp
    except Exception as e:
        response['error'] = str(e)
    return jsonify(response)

def build_message(msgtype, agentid, touser, title, content, redirect_url, picurl, media_id):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if msgtype == '1':  # Text message
        return {
            'msgtype': 'text',
            'agentid': agentid,
            'touser': touser,
            'text': {'content': f"{title}\n{content}\n发送时间: {timestamp}"}
        }
    elif msgtype == '2':  # News
        return {
            'msgtype': 'news',
            'agentid': agentid,
            'touser': touser,
            'news': {'articles': [{'title': title, 'description': content, 'url': redirect_url, 'picurl': picurl}]}
        }
    elif msgtype == '3':  # MPNews
        return {
            'msgtype': 'mpnews',
            'agentid': agentid,
            'touser': touser,
            'mpnews': {'articles': [{'title': title, 'content': content, 'thumb_media_id': media_id}]}
        }
    else:
        raise ValueError("Unsupported msgtype")

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    return jsonify({'status': 'failed', 'error': 'Invalid access', 'version': VERSION, 'buildtime': BUILDTIME})

if __name__ == '__main__':
    app.run('0.0.0.0', 5005, debug=True)
