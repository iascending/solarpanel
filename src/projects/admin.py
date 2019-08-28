import pdb
from django.contrib import admin
from projects.models import Customer, Quote, Application, Installation, Paperwork
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer
        skip_unchanged = True
        report_skipped = False

class QuoteResource(resources.ModelResource):
    class Meta:
        model = Quote
        skip_unchanged = True
        report_skipped = False

class ApplicationResource(resources.ModelResource):
    class Meta:
        model = Application
        skip_unchanged = True
        report_skipped = False

class InstallationResource(resources.ModelResource):
    class Meta:
        model = Installation
        skip_unchanged = True
        report_skipped = False

class PaperworkResource(resources.ModelResource):
    class Meta:
        model = Paperwork
        skip_unchanged = True
        report_skipped = False

class CustomerAdmin(ImportExportModelAdmin):
    resource_class = CustomerResource
    list_display  = ('first_name', 'last_name', 'email', 'phone', 'address', 'dateCreate', 'createBy', 'dateUpdate')
    list_filter   = ['first_name', 'last_name', 'email', 'createBy']
    search_fields = ['first_name', 'last_name', 'email', 'phone']

class QuoteAdmin(ImportExportModelAdmin):
    resource_class = QuoteResource
    list_display  = ('customer', 'dateQuote', 'taxAssess', 'powerBill', 'cncilRate', 'nearMap', 'quoteFile', 'dateCreate', 'createBy', 'dateUpdate')
    list_filter   = ['customer', 'dateQuote', 'createBy', 'dateUpdate']
    search_fields = ['customer', 'createBy', 'dateQuote']

    # def get_readonly_fields(self, request, obj=None):
    #     user_in_groups = list(request.user.groups.values_list('name', flat=True))
    #     if not "Quote Approval" in user_in_groups:
    #         return ("is_approved", "approved_by", "date_approved")

class ApplicationAdmin(ImportExportModelAdmin):
    resource_class = ApplicationResource
    list_display  = ('customer', 'quote', 'dateApply', 'vicApprove', 'createBy', 'dateCreate', 'dateUpdate')
    list_filter   = ['customer', 'dateApply', 'createBy', 'dateCreate']
    search_fields = ['customer', 'dateApply', 'createBy']

class InstallationAdmin(ImportExportModelAdmin):
    resource_class = InstallationResource
    list_display  = ('customer', 'application', 'installer', 'dateInstall', 'installFile', 'inspectFile', 'createBy', 'dateCreate', 'dateUpdate')
    list_filter   = ['customer', 'installer', 'dateInstall', 'createBy', 'dateCreate']
    search_fields = ['customer', 'installer', 'dateInstall', 'createBy']

class PaperworkAdmin(ImportExportModelAdmin):
    resource_class = PaperworkResource
    list_display  = ('customer', 'install', 'datePaper', 'ewrFile', 'pvFile', 'invoiceFile', 'createBy', 'dateCreate', 'dateUpdate')
    list_filter   = ['customer', 'install', 'datePaper', 'createBy', 'dateCreate']
    search_fields = ['customer', 'datePaper', 'createBy']

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Installation, InstallationAdmin)
admin.site.register(Paperwork, PaperworkAdmin)
