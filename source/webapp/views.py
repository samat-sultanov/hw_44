from django.shortcuts import render


def game_page(request):
    if request.method == 'GET':
        return render(request, 'input_form.html')
