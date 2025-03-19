from loguru import logger


def list_routes(app):
    # 获取所有路由
    routes = []
    for rule in app.url_map.iter_rules():
        # 只显示以 '/tiktok' 为前缀的路由
        if rule.endpoint.startswith('tiktok'):
            routes.append(str(rule))
    routes.pop()
    logger.success("获取所有方法")
    return {'routes': routes}  # 返回为一个 JSON 格式的数组
