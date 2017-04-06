from django.shortcuts import render, render_to_response
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.db import connection
import os
import sqlite3

cursordb = connection.cursor()

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
            data_response['id'].append({'fullname':raw_name_log_data,'nickname':raw_nickname_log_data,'status':raw_years_log_data})
    return JsonResponse(data_response)

def login(request):
    if request.method == 'GET':
        email_login = 'chat@gmail.com'
        password_login = 'eiei1132'
        token_login = ''
        try:
            cursordb.execute('SELECT %s FROM esl_member WHERE %s = "%s";' % ('password','email',email_login))
            password_fetch=cursordb.fetchone()[0]
            cursordb.execute('SELECT %s FROM esl_member WHERE %s = "%s";' % ('token','email',email_login))
            token_fetch = cursordb.fetchone()[0] 
        except:
            print('can\'t find email_login in database')
    return HttpResponse(request)