from loguru import logger
from flask import Flask, jsonify, render_template, request, send_from_directory
import uiautomator2 as u2

from tiktok.main import tiktok
from util.select_router import list_routes

app = Flask(__name__)

devices_id = "QKYPIZA6R8IJ7TLV"
# 连接到安卓设备
d = u2.connect(devices_id)  # 默认连接到第一个设备，如果有多个设备可以指定设备ID

# 设置每次单击UI后再次单击之间延迟1.5秒
d.click_post_delay = 1.5  # 默认无延迟

# 设置默认元素等待超时（秒）
d.wait_timeout = 10.0  # 默认20.0秒

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
    # e = d.xpath("//android.widget.TextView[@text='关注']").all()
    # print(f"{e[1].info}")
    # tiktok_bot.click_element("like_video", "android.widget.ImageView", description="赞")
    d.press("BACK")  # 按下back键的常规方式
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


@app.route("/wake_up", methods=["POST"])
def wake_up():
    keyword = request.form.get("keyword")
    s, m = tiktok_bot.wake_up(keyword)
    return jsonify({"message": m, "status": "success"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)


# pip freeze > requirements.txt 生成依赖包
# pip install -r requirements.txt 安装依赖包
