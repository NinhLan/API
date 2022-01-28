# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 11:07:28 2021

@author: ninht
"""

from flask import Flask
app = Flask(__name__)
app.secret_key='lan'
from app import views

#il s'agit d'un point d'entrée de l'application