from django.contrib import admin
from core.models import Location, Meeting, Company, User
from django.contrib.auth.admin import UserAdmin
from django import forms
admin.site.register(Location)
admin.site.register(Meeting)
admin.site.register(Company)

#Form to hash password and add company of custom user model
class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm
    list_display = ("username",)
    ordering = ("username",)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'username', 'company')}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'username', 'is_superuser', 'is_staff', 'is_active', 'company')}
            ),
        )

    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)