from django.urls import path
from .views import *

urlpatterns = [
    path('login', login_page, name='login'),
    path('home', homepage, name='homepage'),
    
    #urls for outgoing documents
    path('outgoing-documents/list', outgoing_docs, name='outgoing-list'),
    path('outgoing-documents/add', add_outgoing, name='outgoing-add'),
    path('outgoing-documents/view/<str:pk>', view_outgoing, name='outgoing-view'),

    #urls for incoming documents
    path('outgoing-documents/release/<str:pk>', release_docs, name='incoming-release'),

    #urls for document type
    path('category/list', category, name='category-list'),
    path('category/add', add_category, name='category-add'),

    #urls for department
    path('department/list', department, name='department-list'),
    path('department/add', add_department, name='department-add'),

]
