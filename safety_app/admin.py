from django.contrib import admin
from .models import Department, SafetyTopic, Employee, AssessmentAttempt, AnswerLog


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


@admin.register(SafetyTopic)
class SafetyTopicAdmin(admin.ModelAdmin):
    list_display = ('sop_code', 'title', 'topic_id')
    search_fields = ('title', 'sop_code', 'topic_id')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'emp_id', 'department', 'created_at')
    list_filter = ('department',)
    search_fields = ('name', 'emp_id')


class AnswerLogInLine(admin.TabularInline):
    model = AnswerLog
    extra = 0
    readonly_fields = ('topic_id', 'question_text', 'chosen_option', 'correct_option', 'is_correct', 'sop_reference')


@admin.register(AssessmentAttempt)
class AssessmentAttemptAdmin(admin.ModelAdmin):
    list_display = ('employee', 'topic_title', 'difficulty', 'score', 'percentage', 'is_remediation', 'created_at')
    list_filter = ('difficulty', 'is_remediation', 'created_at')
    search_fields = ('employee__name', 'employee__emp_id', 'topic_title')
    inlines = [AnswerLogInLine]


@admin.register(AnswerLog)
class AnswerLogAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'topic_id', 'chosen_option', 'correct_option', 'is_correct')
    list_filter = ('is_correct', 'topic_id')
