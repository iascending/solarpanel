import pdb
from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.db.utils import OperationalError
from django.db.models import F, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import QuoteCreationForm, ApprovalCreationForm
from .models import Customer, Quote, Approval, Application, Installation, Paperwork
from .multiforms import MultiFormsView

# Create your views here.
class NewCustomer(LoginRequiredMixin, CreateView):
    fields = '__all__'
    model  = Customer
    template_name = 'projects/customer_form.html'

    def form_valid(self, form):
        form.instance.createBy = self.request.user
        return super(NewCustomer, self).form_valid(form)

    def user_perm_check(self, request):
        if request.user.has_perm('projects.add_customer'):
            return True

    def dispatch(self, request, *args, **kwargs):
        if not self.user_perm_check(request):
            raise PermissionDenied
        return super(NewCustomer, self).dispatch(request, *args, **kwargs)

# class NewQuote(LoginRequiredMixin, CreateView):
#     form_class = QuoteCreationForm
#     template_name = 'projects/quote_form.html'

#     def form_valid(self, form):
#         form.instance.createBy = self.request.user
#         return super(NewQuote, self).form_valid(form)

#     def user_perm_check(self, request):
#         if request.user.has_perm('projects.add_quote'):
#             return True

#     def dispatch(self, request, *args, **kwargs):
#         if not self.user_perm_check(request):
#             raise PermissionDenied
#         return super(NewQuote, self).dispatch(request, *args, **kwargs)

#     def get_form_kwargs(self):
#         kwargs = super(NewQuote, self).get_form_kwargs()
#         kwargs.update({'user': self.request.user})
#         return kwargs

class NewQuote(LoginRequiredMixin, MultiFormsView):
    template_name = 'projects/quote_form.html'
    form_classes  = {'quote': QuoteCreationForm, 'approval': ApprovalCreationForm}
    success_url   = '/'

    def quote_form_valid(self, form):
        form.instance.createBy = self.request.user
        return form.quote(self.request, redirect_url=self.get_success_url())

    def approval_form_valid(self, form):
        form.instance.approvedBy = self.request.user
        return form.approval(self.request, redirect_url=self.get_success_url())

    def get_context_data(self, **kwargs):
        return super(NewQuote, self).get_context_data(**kwargs)

    # def user_perm_check(self, request):
    #     if request.user.has_perm('projects.add_quote'):
    #         return True

    # def dispatch(self, request, *args, **kwargs):
    #     if not self.user_perm_check(request):
    #         raise PermissionDenied
    #     return super(NewQuote, self).dispatch(request, *args, **kwargs)

class NewApplication(LoginRequiredMixin, CreateView):
    fields = '__all__'
    model  = Application
    template_name = 'projects/application_form.html'

    def form_valid(self, form):
        form.instance.createBy = self.request.user
        return super(NewApplication, self).form_valid(form)

    def user_perm_check(self, request):
        if request.user.has_perm('projects.add_application'):
            return True

    def dispatch(self, request, *args, **kwargs):
        if not self.user_perm_check(request):
            raise PermissionDenied
        return super(NewApplication, self).dispatch(request, *args, **kwargs)

class NewInstallation(LoginRequiredMixin, CreateView):
    fields = '__all__'
    model  = Installation
    template_name = 'projects/installation_form.html'

    def form_valid(self, form):
        form.instance.createBy = self.request.user
        return super(NewInstallation, self).form_valid(form)

    def user_perm_check(self, request):
        if request.user.has_perm('projects.add_installation'):
            return True

    def dispatch(self, request, *args, **kwargs):
        if not self.user_perm_check(request):
            raise PermissionDenied
        return super(NewInstallation, self).dispatch(request, *args, **kwargs)

class NewPaperwork(LoginRequiredMixin, CreateView):
    fields = '__all__'
    model  = Paperwork
    template_name = 'projects/paperwork_form.html'

    def form_valid(self, form):
        form.instance.createBy = self.request.user
        return super(NewPaperwork, self).form_valid(form)

    def user_perm_check(self, request):
        if request.user.has_perm('projects.add_paperwork'):
            return True

    def dispatch(self, request, *args, **kwargs):
        if not self.user_perm_check(request):
            raise PermissionDenied
        return super(NewPaperwork, self).dispatch(request, *args, **kwargs)

class ListCustomers(ListView):
    paginate_by = 100
    default_ordering = '-dateCreate'
    template_name = 'projects/customers_list.html'

    def get_queryset(self):
        query    = self.request.GET.get('search')
        order_by = self.request.GET.get('order_by', self.default_ordering)
        qs       = Customer.objects.order_by(order_by)

        if query is not None:
            search_condition = Q(first_name__icontains=query)|Q(last_name__icontains=query)\
                              |Q(phone__icontains=query)|Q(address__icontains=query)\
                              |Q(email__icontains=query)
            return qs.filter(search_condition)
        return qs

    def get_context_data(self, **kwargs):
        context = super(ListCustomers, self).get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        try:
            customer_page = paginator.page(page)
        except PageNotAnInteger:
            customer_page = paginator.page(1)
        except EmptyPage:
            customer_page = paginator.page(paginator.num_pages)
        context['customers_list'] = customer_page
        return context

class ListQuotes(ListView):
    paginate_by = 100
    default_ordering = '-dateQuote'
    template_name = 'projects/quotes_list.html'

    def get_queryset(self):
        query    = self.request.GET.get('search', None)
        order_by = self.request.GET.get('order_by', self.default_ordering)
        qs       = Quote.objects.order_by(order_by)

        if query is not None:
            search_condition = Q(customer__first_name__icontains=query)\
                              |Q(customer__last_name__icontains=query)\
                              |Q(createBy__first_name__icontains=query)\
                              |Q(createBy__last_name__icontains=query)
            return qs.filter(search_condition)
        return qs

    def get_context_data(self, **kwargs):
        context = super(ListQuotes, self).get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        try:
            quote_page = paginator.page(page)
        except PageNotAnInteger:
            quote_page = paginator.page(1)
        except EmptyPage:
            quote_page = paginator.page(paginator.num_pages)
        context['quotes_list'] = quote_page
        return context

class ListApplications(ListView):
    paginate_by = 100
    default_ordering = '-dateApply'
    template_name = 'projects/applications_list.html'

    def get_queryset(self):
        query    = self.request.GET.get('search')
        order_by = self.request.GET.get('order_by', self.default_ordering)
        qs       = Application.objects.order_by(order_by)

        if query is not None:
            search_condition = Q(customer__first_name__icontains=query)\
                              |Q(customer__last_name__icontains=query)\
                              |Q(createBy__first_name__icontains=query)\
                              |Q(createBy__last_name__icontains=query)
            return qs.filter(search_condition)
        return qs

    def get_context_data(self, **kwargs):
        context = super(ListApplications, self).get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        try:
            application_page = paginator.page(page)
        except PageNotAnInteger:
            application_page = paginator.page(1)
        except EmptyPage:
            application_page = paginator.page(paginator.num_pages)
        context['applications_list'] = application_page
        return context

class ListInstallations(ListView):
    paginate_by = 100
    default_ordering = '-dateInstall'
    template_name = 'projects/installations_list.html'

    def get_queryset(self):
        query    = self.request.GET.get('search')
        order_by = self.request.GET.get('order_by', self.default_ordering)
        qs       = Installation.objects.order_by(order_by)

        if query is not None:
            search_condition = Q(customer__first_name__icontains=query)\
                              |Q(customer__last_name__icontains=query)\
                              |Q(createBy__first_name__icontains=query)\
                              |Q(createBy__last_name__icontains=query)\
                              |Q(installer__icontains=query)
            return qs.filter(search_condition)
        return qs

    def get_context_data(self, **kwargs):
        context = super(ListInstallations, self).get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        try:
            installation_page = paginator.page(page)
        except PageNotAnInteger:
            installation_page = paginator.page(1)
        except EmptyPage:
            installation_page = paginator.page(paginator.num_pages)
        context['installations_list'] = installation_page
        return context

class ListPaperworks(ListView):
    paginate_by = 100
    default_ordering = '-datePaper'
    template_name = 'projects/paperworks_list.html'

    def get_queryset(self):
        query    = self.request.GET.get('search')
        order_by = self.request.GET.get('order_by', self.default_ordering)
        qs       = Paperwork.objects.order_by(order_by)

        if query is not None:
            search_condition = Q(customer__first_name__icontains=query)\
                              |Q(customer__last_name__icontains=query)\
                              |Q(createBy__first_name__icontains=query)\
                              |Q(createBy__last_name__icontains=query)
            return qs.filter(search_condition)
        return qs

    def get_context_data(self, **kwargs):
        context = super(ListPaperworks, self).get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        try:
            paperwork_page = paginator.page(page)
        except PageNotAnInteger:
            paperwork_page = paginator.page(1)
        except EmptyPage:
            paperwork_page = paginator.page(paginator.num_pages)
        context['paperworks_list'] = paperwork_page
        return context

class ListProjects(ListView):
    paginate_by = 100
    default_ordering = '-dateQuote'
    template_name = 'projects/projects_list.html'

    def get_queryset(self):
        query      = self.request.GET.get('search')
        order_by   = self.request.GET.get('order_by', self.default_ordering)
        qs         = Quote.objects.annotate(
                        phone       = F('customer__phone'),
                        dateApply   = F('app_for_quote__dateApply'),
                        vicApprove  = F('app_for_quote__vicApprove'),
                        dateInstall = F('app_for_quote__install_for_app__dateInstall'),
                        inspectFile = F('app_for_quote__install_for_app__inspectFile'),
                        installFile = F('app_for_quote__install_for_app__installFile'),
                        installer   = F('app_for_quote__install_for_app__installer'),
                        datePaper   = F('app_for_quote__install_for_app__pw_for_install__datePaper'),
                        ewrFile     = F('app_for_quote__install_for_app__pw_for_install__ewrFile'),
                        pvFile      = F('app_for_quote__install_for_app__pw_for_install__pvFile'),
                        invoiceFile = F('app_for_quote__install_for_app__pw_for_install__invoiceFile')
                     ).order_by(order_by)

        if query is not None:
            search_condition = Q(customer__first_name__icontains=query) \
                              |Q(customer__last_name__icontains=query)\
                              |Q(customer__phone__icontains=query)\
                              |Q(customer__address__icontains=query)\
                              |Q(customer__email__icontains=query)\
                              |Q(app_for_quote__install_for_app__installer__icontains=query)
            return qs.filter(search_condition)
        return qs

    def get_context_data(self, **kwargs):
        context = super(ListProjects, self).get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        try:
            project_page = paginator.page(page)
        except PageNotAnInteger:
            project_page = paginator.page(1)
        except EmptyPage:
            project_page = paginator.page(paginator.num_pages)
        context['projects_list'] = project_page
        return context

class CustomerUpdate(LoginRequiredMixin, UpdateView):
    model = Customer
    fields = ['first_name', 'last_name', 'email', 'phone', 'address']
    template_name_suffix = '_update_form'

    def user_perm_check(self, request):
        if request.user.has_perm('projects.change_customer'):
            return True

    def dispatch(self, request, *args, **kwargs):
        if not self.user_perm_check(request):
            raise PermissionDenied
        return super(CustomerUpdate, self).dispatch(request, *args, **kwargs)

# class QuoteUpdate(LoginRequiredMixin, UpdateView):
#     model = Quote
#     fields = ['dateQuote', 'taxAssess', 'powerBill', 'cncilRate', 'nearMap', 'quoteFile']
#     # form_class = QuoteCreationForm

#     template_name_suffix = '_update_form'

#     def user_perm_check(self, request):
#         if request.user.has_perm('projects.change_quote'):
#             return True

#     def dispatch(self, request, *args, **kwargs):
#         if not self.user_perm_check(request):
#             raise PermissionDenied
#         # user_in_groups = list(request.user.groups.values_list('name', flat=True))
#         # if "Quote Approval" not in user_in_groups:
#         #     self.fields.pop('is_approved')
#         #     self.fields.pop('approved_by')
#         #     self.fields.pop('date_approved')
#         return super(QuoteUpdate, self).dispatch(request, *args, **kwargs)

class QuoteUpdate(LoginRequiredMixin, UpdateView):
    model = Quote
    fields = ['dateQuote', 'taxAssess', 'powerBill',
              'cncilRate', 'nearMap', 'quoteFile']
    # form_class = QuoteCreationForm

    template_name_suffix = '_update_form'

    def user_perm_check(self, request):
        if request.user.has_perm('projects.change_quote'):
            return True

    def dispatch(self, request, *args, **kwargs):
        if not self.user_perm_check(request):
            raise PermissionDenied
        # user_in_groups = list(request.user.groups.values_list('name', flat=True))
        # if "Quote Approval" not in user_in_groups:
        #     self.fields.pop('is_approved')
        #     self.fields.pop('approved_by')
        #     self.fields.pop('date_approved')
        return super(QuoteUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QuoteUpdate, self).get_context_data(**kwargs)
        user_in_groups = list(self.request.user.groups.values_list('name', flat=True))
        if "Quote Approval" in user_in_groups:
            try:
                quoteApproval = Approval.objects.get(customer__exact=self.object.customer)
            except:
                quoteApproval = Approval.objects.create(customer=self.object.customer, quote=self.object)
            context['Approval'] = quoteApproval
        return context

class ApplicationUpdate(LoginRequiredMixin, UpdateView):
    model = Application
    fields = ['dateApply', 'vicApprove']
    template_name_suffix = '_update_form'

    def user_perm_check(self, request):
        if request.user.has_perm('projects.change_application'):
            return True

    def dispatch(self, request, *args, **kwargs):
        if not self.user_perm_check(request):
            raise PermissionDenied
        return super(ApplicationUpdate, self).dispatch(request, *args, **kwargs)

class InstallationUpdate(LoginRequiredMixin, UpdateView):
    model = Installation
    fields = ['installer', 'dateInstall', 'installFile', 'inspectFile']
    template_name_suffix = '_update_form'

    def user_perm_check(self, request):
        if request.user.has_perm('projects.change_installation'):
            return True

    def dispatch(self, request, *args, **kwargs):
        if not self.user_perm_check(request):
            raise PermissionDenied
        return super(InstallationUpdate, self).dispatch(request, *args, **kwargs)

class PaperworkUpdate(LoginRequiredMixin, UpdateView):
    model = Paperwork
    fields = ['datePaper', 'ewrFile', 'pvFile', 'invoiceFile']
    template_name_suffix = '_update_form'

    def user_perm_check(self, request):
        if request.user.has_perm('projects.change_paperwork'):
            return True

    def dispatch(self, request, *args, **kwargs):
        if not self.user_perm_check(request):
            raise PermissionDenied
        return super(PaperworkUpdate, self).dispatch(request, *args, **kwargs)

class CustomerDelete(LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy('projects:customers_list')

    def user_perm_check(self, request):
        if request.user.has_perm('projects.delete_customer'):
            return True

    def dispatch(self, request, *args, **kwargs):
        if not self.user_perm_check(request):
            raise PermissionDenied
        return super(CustomerDelete, self).dispatch(request, *args, **kwargs)

class QuoteDelete(LoginRequiredMixin, DeleteView):
    model = Quote
    success_url = reverse_lazy('projects:quotes_list')

    def user_perm_check(self, request):
        if request.user.has_perm('projects.delete_quote'):
            return True

    def dispatch(self, request, *args, **kwargs):
        if not self.user_perm_check(request):
            raise PermissionDenied
        return super(QuoteDelete, self).dispatch(request, *args, **kwargs)

class ApplicationDelete(LoginRequiredMixin, DeleteView):
    model = Application
    success_url = reverse_lazy('projects:applications_list')

    def user_perm_check(self, request):
        if request.user.has_perm('projects.delete_application'):
            return True

    def dispatch(self, request, *args, **kwargs):
        if not self.user_perm_check(request):
            raise PermissionDenied
        return super(ApplicationDelete, self).dispatch(request, *args, **kwargs)

class InstallationDelete(LoginRequiredMixin, DeleteView):
    model = Installation
    success_url = reverse_lazy('projects:installations_list')

    def user_perm_check(self, request):
        if request.user.has_perm('projects.delete_installation'):
            return True

    def dispatch(self, request, *args, **kwargs):
        if not self.user_perm_check(request):
            raise PermissionDenied
        return super(InstallationDelete, self).dispatch(request, *args, **kwargs)

class PaperworkDelete(LoginRequiredMixin, DeleteView):
    model = Paperwork
    success_url = reverse_lazy('projects:paperworks_list')

    def user_perm_check(self, request):
        if request.user.has_perm('projects.delete_paperwork'):
            return True

    def dispatch(self, request, *args, **kwargs):
        if not self.user_perm_check(request):
            raise PermissionDenied
        return super(PaperworkDelete, self).dispatch(request, *args, **kwargs)
