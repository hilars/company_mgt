from django import forms
from .models import Employee, ContractType
from . import widgets

'''class EmployeeForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    designation = forms.CharField(max_length=30)
    image = forms.ImageField(upload_to ='employee_%Y-%m-%d', )
    nationality = forms.CharField(max_length=30)
    qid = forms.CharField(max_length=30)
    qid_img = forms.ImageField(upload_to ='qid_%Y-%m-%d', )
    date_of_birth = forms.DateField(auto_now=False, auto_now_add=False)
    company = forms.ForeignKey(Company, on_delete=models.CASCADE)'''

class EmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)

        self.fields['date_of_birth'].widget = widgets.DateInput()
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'designation', 'image', 'nationality', 'qid', 'qid_img', 'date_of_birth', 'company']
        #required_css_class = 'required'


class ContractsForm(forms.Form):
    contracttype = forms.ModelChoiceField(
            widget= forms.Select(attrs={'placeholder':"Meter make",'id':'meter','class':'form-control form-control-sm',}), queryset=ContractType.objects.all())
    contract_start = forms.DateField(widget=widgets.DateInput())
