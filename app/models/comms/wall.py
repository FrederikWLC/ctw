from app import db
from app.models.base import Base
from time import time
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
import json
from sqlalchemy.ext.declarative import declared_attr


posts = db.Table('posts',
                  db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                  db.Column('wall_id', db.Integer, db.ForeignKey('wall.id'))
                  )

class Wall(Base, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	posts = db.relationship(
	    'Post', secondary=posts, backref="walls", lazy='dynamic')

class Media:

	@declared_attr
	def author_id(self):
		author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	creation_datetime = db.Column(db.DateTime, index=True)
	title = db.Column(db.String)
	content = db.Column(db.Text)

	@declared_attr
	def upvotes(self):
		db.relationship('Vote')

	@declared_attr
	def downvotes(self):
		db.relationship('Vote')

class Vote:
	id = db.Column(db.Integer, primary_key=True)
	upvote = db.Column(db.Boolean)
	voter = db.Column(db.Integer, db.ForeignKey('user.id'))

class Post(Media,Base,db.Model):
	id = db.Column(db.Integer, primary_key=True)

	replies = db.relationship('Post', backref=db.backref("to", remote_side=[id]), lazy='dynamic',
        foreign_keys='Post.to_id')
	to_id = db.Column(db.Integer, db.ForeignKey('post.id'))