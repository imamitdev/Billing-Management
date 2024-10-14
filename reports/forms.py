from django import forms
from django.core.exceptions import ValidationError

class ReportForm(forms.Form):
    start_date = forms.DateField(
        required=True,
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'class': 'form-control datetimepicker', 'placeholder': 'YYYY-MM-DD'})
    )
    end_date = forms.DateField(
        required=True,
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'class': 'form-control datetimepicker', 'placeholder': 'YYYY-MM-DD'})
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and start_date > end_date:
            raise ValidationError("End date should be greater than or equal to start date.")
