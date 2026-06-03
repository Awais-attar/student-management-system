import os

from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from flask_mail import Mail, Message
import random

from config import Config

from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle
)

from flask import send_file

from reportlab.lib import colors
app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = "student_secret_key"

app.config.from_object(Config)

db = SQLAlchemy(app)

# ==================================
# MAIL CONFIG
# ==================================

app.config['MAIL_SERVER'] = 'smtp.gmail.com'

app.config['MAIL_PORT'] = 587

app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = 'YOUR_GMAIL@gmail.com'

app.config['MAIL_PASSWORD'] = 'YOUR_16_DIGIT_APP_PASSWORD'

mail = Mail(app)


# ==================================
# Teacher Table
# ==================================

# ==================================
# Teacher Table
# ==================================

class Teacher(db.Model):

    __tablename__ = 'teachers'

    teacher_id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    subject = db.Column(
        db.String(100)
    )

    phone = db.Column(
        db.String(15)
    )

    teacher_image = db.Column(
        db.String(200)
    )

    teacher_code = db.Column(
        db.String(20)
    )

    role = db.Column(
        db.String(20),
        default='teacher'
    )

    # =========================
    # NEW COLUMNS
    # =========================

    last_login = db.Column(
        db.String(100)
    )

    last_action = db.Column(
        db.String(100)
    )

    is_online = db.Column(
        db.Boolean,
        default=False
    )

    status = db.Column(
        db.String(20),
        default="Active"
    )

# ==================================
# Student Table
# ==================================

class Student(db.Model):

    __tablename__ = 'students'

    student_id = db.Column(
        db.Integer,
        primary_key=True
    )

    roll_no = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )
    unique_student_id = db.Column(
    db.String(20),
    unique=True
)
    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    age = db.Column(
        db.Integer
    )

    gender = db.Column(
        db.String(20)
    )

    student_class = db.Column(
        db.String(50)
    )
    
    parent_phone = db.Column(
        db.String(15)
    )
    student_image = db.Column(
    db.String(200)
)
# ==================================
# Attendance Table
# ==================================

class Attendance(db.Model):

    __tablename__ = 'attendance'

    attendance_id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(

    db.Integer,

    db.ForeignKey(
        'students.student_id'
    )
)

    student_name = db.Column(
        db.String(100),
        nullable=False
    )

    attendance_date = db.Column(
        db.String(50)
    )

    status = db.Column(
        db.String(20)
    )
    teacher_name = db.Column(
    db.String(100)
)


# ==================================
# Class Table
# ==================================

class ClassRoom(db.Model):

    __tablename__ = 'classes'

    class_id = db.Column(
        db.Integer,
        primary_key=True
    )

    class_name = db.Column(
        db.String(50),
        nullable=False
    )

    class_teacher = db.Column(
        db.String(100)
    )

    total_students = db.Column(
        db.Integer
    )

# ==================================
# Subject Table
# ==================================

class Subject(db.Model):

    __tablename__ = 'subjects'

    subject_id = db.Column(
        db.Integer,
        primary_key=True
    )

    subject_name = db.Column(
        db.String(100),
        nullable=False
    )

    class_name = db.Column(
        db.String(50)
    )

    subject_teacher = db.Column(
        db.String(100)
    )

# ==================================
# Timetable Table
# ==================================

class Timetable(db.Model):

    __tablename__ = 'timetable'

    timetable_id = db.Column(
        db.Integer,
        primary_key=True
    )

    class_name = db.Column(
        db.String(50)
    )

    subject_name = db.Column(
        db.String(100)
    )

    teacher_name = db.Column(
        db.String(100)
    )

    period_number = db.Column(
        db.Integer
    )

    period_time = db.Column(
        db.String(50)
    )


# ==================================
# Exam Table
# ==================================
# ==================================

# EXAM TABLE

# ==================================

class Exam(db.Model):
    __tablename__ = 'exams'

    exam_id = db.Column(
    db.Integer,
    primary_key=True
)
    student_id = db.Column(
    db.Integer,
    db.ForeignKey(
        'students.student_id'
    )
)
    student_name = db.Column(
    db.String(100)
)


    subject_name = db.Column(
    db.String(100)
)

    marks = db.Column(
    db.Integer
)

    total_marks = db.Column(
    db.Integer
)

    result = db.Column(
    db.String(20)
)

    # ==================================
# Fees Table
# ==================================

class Fees(db.Model):

    __tablename__ = 'fees'

    fee_id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(

        db.Integer,

        db.ForeignKey(
            'students.student_id'
        )
    )

    student_name = db.Column(
        db.String(100)
    )

    class_name = db.Column(
        db.String(50)
    )

    total_fee = db.Column(
        db.Integer
    )

    paid_fee = db.Column(
        db.Integer
    )

    pending_fee = db.Column(
        db.Integer
    )

    status = db.Column(
        db.String(20)
    )

    student = db.relationship(

        'Student',

        backref='fees'
    )
# ==================================
# LOGIN
# ==================================

@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        teacher = Teacher.query.filter_by(
            email=email
        ).first()

        # CHECK LOGIN

        if teacher and check_password_hash(
            teacher.password,
            password
        ):

            # SESSION

            session['teacher_name'] = teacher.full_name
            session['teacher_image'] = teacher.teacher_image
            session['teacher_code'] = teacher.teacher_code
            session['role'] = teacher.role

            # UPDATE ACTIVITY

            teacher.last_login = str(
                datetime.now()
            )

            teacher.last_action = "Logged In"

            teacher.is_online = True

            db.session.commit()

            # ADMIN LOGIN

            if teacher.role == 'admin':

                return redirect(
                    url_for('admin_dashboard')
                )

            # TEACHER LOGIN

            else:

                return redirect(
                    url_for('dashboard')
                )

        else:

            return "Invalid Email or Password"

    return render_template(
        'login.html'
    )


# ==================================
# REGISTER
# ==================================

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        teacher_code = request.form['teacher_code']

        image = request.files['teacher_image']

        filename = secure_filename(
            image.filename
        )

        # CREATE UPLOAD FOLDER

        os.makedirs(
            app.config['UPLOAD_FOLDER'],
            exist_ok=True
        )

        # SAVE IMAGE

        image.save(
            os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )
        )

        role = request.form['role']
        subject = request.form['subject']
        phone = request.form['phone']

        # CHECK EXISTING EMAIL

        existing_teacher = Teacher.query.filter_by(
            email=email
        ).first()

        if existing_teacher:

            return "Email already exists"

        # HASH PASSWORD

        hashed_password = generate_password_hash(
            password
        )

        # CREATE TEACHER

        teacher = Teacher(

            full_name=full_name,

            email=email,

            password=hashed_password,

            teacher_code=teacher_code,

            teacher_image=filename,

            role=role,

            subject=subject,

            phone=phone
        )

        db.session.add(teacher)

        db.session.commit()

        return redirect(
            url_for('login')
        )

    return render_template(
        'register.html'
    )

# ==================================
# ADD STUDENT
# ==================================

@app.route('/add-student', methods=['GET', 'POST'])

def add_student():

    if request.method == 'POST':

        full_name = request.form['full_name']
        age = request.form['age']
        gender = request.form['gender']
        student_class = request.form['student_class']
        current_year = datetime.now().year

        students_in_class = Student.query.filter_by(
    student_class=student_class
).count() + 1

        roll_number = str(
    students_in_class
).zfill(3)

        unique_student_id = (
    f"{current_year}"
    f"{student_class}"
    f"{roll_number}"
)
        parent_phone = request.form['parent_phone']
        image = request.files['student_image']

        filename = secure_filename(
            image.filename
         )
        os.makedirs(
    app.config['UPLOAD_FOLDER'],
    exist_ok=True
)
        image.save(
          os.path.join(
        app.config['UPLOAD_FOLDER'],
        filename
    )
)

        last_student = Student.query.order_by(
            Student.student_id.desc()
        ).first()

        if last_student:
            new_id = last_student.student_id + 1
        else:
            new_id = 1

        roll_no = f"STD{new_id:03d}"

        student = Student(
            roll_no=roll_no,
            unique_student_id=
unique_student_id,
            full_name=full_name,
            age=age,
            gender=gender,
            student_class=student_class,
            parent_phone=parent_phone,
            student_image=filename
        )

        db.session.add(student)
        db.session.commit()

        return redirect(url_for('students'))

    return render_template(
        'students/add_student.html'
    )

# ==================================
# STUDENTS LIST
# ==================================

@app.route('/students')

def students():

    search = request.args.get('search')

    if search:

        all_students = Student.query.filter(
            Student.full_name.contains(search)
        ).all()

    else:

        all_students = Student.query.all()

    return render_template(
        'students/students.html',
        students=all_students
    )


# ==================================
# TAKE ATTENDANCE
# ==================================

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if session.get('role') == 'admin':

        return "Admin cannot take attendance"
    students = Student.query.all()

    if request.method == 'POST':

        # DELETE OLD ATTENDANCE

        Attendance.query.delete()

        db.session.commit()

        # SAVE NEW ATTENDANCE

        for student in students:

            status = request.form.get(
                f'attendance_{student.student_id}'
            )

            attendance_record = Attendance(

                student_id=student.student_id,

                student_name=student.full_name,

                attendance_date=datetime.now().strftime(
                    "%d-%m-%Y"
                ),

                status=status,

                teacher_name=session.get(
                    'teacher_name'
                )
            )

            db.session.add(
                attendance_record
            )

        db.session.commit()

        return redirect(
            url_for('attendance_report')
        )

    return render_template(

        'attendance/take_attendance.html',

        students=students
    )


# ==================================
# ATTENDANCE REPORT
# ==================================

@app.route('/attendance-report')

def attendance_report():

    all_attendance = Attendance.query.all()

    return render_template(
        'attendance/attendance_report.html',
        records=all_attendance
    )

# ==================================
# ADD CLASS
# ==================================

@app.route('/add-class', methods=['GET', 'POST'])

def add_class():

    if request.method == 'POST':

        class_name = request.form['class_name']

        class_teacher = request.form['class_teacher']

        total_students = request.form['total_students']

        classroom = ClassRoom(

            class_name=class_name,

            class_teacher=class_teacher,

            total_students=total_students
        )

        db.session.add(classroom)

        db.session.commit()

        return redirect(url_for('classes'))

    return render_template(
        'classes/add_class.html'
    )

# ==================================
# VIEW CLASSES
# ==================================

@app.route('/classes')

def classes():

    all_classes = ClassRoom.query.all()

    return render_template(
        'classes/classes.html',
        classes=all_classes
    )

# ==================================
# ADD SUBJECT
# ==================================

@app.route('/add-subject', methods=['GET', 'POST'])

def add_subject():

    if request.method == 'POST':

        subject_name = request.form['subject_name']

        class_name = request.form['class_name']

        subject_teacher = request.form['subject_teacher']

        subject = Subject(

            subject_name=subject_name,

            class_name=class_name,

            subject_teacher=subject_teacher
        )

        db.session.add(subject)

        db.session.commit()

        return redirect(url_for('subjects'))

    return render_template(
        'subjects/add_subject.html'
    )

# ==================================
# VIEW SUBJECTS
# ==================================

@app.route('/subjects')

def subjects():

    all_subjects = Subject.query.all()

    return render_template(
        'subjects/subjects.html',
        subjects=all_subjects
    )

# ==================================
# ADD TIMETABLE
# ==================================

@app.route('/add-timetable', methods=['GET', 'POST'])

def add_timetable():

    if request.method == 'POST':

        class_name = request.form['class_name']

        subject_name = request.form['subject_name']

        teacher_name = request.form['teacher_name']

        period_number = request.form['period_number']

        period_time = request.form['period_time']

        timetable = Timetable(

            class_name=class_name,

            subject_name=subject_name,

            teacher_name=teacher_name,

            period_number=period_number,

            period_time=period_time
        )

        db.session.add(timetable)

        db.session.commit()

        return redirect(url_for('view_timetable'))

    return render_template(
        'timetable/add_timetable.html'
    )

# ==================================
# VIEW TIMETABLE
# ==================================

@app.route('/timetable')

def view_timetable():

    all_timetable = Timetable.query.all()

    return render_template(
        'timetable/timetable.html',
        timetable=all_timetable
    )


# ==================================
# ADD EXAM MARKS
# ==================================

@app.route('/add-marks', methods=['GET', 'POST'])

def add_marks():

    if request.method == 'POST':

        student_name = request.form['student_name']

        student = Student.query.filter_by(

    full_name=student_name

).first()

        subject_name = request.form['subject_name']

        marks = int(request.form['marks'])

        total_marks = int(request.form['total_marks'])

        if marks >= 35:
            result = "Pass"
        else:
            result = "Fail"

        exam = Exam(

    student_name=student_name,

    student_id=student.student_id,

    subject_name=subject_name,

    marks=marks,

    total_marks=total_marks,

    result=result
)

        db.session.add(exam)

        db.session.commit()

        return redirect(url_for('exam_report'))

    return render_template(
        'exams/add_marks.html'
    )

# ==================================
# EXAM REPORT
# ==================================

@app.route('/exam-report')

def exam_report():

    all_results = Exam.query.all()

    total_students = len(all_results)

    passed_students = len(
        [x for x in all_results if x.result == "Pass"]
    )

    if total_students > 0:
        pass_percentage = (
            passed_students / total_students
        ) * 100
    else:
        pass_percentage = 0

    return render_template(
        'exams/exam_report.html',
        results=all_results,
        pass_percentage=pass_percentage
    )


# ==================================
# STUDENT PROFILE
# ==================================

@app.route('/student/<int:student_id>')

def student_profile(student_id):

    student = Student.query.get_or_404(
        student_id
    )

    attendance_records = Attendance.query.filter_by(
        student_id=student_id
    ).all()

    exam_records = Exam.query.filter_by(
        student_name=student.full_name
    ).all()

    return render_template(
        'students/student_profile.html',
        student=student,
        attendance_records=attendance_records,
        exam_records=exam_records
    )

# ==================================
# EDIT STUDENT
# ==================================

@app.route('/edit-student/<int:student_id>',
methods=['GET', 'POST'])

def edit_student(student_id):

    student = Student.query.get_or_404(
        student_id
    )

    if request.method == 'POST':

        student.full_name = request.form[
            'full_name'
        ]

        student.age = request.form[
            'age'
        ]

        student.gender = request.form[
            'gender'
        ]

        student.student_class = request.form[
            'student_class'
        ]

        student.parent_phone = request.form[
            'parent_phone'
        ]

        db.session.commit()

        return redirect(url_for('students'))

    return render_template(
        'students/edit_student.html',
        student=student
    )

# ==================================
# DELETE STUDENT
# ==================================

@app.route('/delete-student/<int:student_id>')

def delete_student(student_id):

    student = Student.query.get_or_404(
        student_id
    )

    db.session.delete(student)

    db.session.commit()

    return redirect(url_for('students'))


# ==================================
# ADD UPCOMING EXAM
# ==================================

@app.route('/add-upcoming-exam',
methods=['GET', 'POST'])

def add_upcoming_exam():

    if request.method == 'POST':

        exam_name = request.form['exam_name']

        subject_name = request.form['subject_name']

        exam_date = request.form['exam_date']

        exam_time = request.form['exam_time']

        class_name = request.form['class_name']

        exam = UpcomingExam(

            exam_name=exam_name,

            subject_name=subject_name,

            exam_date=exam_date,

            exam_time=exam_time,

            class_name=class_name
        )

        db.session.add(exam)

        db.session.commit()

        return redirect(
            url_for('upcoming_exams')
        )

    return render_template(
        'exams/add_upcoming_exam.html'
    )
# ==================================

# UPCOMING EXAM TABLE

# ==================================

class UpcomingExam(db.Model):
    __tablename__ = 'upcoming_exams'

    exam_id = db.Column(
    db.Integer,
    primary_key=True
)

    exam_name = db.Column(
    db.String(100)
)

    subject_name = db.Column(
    db.String(100)
)

    exam_date = db.Column(
    db.String(50)
)

    exam_time = db.Column(
    db.String(50)
)

    class_name = db.Column(
    db.String(50)
)


# ==================================

# ANNOUNCEMENT TABLE

# ==================================

class Announcement(db.Model):
    __tablename__ = 'announcements'

    announcement_id = db.Column(
    db.Integer,
    primary_key=True
)

    title = db.Column(
    db.String(200)
)

    message = db.Column(
    db.Text
)

    posted_by = db.Column(
    db.String(100)
)

# ==================================
# ADD FEES
# ==================================
@app.route('/add-fees',
methods=['GET', 'POST'])

def add_fees():

    if request.method == 'POST':

        unique_student_id = request.form[
            'unique_student_id'
        ]

        total_fee = int(

            request.form['total_fee']
        )

        paid_fee = int(

            request.form['paid_fee']
        )

        # Find Student

        student = Student.query.filter_by(

            unique_student_id=
            unique_student_id

        ).first()

        # Balance Fee

        pending_fee = (
            total_fee - paid_fee
        )

        # Status

        if pending_fee == 0:

            status = "Paid"

        else:

            status = "Pending"

        fee = Fees(

            student_id=
            student.student_id,

            student_name=
            student.full_name,

            class_name=
            student.student_class,

            total_fee=
            total_fee,

            paid_fee=
            paid_fee,

            pending_fee=
            pending_fee,

            status=status
        )

        db.session.add(fee)

        db.session.commit()

        return redirect(
            url_for('fees_report')
        )

    return render_template(
        'fees/add_fees.html'
    )


# ==================================
# FEES REPORT
# ==================================

@app.route('/fees-report')

def fees_report():

    all_fees = Fees.query.all()

    return render_template(
        'fees/fees_report.html',
        fees=all_fees
    )

# ==================================
# DOWNLOAD ATTENDANCE PDF
# ==================================

@app.route('/download-attendance-pdf')

def download_attendance_pdf():

    attendance_data = Attendance.query.all()

    pdf_file = "attendance_report.pdf"

    pdf = SimpleDocTemplate(pdf_file)

    data = [[
        'Student',
        'Date',
        'Status'
    ]]

    for item in attendance_data:

        data.append([

            item.student_name,

            item.attendance_date,

            item.status
        ])

    table = Table(data)

    table.setStyle(TableStyle([

        ('BACKGROUND', (0,0), (-1,0),
        colors.blue),

        ('TEXTCOLOR', (0,0), (-1,0),
        colors.white),

        ('GRID', (0,0), (-1,-1),
        1, colors.black),

        ('BACKGROUND', (0,1), (-1,-1),
        colors.beige)

    ]))

    elements = [table]

    pdf.build(elements)

    return send_file(

        pdf_file,

        as_attachment=True
    )


# ==================================
# STUDENT ID CARD
# ==================================

@app.route('/student-id/<int:student_id>')

def student_id(student_id):

    student = Student.query.get_or_404(
        student_id
    )

    card = Image.new(
        'RGB',
        (600, 350),
        color='#1e293b'
    )

    draw = ImageDraw.Draw(card)

    draw.text(
        (200, 30),

        "STUDENT ID CARD",

        fill='white'
    )

    draw.text(
        (200, 100),

        f"Name: {student.full_name}",

        fill='white'
    )

    draw.text(
        (200, 150),

        f"Roll No: {student.roll_no}",

        fill='white'
    )

    draw.text(
        (200, 200),

        f"Class: {student.student_class}",

        fill='white'
    )

    image_path = os.path.join(

        app.config['UPLOAD_FOLDER'],

        student.student_image
    )

    student_img = Image.open(image_path)

    student_img = student_img.resize(
        (120, 120)
    )

    card.paste(student_img, (40, 90))

    output_path = os.path.join(

        app.config['UPLOAD_FOLDER'],

        f"id_card_{student.student_id}.png"
    )

    card.save(output_path)

    return send_file(
        output_path,
        as_attachment=True
    )

# ==================================
# ADMIN DASHBOARD
# ==================================

@app.route('/admin-dashboard')
def admin_dashboard():

    if session.get('role') != 'admin':

        return redirect(
            url_for('dashboard')
        )

    total_teachers = Teacher.query.count()

    total_students = Student.query.count()

    total_classes = ClassRoom.query.count()

    total_subjects = Subject.query.count()

    total_attendance = Attendance.query.count()

    total_exams = Exam.query.count()

    total_fees = Fees.query.count()

    recent_teachers = Teacher.query.order_by(
        Teacher.teacher_id.desc()
    ).all()

    return render_template(

        'admin_dashboard.html',

        total_teachers=total_teachers,

        total_students=total_students,

        total_classes=total_classes,

        total_subjects=total_subjects,

        total_attendance=total_attendance,

        total_exams=total_exams,

        total_fees=total_fees,

        recent_teachers=recent_teachers
    )


# ==================================
# TEACHER PROFILE
# ==================================

@app.route('/teacher/<int:teacher_id>')
def teacher_profile(teacher_id):

    # ONLY ADMIN ACCESS

    if session.get('role') != 'admin':

        return redirect(
            url_for('dashboard')
        )

    # GET TEACHER

    teacher = Teacher.query.get_or_404(
        teacher_id
    )

    # GET ATTENDANCE ACTIVITY

    teacher_attendance = Attendance.query.filter_by(
        teacher_name=teacher.full_name
    ).all()

    total_attendance = len(
        teacher_attendance
    )

    return render_template(

        'teacher_profile.html',

        teacher=teacher,

        teacher_attendance=teacher_attendance,

        total_attendance=total_attendance
    )

# ==================================
# DELETE TEACHER
# ==================================

@app.route('/delete-teacher/<int:teacher_id>')
def delete_teacher(teacher_id):

    if session.get('role') != 'admin':

        return redirect(
            url_for('dashboard')
        )

    teacher = Teacher.query.get_or_404(
        teacher_id
    )

    db.session.delete(teacher)

    db.session.commit()

    return redirect(
        url_for('admin_dashboard')
    )

# ==================================
# TOGGLE TEACHER STATUS
# ==================================

@app.route('/toggle-teacher/<int:teacher_id>')
def toggle_teacher(teacher_id):

    if session.get('role') != 'admin':

        return redirect(
            url_for('dashboard')
        )

    teacher = Teacher.query.get_or_404(
        teacher_id
    )

    if teacher.status == "Active":

        teacher.status = "Inactive"

    else:

        teacher.status = "Active"

    db.session.commit()

    return redirect(
        url_for('admin_dashboard')
    )

# ==================================
# ADD ANNOUNCEMENT
# ==================================

@app.route('/add-announcement',
methods=['GET', 'POST'])

def add_announcement():

    if session.get('role') != 'admin':

        return redirect(
            url_for('dashboard')
        )

    if request.method == 'POST':

        title = request.form['title']

        message = request.form['message']

        announcement = Announcement(

            title=title,

            message=message,

            posted_by=session.get(
                'teacher_name'
            )
        )

        db.session.add(
            announcement
        )

        db.session.commit()

        return redirect(
            url_for('admin_dashboard')
        )

    return render_template(
        'announcements/add_announcement.html'
    )

# ==================================
# FORGOT PASSWORD
# ==================================

@app.route('/forgot-password',
methods=['GET', 'POST'])

def forgot_password():

    if request.method == 'POST':

        email = request.form['email']

        teacher = Teacher.query.filter_by(
            email=email
        ).first()

        if teacher:

            otp = random.randint(
                100000,
                999999
            )

            session['reset_otp'] = str(otp)

            session['reset_email'] = email

            msg = Message(

                'Password Reset OTP',

                sender=
                app.config['MAIL_USERNAME'],

                recipients=[email]
            )

            msg.body = (
                f'Your OTP is: {otp}'
            )

            mail.send(msg)

            return redirect(
                url_for('verify_otp')
            )

        else:

            return "Email not found"

    return render_template(
        'forgot_password.html'
    )

# ==================================
# DASHBOARD
# ==================================

@app.route('/dashboard')
def dashboard():

    total_students = Student.query.count()

    total_classes = ClassRoom.query.count()

    total_subjects = Subject.query.count()

    total_attendance = Attendance.query.count()

    total_fees = Fees.query.count()

    today_date = datetime.now().strftime(
        "%d %B %Y"
    )

    # RECENT ATTENDANCE

    recent_attendance = Attendance.query.order_by(
        Attendance.attendance_id.desc()
    ).limit(5).all()

    # ANNOUNCEMENTS

    announcements = Announcement.query.order_by(
        Announcement.announcement_id.desc()
    ).all()

    return render_template(

        'dashboard.html',

        total_students=total_students,

        total_classes=total_classes,

        total_subjects=total_subjects,

        total_attendance=total_attendance,

        total_fees=total_fees,

        today_date=today_date,

        recent_attendance=recent_attendance,

        announcements=announcements
    )

# ==================================
# LOGOUT
# ==================================

@app.route('/logout')
def logout():

    teacher = Teacher.query.filter_by(
        full_name=session.get(
            'teacher_name'
        )
    ).first()

    if teacher:

        teacher.is_online = False

        teacher.last_action = "Logged Out"

        db.session.commit()

    session.clear()

    return redirect(
        url_for('login')
    )


# ==================================
# RUN APP
# ==================================

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)