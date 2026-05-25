from django.db import models

class Board(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.title

class Task(models.Model):

    STATUS = (
        ('PENDING', 'Pendente'),
        ('IN_PROGRESS', 'Em Progresso'),
        ('DONE', 'Concluída'),
    )

    PRIORITY = (
        ('LOW', 'Baixa'),
        ('MEDIUM', 'Média'),
        ('HIGH', 'Alta'),
    )

    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS, default='PENDING')
    priority = models.CharField(max_length=10, choices=PRIORITY, default='MEDIUM')
    like_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100, blank=True, default='Anónimo')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comentário de {self.author} em {self.task.title}'
