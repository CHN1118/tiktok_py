from loguru import logger
import uiautomator2 as u2
from airtest.core.api import *
import time
import json
import os


class TikTokAutomation:
    def __init__(self, device: u2.Device):
        """
        初始化自动化对象，接收 uiautomator2 设备实例
        :param device: 连接的安卓设备对象
        """
        self.d = device  # 存储设备对象
        self.package_name = "com.zhiliaoapp.musically"  # TikTok 包名
        self.stop_flag = False  # 用于控制自动观看的标志
        self.status_bar_h = device(
            resourceId="com.android.systemui:id/status_bar"
        ).info["bounds"]["bottom"]
        self.cache_file = ".cache/resource_id_cache.json"
        self.resource_id_cache = self._load_cache()

    def _load_cache(self):
        """加载本地缓存文件"""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        """保存缓存到本地"""
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self.resource_id_cache, f, indent=4)

    def _update_cache(self, key, resource_id):
        """更新缓存"""
        self.resource_id_cache[key] = resource_id
        self._save_cache()

    def find_element(
        self, key, class_name: str = None, xpath: str = None, all: int = None, **kwargs
    ):
        """
        查找 UI 元素，优先使用缓存的 resourceId，失败后回退到 className + 其他参数匹配
        :param all:
        :param xpath:
        :param key: 元素的唯一标识符（比如 'like_button'）
        :param class_name: 元素 class
        :param kwargs: 其他查询条件，比如 text、description、descriptionMatches 等
        """
        # 如果元素已经存在于缓存中，直接使用缓存的 resourceId
        if key in self.resource_id_cache:
            # 1. 尝试用 resourceId 查询
            resource_id = self.resource_id_cache[key]
            element = self.d(resourceId=resource_id)
            if element.exists:
                logger.success(f"找到 {key} 元素，使用缓存")
                return element

        # 1. 确保至少有一个有效的查询条件并且 xpath 为空
        if not kwargs and xpath is None:
            logger.warning("未提供查询条件")
            return None

        element = None

        if xpath:
            if all:
                element = self.d.xpath(xpath).all()[all]
            else:
                element = self.d.xpath(xpath)
        else:
            kwargs["className"] = class_name
            element = self.d(**kwargs)
        # 3. 如果成功查询，记录新的 resourceId
        if element and element:
            new_resource_id = element.info.get("resourceName")
            if new_resource_id:
                logger.success(f"更新 {key} 元素的 resourceId 为 {new_resource_id}")
                self._update_cache(key, new_resource_id)

        return element

    def click_element(
        self,
        key: str,
        class_name: str = None,
        xpath: str = None,
        all: int = None,
        **kwargs,
    ):
        """点击元素"""
        try:
            element = self.find_element(key, class_name, xpath, all, **kwargs)
            print(element.info)
            if element.click_exists(timeout=0.1):
                logger.success(
                    f"成功点击 {kwargs.get('description') or kwargs.get('descriptionMatches') or kwargs.get('text')} 按钮"
                )
                return (
                    True,
                    f"点击 {kwargs.get('description') or kwargs.get('descriptionMatches') or kwargs.get('text')} 按钮成功",
                )
            else:
                logger.warning(
                    f"未找到 {kwargs.get('description') or kwargs.get('descriptionMatches') or kwargs.get('text')} 按钮"
                )
                return (
                    False,
                    f"未找到 {kwargs.get('description') or kwargs.get('descriptionMatches') or kwargs.get('text')} 按钮",
                )
        except Exception as e:
            logger.warning(f"按钮点击失败: {e}")
            return False, f"按钮点击失败: {e}"

    # * 抽离公共方法
    def _click_button(
        self,
        class_name: str,
        description: str = None,
        descriptionMatches: str = None,
        text: str = None,
        index: int = None,
    ):
        """
        优化通用按钮点击方法，加快点击速度
        """
        try:
            button = None
            if description:
                button = self.d(
                    className=class_name, index=index, description=description
                )
            elif descriptionMatches:
                button = self.d(
                    className=class_name,
                    index=index,
                    descriptionMatches=descriptionMatches,
                )
            elif text:
                button = self.d(className=class_name, index=index, text=text)
            else:
                raise ValueError("必须提供 description、descriptionMatches 或 text")

            # 直接使用 click_exists，减少等待
            if button.click_exists(timeout=0.1):
                logger.success(
                    f"成功点击 {description or descriptionMatches or text} 按钮"
                )
                return (
                    True,
                    f"点击 {description or descriptionMatches or text} 按钮成功",
                )
            else:
                logger.warning(
                    f"未找到 {description or descriptionMatches or text} 按钮"
                )
                return False, f"未找到 {description or descriptionMatches or text} 按钮"

        except Exception as e:
            logger.warning(f"按钮点击失败: {e}")
            return False, f"按钮点击失败: {e}"

    # 重启
    def restart_app(self):
        """关闭 TikTok 并重新打开"""
        try:
            logger.info("关闭 TikTok 应用...")
            self.d.app_stop(self.package_name)  # 关闭应用
            time.sleep(2)

            logger.info("重新启动 TikTok 应用...")
            self.d.app_start(self.package_name)  # 启动应用
            time.sleep(5)  # 等待应用完全打开

            logger.success("TikTok 已重新启动")
            return True, "应用重启成功"
        except Exception as e:
            logger.error(f"应用重启失败: {e}")
            return False, f"应用重启失败: {e}"

    # 获取屏幕大小
    def get_screen_size(self):
        """获取屏幕大小"""
        return self.d.window_size()

    # 上滑
    def swipe_up(self):
        """向上滑动，切换下一个视频"""
        try:
            width, height = self.get_screen_size()
            self.d.swipe(width // 2, height * 3 // 4, width // 2, height // 4, 0.01)
            # self.d.press("up")
            logger.success("上滑视频")
            return True, "成功滑动到下一个视频"
        except Exception as e:
            logger.warning(f"滑动失败: {e}")
            return False, f"滑动失败: {e}"

    # 下滑
    def swipe_down(self):
        """向下滑动，回到上一个视频"""
        try:
            width, height = self.get_screen_size()
            self.d.swipe(width // 2, height // 4, width // 2, height * 3 // 4, 0.01)
            logger.success("下滑视频")
            return True, "成功回到上一个视频"
        except Exception as e:
            logger.warning(f"滑动失败: {e}")
            return False, f"滑动失败: {e}"

    # 左滑
    def swipe_left(self):
        """向左滑动，例如浏览 TikTok 个人主页的内容"""
        try:
            width, height = self.get_screen_size()
            self.d.swipe(width * 3 // 4, height // 2, width // 4, height // 2, 0.01)
            logger.success("左滑屏幕")
            return True, "成功向左滑动"
        except Exception as e:
            logger.warning(f"左滑失败: {e}")
            return False, f"左滑失败: {e}"

    # 右滑
    def swipe_right(self):
        """向右滑动，例如从评论区返回视频页面"""
        try:
            width, height = self.get_screen_size()
            self.d.swipe(width // 4, height // 2, width * 3 // 4, height // 2, 0.01)
            logger.success("右滑屏幕")
            return True, "成功向右滑动"
        except Exception as e:
            logger.warning(f"右滑失败: {e}")
            return False, f"右滑失败: {e}"

    # 停止自动观看视频
    def stop_watching(self):
        """停止自动观看"""
        self.stop_flag = True
        logger.success("停止自动观看视频")
        return True, "已成功停止自动观看"  # 添加返回值，避免 NoneType 解包错误

    # 自动观看视频
    def auto_watch(self, count=10, delay=3):
        """自动观看 count 个视频，每个视频停留 delay 秒"""
        try:
            self.stop_flag = False  # 先重置标志
            for i in range(count):
                if self.stop_flag:  # 发现 stop_flag 被设置，停止观看
                    logger.success("检测到停止信号，终止自动观看")
                    return False, "自动观看已停止"

                logger.success(f"正在观看第 {i+1} 个视频")
                time.sleep(delay)  # 模拟观看
                self.swipe_up()  # 滑动到下一个视频

            return True, f"成功观看了 {count} 个视频"
        except Exception as e:
            logger.warning(f"自动观看失败: {e}")
            return False, f"自动观看失败: {e}"

    # 判断当前页面
    def judgment_page(self):
        """逐个条件搜索页面，并返回匹配的标题"""
        try:
            # 定义多个搜索条件（每个条件的值会带上标题）
            search_conditions = [
                {
                    "title": "搜索页面",
                    "condition": {
                        "resourceId": "com.zhiliaoapp.musically:id/fho",
                        "index": 2,
                    },
                },  # 第一个条件
                {
                    "title": "首页",
                    "condition": {
                        "className": "android.widget.LinearLayout",
                        "description": "推荐",
                    },
                },  # 第二个条件（备用）
                {
                    "title": "搜索框",
                    "condition": {
                        "text": "搜索",
                        "className": "android.widget.TextView",
                    },
                },  # 第三个条件（备用）
                # 可以继续添加其他条件和标题
            ]

            # 遍历每个条件，逐个检查
            for item in search_conditions:
                search_page = self.d(**item["condition"])  # 使用动态传入的条件进行搜索
                if search_page.exists:
                    logger.success(f"当前页面匹配: {item['title']}")
                    return True, f"{item['title']}"

            # 如果所有条件都没有找到页面，返回无法判断
            logger.warning("未找到匹配页面")
            return False, "无法判断"

        except Exception as e:
            logger.warning(f"无法判断: {e}")
            return False, f"无法判断: {e}"

    # *  视频页面操作
    def like_video(self):
        """点赞视频"""
        return self.click_element(
            "like_video", "android.widget.ImageView", description="赞"
        )

    def follow_user(self):
        """关注用户"""
        title = self.d(resourceId="com.zhiliaoapp.musically:id/title").get_text()
        return self.click_element(
            "follow_user",
            "android.widget.Button",
            description=f"关注 {title}",
        )

    def favorite_video(self):
        """收藏视频"""
        return self.click_element(
            "favorite_video",
            "android.widget.Button",
            description="将此视频添加到或移出收藏。",
        )

    def share_video(self):
        """分享视频"""
        return self._click_button(
            "android.widget.Button", descriptionMatches="^分享视频。.*"
        )

    def blogger_home(self):
        """观看视频时——点击头像进入博主主页"""
        return self.click_element(
            "blogger_home", "android.widget.ImageView", descriptionMatches="^.*主页"
        )

    def blogger_fallow(self):
        """博主页面关注"""
        return self.click_element(
            "blogger_fallow",
            xpath="//android.widget.TextView[@text='关注']",
            all=1,
            descriptionMatches="主页关注",
        )

    # * 博主页面第一个视频
    def blogger_first_video(self):
        """博主第一个视频"""
        try:
            button = self.d(className="android.widget.GridView").child(
                className="android.widget.FrameLayout"
            )
            if button.exists:
                button.click()
                logger.success("已打开博主第一个视频")
                return True, "已打开博主第一个视频"
            else:
                logger.success("未找到")
                return False, "未找到"
        except Exception as e:
            logger.warning(f"打开失败: {e}")
            return False, f"打开失败: {e}"

    # * 主页右上角的搜索
    def search_video(self):
        """主页右上角的搜索"""
        try:
            button = self.d(className="android.widget.LinearLayout", description="推荐")
            if button.exists:
                w, h = self.d.window_size()
                self.d.click(w - 20, self.status_bar_h + 20)
                logger.success("进入搜索页面")
                return True, "进入搜索页面"
            else:
                logger.success("未找到按钮")
                return False, "未找到按钮"
        except Exception as e:
            logger.warning(f"进入失败: {e}")
            return False, f"进入失败: {e}"

    # * 在搜索框输入关键字并搜索
    def search_input(self, keyword: str = ""):
        """在搜索框输入关键字并搜索"""
        try:
            # 获取搜索框
            search_box = self.d(className="android.widget.EditText")

            if search_box.exists:
                # 清空输入框（可选）
                search_box.clear_text()

                # 输入搜索关键词
                search_box.set_text(keyword)

                logger.success(f"已输入搜索关键字: {keyword}")

                # 触发搜索（模拟回车键）
                self.d.press("enter")

                return True, f"搜索 {keyword} 成功"
            else:
                logger.warning("未找到搜索框")
                return False, "未找到搜索框"

        except Exception as e:
            logger.warning(f"搜索失败: {e}")
            return False, f"搜索失败: {e}"

    # * 暂停播放
    def stop_video(self):
        """暂停播放"""
        try:
            button = self.d(className="android.widget.LinearLayout", description="推荐")
            if button.exists:
                w, h = self.d.window_size()
                self.d.click(w / 2, h / 2)
                logger.success("暂停/播放")
                return True, "暂停/播放"
            else:
                logger.success("未找到按钮")
                return False, "未找到按钮"
        except Exception as e:
            logger.warning(f"进入失败: {e}")
            return False, f"进入失败: {e}"

    # * 唤醒手机
    def wake_up(self, keyword):
        """唤醒手机"""
        try:
            if not self.d.info.get("screenOn"):
                self.d.screen_on()
                self.d.swipe(500, 1500, 500, 500)
                logger.success("唤醒手机")
                return True, "唤醒手机"
            else:
                logger.success("当前已活跃状态")
                return False, "当前已活跃状态"
        except Exception as e:
            logger.warning(f"唤醒失败: {e}")
            return False, f"唤醒失败: {e}"
