import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Department, SafetyTopic, Employee, AssessmentAttempt, AnswerLog
from .ai_generator import generate_questions


def get_current_employee(request):
    emp_id = request.session.get("employee_id")
    if emp_id:
        try:
            return Employee.objects.get(emp_id=emp_id)
        except Employee.DoesNotExist:
            return None
    return None


def login_view(request):
    employee = get_current_employee(request)
    if employee:
        return redirect("training_hub")

    error = None
    emp_id = ""

    if request.method == "POST":
        emp_id = request.POST.get("emp_id", "").strip()

        if not emp_id:
            error = "Please enter your Employee ID."
        else:
            employee = Employee.objects.filter(emp_id__iexact=emp_id).first()
            if employee:
                request.session["employee_id"] = employee.emp_id
                return redirect("training_hub")
            else:
                error = f"Employee ID '{emp_id}' not found. Please sign up first to create your account."

    departments = Department.objects.all()
    return render(request, "safety_app/login.html", {
        "departments": departments,
        "active_tab": "login",
        "error": error,
        "emp_id": emp_id,
    })


def signup_view(request):
    employee = get_current_employee(request)
    if employee:
        return redirect("training_hub")

    error = None
    name = ""
    emp_id = ""
    department_id = None

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        emp_id = request.POST.get("emp_id", "").strip()
        department_id = request.POST.get("department_id")

        if not name:
            error = "Please enter your Full Name."
        elif not emp_id:
            error = "Please enter an Employee ID."
        elif not department_id:
            error = "Please select your plant department."
        else:
            if Employee.objects.filter(emp_id__iexact=emp_id).exists():
                error = f"Employee ID '{emp_id}' is already registered. Please switch to Log In."
            else:
                department = get_object_or_404(Department, id=department_id)
                employee = Employee.objects.create(
                    emp_id=emp_id,
                    name=name,
                    department=department
                )
                request.session["employee_id"] = employee.emp_id
                return redirect("training_hub")

    departments = Department.objects.all()
    return render(request, "safety_app/login.html", {
        "departments": departments,
        "active_tab": "signup",
        "error": error,
        "name": name,
        "emp_id": emp_id,
        "selected_dept": int(department_id) if department_id and str(department_id).isdigit() else None,
    })


def logout_view(request):
    request.session.flush()
    return redirect("login")


def training_hub(request):
    employee = get_current_employee(request)
    if not employee:
        return redirect("login")

    topics = SafetyTopic.objects.all()
    topic_perf = employee.get_topic_performance()
    weak_topics = employee.get_weak_topics()

    # Enhance topic objects with stats
    topic_list = []
    for t in topics:
        perf = topic_perf.get(t.topic_id, {"total": 0, "correct": 0, "percentage": 0})
        is_weak = perf["total"] >= 2 and perf["percentage"] < 70
        is_mastered = perf["percentage"] >= 80
        topic_list.append({
            "topic": t,
            "perf": perf,
            "is_weak": is_weak,
            "is_mastered": is_mastered
        })

    api_key = request.session.get("gemini_api_key", "")

    return render(request, "safety_app/training_hub.html", {
        "employee": employee,
        "topic_list": topic_list,
        "weak_topics": weak_topics,
        "api_key": api_key,
    })


def start_assessment(request):
    employee = get_current_employee(request)
    if not employee:
        return redirect("login")

    if request.method == "POST":
        topic_id = request.POST.get("topic_id", "all")
        difficulty = request.POST.get("difficulty", "intermediate")
        count = int(request.POST.get("count", 5))

        api_key = request.session.get("gemini_api_key", "")
        questions = generate_questions(
            topic_id=topic_id,
            department_name=employee.department.name,
            difficulty=difficulty,
            count=count,
            api_key=api_key
        )

        request.session["current_assessment"] = {
            "topic_id": topic_id,
            "difficulty": difficulty,
            "is_remediation": False,
            "questions": questions,
        }

        return redirect("take_assessment")

    return redirect("training_hub")


def retest_weak_areas(request):
    employee = get_current_employee(request)
    if not employee:
        return redirect("login")

    weak_topics = employee.get_weak_topics()
    weak_ids = [w["topic_id"] for w in weak_topics]

    if not weak_ids:
        weak_ids = ["ppe"]

    api_key = request.session.get("gemini_api_key", "")
    questions = generate_questions(
        topic_id="all",
        department_name=employee.department.name,
        difficulty="intermediate",
        count=5,
        is_remediation=True,
        weak_topic_ids=weak_ids,
        api_key=api_key
    )

    request.session["current_assessment"] = {
        "topic_id": "weak-areas",
        "difficulty": "intermediate",
        "is_remediation": True,
        "questions": questions,
    }

    return redirect("take_assessment")


def take_assessment(request):
    employee = get_current_employee(request)
    if not employee:
        return redirect("login")

    assessment_data = request.session.get("current_assessment")
    if not assessment_data or not assessment_data.get("questions"):
        return redirect("training_hub")

    return render(request, "safety_app/assessment.html", {
        "employee": employee,
        "assessment": assessment_data,
        "questions_json": json.dumps(assessment_data["questions"]),
    })


@require_POST
def submit_assessment(request):
    employee = get_current_employee(request)
    if not employee:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    try:
        data = json.loads(request.body)
        answers = data.get("answers", [])
        topic_id = data.get("topic_id", "general")
        difficulty = data.get("difficulty", "intermediate")
        is_remediation = data.get("is_remediation", False)

        topic_obj = SafetyTopic.objects.filter(topic_id=topic_id).first()
        topic_title = topic_obj.title if topic_obj else ("Targeted AI Remediation" if is_remediation else "Safety Assessment")

        total_questions = len(answers)
        correct_count = sum(1 for a in answers if a.get("is_correct"))
        score = correct_count * 10
        max_score = total_questions * 10
        percentage = round((score / max_score) * 100) if max_score > 0 else 0

        attempt = AssessmentAttempt.objects.create(
            employee=employee,
            topic=topic_obj,
            topic_title=topic_title,
            difficulty=difficulty,
            is_remediation=is_remediation,
            score=score,
            max_score=max_score,
            percentage=percentage
        )

        for ans in answers:
            AnswerLog.objects.create(
                attempt=attempt,
                topic_id=ans.get("topic_id") or topic_id,
                scenario_context=ans.get("scenario_context", ""),
                question_text=ans.get("question", ""),
                chosen_option=ans.get("chosen_option_id", ""),
                chosen_text=ans.get("chosen_text", ""),
                correct_option=ans.get("correct_option_id", ""),
                correct_text=ans.get("correct_text", ""),
                is_correct=ans.get("is_correct", False),
                explanation=ans.get("explanation", ""),
                consequence=ans.get("consequence", ""),
                sop_reference=ans.get("sop_reference", "")
            )

        # Clear active quiz from session
        if "current_assessment" in request.session:
            del request.session["current_assessment"]

        return JsonResponse({"redirect_url": f"/results/{attempt.id}/"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def results_view(request, attempt_id):
    employee = get_current_employee(request)
    if not employee:
        return redirect("login")

    attempt = get_object_or_404(AssessmentAttempt, id=attempt_id, employee=employee)
    answers = attempt.answers.all()

    incorrect_answers = answers.filter(is_correct=False)
    is_passed = attempt.percentage >= 80

    # Identified weak topics for this user
    weak_topics = employee.get_weak_topics()

    return render(request, "safety_app/results.html", {
        "employee": employee,
        "attempt": attempt,
        "answers": answers,
        "incorrect_count": incorrect_answers.count(),
        "is_passed": is_passed,
        "weak_topics": weak_topics,
    })


def dashboard_view(request):
    employee = get_current_employee(request)
    if not employee:
        return redirect("login")

    topics = SafetyTopic.objects.all()
    topic_perf = employee.get_topic_performance()
    weak_topics = employee.get_weak_topics()
    attempts = employee.attempts.all()[:10]

    topic_metrics = []
    for t in topics:
        perf = topic_perf.get(t.topic_id, {"total": 0, "correct": 0, "percentage": 0})
        is_weak = perf["total"] >= 2 and perf["percentage"] < 70
        is_mastered = perf["percentage"] >= 80
        topic_metrics.append({
            "topic": t,
            "perf": perf,
            "is_weak": is_weak,
            "is_mastered": is_mastered
        })

    return render(request, "safety_app/dashboard.html", {
        "employee": employee,
        "topic_metrics": topic_metrics,
        "weak_topics": weak_topics,
        "attempts": attempts,
        "overall_accuracy": employee.overall_accuracy(),
        "total_attempts": employee.attempts.count(),
    })


@require_POST
def set_api_key(request):
    key = request.POST.get("api_key", "").strip()
    if key:
        request.session["gemini_api_key"] = key
    else:
        if "gemini_api_key" in request.session:
            del request.session["gemini_api_key"]
    return redirect(request.META.get("HTTP_REFERER", "training_hub"))
