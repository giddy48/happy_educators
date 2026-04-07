from django.shortcuts import redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer, PageBreak
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from .models import (
    Student, Teacher, SchoolClass,
    Subject, Mark, AcademicTerm
)

# ---------------------------------------------------
# SCHOOL INFO
# ---------------------------------------------------
SCHOOL_NAME = "A.I.C KAKUYUNI SENIOR SCHOOL"
SCHOOL_MOTTO = "Education Enables"


# ---------------------------------------------------
# HELPERS
# ---------------------------------------------------
def get_grade(avg):
    if avg >= 70:
        return "A"
    elif avg >= 60:
        return "B"
    elif avg >= 50:
        return "C"
    elif avg >= 40:
        return "D"
    else:
        return "E"


# ---------------------------------------------------
# AUTH
# ---------------------------------------------------
def home(request):
    return redirect("dashboard" if request.user.is_authenticated else "login")


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")

    return render(request, "academics/login.html")
# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------
@login_required
def dashboard_home(request):
    students = Student.objects.all()
    marks = Mark.objects.all()

    student_scores = []
    for s in students:
        total = sum(m.score for m in Mark.objects.filter(student=s))
        student_scores.append({"student": s, "total": total})

    top_student = None
    if student_scores:
        student_scores.sort(key=lambda x: x["total"], reverse=True)
        top_student = student_scores[0]

    return render(request, "academics/dashboard.html", {
        "total_students": students.count(),
        "total_marks": marks.count(),
        "total_classes": SchoolClass.objects.count(),
        "top_student": top_student,
    })


# ---------------------------------------------------
# STUDENTS
# ---------------------------------------------------
@login_required
def students_view(request):
    return render(request, "academics/students.html", {
        "students": Student.objects.all()
    })


@login_required
def student_detail(request, id):
    student = get_object_or_404(Student, id=id)
    marks = Mark.objects.filter(student=student)

    return render(request, "academics/student_detail.html", {
        "student": student,
        "marks": marks
    })


# ---------------------------------------------------
# RESULTS (FINAL CLEAN VERSION)
# ---------------------------------------------------
def results(request):
    classes = SchoolClass.objects.all()
    terms = AcademicTerm.objects.all()

    class_id = request.GET.get("class_id")
    term_id = request.GET.get("term_id")

    selected_class = None
    selected_term = None
    report_data = []

    if class_id and term_id:
        selected_class = SchoolClass.objects.get(id=class_id)
        selected_term = AcademicTerm.objects.get(id=term_id)

        students = Student.objects.all()

        for student in students:
            marks = Mark.objects.filter(
                student=student,
                school_class=selected_class,
                term=selected_term
            )

            subject_results = []
            total = 0
            count = 0

            for mark in marks:
                total += mark.score
                count += 1

                subject_results.append({
                    "subject": mark.subject.name,
                    "score": mark.score,
                    "grade": get_grade(mark.score)
                })

            average = total / count if count > 0 else 0

            report_data.append({
                "student": student,
                "subjects": subject_results,
                "total": total,
                "average": round(average, 2),
                "grade": get_grade(average)
            })

        report_data.sort(key=lambda x: x["average"], reverse=True)

        for i, item in enumerate(report_data, start=1):
            item["rank"] = i

    return render(request, "academics/report_card.html", {
        "classes": classes,
        "terms": terms,
        "selected_class": selected_class,
        "selected_term": selected_term,
        "report_data": report_data
    })


# ---------------------------------------------------
# ENTER MARKS
# ---------------------------------------------------
@login_required
def enter_marks(request):
    classes = SchoolClass.objects.all()
    subjects = Subject.objects.all()
    students = Student.objects.all()

    if request.method == "POST":
        class_id = request.POST.get("class_id")
        subject_id = request.POST.get("subject_id")

        selected_class = SchoolClass.objects.get(id=class_id)
        selected_subject = Subject.objects.get(id=subject_id)

        for student in students:
            mark_value = request.POST.get(f"mark_{student.id}")

            if mark_value:
                Mark.objects.update_or_create(
                    student=student,
                    subject=selected_subject,
                    school_class=selected_class,
                    defaults={"score": mark_value}
                )

        return redirect("results")

    return render(request, "academics/enter_marks.html", {
        "classes": classes,
        "subjects": subjects,
        "students": students,
    })


# ---------------------------------------------------
# API
# ---------------------------------------------------
def get_students(request):
    return JsonResponse({
        "students": [{"id": s.id, "name": s.name} for s in Student.objects.all()]
    })


# ---------------------------------------------------
# CLASS DASHBOARD
# ---------------------------------------------------
@login_required
def class_dashboard(request, class_id):
    school_class = SchoolClass.objects.get(id=class_id)
    students = Student.objects.filter(school_class=school_class)

    data = []

    for s in students:
        marks = Mark.objects.filter(student=s)
        total = sum(m.score for m in marks)
        avg = total / marks.count() if marks.exists() else 0

        data.append({
            "student": s,
            "total": total,
            "average": avg
        })

    data.sort(key=lambda x: x["average"], reverse=True)

    for i, item in enumerate(data, start=1):
        item["rank"] = i

    return render(request, "academics/class_dashboard.html", {
        "class": school_class,
        "data": data
    })


# ---------------------------------------------------
# STUDENT REPORT
# ---------------------------------------------------
@login_required
def student_report(request, id):
    student = get_object_or_404(Student, id=id)
    marks = Mark.objects.filter(student=student)

    total = sum(m.score for m in marks)
    avg = total / marks.count() if marks.exists() else 0

    return render(request, "academics/student_report.html", {
        "student": student,
        "marks": marks,
        "total": total,
        "average": round(avg, 2),
    })


# ---------------------------------------------------
# TEACHER DASHBOARD
# ---------------------------------------------------
@login_required
def teacher_dashboard(request):
    if not hasattr(request.user, "teacher"):
        return HttpResponse("Unauthorized")

    teacher = request.user.teacher
    marks = Mark.objects.filter(teacher=teacher)

    return render(request, "academics/teacher_dashboard.html", {
        "teacher": teacher,
        "marks": marks,
    })


# ---------------------------------------------------
# CLASS LIST
# ---------------------------------------------------
@login_required
def class_list(request):
    return render(request, "academics/class_list.html", {
        "classes": SchoolClass.objects.all()
    })


# ---------------------------------------------------
# BULK PDF REPORT CARDS
# ---------------------------------------------------
def bulk_report_card_pdf(request, class_id):
    school_class = SchoolClass.objects.get(id=class_id)
    students = Student.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{school_class.name}_bulk_report_cards.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"{school_class.name} - BULK REPORT CARDS", styles['Title']))
    elements.append(Spacer(1, 12))

    for student in students:
        marks = Mark.objects.filter(student=student, school_class=school_class)

        if not marks.exists():
            continue

        total = sum(m.score for m in marks)
        count = marks.count()
        average = total / count if count > 0 else 0

        elements.append(Paragraph(f"Student: {student.name}", styles['Heading2']))
        elements.append(Paragraph(
            f"Total: {total} | Average: {round(average,2)} | Grade: {get_grade(average)}",
            styles['Normal']
        ))
        elements.append(Spacer(1, 8))

        data = [["Subject", "Score", "Grade"]]

        for m in marks:
            data.append([
                m.subject.name,
                m.score,
                get_grade(m.score)
            ])

        data.append(["TOTAL", total, ""])
        data.append(["AVERAGE", round(average, 2), get_grade(average)])

        table = Table(data)

        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ]))

        elements.append(table)
        elements.append(PageBreak())

    doc.build(elements)
    return response
def report_card_pdf(request, class_id, student_id):
    student = Student.objects.get(id=student_id)
    school_class = SchoolClass.objects.get(id=class_id)

    marks = Mark.objects.filter(
        student=student,
        school_class=school_class
    )

    total = sum(m.score for m in marks)
    count = marks.count()
    average = total / count if count > 0 else 0

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.name}_report_card.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()
    elements = []

    # TITLE
    elements.append(Paragraph("STUDENT REPORT CARD", styles['Title']))
    elements.append(Spacer(1, 12))

    # INFO
    elements.append(Paragraph(f"Student: {student.name}", styles['Normal']))
    elements.append(Paragraph(f"Class: {school_class.name}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # TABLE
    data = [["Subject", "Score", "Grade"]]

    for m in marks:
        data.append([m.subject.name, m.score, get_grade(m.score)])

    data.append(["TOTAL", total, ""])
    data.append(["AVERAGE", round(average, 2), get_grade(average)])

    table = Table(data)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
    ]))

    elements.append(table)

    doc.build(elements)
    return response
def bulk_report_card_pdf(request, class_id):
    school_class = SchoolClass.objects.get(id=class_id)
    students = Student.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{school_class.name}_bulk_report_cards.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"{school_class.name} - BULK REPORT CARDS", styles['Title']))
    elements.append(Spacer(1, 12))

    for student in students:
        marks = Mark.objects.filter(student=student, school_class=school_class)

        if not marks.exists():
            continue

        total = sum(m.score for m in marks)
        count = marks.count()
        average = total / count if count > 0 else 0

        elements.append(Paragraph(f"Student: {student.name}", styles['Heading2']))
        elements.append(Paragraph(
            f"Total: {total} | Average: {round(average,2)} | Grade: {get_grade(average)}",
            styles['Normal']
        ))
        elements.append(Spacer(1, 8))

        data = [["Subject", "Score", "Grade"]]

        for m in marks:
            data.append([m.subject.name, m.score, get_grade(m.score)])

        data.append(["TOTAL", total, ""])
        data.append(["AVERAGE", round(average, 2), get_grade(average)])

        table = Table(data)

        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ]))

        elements.append(table)
        elements.append(PageBreak())

    doc.build(elements)
    return response
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect("login")