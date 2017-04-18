from django.shortcuts import render, render_to_response
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.db import connection
import os
import sqlite3
import random
import time
import base64

cursordb = connection.cursor()
print(time.time())
def dashboard(request):
    return render(request, 'EslWeb/dashboard.html')

def controller(request):
    return render(request, 'EslWeb/controller.html')

def member(request):
    return render(request, 'EslWeb/member.html')

def historyTable(request):
    if request.method == 'POST':
        data_response = {'id': []}
        cursordb.execute('SELECT email FROM esldoor_log ;')
        temp_data = cursordb.fetchall()
        raw_email_log_data = [temp_data[i][0] for i in range(len(temp_data))]
        for i in range(len(raw_email_log_data)):
            cursordb.execute('SELECT %s FROM esl_member WHERE email = "%s";' % ('name',raw_email_log_data[i]) )
            raw_name_log_data=(cursordb.fetchone()[0])
            cursordb.execute('SELECT %s FROM esl_member WHERE email = "%s";' % ('nickname',raw_email_log_data[i]) )
            raw_nickname_log_data=(cursordb.fetchone()[0])
            cursordb.execute('SELECT %s FROM esl_member WHERE email = "%s";' % ('years',raw_email_log_data[i]) )
            raw_years_log_data=(cursordb.fetchone()[0])
            data_response['id'].append({'fullName':raw_name_log_data,'nickName':raw_nickname_log_data,'status':raw_years_log_data})
    return JsonResponse(data_response)

def login(request):
    
    if request.method == 'POST':
    
        email_login,password_login = request.body.split("&")
        email_login = email_login.replace('userName=','')
        password_login = password_login.replace('passWord=','')

        try:
            cursordb.execute('SELECT %s FROM esl_member WHERE %s = "%s";' % ('password','email',email_login))
            password_fetch=cursordb.fetchone()[0]
            if password_fetch == password_login:
                try:
                    token_generated = base64.urlsafe_b64encode(str(random.random()))
                    cursordb.execute('UPDATE esl_member SET token = "%s" WHERE email = "%s" ;' % (token_generated,email_login))
                except:
                    print("Error! Fail to create token...")
                print('email: %s success to login!' % email_login)
                return HttpResponse(token_generated)
            else:
                print('email: %s is attemping login but Email or Password is wrong... ' % email_login)
                return HttpResponse('null')
        except:
            print('email: %s is attemping login but Email or Password is wrong... ' % email_login)
            return HttpResponse('null')


def logout(request):
    if request.method == 'POST':
        pass




def instant_open_door(request):
    if request.method == 'POST':
        token_login = request.body.replace('token=','')
        try:
            cursordb.execute('SELECT %s FROM esl_member WHERE %s = "%s"' % ('token','token',token_login))      
            print("INSTANT OPEN DOOR")
            return HttpResponse("Alohomora")
        except:
            print("someone try to INSTANT_OPEN_DOOR but token is worng...")
            return HttpResponse("null")

def generate_door_password(request):
    if request.method == 'POST':
        type_request_gen,token_login = request.body.split('&')
        type_request_gen  = type_request_gen.replace('typePermision=','')
        token_login = token_login.replace('token=','')
        
        try:
            cursordb.execute('SELECT %s FROM esl_member WHERE %s = "%s"' % ('token','token',token_login))
        except:
            return HttpResponse('null')

        if type_request_gen == 'normal':
            return HttpResponse(random.randrange(1000,1000000))
        elif type_request_gen == 'study':
            return HttpResponse(random.randrange(1000,1000000))
        elif type_request_gen == 'meeting':
            return HttpResponse(random.randrange(1000,1000000))
    

def clear_generate_door_password(password_door):
    pass