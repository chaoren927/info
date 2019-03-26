from datetime import datetime
from apps import db


#用户收藏表 多对多
tbl_user_collect=db.Table(
    'user_collect',
    db.Column('id',db.Integer,primary_key=True),
    db.Column('user_id',db.Integer,db.ForeignKey("user.id")),
    db.Column('news_id',db.Integer,db.ForeignKey("news.id")),
)




#用户关注表 一张表当做两张表来用
tbl_user_followed=db.Table(
    'user_followed',
    db.Column('id',db.Integer,primary_key=True),
    db.Column('user_id',db.Integer,db.ForeignKey("user.id")),
    db.Column('followed_id',db.Integer,db.ForeignKey("user.id")),
)



#创建一个能用的类，它是用于记录创建时间和修改时间
class BaseModel(object):
    create_time = db.Column(db.DateTime,default=datetime.now)
    update_time = db.Column(db.DateTime,default=datetime.now)

#管理员表
class Admin(BaseModel,db.Model):
    __tablename__='admin'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30))
    password_hash = db.Column(db.String(255))

#分类表
class News_type(BaseModel,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30))
   
#用户表
class User(BaseModel,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nick_name = db.Column(db.String(30))
    password_hash = db.Column(db.String(255))
    mobile = db.Column(db.String(11),unique=True)
    avatar_url = db.Column(db.String(100))
    joy = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    language = db.Column(db.Integer)
    user_collect = db.relationship('News',secondary=tbl_user_collect,lazy='dynamic')
    user_followed = db.relationship('User',secondary=tbl_user_followed,primaryjoin = id==tbl_user_followed.c.user_id,secondaryjoin = id ==tbl_user_followed.c.followed_id,lazy='dynamic')

    def to_dict(self):
        userdict ={'id':self.id,'nick_name':self.nick_name,'avatar_url':self.avatar_url}
        return userdict

#新闻表
class News(BaseModel,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30))
    descrp = db.Column(db.String(255))
    image_url = db.Column(db.String(100))
    content = db.Column(db.Text)
    is_exam = db.Column(db.Integer)
    reason = db.Column(db.String(100))
    cid = db.Column(db.Integer,db.ForeignKey("news_type.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    news_type = db.relationship(News_type,backref="news")
    author = db.relationship(User,backref="news")
    clicks = db.Column(db.Integer,default=0)

    def to_dict(self):
        newdict = {'id':self.id,'name':self.name,'image_url':self.image_url,'create_time':datetime.strftime(self.create_time,'%Y-%m-%d %H:%M:%S'),'descrp':self.descrp}
        return newdict


#评论表
class Comment(BaseModel,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(30))
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    news_id = db.Column(db.Integer,db.ForeignKey("news.id"))
    like_count = db.Column(db.Integer,default=0)
    user = db.relationship(User)
    def to_dict(self):
        commentdict = {'id':self.id,'content':self.content,'create_time':datetime.strftime(self.create_time,'%Y-%m-%d %H:%M:%S'),
        'user':User.query.filter(User.id==self.user_id).first().to_dict()
        }
        return commentdict
