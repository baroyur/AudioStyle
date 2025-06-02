from django.contrib import admin
from .models import Test, Question, AnswerOption, Student, StudentAnswer

# Inline для вариантов ответов
class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 2  # Кол-во пустых форм по умолчанию

# Inline для вопросов
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

# Отображение вопросов с вариантами ответов
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'test']
    inlines = [AnswerOptionInline]

# Отображение тестов с вопросами
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [QuestionInline]

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'group_number', 'created_at']

@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ['student', 'question', 'selected_option']
