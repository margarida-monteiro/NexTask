from django.db import models

class Board(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Task(models.Model):

    STATUS = (
        ('to-do', 'To Do'),
        ('doing', 'Doing'),
        ('done', 'Done')
    )

    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default='to-do')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title