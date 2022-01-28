# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 17:21:45 2021

@author: ninht
"""

from app import app
from flask import render_template,request, session, redirect,url_for
import sqlite3

with sqlite3.connect("patients.db") as con: 
    cur = con.cursor()
    cur.execute("SELECT * FROM patients")
    global patients
    patients=cur.fetchall()
    
with sqlite3.connect("soignants.db") as con: 
    cur = con.cursor()
    cur.execute("SELECT * FROM soignants")
    global soignants
    soignants=cur.fetchall()


@app.route('/login/', methods=['GET', 'POST'])
def login():
    
    msg=''
     # Vérifier si les requêtes POST "username" et "password" existent
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Créer des variables pour plus facillle à acces
        username = request.form['username']
        password = request.form['password']

        global patients
        global soignants
        for i in soignants:               
            if (i[0] == username) and (i[1] == password):
                session['loggedinS'] = True
                session['username'] = i[0]
                return render_template ('bienvenueS.html', title='Bienvenue', utilisateur=session['username'])
            else:
            # Le compte n'existe pas ou le nom d'utilisateur/mot de passe est incorrect.
                msg = 'Nom d\'utilisateur et/ou le mot de passe sont incorrects, veuillez-les corriger ou créer un compte.' 
        # Si le compte existe dans la table "patients" dans la base de données externe
        for i in patients:
            if (i[2] == username or i[0] == username) and (i[1] == password):
                session['loggedinP'] = True
                session['username'] = i[2]
                session['password'] = i[1]
                return render_template ('home.html', title='Bienvenue', utilisateur=session['username'])
            else:
            # Le compte n'existe pas ou le nom d'utilisateur/mot de passe est incorrect.
                msg = 'Nom d\'utilisateur et/ou le mot de passe sont incorrects, veuillez-les corriger ou créer un compte.' 

    return render_template('index.html', msg=msg)
@app.route('/login/logout')
def logout():
    session.pop('loggedinP', None)
    session.pop('loggedinS', None)
    session.pop('username', None)
    session.pop('password', None)    
    return redirect(url_for('login'))

@app.route('/login/home')
def home():

    if 'loggedinP' in session:
        return render_template('home.html', utilisateur=session['username'])

    if 'loggedinS' in session:
        return render_template('bienvenueS.html', utilisateur=session['username'])     
    
    return redirect(url_for('login'))

@app.route('/login/profile')
def profile():
    global patients
    # Vérifier si l'utilisateur est connecté
    if 'loggedinP' in session:
        for i in patients:
            if (i[0] == session['username'] or i[2] == session['username']) and i[1] == session['password']:
                
                return render_template('profile.html',n_id=i[0], mdp = i[1], name = i[2],gendre = i[3],age = i[4],chest = i[5],resting_blood_pressure = i[6],cholestoral = i[7],sugar = i[8],electrocardiographic = i[9],maximumheart = i[10],exercise_induced_angina = i[11],oldpeak = i[12],slope = i[13],majorvessels= i[14],thal = i[15],result = i[16])
    # L'utilisateur n'est pas connecté et est redirigé vers la page de connexion.
    return redirect(url_for('login'))

@app.route('/login/dossier')
def dossier():
    msg=''
    global soignants
    # Vérifier si l'utilisateur est connecté
    if 'loggedinS' in session:
        return render_template('recherche.html', msg=msg)
    # L'utilisateur n'est pas connecté et est redirigé vers la page de connexion.

@app.route('/login/trouver', methods=['GET', 'POST'])
def trouver():
    if request.method == 'POST' and 'nid' in request.form:
        global patients
        nid = request.form['nid']
        session['loggedinP'] = False
        for j in patients:
            if j[0] == nid:
                session['loggedinP'] = True
                i=j
        if 'loggedinP' in session:
             return render_template('dossier.html',n_id=i[0], mdp = i[1], name = i[2],gendre = i[3],age = i[4],chest = i[5],resting_blood_pressure = i[6],cholestoral = i[7],sugar = i[8],electrocardiographic = i[9],maximumheart = i[10],exercise_induced_angina = i[11],oldpeak = i[12],slope = i[13],majorvessels= i[14],thal = i[15],result = i[16])
        else:
            msg = 'ID du patient n\'existe pas!'
            return render_template('recherche.html', msg=msg)
        
        
    
    
