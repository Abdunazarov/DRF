from django.db import models
from user.models import User, Account
        

class BlogPost(models.Model):
    text = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default=None)

    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    not_allowed_for = models.ManyToManyField(Account)



    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return f"{self.text[0:20]} ({str(self.author)})"


class BlogPostComments(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    def __str__(self):
        return str(self.body)[0:20]    



class BlogPostRus(models.Model):
    text = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    image = models.ImageField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'Blog (rus)'
        verbose_name_plural = 'Blogs (rus)'

    def __str__(self):
        return f"{str(self.author)} - {self.text[0:20]}"
    

class BlogNotAllowedTo(models.Model):
    user = models.ManyToManyField(User)
    blog_post = models.ManyToManyField(BlogPost)

    def __str__(self):
        return f" User {self.user.name} is not allowed to see {self.blog_post}"

    


    
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from translate import Translator

@receiver(post_save, sender=BlogPost) # bu nima enandi?
def create_blog_post_rus(sender, instance=None, created=False, **kwargs):
    if created:

        translator = Translator(to_lang='ru')
        translation = translator.translate(instance.text)


        BlogPostRus.objects.create(
            id=instance.id,
            text=translation,
            author=instance.author, 
            image=instance.image
        )