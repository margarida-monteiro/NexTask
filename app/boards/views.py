from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Task, Comment

# 1. Página HOME (Mostra todos os boards)
def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})


# 2. Página BOARD (Mostra o board específico, as suas tarefas + FILTROS e CRIAÇÃO)
def board_page(request, id):
    board = get_object_or_404(Board, id=id)
    tasks = Task.objects.filter(board=board)

    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')

    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        priority = request.POST.get('priority')
        if title:
            Task.objects.create(
                board=board,
                title=title,
                description=description,
                status=status or 'PENDING',
                priority=priority or 'MEDIUM'
            )
            return redirect('board', id=board.id)

    context = {
        'board': board,
        'tasks': tasks,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
    }
    return render(request, 'board.html', context)


# 3. Página TASK (Detalhe da tarefa + EDITAR + COMENTÁRIOS + LIKE)
def task_page(request, id):
    task = get_object_or_404(Task, id=id)
    comments = task.comments.all()
    # Only handle likes and comments on the public task page
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'like':
            task.like_count += 1
            task.save()
            return redirect('task', id=task.id)

        if action == 'comment':
            author = request.POST.get('author', '').strip() or 'Anónimo'
            comment_text = request.POST.get('comment_text', '').strip()
            if comment_text:
                Comment.objects.create(task=task, author=author, text=comment_text)
            return redirect('task', id=task.id)

    return render(request, 'task.html', {'task': task, 'comments': comments})


def task_edit(request, id):
    task = get_object_or_404(Task, id=id)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.status = request.POST.get('status')
        task.priority = request.POST.get('priority')
        task.save()
        return redirect('board', id=task.board.id)

    return render(request, 'task_edit.html', {'task': task})


def task_add(request):
    boards = Board.objects.all()

    if request.method == 'POST':
        board_id = request.POST.get('board')
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        priority = request.POST.get('priority')

        if board_id and title:
            board = get_object_or_404(Board, id=board_id)
            task = Task.objects.create(
                board=board,
                title=title,
                description=description,
                status=status or 'PENDING',
                priority=priority or 'MEDIUM'
            )
            return redirect('task_list')

    return render(request, 'task_add.html', {'boards': boards})


def task_list(request):
    tasks = Task.objects.select_related('board').all()
    boards = Board.objects.all()

    board_filter = request.GET.get('board')
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')

    if board_filter:
        tasks = tasks.filter(board_id=board_filter)
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)

    context = {
        'tasks': tasks,
        'boards': boards,
        'board_filter': board_filter,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
    }
    return render(request, 'task_list.html', context)


# Função Extra: APAGAR TAREFA (Requisito obrigatório do CRUD)
def task_delete(request, id):
    task = get_object_or_404(Task, id=id)
    board_id = task.board.id
    task.delete()
    return redirect('board', id=board_id)
