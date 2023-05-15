from django.urls import path
from .views import *

urlpatterns = [
    #urls for login and logout
    path('login', login_page, name='login'),
    path('logout', logout_page, name='logout'),

    #urls for homepage
    path('', homepage, name='homepage'),
    
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

    #urls for user
    path('user/list', account, name='user-list'),
    path('user/add', add_account, name='user-add'),
    path('user/view/<str:pk>', view_account, name='user-view'),
    path('user/update/<str:pk>', update_account, name='user-update'),
    path('user/profile', profile, name='user-profile'),
    path('user/change-password', password_update, name='user-update-password'),


]
