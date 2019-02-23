# app/models.py

import inspect
import sys
from flask import session, redirect, url_for, request
import requests
import json
import os
from app import db, admin
from sqlalchemy.sql import select, func
from flask_admin.contrib.sqla import ModelView
import datetime
from app.utils import my_datetime


class Sms(db.Model):
    __tablename__ = 'tbl_sms'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    msisdn = db.Column(db.String(20), nullable=False)
    message_id = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Integer)
    record_date = db.Column(db.DateTime(timezone=True),
                            default=my_datetime)
    last_update = db.Column(db.DateTime(timezone=True),
                            default=my_datetime)

    def __repr__(self):
        return '{}'.format(self.message)


class Token(db.Model):
    __tablename__ = 'tbl_token'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), nullable=False)
    owner_id = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Integer)
    expiry_date = db.Column(db.DateTime(timezone=True))
    record_date = db.Column(db.DateTime(timezone=True),
                            default=my_datetime)
    last_update = db.Column(db.DateTime(timezone=True),
                            default=my_datetime)

    def __repr__(self):
        return '{}'.format(self.token)


class Group(db.Model):
    __tablename__ = 'tbl_group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('tbl_neighbor.id'))
    record_date = db.Column(db.DateTime(timezone=True),
                            default=my_datetime)
    last_update = db.Column(db.DateTime(timezone=True),
                            default=my_datetime)
    neighbors = db.relationship('NeighborGroup', lazy='select')

    def __repr__(self):
        return '{}'.format(self.name)


class NeighborGroup(db.Model):
    __tablename__ = 'tbl_neighbor_group'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey(
        'tbl_group.id'), nullable=False)
    neighbor_id = db.Column(db.Integer, db.ForeignKey(
        'tbl_neighbor.id'), nullable=False)
    record_date = db.Column(db.DateTime(timezone=True),
                            default=my_datetime)
    last_update = db.Column(db.DateTime(timezone=True),
                            default=my_datetime)
    group = db.relationship("Group")

    def __repr__(self):
        return '{}'.format(self.group)


class Neighbor(db.Model):
    __tablename__ = 'tbl_neighbor'
    id = db.Column(db.Integer, primary_key=True)
    msisdn = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(80))
    fcm_id = db.Column(db.String(255))
    fcm_token = db.Column(db.String(255))
    status = db.Column(db.Integer)
    record_date = db.Column(db.DateTime(timezone=True),
                            default=my_datetime)
    last_update = db.Column(db.DateTime(timezone=True),
                            default=my_datetime)
    groups = db.relationship('NeighborGroup', lazy='select')

    def __repr__(self):
        return '{}'.format(self.name)


def load_models_into_admin():
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            if issubclass(obj, db.Model):
                admin.add_view(ModelView(obj, db.session))
                print(obj)


load_models_into_admin()
