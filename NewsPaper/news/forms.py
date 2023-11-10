from django import forms
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_title', 'post_content', 'author', 'categories']


class CustomSignupForm(SignupForm):

    def save(self, request):
        user = super().save(request)

        common_users = Group.objects.get(name="common users")
        user.groups.add(common_users)

        subject = 'Welcome!'
        text = f'{user.username}, you have successfully registered!'
        html = (
            f'<b>{user.username}</b>, you have successfully registered!'
            f'<a href="http://127.0.0.1:8000/posts">site</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

        return user





