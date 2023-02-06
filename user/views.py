# file: user/views.py
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import User
from hashlib import md5

def login_view(request):
    if request.method == 'GET':
        email = request.COOKIES.get('email', '')
        return render(request, 'user/login.html', locals())
    elif request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('pwd', '')
        if not email:
            email_error = 'Email不得為空'
            return render(request, 'user/login.html', locals())
        if not password:
            pwd_error = '密碼不得為空'
            return render(request, 'user/login.html', locals())
        try:
            aUser = User.objects.filter(email=email)
            aUser =aUser[0]
            m = md5()
            m.update(password.encode())
            if m.hexdigest() == aUser.password:
                request.session['user'] ={
                    'username': aUser.username,
                    'userid': aUser.id
                }
                print(request.session['user']['userid'])
                resp = HttpResponseRedirect('/')
                # resp = render(request,'index/index.html')
                if 'remember' in request.POST:
                    resp.set_cookie('email', email)
                return resp
            else:
                idOrPwd_error = 'Email 或 密碼錯誤'
                password = ''
                return render(request, 'user/login.html', locals())
        except:
            idOrPwd_error = 'Email 或 密碼錯誤'
            password = ''
            return render(request, 'user/login.html', locals())


def logout_view(request):
    # 若在request.session中存在 user 這個鍵，即清除該鍵值
    if 'user' in request.session:
        del request.session['user']
    return HttpResponseRedirect('/')


def register_view(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        pwd1 = request.POST.get('pwd1', '').strip()
        pwd2 = request.POST.get('pwd2', '').strip()

        if len(username) < 2:
            username_error = '會員名稱需大於2個字以上'
            return render(request, 'user/register.html', locals())
        if len(pwd1) < 6:
            pwd1_error = '登入密碼不得為空或小於6碼'
            return render(request, 'user/register.html', locals())
        if pwd1 != pwd2:
            pwd2_error = '兩次密碼不一致'
            return render(request, 'user/register.html', locals())
        try:
            User.objects.get(email=email)
            email_error = '註冊帳號email已存在，請重新注冊'
            return render(request,'user/register.html', locals())
        except:
            # 密碼處理 md5哈希/散列
            m = md5()
            # 從request.body取出的為字串，使用hash計算需轉為字節串，故需使用encode()
            m.update(pwd1.encode())
        # 新增使用者使用try except，確認創建使用者是否成功，若不成功代表資料庫已有該email了
        try:
            User.objects.create(
                username=username, email=email,
                password=m.hexdigest()
            )
            
            reg_res = '註 冊 成 功'
        except:
            return HttpResponse('server is busy')
        resp = render(request,'user/login.html', locals())
        resp.set_cookie('email', email)
        return resp

        
        