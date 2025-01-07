# example/views.py
from datetime import datetime
from django.shortcuts import render

def index(request):
    now = datetime.now()
    context = {'now': now}
    return render(request, 'index.html', context)
