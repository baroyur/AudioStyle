from django.shortcuts import render

def index(request):
    return render(request, 'labs/index.html')

def lab1(request):
    return render(request, 'labs/lab1.html')

def lab2_form(request):
    result = None
    if request.method == 'POST':
        text = request.POST.get('text_input')
        select = request.POST.get('select_input')
        gender = request.POST.get('gender')
        interests = request.POST.getlist('interest')

        result = {
            'text': text,
            'select': select,
            'gender': gender,
            'interests': interests,
        }

    return render(request, 'labs/lab2_form.html', {'result': result})
