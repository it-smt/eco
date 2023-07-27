from django import forms

from .models import Message


class AddMessageForm(forms.ModelForm):
	type = forms.ChoiceField(label='Тип', choices=Message.Type.choices, widget=forms.Select(attrs={
		'class': 'form-control'
	}))
	weight = forms.FloatField(label='Вес (в кг)', widget=forms.NumberInput(attrs={
		'class': 'form-control'
	}))
	address = forms.CharField(label='Адрес', widget=forms.TextInput(attrs={
		'class': 'form-control address',
		'autocomplete': 'off'
	}))
	time_s = forms.TimeField(label='Присутствую с', widget=forms.TimeInput(attrs={
		'class': 'form-control',
		'type': 'time',
		'type': 'time'
	}))
	time_b = forms.TimeField(label='До', widget=forms.TimeInput(attrs={
		'class': 'form-control',
		'type': 'time',
		'type': 'time'
	}))

	class Meta:
		model = Message
		fields = ('address', 'type', 'weight', 'time_s', 'time_b')