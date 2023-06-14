# -*- coding: utf-8 -*-
from flask import redirect, url_for, render_template, abort, current_app
from flask import request as flask_request
from app import db, models
import json
import re
import math
from datetime import date
from requests import HTTPError
from app.routes.profile import bp
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from app.routes.profile.user.routes import *
from app.routes.idea.routes import *




@ bp.route("/get/allies/", methods=["POST"])
def get_allies():
    if flask_request.method == 'POST':
        text = flask_request.form.get("text")
        already_chosen = eval(flask_request.form.get("already_chosen"))
        allies = current_user.get_allies_from_text(text, already_chosen).limit(10).all()
        formatted_allies = [{"username": ally.username, "name": ally.name, "bio": ally.bio, "photo_src": ally.profile_photo.src, "symbol": ally.symbol} for ally in allies]
        return json.dumps({'status': 'success', 'allies': formatted_allies})

@ bp.route("/connect/<username>/", methods=["POST"])
def connect(username):
    user = models.User.query.filter_by(username=username).first()
    if user and flask_request.method == 'POST':
        sent_request = models.UserToUserRequest.query.filter_by(type="ally", sender=current_user, receiver=user).first()
        received_request = models.UserToUserRequest.query.filter_by(type="ally", receiver=current_user, sender=user).first()
        if flask_request.form.get("do") and not sent_request and not received_request:
            request = models.UserToUserRequest(type="ally", sender=current_user, receiver=user)
            db.session.add(request)
            db.session.commit()
            return json.dumps({'status': 'success'})
        elif flask_request.form.get("accept") and received_request:
            received_request.accept()
            db.session.commit()
            return json.dumps({'status': 'success'})
        elif flask_request.form.get("undo") and sent_request:
            sent_request.regret()
            db.session.commit()
            return json.dumps({'status': 'success'})
        elif flask_request.form.get("disconnect"):
            current_user.allies.remove(user)
            user.allies.remove(current_user)
            db.session.commit()
            return json.dumps({'status': 'success'})
        return json.dumps({'status': 'error'})

@ bp.route("/idea/<handle>/invite/", methods=["POST"])
@ bp.route("/$<handle>/invite/", methods=["POST"])
def invite_to_idea(handle):
    project = models.Project.query.filter_by(handle=handle).first()
    if project not in current_user.project:
        abort(404)
    if flask_request.method == 'POST':
        usernames = json.loads(flask_request.form.get("usernames"))
        for username in usernames:
            user = models.User.query.filter_by(username=username).first()
            sent_request = models.ProjectToUserRequest.query.filter_by(type="invite", sender=project, receiver=user).first()
            received_request = models.UserToProjectRequest.query.filter_by(type="join", receiver=user, sender=project).first()
            if flask_request.form.get("do") and not sent_request and not received_request:
                request = models.ProjectToUserRequest(type="invite", sender=project, receiver=user)
                db.session.add(request)
            elif flask_request.form.get("accept") and received_request:
                received_request.accept()
            elif flask_request.form.get("undo") and sent_request:
                sent_request.regret()
        db.session.commit()
        return json.dumps({'status': 'success', 'handle':handle})

@login_required
@ bp.route("/join/idea/<handle>/", methods=["POST"])
@ bp.route("/join/$<handle>/", methods=["POST"])
def join_project(handle):
    project = models.Project.query.filter_by(handle=handle).first()
    
    if flask_request.method == 'POST':
        received_request = models.ProjectToUserRequest.query.filter_by(type="invite", sender=project, receiver=current_user).first()
        sent_request = models.UserToProjectRequest.query.filter_by(type="join", receiver=project, sender=current_user).first()
        if flask_request.form.get("do") and not sent_request and not received_request:
            request = models.UserToProjectRequest(type="join", receiver=project, sender=current_user)
            db.session.add(request)
        elif flask_request.form.get("accept") and received_request:
            received_request.accept()
        elif flask_request.form.get("undo") and sent_request:
            sent_request.regret()
        db.session.commit()
        return json.dumps({'status': 'success', 'handle':handle})

@ bp.route("/idea/<handle>/exit/", methods=["POST"])
@ bp.route("/$<handle>/exit/", methods=["POST"])
def exit_from_project(handle):
    """
    if flask_request.form.get("disconnect"):
            project.remove_member(user)
            db.session.commit()
            return json.dumps({'status': 'success'})
    """
    pass