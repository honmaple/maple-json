#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: model.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-02-04 23:44:10 (CST)
# Last Update:星期三 2017-2-8 1:2:17 (CST)
#          By:
# Description:
# **************************************************************************
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime

db = None


class ModelMixin(object):
    @declared_attr
    def id(cls):
        return db.Column(db.Integer, primary_key=True)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # @classmethod
    # def bulk_create(cls, instances):
    #     db.session.add_all(instances)
    #     db.session.commit()

    @classmethod
    def bulk_insert(cls, mappings, return_defaults=False):
        b = db.session.bulk_insert_mappings(cls, mappings, return_defaults)
        db.session.commit()
        return b

    @classmethod
    def bulk_update(cls, mappings):
        b = db.session.bulk_update_mappings(cls, mappings)
        db.session.commit()
        return b

    @classmethod
    def bulk_save(cls,
                  objects,
                  return_defaults=False,
                  update_changed_only=True):
        b = db.session.bulk_save_objects(
            objects, return_defaults=return_defaults, update_changed_only=update_changed_only)
        db.session.commit()
        return b


class ModelTimeMixin(ModelMixin):
    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, default=datetime.utcnow())

    @declared_attr
    def updated_at(cls):
        return db.Column(
            db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())


class ModelUserMixin(ModelTimeMixin):
    @declared_attr
    def user_id(cls):
        return db.Column(
            db.Integer, db.ForeignKey(
                'user.id', ondelete="CASCADE"))

    @declared_attr
    def user(cls):
        name = cls.__name__.lower()
        if not name.endswith('s'):
            name = name + 's'
        if hasattr(cls, 'user_related_name'):
            name = cls.user_related_name
        return db.relationship(
            'User',
            backref=db.backref(
                name, cascade='all,delete', lazy='dynamic'),
            uselist=False,
            lazy='joined')
