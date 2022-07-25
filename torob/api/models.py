from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100)
    level = models.PositiveSmallIntegerField()
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Category => Id: {self.id}, Title: {self.title}, Level: {self.level}, Parent: {self.parent_id}"