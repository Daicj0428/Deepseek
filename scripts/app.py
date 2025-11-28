from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from . deepseek_api import deepseek1
from datetime import datetime
import sys
import time
import uuid
from flask import request
import os
import time
from datetime import datetime, timezone, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] =  os.getenv('FLASK_SECRET', 'dev-secret-key')

socketio = SocketIO(app, 
                   cors_allowed_origins="*",
                   async_mode='threading',
                   logger=False,
                   engineio_logger=False,
                   log_output=True)

# 设置时区
TZ = os.getenv('TZ', 'Asia/Shanghai')
try:
    # 尝试设置系统时区
    os.environ['TZ'] = TZ
    time.tzset()
except:
    # Windows系统不支持time.tzset()，使用datetime的时区功能
    pass

# 创建时区对象
try:
    tz = timezone(timedelta(hours=8))  # 默认北京时间
    if TZ == 'Asia/Shanghai':
        tz = timezone(timedelta(hours=8))
    elif TZ == 'UTC':
        tz = timezone.utc
    # 可以添加更多时区支持...
except:
    tz = None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    # 获取客户端会话ID，如果没有则生成一个
    session_id = data.get('session_id', str(uuid.uuid4()))
    client_ip = request.remote_addr
    
    # 获取当前时间并格式化 - 使用设置的时区
    if tz:
        current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    else:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 获取当前时间并格式化
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 打印带会话信息的用户消息
    user_message = data.get('content', '')
    if user_message:
        print(f"\n[{current_time}] [会话ID: {session_id}] [客户端IP: {client_ip}] [用户消息] {user_message}\n")
    
    api_messages = data.get('context', [])
    
    # 发送开始标记（包含会话ID）
    emit('message', {'type': 'start', 'content': '', 'session_id': session_id})
    
    full_response = ""
    try:
        for chunk in deepseek1(api_messages):
            if chunk:
                full_response += chunk
                # 实时发送到前端（包含会话ID）
                emit('message', {
                    'type': 'stream',
                    'content': chunk.replace('\n', '\n'),
                    'session_id': session_id
                })
                
    except Exception as e:
        print(f"\n[{current_time}] [会话ID: {session_id}] [错误] {str(e)}\n")
        emit('message', {
            'type': 'error',
            'content': f"处理出错: {str(e)}",
            'session_id': session_id
        })
    
    # 发送结束标记（包含会话ID）
    emit('message', {'type': 'end', 'content': '', 'session_id': session_id})
    
    # 打印带会话信息的完整AI响应
    if full_response:
        print(f"\n[{current_time}] [会话ID: {session_id}] [AI完整响应]")
        print("-"*50)
        print(full_response)
        print("-"*50 + "\n")
    
    # 保存完整响应（包含会话ID）
    emit('message', {
        'type': 'full',
        'content': full_response,
        'session_id': session_id
    })

if __name__ == '__main__':
    print("服务器正在启动...")
    socketio.run(app, 
                host='0.0.0.0', 
                port=int(os.getenv('PORT', 21048)), 
                debug=bool(int(os.getenv('FLASK_DEBUG', 0))),
                use_reloader=False)
