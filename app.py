import datetime
from flask import Flask, request, jsonify, render_template_string

# 1. 初始化 Flask 应用
app = Flask(__name__)

# 2. 全局变量，用来在内存中保存最新的 DNA 模拟数据
latest_simulation_data = {
    "step": 0,
    "progress": 0.0,
    "status": "尚未收到模拟数据，等待本地程序启动...",
    "timestamp": None
}


# 3. 主页路由 (GET 请求)：供你在浏览器（包括手机、电脑）中查看进度
@app.route('/', methods=['GET'])
def index():
    # 工业风、高颜值的全响应式监控大屏模板
    html_template = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DNA 模拟远程监控面板</title>
        <style>
            body {
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                background-color: #f0f2f5;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .card {
                background: #ffffff;
                border-radius: 16px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
                padding: 30px;
                width: 100%;
                max-width: 450px;
                box-sizing: border-box;
            }
            .header {
                border-bottom: 2px solid #0056b3;
                padding-bottom: 15px;
                margin-bottom: 25px;
                text-align: center;
            }
            .header h2 {
                margin: 0;
                color: #1a1a1a;
                font-size: 24px;
            }
            .header p {
                margin: 5px 0 0 0;
                color: #666;
                font-size: 14px;
            }
            .data-item {
                margin-bottom: 20px;
            }
            .data-label {
                font-size: 14px;
                color: #8c8c8c;
                margin-bottom: 5px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .data-value {
                font-size: 20px;
                color: #262626;
                font-weight: 600;
            }
            .progress-container {
                background-color: #e8e8e8;
                border-radius: 8px;
                position: relative;
                height: 20px;
                width: 100%;
                margin-top: 10px;
                overflow: hidden;
            }
            .progress-bar {
                background-image: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
                height: 100%;
                width: {{ data.progress }}%;
                transition: width 0.5s ease-in-out;
            }
            .status-box {
                background-color: #e6f7ff;
                border: 1px solid #91d5ff;
                border-radius: 8px;
                padding: 12px;
                color: #0050b3;
                font-size: 14px;
                line-height: 1.5;
            }
            .footer {
                text-align: center;
                font-size: 11px;
                color: #bfbfbf;
                margin-top: 30px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <h2>🧬 DNA 电泳模拟监控</h2>
                <p>布朗动力学远程实验室</p>
            </div>

            <div class="data-item">
                <div class="data-label">当前计算帧数 (Frame)</div>
                <div class="data-value" style="color: #007bff; font-size: 28px;">{{ data.step }}</div>
            </div>

            <div class="data-item">
                <div class="data-label">生产步总进度</div>
                <div class="data-value">{{ data.progress }}%</div>
                <div class="progress-container">
                    <div class="progress-bar"></div>
                </div>
            </div>

            <div class="data-item">
                <div class="data-label">物理系统状态</div>
                <div class="status-box">{{ data.status }}</div>
            </div>

            <div class="footer">
                页面每 2 秒自动刷新 · 云端最新同步时间: {{ data.timestamp if data.timestamp else '无数据' }}
            </div>
        </div>

        <script>
            // 让浏览器每隔 2 秒自动刷新页面以获取最新数据
            setTimeout(function(){ location.reload(); }, 2000);
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template, data=latest_simulation_data)


# 4. 接收数据路由 (POST 请求)：供你本地的 Python 模拟程序调用上传数据
@app.route('/api/upload_data', methods=['POST'])
def upload_data():
    global latest_simulation_data

    # 安全校验：确保上传的是标准 JSON
    if not request.is_json:
        return jsonify({"status": "error", "message": "Content-Type 必须为 application/json"}), 400

    # 提取本地发来的字典数据
    received_json = request.get_json()

    # 更新到云端的全局内存中
    latest_simulation_data["step"] = received_json.get("step", 0)
    latest_simulation_data["progress"] = received_json.get("progress", 0.0)
    latest_simulation_data["status"] = received_json.get("status", "运行中")
    latest_simulation_data["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 打印到 Render 控制台日志中，方便排查
    print(f"[数据同步成功] Frame: {latest_simulation_data['step']} | 进度: {latest_simulation_data['progress']}%")

    return jsonify({"status": "success", "message": "数据已接收"}), 200


# 5. 启动代码（满足 Render 的 host 与端口自动分配要求）
if __name__ == '__main__':
    # 采用 0.0.0.0 允许外部网络（Render/局域网）访问端口 5000
    app.run(host='0.0.0.0', port=5000, debug=True)