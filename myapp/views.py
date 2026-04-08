from urllib import request

from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import *
from django.forms.models import model_to_dict

def search_list(request):
    if 'cname' in request.GET:
        cname = request.GET['cname']    
        print(cname)
        # resultList = students.objects.filter(cname=cname)
        resultList = students.objects.filter(cname__contains=cname)  # 查询
    else:
        resultList = students.objects.all().order_by('cid')


    for item in resultList:
        print(model_to_dict(item))
    # return HttpResponse("Hello, this is the search list page.")
    errormessage=""
    # resultList=[] #模拟查询结果为空

    if not resultList:
        errormessage="No data found."
    # return render(request, 'search_list.html', locals())
    return render(request, 'search_list.html', {'resultList': resultList, 'errormessage': errormessage})

def search_name(request):   
    return render(request, 'search_name.html')

from django.db.models import Q
from django.core.paginator import Paginator 
def index(request):
    if 'site_search' in request.GET:
        site_search = request.GET["site_search"]
        site_search = site_search.strip() #去除前後空白
        keywords = site_search.split() #以空白分割成多個關鍵字
        # print(f"site_search={site_search}")
        print(keywords)
        # 一個關鍵字+搜尋一個欄位
        # resultList = students.objects.filter(cname__contains=site_search).order_by('cid')  # 查询
        # 一個關鍵字+搜尋多個欄位
        # resultList = students.objects.filter(
        #     Q(cid__contains=site_search) | 
        #     Q(cname__contains=site_search) | 
        #     Q(cbirthday__contains=site_search) | 
        #     Q(cemail__contains=site_search) | 
        #     Q(cphone__contains=site_search) | 
        #     Q(caddr__contains=site_search)
        # )

        # github copilot
        # # 多個關鍵字+搜尋多個欄位
        # query = Q()
        # for keyword in keywords:        
        #     query |= Q(cid__contains=keyword) | Q(cname__contains=keyword) | Q(cbirthday__contains=keyword) | Q(cemail__contains=keyword) | Q(cphone__contains=keyword) | Q(caddr__contains=keyword)
        # resultList = students.objects.filter(query).order_by('cid')
        # by chatgpt
        q_objects = Q()
        for keyword in keywords:
            q_objects |= (
                Q(cname__icontains=keyword) |
                Q(cemail__icontains=keyword) |
                Q(cphone__icontains=keyword) |
                Q(caddr__icontains=keyword)
            )
        resultList = students.objects.filter(q_objects)
        # by tony
        # q_objects = Q()
        # for keyword in keywords:
        #     q_objects.add(Q(cname__contains=keyword), Q.OR) 
        #     q_objects.add(Q(csex__contains=keyword), Q.OR)
        #     q_objects.add(Q(cbirthday__contains=keyword), Q.OR)
        #     q_objects.add(Q(cemail__contains=keyword), Q.OR)
        #     q_objects.add(Q(cphone__contains=keyword), Q.OR)
        #     q_objects.add(Q(caddr__contains=keyword), Q.OR)
        # print(q_objects)

    else:
        resultList = students.objects.all().order_by('cid')

    for item in resultList:
        print(model_to_dict(item))
    data_count = len(resultList)
    print(f"Total data count: {data_count}")
    status = True
    errormessage=""
    if not resultList:
        status = False
        errormessage = "No data found."
    # return HttpResponse("Hello, this is the index page.")

    # 分頁設定，每頁顯示2筆資料
    paginator = Paginator(resultList, 2)
    page_nmber = request.GET.get('page')  # 獲取當前頁碼
    page_obj = paginator.get_page(page_nmber)  # 獲取當前頁的資料
    print(f"page_nmber={page_nmber}")
    for item in page_obj:
        print(model_to_dict(item))


    return render(request, 'index.html', 
                  {'resultList': resultList, 
                   'status': status, 
                   'errormessage': errormessage,
                   'data_count': data_count,
                   'page_obj': page_obj
                   }
                  )
from django.shortcuts import redirect
def post(request): 
    if request.method == 'POST':
        cname = request.POST.get('cname')
        csex = request.POST.get('csex')
        cbirthday = request.POST.get('cbirthday')
        cemail = request.POST.get('cemail')
        cphone = request.POST.get('cphone')
        caddr = request.POST.get('caddr')
        print(f"Received POST data: cname={cname}, csex={csex}, cbirthday={cbirthday}, cemail={cemail}, cphone={cphone}, caddr={caddr}")
        add = students(cname=cname, csex=csex, cbirthday=cbirthday, cemail=cemail, cphone=cphone, caddr=caddr)
        add.save()

        # return HttpResponse("已送出 POST 请求。")
        return redirect('index')  # 重定向到 index 页面，显示更新后的数据列表
    else:
        return render(request, 'post.html')
    # return HttpResponse("Hello, this is the post page.")

def edit(request, id):
    print(id)
    if request.method == 'POST':
        cname = request.POST.get('cname')
        csex = request.POST.get('csex')
        cbirthday = request.POST.get('cbirthday')
        cemail = request.POST.get('cemail')
        cphone = request.POST.get('cphone')
        caddr = request.POST.get('caddr')
        print(f"Received POST data: cname={cname}, csex={csex}, cbirthday={cbirthday}, cemail={cemail}, cphone={cphone}, caddr={caddr}")
        #orm
        update = students.objects.get(cid=id)
        update.cname = cname
        update.csex = csex
        update.cbirthday = cbirthday
        update.cemail = cemail  
        update.cphone = cphone
        update.caddr = caddr
        update.save()
        return redirect('index')  # 重定向到 index 页面，显示更新后的数据列表

        # return HttpResponse("已送出 POST 请求。")
    else:
        obj_data = students.objects.get(cid=id)
        print(model_to_dict(obj_data))
        # return HttpResponse("Hello")
        return render(request, 'edit.html', {'obj_data': obj_data})
    

def delete(request, id):
    print(id)
    if request.method == 'POST':
        delete_data = students.objects.get(cid=id)
        delete_data.delete()
        return redirect('index')  # 重定向到 index 页面，显示更新后的数据列表
        # return HttpResponse("已送出 POST 请求。")
    else:
        obj_data = students.objects.get(cid=id)
        print(model_to_dict(obj_data))
        return render(request, 'delete.html', {'obj_data': obj_data})
    
from django.http import JsonResponse
def getAllItems(request):
    resultObject = students.objects.all().order_by('cid')
    # print(type(resultList))
    # for item in resultObject:
    #     # print(model_to_dict(item))
    #     print(type(item))
    resultList = list(resultObject.values()) #將「querySet，元素為object」轉成「list，元素為dict」的型態
    # print(type(resultList))
    # for item in resultList:
    #     # print(model_to_dict(item))
    #     print(type(item))

    # return HttpResponse("Hello")
    return JsonResponse(resultList, safe=False)
    # safe=True,只允許傳入dict
    # safe=False,只允傳非dict


def getItem(request, id):
    try:
        obj = students.objects.get(cid=id) # 取得單一object
        # print(model_to_dict(obj))
        resultDict = model_to_dict(obj) # 將object轉成dict
        # return HttpResponse("Hello")
        return JsonResponse(resultDict, safe=False)
    except:
        # return HttpResponse("False")
        return JsonResponse({"error": "Item not found"}, status=404)


    