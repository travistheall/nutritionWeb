from django.forms import ModelForm
from customProfile.models import CustomUser, UserConsumedFood
from django import forms


class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        widgets = {'user': forms.HiddenInput()}
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CustomConsumptionForm(ModelForm):
    class Meta:
        model = UserConsumedFood
        fields = "__all__"
        widgets = {'user': forms.HiddenInput(),
                   'day': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(CustomConsumptionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
