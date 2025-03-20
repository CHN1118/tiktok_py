from flask import Blueprint, jsonify, request  # type: ignore
from loguru import logger

from tiktok.controls import TikTokAutomation


def tiktok(app, d):
    # 创建蓝图对象 tiktok_blueprint，用来管理与 tiktok 相关的路由
    tiktok_blueprint = Blueprint("tiktok", __name__, url_prefix="/tiktok")

    tiktok_bot = TikTokAutomation(d)

    # 在蓝图中定义子路由
    @tiktok_blueprint.route("/swipe_up")
    def swipe_up():
        s, m = tiktok_bot.swipe_up()
        return app_return(s, m)

    @tiktok_blueprint.route("/swipe_down")
    def swipe_down():
        s, m = tiktok_bot.swipe_down()
        return app_return(s, m)

    @tiktok_blueprint.route("/swipe_left")
    def swipe_left():
        s, m = tiktok_bot.swipe_left()
        return app_return(s, m)

    @tiktok_blueprint.route("/swipe_right")
    def swipe_right():
        s, m = tiktok_bot.swipe_right()
        return app_return(s, m)

    @tiktok_blueprint.route("/auto_watch")
    def auto_watch():
        s, m = tiktok_bot.auto_watch()
        return app_return(s, m)

    @tiktok_blueprint.route("/stop_watching")
    def stop_watching():
        s, m = tiktok_bot.stop_watching()
        return app_return(s, m)

    @tiktok_blueprint.route("/blogger_home")
    def blogger_home():
        s, m = tiktok_bot.blogger_home()
        return app_return(s, m)

    @tiktok_blueprint.route("/follow_user")
    def follow_user():
        s, m = tiktok_bot.follow_user()
        return app_return(s, m)

    @tiktok_blueprint.route("/like_video")
    def like_video():
        s, m = tiktok_bot.like_video()
        return app_return(s, m)

    @tiktok_blueprint.route("/favorite_video")
    def favorite_video():
        s, m = tiktok_bot.favorite_video()
        return app_return(s, m)

    @tiktok_blueprint.route("/share_video")
    def share_video():
        s, m = tiktok_bot.share_video()
        return app_return(s, m)

    @tiktok_blueprint.route("/blogger_fallow")
    def blogger_fallow():
        s, m = tiktok_bot.blogger_fallow()
        return app_return(s, m)

    @tiktok_blueprint.route("/blogger_first_video")
    def blogger_first_video():
        s, m = tiktok_bot.blogger_first_video()
        return app_return(s, m)

    @tiktok_blueprint.route("/search_video")
    def search_video():
        s, m = tiktok_bot.search_video()
        return app_return(s, m)

    # 注册蓝图，使其成为父路由下的子路由
    app.register_blueprint(tiktok_blueprint)

    return tiktok_bot


def app_return(s, m):
    if s:
        return jsonify({"message": m, "status": "success"})
    else:
        return jsonify({"message": m, "status": "failure"})
