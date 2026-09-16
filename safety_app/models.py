from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    primary_hazards = models.TextField(blank=True, help_text="Comma-separated major hazards")

    def __str__(self):
        return f"{self.name} ({self.code})"


class SafetyTopic(models.Model):
    topic_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=150)
    sop_code = models.CharField(max_length=20)
    sop_name = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="shield")

    def __str__(self):
        return f"{self.sop_code}: {self.title}"


class Employee(models.Model):
    emp_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="employees")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} [{self.emp_id}] - {self.department.name}"

    def get_topic_performance(self):
        """
        Calculates accuracy % and total attempts per topic for this employee.
        """
        answers = AnswerLog.objects.filter(attempt__employee=self)
        perf = {}

        for ans in answers:
            tid = ans.topic_id or "general"
            if tid not in perf:
                perf[tid] = {"total": 0, "correct": 0, "incorrect": 0, "percentage": 0}
            perf[tid]["total"] += 1
            if ans.is_correct:
                perf[tid]["correct"] += 1
            else:
                perf[tid]["incorrect"] += 1

        for tid, data in perf.items():
            if data["total"] > 0:
                data["percentage"] = round((data["correct"] / data["total"]) * 100)

        return perf

    def get_weak_topics(self):
        """
        Returns list of topics where accuracy is below 70% with at least 2 questions answered.
        """
        perf = self.get_topic_performance()
        weak = []
        for tid, data in perf.items():
            if data["total"] >= 2 and data["percentage"] < 70:
                try:
                    topic_obj = SafetyTopic.objects.get(topic_id=tid)
                    title = topic_obj.title
                    sop = topic_obj.sop_code
                except SafetyTopic.DoesNotExist:
                    title = tid.replace("-", " ").title()
                    sop = "TSS"

                weak.append({
                    "topic_id": tid,
                    "title": title,
                    "sop_code": sop,
                    "percentage": data["percentage"],
                    "total": data["total"],
                    "incorrect": data["incorrect"],
                })

        return sorted(weak, key=lambda x: x["percentage"])

    def overall_accuracy(self):
        answers = AnswerLog.objects.filter(attempt__employee=self)
        total = answers.count()
        if total == 0:
            return 0
        correct = answers.filter(is_correct=True).count()
        return round((correct / total) * 100)


class AssessmentAttempt(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attempts")
    topic = models.ForeignKey(SafetyTopic, on_delete=models.SET_NULL, null=True, blank=True)
    topic_title = models.CharField(max_length=150, blank=True)
    difficulty = models.CharField(max_length=50, default="intermediate")
    is_remediation = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=0)
    percentage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee.name} - {self.topic_title or 'Assessment'} ({self.percentage}%)"


class AnswerLog(models.Model):
    attempt = models.ForeignKey(AssessmentAttempt, on_delete=models.CASCADE, related_name="answers")
    topic_id = models.CharField(max_length=50)
    scenario_context = models.TextField(blank=True)
    question_text = models.TextField()
    chosen_option = models.CharField(max_length=10)
    chosen_text = models.TextField()
    correct_option = models.CharField(max_length=10)
    correct_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    explanation = models.TextField()
    consequence = models.TextField()
    sop_reference = models.CharField(max_length=150, blank=True)

    def __str__(self):
        status = "Correct" if self.is_correct else "Violated"
        return f"Q: {self.question_text[:30]}... [{status}]"
