from django.contrib import admin
from drugs.models import Drugs
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class DrugsAdmin(admin.ModelAdmin):
    list_display = ['id','manufacturer','name','generic','dosage','strength']
    # list_editable = ['teacher_name']
    list_filter = ['name',]
    search_fields = ['name','generic','strength']
    list_per_page = 10
    
admin.site.register(Drugs,DrugsAdmin)

# @admin.register(Drugs)
# class DrugAdmin(ImportExportModelAdmin):
#     pass