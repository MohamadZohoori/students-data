from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name = 'index' ),
    path('add/',views.add, name = 'add'),
    path('add/addStudent/',views.addstudent, name = 'addStudent'),
    path('delete/<int:id>',views.delete, name = 'delete' ),
    path('update/<int:id>',views.update, name = 'update' ),
    path('update/updaterecord/<int:id>', views.updaterecord, name = 'updaterecord'),
    path('stuinfo/<int:id>', views.stuinfo, name = 'stuinfo'),
    path('downloadpdf/', views.pdf_download, name = 'download' ),
    path('downloadexcel/' , views.excel_download, name = 'download-excel'),
]