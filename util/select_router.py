from loguru import logger


def list_routes(app):
    # 获取所有路由
    routes = []
    for rule in app.url_map.iter_rules():
        # 只显示以 '/tiktok' 为前缀的路由
        if rule.endpoint.startswith("tiktok"):
            view_func = app.view_functions[rule.endpoint]
            description = view_func.__doc__.strip() if view_func.__doc__ else "暂无描述"
            routes.append({"path": rule.rule, "description": description})
    routes.pop()
    logger.success("获取所有方法")
    return {"routes": routes}  # 返回为一个 JSON 格式的数组
