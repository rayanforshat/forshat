import re
from django import forms
from .models import TreatmentRequest


class TreatmentRequestForm(forms.ModelForm):
    privacy_policy = forms.BooleanField(
        required=True,
        label='',
        error_messages={'required': 'يجب الموافقة على سياسة الخصوصية وسياسة المبادرة للمتابعة'}
    )

    class Meta:
        model = TreatmentRequest
        fields = [
            'full_name', 'phone', 'id_number',
            'birth_date', 'nationality', 'city',
            'service_type', 'notes',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'مثال: محمد أحمد العمري',
                'class': 'form-input',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '5XXXXXXXX',
                'maxlength': '9',
                'class': 'form-input',
            }),
            'id_number': forms.TextInput(attrs={
                'placeholder': 'رقم الهوية الوطنية أو الإقامة',
                'class': 'form-input',
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input',
            }),
            'nationality': forms.TextInput(attrs={
                'placeholder': 'مثال: سعودي، مصري ...',
                'class': 'form-input',
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'مثال: الرياض، جدة ...',
                'class': 'form-input',
            }),
            'service_type': forms.Select(attrs={
                'class': 'form-input form-select',
            }),
            'notes': forms.Textarea(attrs={
                'placeholder': 'أي تفاصيل إضافية تود إضافتها ...',
                'rows': 4,
                'class': 'form-input form-textarea',
            }),
        }
        labels = {
            'full_name': 'الاسم بالكامل',
            'phone': 'رقم الجوال',
            'id_number': 'رقم الإثبات',
            'birth_date': 'تاريخ الميلاد',
            'nationality': 'الجنسية',
            'city': 'المدينة',
            'service_type': 'نوع الخدمة المطلوبة',
            'notes': 'ملاحظات إضافية',
        }
        error_messages = {
            'full_name': {'required': 'الاسم بالكامل مطلوب'},
            'phone': {'required': 'رقم الجوال مطلوب'},
            'id_number': {'required': 'رقم الإثبات مطلوب'},
            'birth_date': {'required': 'تاريخ الميلاد مطلوب'},
            'nationality': {'required': 'الجنسية مطلوبة'},
            'city': {'required': 'المدينة مطلوبة'},
            'service_type': {'required': 'نوع الخدمة مطلوب'},
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        # Remove leading 0 if user added it
        if phone.startswith('0'):
            phone = phone[1:]
        pattern = re.compile(r'^5\d{8}$')
        if not pattern.match(phone):
            raise forms.ValidationError(
                'رقم الجوال يجب أن يبدأ بالرقم 5 ويتكون من 9 أرقام (مثال: 5XXXXXXXX)'
            )
        return phone
