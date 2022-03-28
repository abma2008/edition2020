from django.contrib import admin
from .models import *
# Register your models here.
#Defining the Filter using the admin.ModelAdmin to display information:
# Expense:
class ExpenseFilter(admin.ModelAdmin):
    list_display=['service','type', 'amount', 'entry_date']
    list_filter =['service','type', 'amount', 'entry_date']
    # list_editable=['service','type', 'amount', 'entry_date'] // There are more additional configurtions to learn in the future.
    # search_fields=['service','type', 'amount', 'entry_date']
admin.site.register(Expense, ExpenseFilter) #display the Expense along with Expense filter on the admin page...

# Type:
class TypeFilter(admin.ModelAdmin):
    list_display=['service','name','entry_date']
    list_filter=['service','name','entry_date']
    # list_editable=['service','name','entry_date'] // There are more additional configurtions to learn in the future.
    # search_fields=['service','name','entry_date']

admin.site.register(Type, TypeFilter)

# payment:
class PaymentFilter(admin.ModelAdmin):
    list_display=['name','entry_date']
    list_filter=['name','entry_date']
    # list_editable=['name','entry_date'] // There are more additional configurtions to learn in the future.
    # search_fields=['name','entry_date']
admin.site.register(Payment, PaymentFilter) #display Payment along with PaymentFilter on the admin page

# Service:
class ServiceFilter(admin.ModelAdmin):
    list_display=['name']
    list_filter=['name']
    # list_editable=['name'] // There are more additional configurtions to learn in the future.
    # search_fields=['name']
admin.site.register(Service, ServiceFilter) #display the Service along with ServiceFilter on the admin page.

#Site:
class SiteFilter(admin.ModelAdmin):
    list_display=['title','url','image']
    list_filter=['title','url']
admin.site.register(Site, SiteFilter) #display the Site along with SiteFilter on the admin page.

#we will not assigning filter for feedback. We will keep it as a way of refreshing
# to do in the future inshallah.
admin.site.register(Feedback)