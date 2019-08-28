import os, pdb
from django.db import models
from datetime import date
from django.urls import reverse_lazy
from django.forms import ValidationError

from accounts.models import User

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=128)
    last_name  = models.CharField(max_length=128)
    phone      = models.CharField(max_length=32)
    email      = models.EmailField(max_length=128)
    address    = models.CharField(max_length=256, unique=True, db_index=True)
    cx_status  = models.CharField("Customer Status", max_length=16, choices=[
                                        ('new', 'New'),
                                        ('info ready', 'Info Ready'), 
                                        ('quote ready', 'Quote Ready'),
                                        ('installation ready', 'Installation Ready'),
                                        ('paperwork ready', 'Paperwork Ready')], 
                                  default='new')
    cx_type    = models.CharField("Customer Type", max_length=32, choices = [
                                        ('walkin', 'Walkin'), 
                                        ('wholesale', 'Wholesale'), 
                                        ('group order', 'Group Order')], 
                                  default='walkin')
    createBy   = models.ForeignKey(User, editable=False, on_delete=models.PROTECT, null=True, related_name='customer_create_by_user')
    dateCreate = models.DateField("Date Created", auto_now_add=True)
    dateUpdate = models.DateField("Date Updated", auto_now=True)

    class Meta:
        managed: True
        unique_together = ('phone', 'email')
        ordering = ['first_name', 'last_name']
        verbose_name_plural = '1. Customer'

    def __str__(self):
        return self.first_name + " " + self.last_name

    def get_absolute_url(self):
        return reverse_lazy("projects:customers_list")

class Quote(models.Model):

    def get_taxassess_upload_path(instance, filename):
        file_name, file_extension = os.path.splitext(filename)
        return '{0}_{1}_tax_assessment_{2}{3}'.format(instance.customer.first_name,
                                              instance.customer.last_name,
                                              instance.dateQuote, file_extension)
    def get_powerbill_upload_path(instance, filename):
        file_name, file_extension = os.path.splitext(filename)
        return '{0}_{1}_power_bill_{2}{3}'.format(instance.customer.first_name,
                                              instance.customer.last_name,
                                              instance.dateQuote, file_extension)
    def get_councilrate_upload_path(instance, filename):
        file_name, file_extension = os.path.splitext(filename)
        return '{0}_{1}_council_rate_{2}{3}'.format(instance.customer.first_name,
                                              instance.customer.last_name,
                                              instance.dateQuote, file_extension)
    def get_nearmap_upload_path(instance, filename):
        file_name, file_extension = os.path.splitext(filename)
        return '{0}_{1}_near_map_{2}{3}'.format(instance.customer.first_name,
                                              instance.customer.last_name,
                                              instance.dateQuote, file_extension)
    def get_quote_upload_path(instance, filename):
        file_name, file_extension = os.path.splitext(filename)
        return  '{0}_{1}_quote_{2}{3}'.format(instance.customer.first_name,
                                              instance.customer.last_name,
                                              instance.dateQuote, file_extension)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='quote_for_customer')
    dateQuote  = models.DateField("Date Quoted", default=date.today)
    taxAssess  = models.FileField("Tax Assessment", upload_to=get_taxassess_upload_path, blank=True)
    powerBill  = models.FileField("Power Bill", upload_to=get_powerbill_upload_path, blank=True)
    cncilRate  = models.FileField("Council Rate", upload_to=get_councilrate_upload_path, blank=True)
    nearMap    = models.FileField("Near Map", upload_to=get_nearmap_upload_path, blank=True)
    quoteFile  = models.FileField("Quote Document", upload_to=get_quote_upload_path, blank=True)
    createBy   = models.ForeignKey(User, editable=False, on_delete=models.PROTECT, null=True, related_name='quote_create_by_user')
    dateCreate = models.DateField("Date Created", auto_now_add=True)
    dateUpdate = models.DateField("Date Updated", auto_now=True)

    class Meta:
        managed: True
        ordering: ['-dateQuote']
        verbose_name_plural = '2. Quote'

    def __str__(self):
        return "Quote for " + self.customer.first_name + " " + self.customer.last_name

    def get_absolute_url(self):
        return reverse_lazy("projects:quotes_list")

class Approval(models.Model):
    customer     = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='approval_for_customer')
    quote        = models.OneToOneField(Quote, on_delete=models.CASCADE, related_name='approval_for_quote')
    approvedBy   = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='approved_by_user')
    isApproved   = models.BooleanField("Approved", default=False)
    dateApproved = models.DateTimeField("Date Approved", auto_now=True)

    class Meta:
        ordering: ['-dateApproved']
        verbose_name_plural = '3. Approval'

    def __str__(self):
        return "Quote Approval for " + self.customer.first_name + " " + self.customer.last_name

    def get_absolute_url(self):
        return reverse_lazy("projects:quotes_list")

class Application(models.Model):
    def get_vicapproval_upload_path(instance, filename):
        file_name, file_extension = os.path.splitext(filename)
        return  '{0}_{1}_vic_approval_{2}{3}'.format(instance.customer.first_name,
                                              instance.customer.last_name,
                                              instance.dateApply, file_extension)
    customer   = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='app_for_customer')
    quote      = models.OneToOneField(Quote, on_delete=models.CASCADE, related_name='app_for_quote')
    dateApply  = models.DateField("Date Applied", default=date.today)
    vicApprove = models.FileField("VIC Approval", upload_to=get_vicapproval_upload_path, blank=True)
    createBy   = models.ForeignKey(User, editable=False, on_delete=models.PROTECT, null=True, related_name='app_create_by_user')
    dateCreate = models.DateField("Date Created", auto_now_add=True)
    dateUpdate = models.DateField("Date Updated", auto_now=True)

    class Meta:
        managed: True
        ordering: ['-dateApply']
        verbose_name_plural = '4. Application'

    def __str__(self):
        return "Application for " + self.customer.first_name + " " + self.customer.last_name

    def is_ready_to_apply(self):
        is_tax_assess_done   = True if self.quote.taxAssess.name else False
        is_power_bill_done   = True if self.quote.powerBill.name else False
        is_council_rate_done = True if self.quote.cncilRate.name else False
        is_near_map_done     = True if self.quote.nearMap.name else False
        is_quote_file_done   = True if self.quote.quoteFile.name else False
        return is_tax_assess_done and is_power_bill_done and is_council_rate_done and is_near_map_done and is_quote_file_done and self.quote.is_approved

    def clean(self):
        if self.quote.customer != self.customer:
            raise ValidationError("The quote you selected is not for that customer")
        if not self.is_ready_to_apply():
            raise ValidationError("Please quote customer first")

    def get_absolute_url(self):
        return reverse_lazy("projects:applications_list")

class Installation(models.Model):
    def get_inspectfile_upload_path(instance, filename):
        file_name, file_extension = os.path.splitext(filename)
        return  '{0}_{1}_inspect_file_{2}{3}'.format(instance.customer.first_name,
                                              instance.customer.last_name,
                                              instance.dateInstall, file_extension)
    def get_installfile_upload_path(instance, filename):
      file_name, file_extension = os.path.splitext(filename)
      return  '{0}_{1}_install_file_{2}{3}'.format(instance.customer.first_name,
                                            instance.customer.last_name,
                                            instance.dateInstall, file_extension)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='install_for_customer')
    application= models.OneToOneField(Application, on_delete=models.CASCADE, related_name='install_for_app')
    installer  = models.CharField(max_length=256)
    dateInstall= models.DateField("Date Installed", default=date.today)
    installFile= models.FileField("Installation Report", upload_to=get_installfile_upload_path, blank=True)
    inspectFile= models.FileField("Inspection Report", upload_to=get_inspectfile_upload_path, blank=True)
    createBy   = models.ForeignKey(User, editable=False, on_delete=models.PROTECT, null=True, related_name='install_create_by_user')
    dateCreate = models.DateField("Date Created", auto_now_add=True)
    dateUpdate = models.DateField("Date Updated", auto_now=True)

    class Meta:
        managed: True
        ordering: ['-dateInstall']
        verbose_name_plural = '5. Installation'

    def __str__(self):
        return "Installation for " + self.customer.first_name + " " + self.customer.last_name

    def is_ready_to_install(self):
        return True if self.application.vicApprove.name else False

    def clean(self):
        if self.application.customer != self.customer:
            raise ValidationError("The application you selected is not for that customer")
        if not self.is_ready_to_install():
            raise ValidationError("Please apply for VIC approval before installation")

    def get_absolute_url(self):
        return reverse_lazy("projects:installations_list")


class Paperwork(models.Model):
    def get_ewrfile_upload_path(instance, filename):
        file_name, file_extension = os.path.splitext(filename)
        return  '{0}_{1}_ewr_file_{2}{3}'.format(instance.customer.first_name,
                                              instance.customer.last_name,
                                              instance.datePaper, file_extension)
    def get_pvfile_upload_path(instance, filename):
        file_name, file_extension = os.path.splitext(filename)
        return  '{0}_{1}_pv_file_{2}{3}'.format(instance.customer.first_name,
                                              instance.customer.last_name,
                                              instance.datePaper, file_extension)
    def get_invoicefile_upload_path(instance, filename):
        file_name, file_extension = os.path.splitext(filename)
        return  '{0}_{1}_invoice_{2}{3}'.format(instance.customer.first_name,
                                              instance.customer.last_name,
                                              instance.datePaper, file_extension)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='pw_for_customer')
    install = models.OneToOneField(Installation, on_delete=models.CASCADE, related_name='pw_for_install', verbose_name="Installation")
    datePaper  = models.DateField("Date Completed", default=date.today)
    ewrFile    = models.FileField("EWR File", upload_to=get_ewrfile_upload_path, blank=True)
    pvFile     = models.FileField("PV File", upload_to=get_pvfile_upload_path, blank=True)
    invoiceFile= models.FileField("Invoice", upload_to=get_invoicefile_upload_path, blank=True)
    createBy   = models.ForeignKey(User, editable=False, on_delete=models.PROTECT, null=True, related_name='pw_create_by_user')
    dateCreate = models.DateField("Date Invoiced", auto_now_add=True)
    dateUpdate = models.DateField("Date Updated", auto_now=True)

    class Meta:
        managed: True
        ordering: ['-datePaper']
        verbose_name_plural = '6. Paperwork'

    def __str__(self):
        return "Paperwork for " + self.customer.first_name + " " + self.customer.last_name

    def is_ready_to_pw(self):
        is_inspection_done   = True if self.install.inspectFile.name else False
        is_installation_done = True if self.install.installFile.name else False
        return is_inspection_done and is_installation_done

    def clean(self):
        if self.install.customer != self.customer:
            raise ValidationError("The installation you selected is not for that customer")
        if not self.is_ready_to_pw():
            raise ValidationError("Please complete installation first.")

    def get_absolute_url(self):
        return reverse_lazy("projects:paperworks_list")
