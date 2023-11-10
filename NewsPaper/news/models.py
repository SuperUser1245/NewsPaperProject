from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        postRating = 0
        authorCommentRating = 0

        post_ratings = self.post_set.values('post_rating')
        for post in post_ratings:
            postRating += post['post_rating']

        authorComment_ratings = self.user.comment_set.values('comment_rating')
        for authorComment in authorComment_ratings:
            authorCommentRating += authorComment['comment_rating']

        Post_comment_ratings = self.post_set.aggregate(comment_rating=Sum('comment__comment_rating'))
        PostCommentRating = Post_comment_ratings.get('comment_rating') or 0

        self.author_rating = postRating * 3 + authorCommentRating + PostCommentRating
        self.save()


class Category(models.Model):
    category_name = models.CharField(unique=True, max_length=255)


class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AT'
    CHOICE = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )

    post_time = models.DateTimeField(auto_now_add=True)
    choice = models.CharField(choices=CHOICE,max_length = 3, default=ARTICLE)
    post_title = models.CharField(blank=False, max_length=255)
    post_content = models.TextField()
    post_rating = models.IntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.post_rating = self.post_rating + 1
        self.save()

    def unlike(self):
        self.post_rating = self.post_rating - 1
        self.save()

    def preview(self):
        return self.post_content[0:124] + '...'

    def __str__(self):
        return f'{self.post_title.title()} : {self.post_content[0:20]} : {self.post_time}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating = self.comment_rating + 1
        self.save()

    def unlike(self):
        self.comment_rating = self.comment_rating - 1
        self.save()
