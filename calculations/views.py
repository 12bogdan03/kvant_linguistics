import string

from django.views import generic
from django.shortcuts import render

from .forms import TextForm
from .utils import generate_variation_series,\
                   generate_characteristics_dict,\
                   generate_frequency_dictionary


class IndexView(generic.View):

    form_class = TextForm
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name,
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            text = form.cleaned_data['text']
            words = [word.strip(string.punctuation) for word in text.split()
                     if word not in [string.punctuation, '', '—', '\n', '\t']]

            if form.cleaned_data['calculation'] == 'Частотний словник':
                frequency_dict = generate_frequency_dictionary(words)
                context = {'frequency_dict': frequency_dict,
                           'text_length': len(words)}

            elif form.cleaned_data['calculation'] == 'Варіаційний ряд':
                word = form.cleaned_data['wordform']
                number_of_samples = form.cleaned_data['number_of_samples']
                sample_length = form.cleaned_data['sample_length']
                series_dict = dict(generate_variation_series(word,
                                                             words,
                                                             number_of_samples,
                                                             sample_length))
                context = {'word': word,
                           'series_dict': series_dict}

            elif form.cleaned_data['calculation'] == 'Статистичні характеристики':
                word = form.cleaned_data['wordform']
                number_of_samples = form.cleaned_data['number_of_samples']
                sample_length = form.cleaned_data['sample_length']
                characteristics_dict = generate_characteristics_dict(word,
                                                                     words,
                                                                     number_of_samples,
                                                                     sample_length)
                context = {'word': word,
                           'characteristics_dict': characteristics_dict}

            return render(request, 'calculations.html', context)

        return render(request, self.template_name, {'form': form})
