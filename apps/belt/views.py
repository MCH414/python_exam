from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
from datetime import datetime

def index(request):
    return render(request,"belt/welcome.html")

#register function
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/main')
    else:
        post = request.POST
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        new_user = User.objects.create(
            name=post['name'], username=post['username'], password=hash1, regdate=post['datehired'])
        request.session['id'] = new_user.id
        return redirect('/wishlist')

#login function
def login(request):
    post = request.POST
    user = User.objects.filter(username=request.POST['username'])
    if not user:
        messages.error(request, 'Wrong Username')
        return redirect('/main')
    login_user = User.objects.get(username=request.POST['username'])
    if not bcrypt.checkpw(request.POST['password'].encode(), login_user.password.encode()):
        messages.error(request, "Loggin Error")
        return redirect('/main')
    else:
        request.session['id'] = login_user.id
        return redirect('/wishlist')

#logout function
def logout(request):
    request.session.clear()
    return redirect("/main")

#triggered by the home button in createwish.html
#redirected by join and remove f
def wishlist(request):
    if 'id' not in request.session:
        messages.error(request, 'please login first')
        return render(request, 'belt/welcome.html')
    else:
        context = {
            'userwish':Wish.objects.filter(wish_creater_id=request.session['id']),
            'otherwish':Wish.objects.exclude(wish_creater_id=request.session['id'])}
        return render(request, 'belt/mywishlist.html', context)

def addpage(request):
    if 'id' not in request.session:
        messages.error(request, 'please login first')
        return render(request, 'belt/welcome.html')
    else:
        return render(request, 'belt/createwish.html')

def processadd(request):
    errors = {}
    # 验证输入的旅游信息是否正确
    #if len(request.POST['itemname']) < 3:
    #    errors["itemname"] = "itemname should be at least 3 characters"
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/addpage')
        #如果旅游信息是valid的话 储存旅游信息
    else:
        new_wish = Wish.objects.create(
            itemname=request.POST['itemname'],
            adddate=request.POST['adddate'],
            wish_creater=User.objects.get(id=request.session['id']))
        new_wish.save()
        context = {
            'userwish':Wish.objects.filter(wish_creater_id=request.session['id']),
            'otherwish':Wish.objects.exclude(wish_creater_id=request.session['id'])}
        print(context)
        return render(request,'belt/mywishlist.html',context)

def wish(request, wishid):
    if 'id' not in request.session:
        messages.error(request, 'please login first')
        return render(request, 'belt/welcome.html')
    else:
        context= {
          'wish': Wish.objects.get(id=int(wishid)),
          'users': User.objects.exclude(attending_wish=wishid)
        }
        return render(request, 'belt/wishinfo.html', context)

def joinwish(request, wishid):
    user = User.objects.get(id=request.session['id'])
    wish = Wish.objects.get(id=int(wishid))
    wish.all_wishmaker.add(user)
    wish.save()
    return redirect('/wishlist')

def deletewish(request,wishid):
    user = User.objects.get(id=request.session['id'])
    wish = Wish.objects.get(id=int(wishid))
    wish.all_wishmaker.remove(user)
    wish.save()
    return redirect('/wishlist')
