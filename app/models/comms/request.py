from app import db
from app.models.comms.notification import Notification
from app.models.base import Base
import json
from sqlalchemy.ext.declarative import declared_attr


class RequestBase:
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, index=True)

    @declared_attr
    def notification_id(self):
        return db.Column(db.Integer, db.ForeignKey('notification.id'))

    @declared_attr
    def notification(self):
        return db.relationship("Notification", foreign_keys=[self.notification_id])

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        # do custom initialization here
        print(self)
        self.sender = kwargs["sender"]
        self.receiver = kwargs["receiver"]
        self.notification = Notification(receiver=self.receiver, payload_json=json.dumps(self.get_notification_payload_json()))

    def accept(self):
        self._do()
        if self.exists_in_db:
            db.session.delete(self)

    def reject(self):
        if self.exists_in_db:
            db.session.delete(self)

    def regret(self):
        if self.exists_in_db:
            db.session.delete(self)
        if self.notification.exists_in_db:
            db.session.delete(self.notification)

    def _do(self):
        # Define
        pass

    def __repr__(self):
        return "<Request {}>".format(self.type)

    def get_notification_payload_json(self):
        # Define this
        return {}.get(self.type)


# From user
# --------------------------------------

class UserToUserRequest(db.Model, RequestBase, Base):
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    sender = db.relationship("User", foreign_keys=[sender_id])
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    receiver = db.relationship("User", foreign_keys=[receiver_id])

    def __init__(self, **kwargs):
        RequestBase.__init__(self, **kwargs)

    def _do(self):
        if self.type == "ally":
            self.receiver.allies.append(self.sender)
            self.sender.allies.append(self.receiver)

    def __repr__(self):
        return "<UserToUserRequest {}>".format(self.type)

    def get_notification_payload_json(self):
        return {"ally": {"type": "request",
                         "request_type":"UserToUserRequest",
                         "request_subtype":"ally",
                         "color": "#3298dc",
                         "icon": "fa fa-user-friends",
                         "sender-name": self.sender.name,
                         "sender-username": self.sender.username,
                         "message": "wants to ally with you",
                         "sender-photo": self.sender.profile_photo.src,
                         "href":f"/@{self.sender.username}/"
                         }}.get(self.type)


class UserToIdeaRequest(db.Model, RequestBase, Base):
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    sender = db.relationship("User", foreign_keys=[sender_id])
    receiver_id = db.Column(db.Integer, db.ForeignKey('idea.id', ondelete='CASCADE'))
    receiver = db.relationship("Idea", foreign_keys=[receiver_id])

    def __init__(self, **kwargs):
        RequestBase.__init__(self, **kwargs)

    def _do(self):
        if self.type == "join":
            self.receiver.viewers.remove(self.sender)
            self.receiver.add_member(self.sender)

    def __repr__(self):
        return "<UserToIdeaRequest {}>".format(self.type)

    def get_notification_payload_json(self):
        return {"join": {"type": "request",
                         "request_type":"UserToIdeaRequest",
                         "request_subtype":"join",
                         "color": "#3298dc",
                         "icon": "fa fa-user-friends",
                         "sender-name": self.sender.name,
                         "sender-username": self.sender.username,
                         "message": "wants to join your Idea",
                         "sender-photo": self.sender.profile_photo.src,
                         "href":f"/£{self.sender.handle}/"
                         }}.get(self.type)

# To user
# --------------------------------------


class IdeaToUserRequest(db.Model, RequestBase, Base):
    sender_id = db.Column(db.Integer, db.ForeignKey('idea.id', ondelete='CASCADE'))
    sender = db.relationship("Idea", foreign_keys=[sender_id])
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    receiver = db.relationship("User", foreign_keys=[receiver_id])

    def __init__(self, **kwargs):
        RequestBase.__init__(self, **kwargs)
        self.sender.viewers.append(self.receiver)

    def _do(self):
        if self.type == "invite":
            self.sender.viewers.remove(self.receiver)
            self.sender.add_member(self.receiver)

    def __repr__(self):
        return "<UserToIdeaRequest {}>".format(self.type)

    def get_notification_payload_json(self):
        return {"invite": {"type": "request",
                           "request_type":"IdeaToUserRequest",
                           "request_subtype":"invite",
                           "color": "#3298dc",
                           "icon": "fa fa-user-friends",
                           "sender-name": self.sender.name,
                           "sender-handle": self.sender.handle,
                           "message": "invites you to join their Idea",
                           "sender-photo": self.sender.profile_photo.src,
                           "href":f"/£{self.sender.handle}/"
                           }}.get(self.type)
