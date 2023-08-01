from django import forms


class PostForm(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=255
    )
    body = forms.CharField(
        label="Body",
        max_length=1000,
        widget=forms.Textarea(attrs={'rows': 3})
    )
