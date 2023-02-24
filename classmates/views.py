from audioop import reverse
from mmap import PAGESIZE
from .models import Classmates
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.http import FileResponse
import io
import xlsxwriter

def index(request):
    myclassmates = Classmates.objects.all().values()
    template = loader.get_template('index.html')
    context = {
        'myclassmates' : myclassmates
    }
    return HttpResponse(template.render(context,request))

def add(request):
    template = loader.get_template('add.html')
    return HttpResponse(template.render({},request))

def addstudent(request):
    f = request.POST['firstn']
    l = request.POST['lastn']
    p = request.POST['phone']
    e = request.POST['email']
    classmate = Classmates(firstname = f , lastname = l , phone = p , email = e)
    classmate.save()
    return HttpResponseRedirect(reverse('index'))

def delete(request, id):
    classmates = Classmates.objects.get(id = id)  
    classmates.delete() 
    return HttpResponseRedirect(reverse('index'))

def update(request, id):
    myclassmate = Classmates.objects.get(id = id)
    template = loader.get_template('update.html')
    context = {
        'myclassmate' : myclassmate
    }
    return HttpResponse(template.render(context,request))

def updaterecord(request, id):
    firstna = request.POST['firstn']
    lastna = request.POST['lastn']
    p = request.POST['phone']
    e = request.POST['email']
    myclassmate = Classmates.objects.get(id = id)
    myclassmate.firstname = firstna
    myclassmate.lastname = lastna
    myclassmate.phone = p
    myclassmate.email = e
    myclassmate.save()
    return HttpResponseRedirect(reverse('index'))

def stuinfo(request, id):
  classmates = Classmates.objects.get(id=id)
  template = loader.get_template('stuInfo.html')
  context = {
    'classmates': classmates,
  }
  return HttpResponse(template.render(context, request))

def pdf_download(request):

    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, PAGESIZE = letter)
    elements = []
    data = [['id','firstname','lastname','email','phone-number']]
    db_len = Classmates.objects.all().values().count()
    
    for i in range(db_len + 3):
        if (i == 0 or i == 2 or i == 3):
            continue
        classmates = Classmates.objects.get(id = i + 1)
        data.append([classmates.id,classmates.firstname,classmates.lastname,
                    classmates.email,classmates.phone])

    t = Table(data)

    t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))

    elements.append(t)
    pdf.build(elements)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment = True, filename = 'class-list.pdf')

def excel_download(request):
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()

    dataHeaders = ['id','Firstname','Lastname','Email', 'Phone-number']

    row = 0
    column = 0

    db_len = Classmates.objects.all().values().count()

    for items in dataHeaders:
        worksheet.write(row, column, items)
        column += 1
    column = 0
    for i in range(db_len + 3):
        row += 1
        worksheet.write(row,column,i+1)
        if (i == 0 or i == 2 or i == 3):
            continue
        classmate = Classmates.objects.get(id = i+1)
        worksheet.write(row, column, classmate.id)
        column += 1
        worksheet.write(row, column, classmate.firstname)
        column += 1
        worksheet.write(row, column, classmate.lastname)
        column += 1
        worksheet.write(row, column, classmate.email)
        column += 1
        worksheet.write(row, column, classmate.phone)
        column = 0
    
    workbook.close()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment = True, filename = 'class-list.xlsx')
  









