"""
调试版本的app.py - 检查错误
"""
print("开始导入...")

try:
    from flask import Flask, render_template, request, jsonify
    print("Flask导入成功")
except Exception as e:
    print(f"Flask导入失败: {e}")
    exit(1)

try:
    import math
    import json
    print("基本模块导入成功")
except Exception as e:
    print(f"基本模块导入失败: {e}")
    exit(1)

print("创建Flask应用...")
app = Flask(__name__)

@app.route('/')
def index():
    return "测试页面"

if __name__ == '__main__':
    print("启动应用...")
    app.run(debug=True, host='127.0.0.1', port=5000)