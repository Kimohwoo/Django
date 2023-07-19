from django.shortcuts import render, redirect
from django.template.context_processors import request
from board.models import Board
from django.views.decorators.csrf import csrf_exempt
import os
from urllib.parse import quote
from django.http.response import HttpResponse
import chunk

# Create your views here.
UPLOAD_DIR = "C:/Users/it/Documents/DjangoWork/pyboard/board/static/images/"

def list(request):
    boardCount = Board.objects.all().count()
    boardList = Board.objects.all().order_by('-bno')
    return render(request, 'board/list.html', {'boardCount': boardCount, 'boardList': boardList})

def register(request):
    return render(request, 'board/register.html')

@csrf_exempt
def insert(request):
    fname = ''
    fsize = 0
    
    if 'file' in request.FILES:
        file = request.FILES['file']
        fname = file.name
        fsize = file.size
        
        fp = open("%s%s"%(UPLOAD_DIR, fname), 'wb')
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()
        
    t = request.POST['title']
    w = request.POST['writer']
    c = request.POST['content']
    dto = Board(title = t, writer = w, content = c, filename = fname, filesize = fsize)
    dto.save()
    return redirect('/list/')

def download(request):
    no = request.GET['bno']
    dto = Board.objects.get(bno = no)
    path = UPLOAD_DIR + dto.filename
    filename = os.path.basename(path)
    
    # 한글파일 이름 처리 하기
    filename = quote(filename)
    with open(path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/actet-stream')
        response['Content-Dispostion'] = 'attachment; filename="UTF-8''{0}'.format(filename)
    
    dto.down_up()
    dto.save()
    return response
    
def detail(request):
    no = request.GET['bno']
    dto = Board.objects.get(bno = no)
    dto.hit_up()
    dto.save()
    
    filesize = "%.2f"%(dto.filesize/1024)
    return render(request, 'board/detail.html', {'dto': dto, 'filesize': filesize})
    
@csrf_exempt
def update(request):
    no = request.POST['bno']
    dto_src = Board.objects.get(bno = no)
    fname = dto_src.filename
    fsize = dto_src.filesize
    if 'file' in request.FILES:
        file = request.FILES['file']
        fname = file.name
        fsize = file.size
        fp = open('%s%s'%(UPLOAD_DIR, fname), 'wb')
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()
    
    dto_new = Board(bno = no, writer= request.POST['writer'], title = request.POST['title'], content = request.POST['content'], 
                    filename = fname, filesize = fsize)
    dto_new.save()
    return redirect("/list/")
    
@csrf_exempt
def delete(request):
    no = request.POST['bno']
    Board.objects.get(bno = no).delete()
    return redirect("/list/")

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    