"""SolarPanels URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from .views import (NewCustomer,     CustomerUpdate,     CustomerDelete,     ListCustomers,
                    NewQuote,        QuoteUpdate,        QuoteDelete,        ListQuotes,
                    NewApplication,  ApplicationUpdate,  ApplicationDelete,  ListApplications,
                    NewInstallation, InstallationUpdate, InstallationDelete, ListInstallations,
                    NewPaperwork,    PaperworkUpdate,    PaperworkDelete,    ListPaperworks,
                    ListProjects )

app_name = 'projects'

urlpatterns = [
    path('new_customer/', NewCustomer.as_view(), name='new_customer'),
    path('customers_list/', ListCustomers.as_view(), name='customers_list'),
    path('customers_list_update/<int:pk>/', CustomerUpdate.as_view(), name='update_customer'),
    path('customers_list_delete/<int:pk>/', CustomerDelete.as_view(), name='delete_customer'),
    path('new_quote/', NewQuote.as_view(), name='new_quote'),
    path('quotes_list/', ListQuotes.as_view(), name='quotes_list'),
    path('quotes_list_update/<int:pk>/', QuoteUpdate.as_view(), name='update_quote'),
    path('quotes_list_delete/<int:pk>/', QuoteDelete.as_view(), name='delete_quote'),
    path('new_application/', NewApplication.as_view(), name='new_application'),
    path('applications_list/', ListApplications.as_view(), name='applications_list'),
    path('applications_list_update/<int:pk>/', ApplicationUpdate.as_view(), name='update_application'),
    path('applications_list_delete/<int:pk>/', ApplicationDelete.as_view(), name='delete_application'),
    path('new_installation/', NewInstallation.as_view(), name='new_installation'),
    path('installations_list/', ListInstallations.as_view(), name='installations_list'),
    path('installations_list_update/<int:pk>/', InstallationUpdate.as_view(), name='update_installation'),
    path('installations_list_delete/<int:pk>/', InstallationDelete.as_view(), name='delete_installation'),
    path('new_paperwork/', NewPaperwork.as_view(), name='new_paperwork'),
    path('paperworks_list/', ListPaperworks.as_view(), name='paperworks_list'),
    path('paperworks_list_update/<int:pk>/', PaperworkUpdate.as_view(), name='update_paperwork'),
    path('paperworks_list_delete/<int:pk>/', PaperworkDelete.as_view(), name='delete_paperwork'),
    path('projects_list/', ListProjects.as_view(), name='projects_list')
]
