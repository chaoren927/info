from flask import Blueprint,render_template,session,request,jsonify,g
from utils.constant import index_news_count
from models import *
from utils.comm import isLogin
news_blue = Blueprint('news',__name__)

#展示首页
@news_blue.route("/")
def index():
    # user_id = session.get("user_id")
    # user = User.query.filter(User.id==user_id).first()
    username =session.get('username')
    if not username:
        user={}
    else:
        user = User.query.filter(User.mobile == username).first()
    categoies = News_type.query.all()
    #首页点击排行排序(order_by)  存几条limit()
    click_news_list = News.query.order_by(News.clicks.desc()).offset(0).limit(10)
    data = {'categoies':categoies,'user_info':user,'click_news_list':click_news_list}
    return render_template('news/index.html',data=data)


#获取某个分类下新闻
@news_blue.route("/getnewslist")
def getnewslist():
    cid = request.args.get('cid')
    current_page = request.args.get('cur_page')
    news = News.query.filter(News.cid==int(cid),News.is_exam==1).paginate(int(current_page),index_news_count,False)
    mes = {}
    mes['code'] = 200
    mes['total_page'] = news.pages
    newslist = []
    for i in news.items:
        newslist.append(i.to_dict())
    mes['newslist'] = newslist
    return jsonify(mes)


# #获取详情页
# @news_blue.route("/detail")
# @isLogin
# def detail():
#     user = g.user
#     #新闻id
#     id = request.args.get('id',0)
#     #是否收藏状态 默认没收藏
#     is_collected = False
#     news = {}
#     if int(id) >0:
#         news = News.query.filter(News.id==id).first()
#         if news in user.user_collect:
#             is_collected=True
#         news.clicks+=1
#         db.session.add(news)
#     user = session.get('username')
#     if user:
#         user1 = User.query.filter(User.mobile == user).first()
#         # 遍历评论
#         comments = Comment.query.filter(Comment.news_id == news.id).all()
#         click_news_list = News.query.order_by(News.clicks.desc()).offset(0).limit(10)     
#         data = {'news':news,'user_info':user1,'comments':comments,'click_news_list':click_news_list,'is_collected':is_collected}
#     else:
#         data = {'news':news}
#     return render_template('news/detail.html',data=data)
   

# 获取详情页
#获取详情页
@news_blue.route("/detail")
def detail():
    id = request.args.get('id',0)
    is_collected = False
    is_followed = False
    news = {}
    if int(id)>0:
        news = News.query.filter(News.id==id).first()
        news.clicks += 1
        db.session.add(news)
    user = session.get('username')
    # print(user)
    if user:
        user1 = User.query.filter(User.mobile == user).first()
        if news in user1.user_collect:
            is_collected=True
        followd = User.query.get(news.author.id)
        if followd in user1.user_followed:
            is_followed = True

        comments =  Comment.query.filter(Comment.news_id == news.id).all()
        counts = Comment.query.filter(Comment.news_id==news.id).count()
        data = {'counts':counts,'news':news,'user_info':user1,'is_collected':is_collected,'comments':comments,'is_followed':is_followed}
    else:
        comments =  Comment.query.filter(Comment.news_id == news.id).all()
        counts = Comment.query.filter(Comment.news_id==news.id).count()
        data = {'news':news,'comments':comments,'counts':counts}

    news_list = News.query.order_by(News.clicks.desc()).offset(0).limit(10)
    date = {"click_news_list":news_list} 

    return render_template("news/detail.html",data=data,date=date)



#获取详情页
# @news_blue.route("/detail")
# def detail():
#     #新闻id
#     id = request.args.get('id',0)
#     #是否收藏状态
#     is_collected = False
#     news = {}
#     if int(id)>0:
#         news = News.query.filter(News.id==id).first()
#         news.clicks += 1
#         db.session.add(news)
#     user = session.get('username')
#     # print(user)
#     if user:
#         user1 = User.query.filter(User.mobile == user).first()
#         if news in user1.user_collect:
#             is_collected=True
#         comments =  Comment.query.filter(Comment.news_id == news.id).all()
#         data = {'news':news,'user_info':user1,'comments':comments,'is_collected':is_collected}
#     else:
#         data = {'news':news}
#     news_list = News.query.order_by(News.clicks.desc()).offset(0).limit(10)
#     date = {"click_news_list":news_list} 
#     return render_template("news/detail.html",data=data,date=date)


#发表评论
@news_blue.route("/news_comment",methods=['post','get'])
@isLogin
def news_comment():
    user = g.user
    news_id = request.form.get('news_id')
    comment = request.form.get('comment')
    comment = Comment(content=comment,user_id=user.id,news_id=news_id)
    db.session.add(comment)
    db.session.commit()
    mes = {}
    mes['code'] = 200
    mes['data'] = comment.to_dict()
    return jsonify(mes)


#收藏和取消收藏
@news_blue.route('/news_collect',methods=['post','get'])
def news_collect():
    mes = {}
    #获取前台信息
    news_id = request.form.get('news_id')
    action = request.form.get('action')
    news = News.query.get(news_id)
    user = session.get('username')
    user = User.query.filter(User.mobile==user).first()
    if user:
        #收藏
        if action not in ['collect','cancel_collect']:
            mes['code'] = 10011
            mes['mes'] = '方法不正确'
        if action == 'collect':
            user.user_collect.append(news)
            mes['code'] = 200
            mes['mes'] = '收藏成功'
        else:
            if action == 'cancel_collect': 
                user.user_collect.remove(news)
                mes['code'] = 200
                mes['mes'] = '取消成功'
    else:
        mes['code'] = 10010
        mes['mes'] = '请先登录'
    return jsonify(mes)


# #关注和取消关注
# @news_blue.route("/followed_user",methods=['post'])
# @isLogin
# def followed_user():
#     mes={}
#     user = g.user
#     action = request.form.get('action')
#     #被关注的id
#     user_id = request.form.get('user_id')
#     followed_user = User.query.get(user_id)
#     if action=='follow':
#         user.user_followed.append(followed_user)
#         mes['code'] = 200
#         mes['mes'] = "关注成功"
#     elif action=='unfollow':
#         user.user_followed.remove(followed_user)
#         mes['code'] = 200
#         mes['mes'] = "取消关注成功"

#     return jsonify(mes)

#关注和取消关注
@news_blue.route("/followed_user",methods=['post'])
def followed_user():
    print(request.form)
    mes = {}
    action = request.form.get('action')
    #被关注的id
    user_id = request.form.get('user_id')
    followed_user = User.query.get(user_id)
    user = session.get('username')
    user = User.query.filter(User.mobile==user).first()
    if user:
        if action not in ['follow','unfollow']:
            mes['code'] = 10011
            mes['mes'] = '方法不正确'
        if action == 'follow':
            user.user_followed.append(followed_user)
            mes['code'] = 200
            mes['mes'] = '关注成功'
        else:
            if action == 'unfollow':
                user.user_followed.remove(followed_user)
                mes['code'] = 200
                mes['mes'] = "取消关注成功"
    else:
        mes['code'] = 10010
        mes['mes'] = '请登录'
    return jsonify(mes)
