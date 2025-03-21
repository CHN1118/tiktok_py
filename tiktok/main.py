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
        """上滑"""
        s, m = tiktok_bot.swipe_up()
        return app_return(s, m)

    @tiktok_blueprint.route("/swipe_down")
    def swipe_down():
        """下滑"""
        s, m = tiktok_bot.swipe_down()
        return app_return(s, m)

    @tiktok_blueprint.route("/swipe_left")
    def swipe_left():
        """左滑"""
        s, m = tiktok_bot.swipe_left()
        return app_return(s, m)

    @tiktok_blueprint.route("/swipe_right")
    def swipe_right():
        """右滑"""
        s, m = tiktok_bot.swipe_right()
        return app_return(s, m)

    @tiktok_blueprint.route("/auto_watch")
    def auto_watch():
        """自动播放"""
        s, m = tiktok_bot.auto_watch()
        return app_return(s, m)

    @tiktok_blueprint.route("/stop_watching")
    def stop_watching():
        """停止自动播放"""
        s, m = tiktok_bot.stop_watching()
        return app_return(s, m)

    @tiktok_blueprint.route("/blogger_home")
    def blogger_home():
        """博主首页"""
        s, m = tiktok_bot.blogger_home()
        return app_return(s, m)

    @tiktok_blueprint.route("/follow_user")
    def follow_user():
        """关注博主"""
        s, m = tiktok_bot.follow_user()
        return app_return(s, m)

    @tiktok_blueprint.route("/like_video")
    def like_video():
        """点赞按钮"""
        s, m = tiktok_bot.like_video()
        return app_return(s, m)

    @tiktok_blueprint.route("/favorite_video")
    def favorite_video():
        """收藏按钮"""
        s, m = tiktok_bot.favorite_video()
        return app_return(s, m)

    @tiktok_blueprint.route("/share_video")
    def share_video():
        """分享按钮"""
        s, m = tiktok_bot.share_video()
        return app_return(s, m)

    @tiktok_blueprint.route("/blogger_fallow")
    def blogger_fallow():
        """博主详情页关注"""
        s, m = tiktok_bot.blogger_fallow()
        return app_return(s, m)

    @tiktok_blueprint.route("/blogger_first_video")
    def blogger_first_video():
        """打开博主第一个视频"""
        s, m = tiktok_bot.blogger_first_video()
        return app_return(s, m)

    @tiktok_blueprint.route("/search_video")
    def search_video():
        """搜索视频"""
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
