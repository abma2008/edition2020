from django import forms
from .models import *

# adding a model form for Models:
# 1- adding the Site Form
class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields ='__all__'
        widgets={
            'title': forms.Textarea(attrs={'rows': '1', 'placeholder': 'Enter Title', 'style': 'resize:none;' }),
            'description': forms.Textarea(attrs={'placeholder': 'Enter Description', 'rows': '5', 'style': 'resize:none;'}),
            'url': forms.Textarea(attrs={'class': 'input', 'type': 'url', 'placeholder': 'Enter URL Here', 'style': 'resize:none;', 'rows': '1'})
            }


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'

        def __init__(self,*args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['type'].queryset = Type.objects.none()


            if 'service' in self.data:
                try:
                    country_id = int(self.data.get('service'))
                    self.fields['type'].queryset = Type.objects.filter(service_id = service_id)
                except (ValueError, TypeError):
                    pass # invalid input, ignore and fall back to the empty list
            elif self.instance.pk:
                self.fields['type'].queryset = self.instance.service.type_set.order_by('name')

        widgets={

            'remark': forms.Textarea(attrs={'rows':'3', 'placeholder': 'Enter Notes Here', 'style': 'color:darkred; font-family: times; font-size: large; resize: none'})
            }

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = '__all__'
        widgets={
            'name': forms.Textarea(attrs={'placeholder': 'Enter Type Name', 'rows': '1', 'style':'resize: none'}),
            'description': forms.Textarea(attrs={'rows': '4', 'placeholder': 'Enter Description', 'style': 'color:darkgreen; resize: none'})
        }
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        widgets={
            'name': forms.Textarea(attrs={'placeholder': 'Type Your Service', 'rows': '1', 'class': 'input', 'style':'resize:none;'})
        }
#This is for the Query Form Experiment:

class QueryExpenseForm(forms.Form):
    all_types = Type.objects.all()
    typesList = [("","")]
    for type in all_types:
        typesList.append((type.name, type.name))
    from_date = forms.DateField(
        required=True, label='Start Date',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Start Date',
                'class': 'input',
                'type': 'date'
            }
        ))

    to_date = forms.DateField(
        required=True, label='End Date',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Start Date',
                'class': 'input',
                'type': 'date'
            }
        ))
    #Choosing the Type of Service here:
    choose_type = forms.CharField(
        label='Choose Type',
        required=False,
        widget=forms.Select(choices=typesList)
    )

    #Selecting Payment Types here:
    payments = Payment.objects.all()
    payment_list = [("","")]
    for payment in payments:
        payment_list.append((payment.name, payment.name))
    ##############################
    payment = forms.CharField(
        label='Payment Type',
        required=False,
        widget=forms.Select(choices=payment_list)
    )

class TotalTypesForm(forms.Form):
    from_date = forms.DateField(label="Start Date", widget=forms.TextInput(attrs={'class': 'input', 'type': 'date'}))
    to_date = forms.DateField(label="End Date", widget=forms.TextInput(attrs={'class': 'input', 'type': 'date'}))



# This form is for getting data for the percentage:
class TotalPercentageForm(forms.Form):
    from_date = forms.DateField(
        label="Start Date",
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                 'placeholder': 'Start Date',
                  'type': 'date',
                  'style': 'color:red; background-color:bisque; font-size:large;'
            }
        )
    )
    to_date = forms.DateField(
        label="To Date",
        widget=forms.TextInput(
            attrs={
                'class':'input',
                'placeholder':'To Date',
                'type': 'date',
                'style': 'color:red; background-color:bisque; font-size:large;'
            }
        )
    )

#this is the form for the feedback model. we are using both modelForm and wisgets in Form classes as you will see in this example:
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields ='__all__'
        widgets={
            'name': forms.Textarea(attrs={'rows': '1', 'placeholder': 'Enter Title', 'style':'resize:none'}),
            'email': forms.Textarea(attrs={'type': 'email', 'rows': '1', 'placeholder': 'Enter Email', 'style': 'resize: none;'}),
            'message': forms.Textarea(attrs={'rows': '4', 'placeholder': 'Enter Message', 'style':'resize: none'})
        }
