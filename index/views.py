# file: index/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator
from favorite.models import Favorite
from tools.Pages import Pages
from django.db.models import Count


# Create your views here.

DEFAULT_PAGE_NUM = 20

def index_view(request):
    # 當使用者登入後，已收藏的文章就無法再被點選收藏了
    userid = ''
    if 'user' in request.session:
        userid = request.session['user']['userid']
    cur_page = request.GET.get("page",1)
    cur_page = int(cur_page)


    # re1 = ((cur_page - 1) * DEFAULT_PAGE_NUM) + 1
    re1 = (cur_page - 1) * DEFAULT_PAGE_NUM
    # re2 = (cur_page) * DEFAULT_PAGE_NUM
    re2 = DEFAULT_PAGE_NUM

    cur_name = request.GET.get('name', '')
    cur_category = request.GET.get('category', '')
    cur_selLocation = request.GET.get('selLocation', '')
    cur_selCategory = request.GET.get('selCategory', '')
    res_name = cur_selLocation if not cur_name else cur_name
    res_category = cur_selCategory if not cur_category else cur_category        
    cur_title = request.GET.get('title', '')
    # sql = "Select a.name,a.category,a.url,a.title,a.reports,a.articlenum,b.user_id from backpacker as a inner join favorite as b on a.articlenum=b.article_id and b.user_id='{}' where a.name like '%%{}%%' and a.category like '%%{}%%' and a.title like '%%{}%%'"
    # backpacker = Backpacker.objects.raw(sql.format(userid,cur_name,cur_category,cur_selLocation,cur_selCategory,cur_title))
    # fbackpacker = list(backpacker) # 不加這行會TypeError: object of type 'RawQuerySet' has no len()
    # abackpacker = Backpacker.objects.all()

    #TODO 檢查sql語法最後的limit使用方式
    sql = """


    SELECT *
    FROM (
        SELECT
            a.name,a.category,a.url,a.title,a.reports,a.articlenum,b.user_id
        FROM
            backpacker a
        LEFT OUTER JOIN
            favorite b
        ON
            a.articlenum=b.article_id
        AND
            b.user_id='{}'
        WHERE
            a.name like '%%{}%%'
        AND
            a.category like '%%{}%%'
        AND
            a.title like '%%{}%%'
    ) c
    limit {},{}
    """
    # print(sql.format(userid,res_name,res_category,cur_title,re1,re2))
    backpacker = Backpacker.objects.raw(sql.format(userid,res_name,res_category,cur_title,re1,re2))
    backpacker = list(backpacker)
    backpacker = [i.__dict__ for i in backpacker]
    csql = """
        SELECT
            *,count(*) as count
        FROM
            backpacker a
        LEFT OUTER JOIN
            favorite b
        ON
            a.articlenum=b.article_id
        AND
            b.user_id='{}'
        WHERE
            a.name like '%%{}%%'
        AND
            a.category like '%%{}%%'
        AND
            a.title like '%%{}%%'
    """
    # print(csql.format(userid,res_name,res_category,cur_title))
    count = Backpacker.objects.raw(csql.format(userid,res_name,res_category,cur_title))
    count = [i.__dict__ for i in list(count)][0]["count"]
    # print(count)
    page_num = count // DEFAULT_PAGE_NUM + 1
    page = Pages(backpacker,cur_page,page_num)

    # if cur_name or cur_category or cur_selCategory or cur_selLocation or cur_title:
    #     backpacker = backpacker.filter(name__contains=cur_name if cur_name else "")
    #     backpacker = backpacker.filter(category__contains=cur_category if cur_category else "")
    #     backpacker = backpacker.filter(name__contains=cur_selLocation if cur_selLocation else "")
    #     backpacker = backpacker.filter(category__contains=cur_selCategory if cur_selCategory else "")
    #     backpacker = backpacker.filter(title__contains=cur_title if cur_title else "")

    # 操作以下方式會使得開啟首頁時延遲超過30秒以上
    ###############################    
    # bp_list =[]
    # for info in backpacker:
    #     d = {}
    #     d['name'] = info.name
    #     d['category'] = info.category
    #     d['url'] = info.url
    #     d['title'] = info.title
    #     d['reports'] = info.reports
    #     d['articlenum'] = info.articlenum
    #     # print('清單文章編號：', info.articlenum)
    #     if userid:
    #         favorites = Favorite.objects.filter(user_id=userid)
    #         for favorite in favorites:
    #             # print('最愛文章編號：', favorite.articlenum)
    #             if str(favorite.articlenum) == str(info.articlenum):
    #             # 如果最愛的文章編號和主頁的文章編號相同，則記錄collect
    #                 d['collect'] = 1
    #                 break
    #     bp_list.append(d)
    # bp_info['res'] = bp_list
    ###############################


    # 在此處添加分頁功能
    # paginator = Paginator(backpacker, 20)
    # cur_page = request.GET.get('page', 1)
    # cur_page = int(cur_page)  # 轉為整數
    # page = paginator.page(cur_page)
    return render(request, 'index/index.html', locals())
