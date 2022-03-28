from django.urls import path
from web import views

# Specifying the path below:

urlpatterns =[
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('sites', views.sites, name='sites'),
    path('add_site', views.add_site, name='add_site'),
    path('delete_site/<str:pk>', views.delete_site, name='delete_site'),
    path('edit_site/<str:pk>', views.edit_site, name='edit_site'),
    path('all_sites_delete', views.all_sites_delete, name='all_sites_delete'),
    #This one is for fun:
    path('feedback', views.feedback, name='feedback'),
    #Lesson URL:
    path('lessons', views.lessons, name='lessons'),
    # send mail url:
    path('send_mail', views.send_mail, name='send_mail'),
    # add_service URL:
    path('add_service', views.add_service, name='add_service'),
    #edit_service URL:
    path('edit_service/<str:pk>', views.edit_service, name='edit_service'),
    # delete_service URL:
    path('delete_service/<str:pk>', views.delete_service, name='delete_service'),
    # add_type URL:
    path('add_type', views.add_type, name='add_type'),
    #edit_type URL:
    path('edit_type/<str:pk>', views.edit_type, name='edit_type'),
    #delete_type URL:
    path('delete_type/<str:pk>', views.delete_type, name='delete_type'),
    # Expense URL:
    path('expense', views.expense, name='expense'),
    # load_types_url URL:
    path('load_types_url', views.load_types_url, name='load_types_url'),
    # view expense URL:
    path('view_expense', views.view_expense, name='view_expense'),
    #Query Expense URL:
    path('query_expense', views.query_expense, name='query_expense'),
    #total_types URL:
    path('total_types', views.total_types, name='total_types'),
    #percentage URL:
    path('percentage', views.percentage, name='percentage'),
    # edit Expense URL:
    path('edit_expense/<str:pk>', views.edit_expense, name='edit_expense'),
    #delete expense URL:
    path('delete_expense/<str:pk>', views.delete_expense, name='delete_expense'),
    # login_note URL:
    path('login_note', views.login_note, name='login_note'),
    #adding an extra one to see if it will work or not:
    path('view_types/<str:pk>', views.view_types, name='view_types'),
    #adding daily_expenses to see the current daily transactions:
    path('daily_expenses', views.daily_expenses, name='daily_expenses'),
    #adding daily_expenses_delete URL:
    path('daily_expense_delete/<str:pk>', views.daily_expense_delete, name='daily_expense_delete'),
]