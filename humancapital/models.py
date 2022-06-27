from django.db import models
import uuid
from django.utils.deconstruct import deconstructible
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField()

    def __str__(self):
        return self.name
    

class Employee(models.Model):
    STATUS_CHOICES = [
        (1,"ACTIVE"),
        (0, "INACTIVE"),
    ]
    emp_no = models.CharField(primary_key=True, max_length=200, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    designation = models.CharField(max_length=30)
    image = models.ImageField(upload_to ="Employee", blank=True)
    nationality = models.CharField(max_length=30)
    qid = models.CharField(max_length=30)
    qid_img = models.ImageField(upload_to ="QID", blank=True)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now=True, auto_now_add=False)
    status =  models.IntegerField(choices=STATUS_CHOICES, default=1)


    @property
    def age(self):
        if self.date_of_birth is None:
            return None

        td = datetime.date.today() - self.date_of_birth
        return int(td.days / 365)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.qid}'



@deconstructible
class UploadTo(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    


class AssetType(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(blank=True)

    def __str__(self):
        return self.name
    


class Asset(models.Model):
    assettype = models.ForeignKey(AssetType, on_delete=models.CASCADE)
    asset_id = models.CharField(max_length=50)
    asset_desc = models.TextField(blank=True)
    assetimage = models.ImageField(upload_to ='assets%Y-%m-%d', )

    def __str__(self):
        return f'{self.assettype.name} {self.asset_id}'

 
class AssetOwner(models.Model):
    owner = models.ForeignKey(Employee, on_delete=models.CASCADE)
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f'{self.asset.asset_id} {self.owner.first_name} {self.owner.last_name}'


class ContractType(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(blank=True)
    contract_duration_months = models.IntegerField(default=36)


    


    def __str__(self):
        return self.name
    

class Contract(models.Model):
    contract_type = models.ForeignKey(ContractType,  on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    contract_start = models.DateField(auto_now=False, auto_now_add=False)
    

    @property
    def contract_end(self):
        contract_end_date = pd.to_datetime(self.contract_start) + pd.DateOffset(months=self.contract_type.contract_duration_months)
        #contract_end_date = datetime.datetime.strptime(self.contract_start, '') + relativedelta(months=self.contract_type.contract_duration_months)
        #contract_end_date = contract_end_date.strftime('%Y-%m-%d')
        return contract_end_date.date()
    
    @property
    def contract_expired(self):
        currentDateTime = datetime.datetime.now()
        contract_end_date = pd.to_datetime(self.contract_start) + pd.DateOffset(months=self.contract_type.contract_duration_months)
        if(currentDateTime.date() > contract_end_date.date()):
            return True
        else:
            return False

    @property
    def months_left_expire(self):
        currentDateTime = datetime.datetime.now()
        contract_end_date = pd.to_datetime(self.contract_start) + pd.DateOffset(months=self.contract_type.contract_duration_months)
        r =  contract_end_date - currentDateTime 
        delta = relativedelta(contract_end_date, currentDateTime)
        #return f"{delta.years} Years, {delta.months} months, {delta.days} days"
        res_months = delta.months + (delta.years * 12)
        return res_months

    def __str__(self):
        return f'{self.employee.first_name} {self.employee.last_name} {self.contract_type.name} {self.contract_start}-{self.contract_end}'
    
    class meta:
        ordering = ['-contract_start']
    