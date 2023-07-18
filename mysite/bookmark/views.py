from django.shortcuts import render
from django.views.generic.list import ListView
from bookmark.models import BookMark
from django.views.generic.detail import DetailView
from django.template.context_processors import request

# Create your views here.

# class  BookMark(ListView):
#     model=BookMark
#
# class BookMarkKDV(DetailView):
#     model=BookMark

def list(request):
    # select * from bookmark order by title
    urlList = BookMark.objects.all().order_by('title')
    # select count(*) from bookmark 
    urlCount = BookMark.objects.all().count()
    
    return render(request, 'bookmark/list.html', {'urlList':urlList, 'urlCount': urlCount})

def detail(request):
    addr = request.GET["url"]
    dto = BookMark.objects.get(url=addr)
    
    return render(request, 'bookmark/detail.html', {'dto': dto})

















