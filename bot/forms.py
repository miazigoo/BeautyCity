from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Comment, Employee

CHOICES_MASTERS = []
for maser in Employee.objects.all():
    CHOICES_MASTERS.append((f'{maser.name}', f'{maser.name}'))


class CommentForm(ModelForm):
    # master = forms.ChoiceField(label='Мастер:', choices=CHOICES_MASTERS, widget=forms.Select(
    #     attrs={'class': 'form-select form-select-lg mb-3'}))
    # author = forms.CharField(label='Ваше имя:', max_length=80, empty_value='Ваше имя:',
    #                          widget=forms.TextInput(attrs={"class": "form-control"})
    #                          )
    # text = forms.CharField(label='Комментарий:',
    #                        widget=forms.Textarea(attrs={"class": "form-control"})
    #                        )

    class Meta:
        model = Comment
        fields = ('master', 'author', 'text')
        widgets = {
            'master': forms.Select(attrs={'class': 'form-select form-select-lg mb-3'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),

        }
        labels = {
            'master': _('Мастер:'),
            'author': _('Ваше имя:'),
            'text': _('Комментарий'),
        }
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['rouse'].widget.attrs.update({'class':'form-control'})
    #     self.fields['color'].widget.attrs.update({'type': 'radio'})
    #     self.fields['color'].widget.attrs.update({'name': 'inlineRadioOptions'})
    #     self.fields['color_type'].widget.attrs.update({'type': 'radio'})
    #     self.fields['color_type'].widget.attrs.update({'name':'inlineRadioOptions'})
