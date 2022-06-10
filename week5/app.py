from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"

class Student(db.Model):
    student_id = db.Column(db.Integer(), autoincrement = True, primary_key = True)
    roll_number = db.Column(db.Integer(), nullable = False, unique = True)
    first_name = db.Column(db.String(), nullable = False)
    last_name = db.Column(db.String())
    courses = db.relationship('Enrollments', cascade='all, delete')

    def __repr__(self):
        return "<Student %r>" % self.roll_number

class Course(db.Model):
    course_id = db.Column(db.Integer(), autoincrement = True, primary_key = True)
    course_code = db.Column(db.String(), nullable = False, unique = True)
    course_name = db.Column(db.String(), nullable = False)
    course_description = db.Column(db.String())
    students = db.relationship('Enrollments')

    def __repr__(self):
        return "<Course %r>" % self.course_name

class Enrollments(db.Model):
    enrollment_id = db.Column(db.Integer(), autoincrement = True, primary_key = True)
    estudent_id = db.Column(db.Integer(), db.ForeignKey('student.student_id',  ondelete="CASCADE"), nullable = False)
    ecourse_id = db.Column(db.Integer(), db.ForeignKey('course.course_id'), nullable = False)
    courses = db.relationship('Student')
    
    
@app.route("/", methods=["GET", "POST"])
def Home():
    value = Student.query.first()
    student = Student.query.all()
    if value == None:
        return render_template("EmptyDB.html")
    return render_template("Home.html", student=student)

@app.route('/student/create', methods=["GET", "POST"])
def add_student():
    if request.method == 'POST':
        roll = request.form['roll']
        first, last, courses = request.form['f_name'], request.form['l_name'], request.form.getlist('courses')
        if db.session.query(Student).filter_by(roll_number= roll).first() is not None:
            return render_template('DuplicateRoll.html')
        else:
            student = Student(roll_number = roll, first_name = first, last_name = last)
            db.session.add(student)
            db.session.commit()
            for i in courses:
                enroll = Enrollments(estudent_id = student.student_id, ecourse_id = int(i[7]))
                db.session.add(enroll)
                db.session.flush()
            db.session.commit()     
        return redirect('/')
    return render_template('AddStudentForm.html')

@app.route('/student/<int:student_id>/update', methods=["GET", "POST"])
def update_student(student_id):   
    student = Student.query.get(student_id)
    roll = student.roll_number 
    if request.method == 'POST':
        student.first_name = request.form['f_name']
        student.last_name = request.form['l_name']
        courses_new = request.form.getlist('courses')
        db.session.add(student)
        db.session.flush() 
        if len(courses_new) != 0:
            Enrollments.query.filter_by(estudent_id=student_id).delete()
            db.session.flush()
            for i in courses_new:
                enroll = Enrollments(estudent_id = student.student_id, ecourse_id = int(i[7]))
                db.session.add(enroll)
                db.session.flush()
        db.session.commit()  
        return redirect('/')
    return render_template('UpdateStudentForm.html', student=student)

@app.route('/student/<int:student_id>/delete', methods=["GET", "POST"])
def delete_student(student_id):
    if request.method == 'GET':
        student = Student.query.get(student_id)
        db.session.delete(student)
        db.session.commit()
        return redirect('/')
    
@app.route('/student/<int:student_id>', methods=["GET", "POST"])
def student_details(student_id):
    if request.method == 'GET':
        student = Student.query.get(student_id)
        courses = db.engine.execute('select * from student as s, course as c, enrollments as e where e.ecourse_id = c.course_id and s.student_id = e.estudent_id and s.student_id = ?', student_id).fetchall()
        return render_template('Index.html', courses=courses, student=student)
    return redirect('/')


if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 8080)
    



















