from django import forms
from django.contrib.auth import get_user_model

Employee = get_user_model()


class EmployeeCreationForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'is_active', 'is_staff']

    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
