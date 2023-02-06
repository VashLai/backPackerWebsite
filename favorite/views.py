# file: favorite/views.py
from django.shortcuts import render,HttpResponseRedirect
from user.models import User
from .models import Favorite
from index.models import Backpacker


# Create your views here.
def is_login(fn):
    def wrap(request, *args, **kwargs):
        if not hasattr(request, 'session'):
            return HttpResponseRedirect('/user/login')
        if 'user' not in request.session:
            return HttpResponseRedirect('/user/login')
        return fn(request, *args, **kwargs)
    return wrap

def make_favo_info(request, aritclenum=None):
    userid = request.session['user']['userid']
    favorite = Favorite.objects.filter(user_id=userid, article_id__contains=aritclenum if aritclenum else "").prefetch_related('bparticlenum')
    favo_info = {}
    favo_list = []
    for list in favorite:
        d = {}
        backpackers = list.bparticlenum.all()
        # print(list.user_id,'here:', ','.join([str(x.title) for x in backpackers]))
        for x in backpackers:
            d['url'] = x.url
            d['region'] = x.name
            d['category'] = x.category
            d['title'] = x.title
            d['reports'] = x.reports
            d['b_time'] = x.b_time
            d['url'] = x.url
            d['note'] = list.note
        d['collect_time'] = list.b_time
        d['article_id'] = list.article_id
        favo_list.append(d)
    favo_info['res'] = favo_list
    return favo_info
 
@is_login
def favorite_view(request):
    favo_info = make_favo_info(request)
    return render(request, 'favorite/favorite.html',locals())

@is_login
def edit_view(request, articlenum):
    if request.method == 'GET':
        favo_info = make_favo_info(request, articlenum)
    elif request.method == 'POST':
        userid = request.session['user']['userid']
        note = request.POST.get('contents', '')
        article_id = request.POST.get('articleId', '')
        afavo = Favorite.objects.get(user_id=userid, article_id=article_id)
        afavo.note=note
        afavo.save()
        return HttpResponseRedirect('/favorite')
    return render(request, 'favorite/edit.html', locals())

@is_login
def add_view(request, articlenum):
    userid = request.session['user']['userid']
    # aUser = User.objects.get(email=email)
    try:
        Favorite.objects.get(article_id=articlenum,user_id=userid)
        return HttpResponseRedirect('/')
    except:
        # TODO 解決如何新增Favorite表的bparticlenum欄位，來與backpacker作為關聯
        backpacker = Backpacker.objects.filter(articlenum=articlenum)[0]
        Favorite.objects.create(article_id=articlenum,user_id=userid, note='尚未備註')
        favorite = Favorite.objects.filter(article_id=articlenum,user_id=userid)[0]
        favorite.bparticlenum.add(backpacker)
        direction = request.META['HTTP_REFERER']
    return HttpResponseRedirect(direction)

@is_login
def del_view(request, articlenum):
    userid = request.session['user']['userid']
    backpacker = Backpacker.objects.filter(articlenum=articlenum)[0]
    afavo = Favorite.objects.get(article_id=articlenum, user_id=userid)
    afavo.bparticlenum.remove(backpacker)
    afavo.delete()
    direction = request.META['HTTP_REFERER']
    return HttpResponseRedirect(direction)
