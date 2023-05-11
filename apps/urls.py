from django.urls import path
from .views import *

urlpatterns = [
    path('login', login_page, name='login'),
    path('home', homepage, name='homepage'),
    path('outgoing-documents/list', outgoing_docs, name='outgoing-list'),
    path('outgoing-documents/add', add_outgoing, name='outgoing-add'),
    path('outgoing-documents/view/<str:pk>', view_outgoing, name='outgoing-view'),
    # path('outgoing-documents/update/<str:pk>', update_outgoing, name='outgoing-update'),

    path('incoming-documents/list', incoming_docs, name='incoming-list'),
    path('outgoing-documents/release/<str:pk>', release_docs, name='incoming-release'),
    
    path('category/list', category, name='category-list'),
    path('category/add', add_category, name='category-add'),

    path('department/list', department, name='department-list'),
    path('department/add', add_department, name='department-add'),

]
