from django import forms
from .models import Quote, Approval

class QuoteCreationForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user')
    #     super(QuoteCreationForm, self).__init__(*args, **kwargs)

    #     user_in_groups = list(user.groups.values_list('name', flat=True))

    #     if "Quote Approval" not in user_in_groups:
    #         self.fields.pop("is_approved")
    #         self.fields.pop("approved_by")
    #         # self.fields.pop("date_approved")

    class Meta:
        model  = Quote
        fields = '__all__'

class ApprovalCreationForm(forms.ModelForm):
    class Meta:
        model  = Approval
        fields = '__all__'