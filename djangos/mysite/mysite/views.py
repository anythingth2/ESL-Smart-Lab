

from django.shortcuts import render, render_to_response
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.db import connection
import os
import sqlite3
import random
import time
import base64
from threading import Timer 
from datetime import datetime
import json 
cs = connection.cursor()

timer_requestDoor_normal = 30
timer_requestDoor_study = 12*60
timer_requestDoor_meeting = 3*60


def dashboard(request):
    return render(request, 'EslWeb/dashboard.html')

def controller(request):
    return render(request, 'EslWeb/controller.html')

def member(request):
    return render(request, 'EslWeb/member.html')

def historyTable(request):
    if request.method == 'POST':
        data_response = {'id': []}
        cs.execute('SELECT email FROM esldoor_log ;')
        temp_data = cs.fetchall()
        raw_email_log_data = [temp_data[i][0] for i in range(len(temp_data))]
        
        for i in range(len(raw_email_log_data)):
            cs.execute('SELECT %s FROM esl_member WHERE email = "%s";' % ('name',raw_email_log_data[i]) )
            raw_name_log_data=(cs.fetchone()[0])
            cs.execute('SELECT %s FROM esl_member WHERE email = "%s";' % ('nickname',raw_email_log_data[i]) )
            raw_nickname_log_data=(cs.fetchone()[0])
            cs.execute('SELECT %s FROM esl_member WHERE email = "%s";' % ('years',raw_email_log_data[i]) )
            raw_years_log_data=(cs.fetchone()[0])
            data_response['id'].append({'fullName':raw_name_log_data,'nickName':raw_nickname_log_data,'status':raw_years_log_data})
    return JsonResponse(data_response)

def generate_token():
    return base64.urlsafe_b64encode(str(random.random()))

def getCurrentTime():
    return datetime.now()


def login(request):
    
    if request.method == 'POST':
    
        email_login,password_login = request.body.split("&")
        email_login = email_login.replace('userName=','')
        password_login = password_login.replace('passWord=','')

        try:
            cs.execute('SELECT %s FROM esl_member WHERE %s = "%s";' % ('password','email',email_login))
            password_fetch=cs.fetchone()[0]
            if password_fetch == password_login:
                try:
                    token_generated = base64.urlsafe_b64encode(str(random.random()))
                    cs.execute('UPDATE esl_member SET token = "%s" WHERE email = "%s" ;' % (token_generated,email_login))
                except:
                    print("Error! Fail to create token...")
                print('email: %s success to login!' % email_login)
                return HttpResponse(token_generated)
            else:
                print('email: %s is attemping login but Email or Password is wrong... ' % email_login)
                return HttpResponse()
        except:
            print('email: %s is attemping login but Email or Password is wrong... ' % email_login)
            return HttpResponse()


def logout(request):
    if request.method == 'POST':
        token_login = request.method.replace("token=",'')
        try:
            cs.execute('UPDATE esl_member SET token="%s" WHERE token="%s";' % (generate_token(),token_login))
        except:
            print("Wrong token when logout...")

def instant_open_door(request):
    if request.method == 'POST':
        token_login = request.body.replace('token=','')
        try:
            cs.execute('SELECT %s FROM esl_member WHERE %s = "%s"' % ('email','token',token_login))
            email_login = cs.fetchone()[0]
            cs.execute('INSERT INTO esldoor_log(email,date) VALUES("%s" ,  "%s" );' % (email_login, getCurrentTime()))
            print("INSTANT OPEN DOOR")
            return HttpResponse("Alohomora")
        except:
            print("someone try to INSTANT_OPEN_DOOR but token is wrong...")
            return HttpResponse()

def clear_generate_door_password(password_door):
    cs.execute('UPDATE esl_member SET passwordDoor="%s" WHERE passwordDoor="%s";' % ('null',password_door))

def generate_door_password(request):
    if request.method == 'POST':
        type_request_gen,token_login = request.body.split('&')
        type_request_gen  = type_request_gen.replace('typePermision=','')
        token_login = token_login.replace('token=','')
        
        try:
            cs.execute('SELECT email FROM esl_member WHERE token = "%s" ;' % (token_login,))
            email_login = cs.fetchone()[0]
        except:
            return HttpResponse()
        
        try:
            #checkToken
            cs.execute('SELECT token FROM esl_member WHERE token = "%s";' % (token_login))
        except:
            return HttpResponse()
 
        password_gen = str(random.randrange(1000,1000000))

        cs.execute('INSERT INTO esldoor_log (email,date) VALUES ("%s","%s");' % (email_login,getCurrentTime()))
        cs.execute('UPDATE esl_member SET passwordDoor="%s" WHERE token="%s";' % (password_gen,token_login))
        
        if type_request_gen == 'normal':
            cs.execute('UPDATE esl_member SET typePasswordDoor= "%s" WHERE token="%s";' % ('normal',token_login))
            
            Timer(timer_requestDoor_normal*60,clear_generate_door_password,(password_gen,)).start()
        elif type_request_gen == 'study':
            cs.execute('UPDATE esl_member SET typePasswordDoor= "%" WHERE token="%s";' % ('tutorial',token_login))
            Timer(timer_requestDoor_study*60,clear_generate_door_password,(password_gen,)).start()
        elif type_request_gen == 'meeting':
            cs.execute('UPDATE esl_member SET typePasswordDoor= "%s" WHERE token="%s";' % ('meeting',token_login))
            Timer(timer_requestDoor_meeting*60,clear_generate_door_password,(password_gen,)).start()

        return HttpResponse(password_gen)




def memberTable(request):

    if True:
        cs.execute('SELECT name FROM esl_member ;')
        name = cs.fetchall()

        cs.execute('SELECT nickname FROM esl_member ;')
        nickname = cs.fetchall()

        cs.execute('SELECT years FROM esl_member ;')
        years = cs.fetchall()

        table =[]
        for i in range(len(name)):
            table.append({'name':name[i][0],'nickname':nickname[i][0],'years':years[i][0]})

    return JsonResponse(table,safe=False)

def add_member(request):
    if request.method == 'POST':
        raw_text = request.body.split('&')
        token_login = raw_text[0].replace('token=','')
        username_login = raw_text[1].replace('userName=','')
        password_login = raw_text[2].replace('passWord=','')
        fullname_login = raw_text[3].replace('fullName=','')
        nickname_login = raw_text[4].replace('nickName=','')
        years_login = raw_text[5].replace('status=','')

        if years_login == '1':
            years_login= '1D'
        elif years_login == '2':
            years_login = '2D'
        elif years_login == '3':
            years_login = '3D'
        elif years_login == '4':
            years_login = '4D'
        elif years_login == '5':
            years_login = 'Master Degree'
        elif year_login == '6':
            years_login = 'Professor'

        cs.execute('INSERT INTO esl_member(email,name,nickname,password,token,years) VALUES("%s","%s","%s","%s","%s","%s");' % (username_login,fullname_login,nickname_login,password_login,token_login,years_login))
        
        return HttpResponse()


    