#!/usr/bin/python3
"""
this is a basmodel from which all other model inherit
"""
from datetime import datetime
import uuid
from app import app, db


class BaseModel(db.Model):
    __abstract__ = True  # This class will not create a table in the database

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()