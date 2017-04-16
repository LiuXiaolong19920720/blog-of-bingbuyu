from django import forms
from .models import Post,Comment

class PostFormNew(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(required=False,widget=forms.Textarea)
    category = forms.CharField(max_length=100)
    tags = forms.CharField(max_length=100)
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text','category','tags')
        
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email','content')
        
        
