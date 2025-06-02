from django.shortcuts import render, redirect, get_object_or_404
from .models import Test, Question, AnswerOption, Student, StudentAnswer
from .forms import StudentForm
from django.contrib.auth.decorators import user_passes_test

def start_test(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            return redirect('lab6:question', student_id=student.id, question_number=1)
    else:
        form = StudentForm()
    return render(request, 'lab6/start.html', {'form': form})

def question_view(request, student_id, question_number):
    student = get_object_or_404(Student, id=student_id)
    questions = list(Question.objects.all())

    if question_number > len(questions):
        return redirect('lab6:results', student_id=student.id)

    question = questions[question_number - 1]
    if request.method == 'POST':
        option_id = request.POST.get('option')
        if option_id:
            option = get_object_or_404(AnswerOption, id=option_id)
            StudentAnswer.objects.create(student=student, question=question, selected_option=option)
            return redirect('lab6:question', student_id=student.id, question_number=question_number + 1)

    return render(request, 'lab6/question.html', {
        'question': question,
        'student': student,
        'question_number': question_number,
        'total': len(questions)
    })

def result_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    answers = StudentAnswer.objects.filter(student=student)
    wrong_answers = []
    correct_count = 0

    for answer in answers:
        if answer.selected_option.is_correct:
            correct_count += 1
        else:
            correct_option = answer.question.options.filter(is_correct=True).first()
            wrong_answers.append({
                'question': answer.question.text,
                'your_answer': answer.selected_option.text,
                'correct_answer': correct_option.text if correct_option else 'Нет данных'
            })

    return render(request, 'lab6/result.html', {
        'student': student,
        'score': correct_count,
        'total': answers.count(),
        'wrong_answers': wrong_answers
    })