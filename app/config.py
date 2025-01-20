#!/usr/bin/env python3
"""
this module contains all my configuration settings
which my app would need to run
"""
import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', "sdt6437859975esdsfthtj545e")
    SQLALCHEMY_DATABASE_URI= os.getenv("DATABASE_URI", "sqlite:///auth.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #mail information
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = os.getenv('MAIL_PORT', 587)
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "jgreat770@gmail.com")
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', "yrby ykhg wast ylvl")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "jgreat770@gmail.com")

    # files
    UPLOAD_FOLDER= os.getenv('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'uploads'))
    ALLOWED_EXTENSIONS =os.getenv('ALLOWED_EXTENSION', {'mp4', 'mov', 'avi', 'mkv', "png", "jpg", "jpeg", "gif"})
