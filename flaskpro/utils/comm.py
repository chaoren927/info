from flask import session,g,redirect,url_for
from models import User
from functools import wraps

#装饰器判断登录，获取用户信息
def isLogin(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        username = session.get("username")
        if not username:
            return redirect(url_for("news.index"))
        else:         
            user = User.query.filter(User.mobile == username).first()
            g.user = user
        return func(*args,**kwargs)
    return wrapper
