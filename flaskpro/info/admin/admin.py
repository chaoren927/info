from flask import Blueprint,render_template,request,flash,session,url_for,redirect,jsonify
from models import *
import re
from utils.response_code import RET,error_map
# 生成密码
from utils.constant import admin_news_count
from werkzeug.security import generate_password_hash,check_password_hash
# 初始化  创建蓝图
admin_blue = Blueprint('admin',__name__)

# 显示登录页面
@admin_blue.route("/login",methods = ['post','get'])
def login():
    if request.method == "POST":
        # 从登陆页面获取用户名和密码
        username = request.form.get('username')
        password = request.form.get('password')
    #     # 如果不存在
        if not all([username,password]):
            flash('亲，信息不完整') 
        else:
            # 用户名必须是数字，字母，下划线
            flag = re.match("\w{5,8}$",username)
            print(flag)
            if flag == False:
                flash('用户名不合法')
            else:
                admin = Admin.query.filter(Admin.name==username).first()
                if not admin:
                    flash('用户不存在')
                else:
                    # 
                    flag = check_password_hash(admin.password_hash,password)
                    if flag:
                        session['username'] = username
                        return redirect(url_for('admin.index'))
                    else:
                        flash('密码错误')
    return render_template('admin/login.html')

# 初始化管理员
@admin_blue.route('/addadmin')
def add_admin():
    password = generate_password_hash('123')
    admin = Admin(name='admin',password_hash=password)
    db.session.add(admin)
    return render_template('admin/index.html')

#主页
@admin_blue.route('/index')
def index():
    # admin_user=session.get('username')
    # if not admin_user:
    #     return redirect(url_for('admin.login'))
    # else:
    #     return render_template('admin/index.html')
    try:
        username = session.get('username')
    except:
        username = ''
    if not username:
        return redirect(url_for('admin.login'))
    return render_template('admin/index.html',username=username)

# 点击新闻分类管理渲染页面
@admin_blue.route('/newscate',methods=['post','get'])
def newscate():
    if request.method=='POST':
        mes={}
        name=request.form.get('name')
        id=request.form.get('id')
        print(name)
        #判断信息是否输入
        if not name:
            mes['code']=RET.OK
            mes['message']=error_map[RET.OK]
        else:
            #根据名称去数据库查询
            cate=News_type.query.filter(News_type.name==name).first()
            if cate:
                mes['code']=RET.OK
                mes['message']=error_map[RET.OK]
            else:
                if not id :
                    cate=News_type(name=name)
                    db.session.add(cate)
                else:
                    News_type.query.filter(News_type.id==id).update({'name':name})
                mes['code']=RET.OK
                mes['message']=error_map[RET.OK]
            return jsonify(mes)
    #查询所有分类
    catelist=News_type.query.all()
    return render_template('admin/news_type.html',catelist=catelist)

# 删除
@admin_blue.route('/deletecate',methods=['get','post'])
def deletecate():
    # 发送post请求
    if request.method == 'POST':
        mes = {}
        id = request.form.get('id')
        news_type = News_type.query.filter(News_type.id==id).delete()
        mes['code'] = RET.OK
        mes['message'] = error_map[RET.OK]     
        return jsonify(mes)


#新闻审核列表
@admin_blue.route("newsreview")
def newsreview():
    current_page= 1
    try:
        p = int(request.args.get('p',0))
    except:
         p=0
    # 搜素
    keyword = request.args.get('keyword')
    if p>0:
        current_page = p
    page_count = admin_news_count
    # 分页
    if keyword:
        news_list = News.query.filter(News.name.like('%'+keyword+'%')).paginate(current_page,page_count,False)
    else:
        keyword=''
        news_list = News.query.paginate(current_page,page_count,False)
    data ={'news_list':news_list.items,'current_page':news_list.page,
    'total_page':news_list.pages,'keyword':keyword}
    return render_template('admin/news_review.html',data=data)


#用户列表
@admin_blue.route("/user_list",methods=['post','get'])
def user_list():
    # 当前的请求页数
    current_page=1
    try:
        p = int(request.args.get('p',0))
    except:
        p=0
    if p>0:
        current_page = p
    # 每页显示条数
    page_count = admin_news_count

    user_list = User.query.paginate(current_page,page_count,False)
    data ={'user_list':user_list.items,'current_page':user_list.page,
    'total_page':user_list.pages}
    return render_template('/admin/user_list.html',data=data)


#审核
@admin_blue.route('news_review_detail',methods=['post','get'])
def news_review_detail():
    if request.method == "POST":
        mes={}
        #获取要更新的值
        id = request.form.get('id')
        action = request.form.get('action')
        reason = request.form.get('reason')
        #通过id获取新闻
        news = News.query.filter(News.id == id).first()
        if news:
            #存在更新字段
            news.is_exam = int(action)
            #失败的时候更新原因
            if int(action) == 2:
                news.reason = reason
            db.session.add(news)
            mes['errno'] = RET.OK
            mes['errmsg'] = error_map[RET.OK]
        else:
            mes['errno'] = 10010
            mes['errmsg'] = '找不到新闻'
        return jsonify(mes)

    id = request.args.get('id')
    news = News.query.filter(News.id == id).first()
    data = {'news':news}
    return render_template('admin/news_review_detail.html',data=data)


from datetime import datetime,timedelta
#用户管理 用户统计
@admin_blue.route('/user_count',methods=['get','post'])
def user_count():
    #总共多少用户
    user = User.query.count()
    #每个月有多少用户
    month_date = datetime.strftime(datetime.now(),"%Y-%m-01")
    month_total = User.query.filter(User.update_time>=month_date).count()

    #每天有多少用户
    day_date = datetime.strftime(datetime.now(), "%Y-%m-%d")
    day_total = User.query.filter(User.update_time >= day_date).count()

    #一个月的日期
    datelist = []
    daycount = []
    for i in range(0,31):
        starttime = datetime.strptime(day_date, "%Y-%m-%d") - timedelta(days=i)
        endtime = datetime.strptime(day_date, "%Y-%m-%d") - timedelta(days=i-1)
        datelist.append(datetime.strftime(starttime,'%Y-%m-%d'))
        count = User.query.filter(User.update_time >= endtime).count()
        daycount.append(count)
    datelist.reverse()
    daycount.reverse()

    #一个月每天登陆的人数
    data = {'total_count':user,'mon_count':month_total,'day_count':day_total,'datelist':datelist,'daycount':daycount}
    return render_template('admin/user_count.html',data=data)


#退出
@admin_blue.route('/logout')
def logout():
    mes = {}
    session.pop('username',None)
    mes['code']= 200
    return redirect('/admin/login')

