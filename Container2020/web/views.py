from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
# Send Mail Classes:
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
# aggregate functions:
from django.db.models import *

#Testing some functionality through using datetime:
from datetime import datetime
from datetime import date


# Create your views here.

def index(request):
    return render(request, 'pages/index.html')

def about(request):
    return render(request, 'pages/about.html')

def login(request):
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            messages.info(request, ' Successful Login')
            return redirect('/')
        else:
            messages.warning(request,' Username or Password is inccorect, please try again')
            return redirect('login')

    return render(request,'pages/login.html')

def subscribe(request):
    if request.method =="POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        email = request.POST["email"]
        try:
            if password == confirm_password:
                if User.objects.filter(username=username).exists():
                    messages.warning(request,'The username is already taken, try a different one')
                    return redirect('subscribe')
                elif User.objects.filter(email=email).exists():
                    messages.warning(request, 'The email is already registered, try a different one')
                    return redirect('subscribe')
                elif User.objects.filter(first_name=first_name, last_name=last_name).exists():
                    messages.warning(request,f" {First_name} {last_name} is already registered, pleasae provide a different first and last name")
                    return redirect('subscribe')
                else:
                    new_user = User.objects.create_user(
                        first_name = first_name,
                        last_name = last_name,
                        username = username,
                        password = password,
                        email = email
                    )
                    new_user.save()
                    messages.info(request,'The username has been registered Successfully')
                    return redirect('subscribe')
            else:
                messages.warning(request,"The Passwords don't match, please try again")
                return redirect('subscribe')
        except Exception as e:
            print(e)

    return render(request,'pages/subscribe.html')

#######################################################################
#  The sites Views
#######################################################################
def sites(request):
    sites = Site.objects.all().order_by('-id')
    context = {'sites': sites}
    return render(request,'pages/sites.html', context)

@login_required(login_url='login')
def add_site(request):
    form = SiteForm()
    try:
        if request.method =="POST":
            form = SiteForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request,'The Site has been added')
                return redirect('add_site')
    except Exception as e:
        messages.warning(request,e)
        messages.info(request,'Something went wrong....')
        return redirect('add_site')
    context = {'form': form}
    return render(request,'pages/add_site.html', context)
@login_required(login_url='login')
def delete_site(request,pk):
    site = Site.objects.get(id=pk)
    if site:
        site.delete()
        messages.info(request,f"The Site titled: {site.title} has been deleted")
        return redirect('sites')
    else:
        messages.warning(request," Couldn't delete the site, no such ID exists")
        return redirect('sites')
@login_required(login_url='login')
def all_sites_delete(request):
    sites = Site.objects.all()
    if sites:
        sites.delete()
        messages.info(request,'All Sites are permanently deleted')
        return redirect('sites')
    else:
        messages.info(request,'No sites to delete')
        return redirect('sites')
@login_required(login_url='login')
def edit_site(request,pk):
    try:
        site_instance = Site.objects.get(id=pk)
        form = SiteForm(instance=site_instance)
        if request.method =="POST":
            form = SiteForm(request.POST, request.FILES, instance=site_instance)
            if form.is_valid():
                form.save()
                messages.info(request,f"The site Titled: {site_instance.title} has been updated")
                return redirect('sites')
        context = {'form': form, 'site_instance': site_instance}
        return render(request,'pages/edit_site.html', context)
    except Exception as e:
        messages.info(request,'Something went wrong, please check the fields !!!')
        messages.warning(request,e)
        return redirect('sites')

################## End of Sites Views #########################################

####### Send Mail View #########################################################
@login_required(login_url='login')
def send_mail(request):
    if request.method =="POST":
        from_email = request.POST['from_email']
        subject = request.POST['subject']
        body = request.POST['message']
        if from_email =="" or subject =="" or body =="":
            messages.warning(request,'One of the fields is empty, fields must be filled, no blanks allowed')
            return redirect('send_mail')
        else:
            try:
                email = EmailMessage(
                    subject,
                    body,
                    settings.EMAIL_HOST_USER,
                    [from_email]
                )
                email.fail_silently=False
                email.send()
                messages.info(request,'The email has been sent succesfully')
                return redirect('send_mail')

            except Exception as e:
                messages.warning(request,e)
                return redirect('send_mail')
    return render(request,'pages/send_mail.html')

##### End of Send Mail View ####################################################

def feedback(request):
    form = FeedbackForm()
    if request.method=="POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,'Thanks for your feedback')
            return redirect('feedback')
    context={'form': form}
    return render(request,'pages/feedback.html', context)

@login_required(login_url='login')
def expense(request):
    form = ExpenseForm()
    if request.method =="POST":
        try:
            form = ExpenseForm(request.POST)
            if form.is_valid():
                form.save()
                messages.info(request,'The Expense has been saved')
                return redirect('expense')
        except Exception as e:
            messages.warning(request, e)
            return redirect('expense')
    context = {'form': form}
    return render(request,'pages/expense.html', context)

@login_required(login_url='login')
def view_expense(request):
    expenses = Expense.objects.all()
    # extract the sum:
    total_sum = expenses.aggregate(total=Sum('amount'))
    total_amount = float(format(total_sum['total'],".2f"))
    total_records = expenses.count()

    context={'expenses': expenses, 'total_amount': total_amount, 'total_records': total_records}
    return render(request,'pages/view_expense.html', context)
#AJAX JSonResponse for populating the type item in the list according to service:
#================================================================================
@login_required(login_url='login')
def load_types_url(request):
    service_id = request.GET.get('service_id')
    types = Type.objects.filter(service_id = service_id)
    return JsonResponse(list(types.values('id', 'name')), safe=False)


@login_required(login_url='login')
def edit_expense(request, pk):
    expense = Expense.objects.get(id=pk)
    form = ExpenseForm(instance=expense)
    if request.method=="POST":
        form = ExpenseForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            form.save()
            messages.info(request,'The expense record has been updated')
            return redirect("daily_expenses")
        else:
            form = ExpenseForm(instance=expense)
            messages.warning(request,'Something went wrong')
            context = {'form': form, 'expense_id': expense.id}
            return render(request,'pages/edit_expense.html', context)
    context = {'form': form, 'expense_id': expense.id}
    return render(request,'pages/edit_expense.html', context)

@login_required(login_url='login')
def delete_expense(request, pk):
    expense = Expense.objects.get(id=pk)
    if expense:
        expense.delete()
        messages.info(request,f"The Expense with ID {pk} falling under category: {expense.service.name}/{expense.type.name} has been deleted successfuly")
        return redirect('view_expense')
    else:
        messages.warning(request,'Nothing has changed')
        return redirect('view_expense')

@login_required(login_url='login')
def query_expense(request):
    form = QueryExpenseForm()
    if request.method =="POST":
        try:
            form = QueryExpenseForm(request.POST)
            if form.is_valid():
                from_date = form.cleaned_data['from_date']
                to_date = form.cleaned_data['to_date']
                choose_type = form.cleaned_data['choose_type']
                payment = form.cleaned_data['payment']
                #Testing new date format below:
                from_date_format = from_date.strftime("%Y-%m-%d")
                to_date_format = to_date.strftime("%Y-%m-%d")

                if from_date =="" or to_date =="":
                    messages.info(request,'Fields empty or one of them is empty, try again')
                    return redirect('query_expense')
                elif choose_type =="" and payment =="":
                    expenses = Expense.objects.filter(only_date__gte=from_date, only_date__lte=to_date).order_by('-id')
                    total_expenses = expenses.count()
                    total_amount = expenses.aggregate(total=Sum('amount'))
                    amount_spent = float(format(total_amount['total'], ".2f"))
                    messages.info(request,f"Querying Expense from {from_date_format} to {to_date_format}")
                    context = {'form': form, 'expenses': expenses, 'total_expenses': total_expenses, 'amount_spent': amount_spent}
                    return render(request,'pages/query_expense.html', context)
                elif choose_type and payment =="":
                    expenses = Expense.objects.filter(only_date__gte=from_date, only_date__lte=to_date, type__name__exact=choose_type).order_by('-id')
                    total_expenses = expenses.count()
                    total_amount = expenses.aggregate(total=Sum('amount'))
                    amount_spent = float(format(total_amount['total'], ".2f"))
                    messages.info(request,f"Querying Expense from {from_date_format} to {to_date_format}")
                    context = {'form': form, 'expenses': expenses, 'total_expenses': total_expenses, 'amount_spent': amount_spent}
                    return render(request,'pages/query_expense.html', context)
                elif payment and choose_type=="":
                    expenses = Expense.objects.filter(only_date__gte=from_date, only_date__lte=to_date, payment__name__exact=payment).order_by('-id')
                    total_expenses = expenses.count()
                    total_amount = expenses.aggregate(total=Sum('amount'))
                    amount_spent = float(format(total_amount['total'], ".2f"))
                    messages.info(request,f"Querying Expense from {from_date_format} to {to_date_format}")
                    context = {'form': form, 'expenses': expenses, 'total_expenses': total_expenses, 'amount_spent': amount_spent}
                    return render(request,'pages/query_expense.html', context)
                else:
                    expenses = Expense.objects.filter(only_date__gte=from_date, only_date__lte=to_date,type__name__exact=choose_type ,payment__name__exact=payment).order_by('-id')
                    total_expenses = expenses.count()
                    total_amount = expenses.aggregate(total=Sum('amount'))
                    amount_spent = float(format(total_amount['total'], ".2f"))
                    messages.info(request,f"Querying Expense from {from_date_format} to {to_date_format}")
                    context = {'form': form, 'expenses': expenses, 'total_expenses': total_expenses, 'amount_spent': amount_spent}
                    return render(request,'pages/query_expense.html', context)
        except Exception as e:
            messages.warning(request,"""
            No records to be retrieved...Please Try again!!!!!
            """)
            context={'form': form}
            return render(request,'pages/query_expense.html', context)
            #return redirect('query_expense')
    context={'form': form}
    return render(request,'pages/query_expense.html', context)


@login_required(login_url='login')
def add_service(request):
    services = Service.objects.all()
    form = ServiceForm()
    if request.method =="POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            service_name = form.cleaned_data['name']
            if service_name =="" or service_name == None:
                messages.info(request," Service name can't be null or empty")
                return redirect('add_service')
            else:
                try:
                    form.save()
                    messages.info(request,'The Service has been added')
                    return redirect('add_service')
                except Exception as e:
                    messages.warning(request,e)
                    return redirect('add_service')

    context = {'services': services, 'form': form}
    return render(request,'pages/add_service.html', context)

@login_required(login_url='login')
def edit_service(request, pk):
    service_instance = Service.objects.get(id=pk)
    form = ServiceForm(instance=service_instance)
    if request.method =="POST":
        try:
            form = ServiceForm(request.POST, instance=service_instance)
            if form.is_valid():
                form.save()
                messages.info(request,f"""
                The Service ID <{service_instance.id}> name updated to <{service_instance.name}>
                """)
                return redirect('add_service')
        except Exception as e:
            messages.warning(request, e)
            return redirect('add_service')
    context = {'form': form}
    return render(request,'pages/edit_service.html', context)

@login_required(login_url='login')
def add_type(request):
    types = Type.objects.all().order_by('service')
    form = TypeForm()
    if request.method =="POST":
        try:
            form = TypeForm(request.POST)
            if form.is_valid():
                # extracting the service_id:
                service = form.cleaned_data['service']
                form.save()
                messages.info(request, 'The Type has been added successfully')
                return redirect('view_types', pk=str(service.id))
        except Exception as e:
            messages.warning(request,e)
            return redirect('add_type')
    context = {'form': form, 'types': types}
    return render(request,'pages/add_type.html', context)

@login_required(login_url='login')
def edit_type(request, pk):
    edit_type = Type.objects.get(id=pk)
    form = TypeForm(instance=edit_type)
    try:
        if request.method =="POST":
            form = TypeForm(request.POST, request.FILES, instance=edit_type)
            if form.is_valid():
                form.save()
                messages.info(request,'The Type has been updated successfully')
                return redirect("view_types", pk=edit_type.service.id)
                # The above return redirect contains a code I have not used before, therefore it is important to keep and fully understand how it operates.
    except Exception as e:
        messages.warning(request,e)
        return redirect("edit_type")
    context = {'form': form}
    return render(request,'pages/edit_type.html', context)

@login_required(login_url='login')
def delete_service(request, pk):
    service = Service.objects.get(id=pk)
    if service:
        service.delete()
        messages.info(request,f"The service ID {pk} and name {service.name} has been deleted")
        return redirect('add_service')
    else:
        messages.info(request,'No service selected for deletion...')
        return redirect('add_service')
#this code below is added online, just for you to keep that in mind:

@login_required(login_url='login')
def delete_type(request,pk):
    type = Type.objects.get(id=pk)
    if type:
        type.delete()
        messages.info(request,f'The Type: {type.name} has been deleted permanently along with its sub records')
        return redirect('view_types', pk=str(type.service.id))
    else:
        messages.info(request,"Can't delete the selected Type")
        return redirect('add_type')

def lessons(request):
    return render(request,'pages/lessons.html')

def login_note(request):
    login_note = "Must be logged in to view the page... Sorry!!!!"
    context = {'login_note': login_note}
    return render(request,'pages/login_note.html', context)

def logout(request):
    auth.logout(request)
    messages.info(request,'You are currently signed out')
    return redirect('index')



# This part is the additional part for total types page.... recently added on July 21st, 2021:
@login_required(login_url='login')
def total_types(request):
    form = TotalTypesForm()
    types = Type.objects.all()
    total_records = Expense.objects.all().count()
    # declaring a dictionary here:
    dict_types = dict()

    if request.method == "POST":
        try:
            form = TotalTypesForm(request.POST, None)
            if form.is_valid():
                from_date = form.cleaned_data['from_date']
                to_date = form.cleaned_data['to_date']
                total_records = Expense.objects.filter(only_date__gte=from_date, only_date__lte=to_date).count()
                #Getting the sum of all Types between the two dates to display the Sum at the end:
                SumTypes = Expense.objects.filter(only_date__gte=from_date, only_date__lte=to_date)
                overall = SumTypes.aggregate(total=Sum('amount'))
                #performing a for loop to calculat the sum of each type separately:
                for type in types:
                    expense = Expense.objects.filter(only_date__gte=from_date, only_date__lte=to_date, type__name__exact=type.name)
                    expense_total = expense.aggregate(total=Sum('amount'))
                    total = expense_total['total']
                    if total == 0 or total is None:
                        continue
                    else:
                        dict_types[type.name] = float(format(total,'.3f'))

                context={'form': form, 'dict_types': dict_types, 'total_records': total_records, 'overall': float(format(overall['total'],'.3f')), 'from_date': from_date, 'to_date': to_date}
                return render(request,'pages/total_types.html', context)
        except Exception as e:
            messages.warning(request,'No Data Found')
            context={'form': form, 'dict_types': dict_types}
            return render(request,'pages/total_types.html', context)


    context={'form': form, 'dict_types': dict_types}
    return render(request,'pages/total_types.html', context)

@login_required(login_url='login')
# This is the part of calculating the percentage of total types per two dates:
def percentage(request):
    form = TotalPercentageForm()
    types = Type.objects.all()
    percentages = dict() #initiating the dictionary to hold the values with percentage
    if request.method =="POST":
        form = TotalPercentageForm(request.POST)
        if form.is_valid():
            try:
                from_date = form.cleaned_data['from_date']
                to_date = form.cleaned_data['to_date']
                expenses = Expense.objects.filter(only_date__gte=from_date, only_date__lte=to_date)
                total_expenses = expenses.aggregate(total=Sum('amount'))
                raw_total = total_expenses['total']
                full_total = raw_total

                for type in types:
                    type_count = Expense.objects.filter(only_date__gte=from_date, only_date__lte=to_date, type__name__exact=type.name)
                    type_total = type_count.aggregate(total=Sum('amount'))
                    T_total = type_total['total']
                    if T_total ==0 or T_total is None:
                        continue
                    else:
                        total_percentage = float(format(((float(T_total)/float(full_total)) * 100),".3f"))
                        percentages[type.name] = total_percentage
                context = {'form': form, 'percentages': percentages, 'from_date': from_date, 'to_date': to_date, 'full_total': float(format(full_total,".3f"))}
                return render(request,'pages/percentage.html', context)
            except Exception as e:
                messages.warning(request,'No records to be retrieved.... Please Try valid dates!!!!')
                return redirect('percentage')


    context = {'form': form}
    return render(request,'pages/percentage.html', context)

#adding this route to be able to view types separately based on service selected:
login_required(login_url='login')
def view_types(request, pk):
    types_dict = dict()
    types = Type.objects.filter(service = pk)
    service = Service.objects.get(id=pk)
    #Declaring counter:
    counter = 1
    for type in types:
        types_dict[counter] = (type.name, type.id)
        counter += 1

    context = {'types_dict': types_dict,'service': service}
    return render(request, 'pages/view_types.html', context)


# Adding the daily_expenses page:
@login_required(login_url='login')
def daily_expenses(request):
    today = date.today()
    today_format = today.strftime('%A, %d of %B, %Y')
    expenses = Expense.objects.filter(only_date = today)
    total_sum = expenses.aggregate(total=Sum('amount'))
    amount = total_sum['total']
    if amount:
        total_amount = str(format(float(amount), '.3f'))
    else:
        total_amount = 0.000
    dict_expenses = dict()
    daily_counter = 1
    for expense in expenses:
        dict_expenses[daily_counter] = (expense.service.name, expense.type.name, expense.amount, expense.payment,expense.remark, expense.id)
        daily_counter +=1
    context = {'dict_expenses': dict_expenses, 'today': today_format, 'total_amount': total_amount}
    return render(request,'pages/daily_expenses.html', context)
#addin a specific daily_expense_delete function:
@login_required(login_url='login')
def daily_expense_delete(request,pk):
    expense = Expense.objects.get(id=pk)
    if expense:
        expense.delete()
        messages.success(request,'Expense Successfully Deleted')
        return redirect('daily_expenses')



