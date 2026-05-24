from django.shortcuts import render, get_object_or_404
from .models import Board, Task


def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})


def board_page(request, id):
    board = get_object_or_404(Board, id=id)
    tasks = Task.objects.filter(board=board)
    return render(request, 'board.html', {'board': board, 'tasks': tasks})


def task_page(request, id):
    task = get_object_or_404(Task, id=id)
    return render(request, 'task.html', {'task': task})