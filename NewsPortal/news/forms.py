from django import forms

from .models import Post


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'category',
            'title',
            'text',
            'author',
        ]

        labels = {
            'category': ("Категория"),
            'title': ("Заголовок"),
        }

        # widgets = {  # Не работает! ???
        #     'category': forms.Select(),
        # }
