from django import forms

class NewTopicForm(forms.Form):
    subject = forms.CharField(max_length=256)
    body = forms.CharField(max_length=16384)

class NewPostForm(forms.Form):
    body = forms.CharField(max_length=16384)

class DeleteTopicForm(forms.Form):
    confirmation = forms.BooleanField()

class DeletePostForm(forms.Form):
    confirmation = forms.BooleanField()
