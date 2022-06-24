from django.contrib import admin
from .models import Employee, Company, Asset, AssetType, ContractType, Contract, AssetOwner
# Register your models here.

class EmployeeAdmin(admin.ModelAdmin):
    readonly_fields=['age']
    list_display = ['qid', 'first_name', 'last_name','age','designation','emp_no','status']
    search_fields = ['designation' ]
    list_filter = ['status', ]
    list_editable = ("status",)
    #date_hierarchy = 'created_on'
    #date_hierarchy_drilldown = False

class ContractAdmin(admin.ModelAdmin):
    #

    readonly_fields=['contract_end']
    '''fieldsets = [
        ('employee', {'fields': ['contract_end',]}),
    ]'''
    list_display = ['employee', 'contract_type', 'contract_start', 'contract_end',]

    #search_fields = ['designation' ]
    list_filter = ['employee', ]
    date_hierarchy = 'contract_start'
    #date_hierarchy_drilldown = False
   

class AssetAdmin(admin.ModelAdmin):
    list_display = ['owner', 'asset', ]
    #search_fields = ['asset_id' ]
    #list_filter = ['assettype', ]
    #date_hierarchy = 'created_on'
    #date_hierarchy_drilldown = False


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Company)
admin.site.register(AssetType)
admin.site.register(AssetOwner, AssetAdmin)
admin.site.register(Asset)
admin.site.register(ContractType)
admin.site.register(Contract, ContractAdmin)