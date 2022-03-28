from django.db import models

# Create your models here.

# This is the Sites Model for sharing:
class Site(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, unique=True, verbose_name="Enter Title")
    description = models.TextField(null=False, blank=False, unique=True, verbose_name="Enter Description")
    url = models.URLField(null=False, blank=False, unique=True, verbose_name="Website URL")
    image = models.ImageField(null=False, blank=False, verbose_name="Upload Image")

    class Meta:
        unique_together=[['title', 'url']]
    def __str__(self):
        return self.title
class Service(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name

class Type(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Choose Service')
    name = models.CharField(max_length=200, null=False, blank=False, unique=False, verbose_name="Add Type")
    description = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Description")
    entry_date = models.DateField(auto_now_add=True, null=False, blank=False)

    class Meta:
        unique_together=[['service', 'name']]

    def __str__(self):
        return self.name

class Payment(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name="Enter Payment Method")
    entry_date  = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return self.name

class Expense(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service', verbose_name="Choose Service")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='type', verbose_name="Choose Type")
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='payment', verbose_name="Payment Method")
    amount = models.FloatField(null=False, blank=False)
    remark = models.TextField(null=True, blank=True, verbose_name="Notes")
    entry_date = models.DateTimeField(auto_now_add=True)
    only_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return str(self.service.name)+'  '+str(self.type.name)+'  '+ str(self.entry_date)

class Feedback(models.Model):
    name  = models.CharField(max_length=200, verbose_name="Title", null=False, blank=False)
    email = models.EmailField(null=False, blank=False, verbose_name="E-Mail Address")
    message = models.TextField(null=False, blank=False, verbose_name="Message")
    entry_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name +"  "+ str(self.entry_date)
