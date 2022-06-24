from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from .forms import EmployeeForm, ContractsForm
from django.contrib import messages
from django.core import serializers
import json
# Create your views here.



from.models import Employee, Contract

 


class LoginView(View):

    template_name = 'auth/login.html'

    def get(self, request):
        # <view logic>
        return render(request, self.template_name, )##HttpResponse('result')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['username'] = username
                redirect_to = request.GET.get('next')
                next_url = cache.get('next')
                if next_url:
                    cache.delete('next')
                    return HttpResponseRedirect(next_url)
                else:
                    return redirect('Dashboard')
            else:

                
                return HttpResponse('result')


class DashboardView(View):
    
    template_name = 'main/dashboard.html'

    def get(self, request):
        # <view logic>
        return render(request, self.template_name, )##HttpResponse('result')


class EmployeeFormView(View):

    template_name = 'main/empform.html'
    
    def get(self, request):
        # <view logic>
        form = EmployeeForm()
        return render(request, self.template_name, context={'empform':form} )##HttpResponse('result')'''
    
    def post(self, request):
        form = EmployeeForm(data=request.POST, files=request.FILES)
        
        if form.is_valid():
            #post = form.save(commit=False)
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            

            #post.save()
            return redirect('Employees')
        else:
            return HttpResponse(f'Error saving form--{form.errors}')



class EmployeeView(View):
    
    template_name = 'main/emp_data.html'

    def get(self, request):
        header='Employees'
        data = serializers.serialize("json", Employee.objects.all())
        
        data=json.loads(data)
        print(data)
        return render(request, self.template_name, {'data':data,'title':header,'header':header})
        
class EmployeeDetailsView(View):
    
    template_name = 'main/emp_details.html'
    def __init__(self, serial):
        serial=self.serial
        
    def get(self, request):
        header='Employees'
        #data = serializers.serialize("json", Employee.objects.get(emp_no=self.serial))
        
        data=Employee.objects.get(emp_no=self.serial)#json.loads(data)
        print(Employee.objects.get(emp_no=self.serial))
        return render(request, self.template_name, {'data':data,'title':header,'header':header})


def get_employee_details(request, serial):
    template_name = 'main/emp_details.html'
    header='Employees'

    data = serializers.serialize("json", Employee.objects.filter(emp_no=serial))
    contract_data = serializers.serialize("json", Contract.objects.filter(employee__pk=serial))
    cdata = Contract.objects.filter(employee__pk=serial)
    data=Employee.objects.filter(emp_no=serial)#json.loads(data)
    #print(Contract.objects.filter(employee__pk=serial)[0].months_left_expire)
    print(Employee.objects.filter(emp_no=serial))
    return render(request, template_name, {'data':data[0],'cdata':cdata,'title':header,'header':header})


class ContractsFormView(View):

    template_name = 'main/empform.html'
    
    def get(self, request):
        # <view logic>
        form = ContractsForm()
        return render(request, self.template_name, context={'contractform':form} )##HttpResponse('result')'''
    
    def post(self, request):
        form = ContractsForm(data=request.POST, files=request.FILES)
        
        if form.is_valid():
            #post = form.save(commit=False)
            # process form data
            obj = Contract() #gets new object
            obj.contract_type = form.cleaned_data['contract_type']
            obj.contract_start = form.cleaned_data['contract_start']
            obj.employee = form.cleaned_data['business_phone']
            
            obj.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            

            #post.save()
            return redirect('Employees')
        else:
            return HttpResponse(f'Error saving form--{form.errors}')










def post_contract(request, serial):
    #title='Add Workshop record -- Meter:'+str(serial)
    header='Service Record '+str(serial)
    if (serial =='' or serial == None):
        return redirect('Meters',{'error':'Visit not recorded'})

    else:
        if request.method == "POST":


            form = ContractsForm(data=request.POST, files=request.FILES)
        
            if form.is_valid():
                #post = form.save(commit=False)
                employee = Employee.objects.get(pk=serial)
                # process form data
                obj = Contract() #gets new object
                obj.contract_type = form.cleaned_data['contracttype']
                obj.contract_start = form.cleaned_data['contract_start']
                obj.employee = employee
                obj.save()
                

                # Get the current instance object to display in the template
                #img_obj = form.instance
                

                #post.save()
                return redirect('Employees')
            else:
                return HttpResponse(f'Error saving form--{form.errors}')
        else:
            form = ContractsForm()
    return render(request, 'main/contractform.html', {'form': form, 'serial':serial,'header':header})

