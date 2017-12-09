from django import forms


class TextForm(forms.Form):

    CALCULATION_CHOICES = (
        ('Частотний словник', 'Частотний словник'),
        ('Варіаційний ряд', 'Варіаційний ряд'),
        ('Статистичні характеристики', 'Статистичні характеристики'),
    )

    text = forms.CharField(widget=forms.Textarea, label='Текст')
    number_of_samples = forms.IntegerField(min_value=2, initial=10,
                                           label='Кількість підвиборок')
    sample_length = forms.IntegerField(min_value=10, initial=100,
                                       label='Розмір підвибірки')
    calculation = forms.ChoiceField(widget=forms.RadioSelect,
                                    choices=CALCULATION_CHOICES,
                                    initial='Частотний словник',
                                    label='Тип обрахунку')
    wordform = forms.CharField(max_length=50, required=False,
                               label='Словоформа')

    def clean(self):
        cleaned_data = super(TextForm, self).clean()
        calculation = cleaned_data.get('calculation')
        wordform = cleaned_data.get('wordform')
        if calculation != 'Частотний словник' and wordform == '':
            raise forms.ValidationError('Для проведення обчислень '
                                        'необхідно заповнити поле '
                                        '"Словоформа".')
        return cleaned_data
