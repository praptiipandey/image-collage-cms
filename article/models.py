from django.db import models

# Create your models here.
class Author(models.Model):
  name = models.CharField(max_length=255)
  email = models.EmailField()

  def __str__(self):
      return self.name

class Article(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    body = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("title", "author")

    def __str__(self):
        return self.title




