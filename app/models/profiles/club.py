from app import db
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from app.models.profiles.group import Group
from app.models.static.photo import Photo
from app.models.base import Base
from app.models.locationBase import locationBase
import app.funcs as funcs
from flask import url_for

viewers = db.Table('club_viewers',
                    db.Column('club_id', db.Integer, db.ForeignKey('club.id')),
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                    )


class Club(db.Model, Base, locationBase):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    handle = db.Column(db.String, index=True, unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = db.relationship("Group", foreign_keys=[group_id])
    name = db.Column(db.String)
    description = db.Column(db.String)
    public = db.Column(db.Boolean, default=False)

    profile_photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'))
    profile_photo = db.relationship("Photo", foreign_keys=[profile_photo_id])

    viewers = db.relationship(
        'User', secondary=viewers, lazy='dynamic')

    def __init__(self, **kwargs):
        super(Club, self).__init__(**{k: kwargs[k] for k in kwargs if k != "members"})
        # do custom initialization here
        members = kwargs["members"]
        self.group = Group(members=members)
        for user in members:
            user.clubs.append(self)
        self.profile_photo = Photo(filename="profile_photo", path=f"static/profiles/clubs/{self.handle}/", replacement="/static/images/club.jpg")

    def add_member(self, user):
        self.group.members.append(user)
        user.clubs.append(self)

    def remove_member(self, user):
        self.group.members.remove(user)
        user.clubs.remove(self)

    def delete(self):
        for m in self.group.members:
            m.clubs.remove(self)
        if self.exists_in_db:
            db.session.delete(self.group)
            db.session.delete(self)

    @property
    def symbol(self):
        return "€"

    @property
    def href(self):
        return url_for("profiles.club", handle=self.handle)

    @hybrid_property
    def identifier(self):
        return self.handle

    def __repr__(self):
        return "<Club {}>".format(self.handle)
