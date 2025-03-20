from loguru import logger
from flask import Flask, jsonify, render_template, request, send_from_directory
import uiautomator2 as u2

from tiktok.main import tiktok
from util.select_router import list_routes

app = Flask(__name__)

devices_id = "QKYPIZA6R8IJ7TLV"
# 连接到安卓设备
d = u2.connect(devices_id)  # 默认连接到第一个设备，如果有多个设备可以指定设备ID

tiktok_bot = tiktok(app, d)


@app.route("/")
def index():
    return render_template("index.html")


# 你可以在这里添加一个路由来触发手机的操作
@app.route("/tiktok")
def tiktok_main():
    """获取所有方法"""
    return list_routes(app)


@app.route("/back_swipe")
def back_swipe():
    """模拟系统退出"""
    tiktok_bot.back_swipe()
    return jsonify({"message": "模拟系统退出", "status": "success"})


@app.route("/restart")
def restart_tiktok():
    """单独提供一个接口来重启 TikTok"""
    tiktok_bot.restart_app()
    return jsonify({"message": "TikTok 已重启", "status": "success"})


@app.route("/judgment_page")
def judgment_page():
    """判断当前页面 TikTok"""
    s, m = tiktok_bot.judgment_page()
    return jsonify({"message": m, "status": "success"})


@app.route("/search_input", methods=["POST"])
def search_input():
    """在搜索页面时,搜索关键字"""
    data = request.json  # 获取 POST 请求的 JSON 数据
    keyword = data.get("keyword") if data else None
    if not keyword:
        logger.warning("缺少 keyword 参数")
        return jsonify({"message": "缺少 keyword 参数", "status": "failure"})

    s, m = tiktok_bot.search_input(keyword)  # 传入 keyword
    return jsonify({"message": m, "status": "success"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
