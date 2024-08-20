from flask import render_template, request, redirect, url_for, session 
from app import app, db
from app.models import Faculty, Program, Subject

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/choose_faculty', methods=['GET', 'POST'])
def choose_faculty():
    if request.method == 'POST':
        faculty_id = request.form.get('faculty')
        return redirect(url_for('choose_program', faculty_id=faculty_id))
    faculties = Faculty.query.all()
    return render_template('choose_faculty.html', faculties=faculties)

@app.route('/choose_program/<int:faculty_id>', methods=['GET', 'POST'])
def choose_program(faculty_id):
    if request.method == 'POST':
        program_id = request.form.get('program')
        return redirect(url_for('enter_results', program_id=program_id))
    programs = Program.query.filter_by(faculty_id=faculty_id).all()
    return render_template('choose_program.html', programs=programs)



@app.route('/enter_results/<int:program_id>', methods=['GET', 'POST'])
def enter_results(program_id):
    if request.method == 'POST':
        # Initialize an empty list to store the results
        results = []
        
        # Retrieve subjects associated with the program_id
        subjects = Subject.query.filter_by(program_id=program_id).all()

        for subject in subjects:
            # Get the grade for each subject from the form
            grade = request.form.get(f'subject{subject.id}')
            
            # Append the subject ID and grade to the results list
            results.append({'subject_id': subject.id, 'grade': grade})

        # Store the results in the session
        session['results'] = results

        # Redirect to review_results with the program_id
        return redirect(url_for('review_results', program_id=program_id))

    subjects = Subject.query.filter_by(program_id=program_id).all()
    return render_template('enter_results.html', subjects=subjects)
    

    
@app.route('/review_results/<int:program_id>', methods=['GET', 'POST'])
def review_results(program_id):
    results = session.get('results', [])  # Retrieve results from session
    
    if request.method == 'POST':
        # Logic for processing results, such as calculating GPA
        total_grade_points = 0
        total_credits = 0
        
        grade_points_map = {
            'A': 5.0,
            'B+': 4.0,
            'B': 3.0,
            'C': 2.0,
            'F': 0.0
        }

        for result in results:
            subject = Subject.query.get(result['subject_id'])
            if not subject:
                continue
            
            grade = result['grade']
            grade_points = grade_points_map.get(grade, 0.0)
            total_grade_points += grade_points * subject.credits
            total_credits += subject.credits

        # Calculate GPA
        gpa = total_grade_points / total_credits if total_credits > 0 else 0.0

        # Display GPA on the page
        return render_template('review_results.html', gpa=gpa, results=results, program_id=program_id)

    return render_template('review_results.html', program_id=program_id, results=results)
    

    
    
    
    



# Route for managing faculties
@app.route('/admin/manage_faculties', methods=['GET', 'POST'])
def manage_faculties():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            faculty = Faculty(name=name)
            db.session.add(faculty)
            db.session.commit()
        return redirect(url_for('manage_faculties'))
    
    faculties = Faculty.query.all()
    return render_template('admin/manage_faculties.html', faculties=faculties)

# Route for editing a faculty
@app.route('/admin/edit_faculty/<int:id>', methods=['GET', 'POST'])
def edit_faculty(id):
    faculty = Faculty.query.get(id)
    if request.method == 'POST':
        faculty.name = request.form.get('name')
        db.session.commit()
        return redirect(url_for('manage_faculties'))
    
    return render_template('admin/faculty.html', faculty=faculty)

# Route for deleting a faculty
@app.route('/admin/delete_faculty/<int:id>')
def delete_faculty(id):
    faculty = Faculty.query.get(id)
    db.session.delete(faculty)
    db.session.commit()
    return redirect(url_for('manage_faculties'))

# Route for managing programs
@app.route('/admin/manage_programs', methods=['GET', 'POST'])
def manage_programs():
    if request.method == 'POST':
        faculty_id = request.form.get('faculty')
        name = request.form.get('name')
        if faculty_id and name:
            program = Program(faculty_id=faculty_id, name=name)
            db.session.add(program)
            db.session.commit()
        return redirect(url_for('manage_programs'))

    faculties = Faculty.query.all()
    programs = Program.query.all()
    return render_template('admin/manage_programs.html', programs=programs, faculties=faculties)

# Route for editing a program
@app.route('/admin/edit_program/<int:id>', methods=['GET', 'POST'])
def edit_program(id):
    program = Program.query.get(id)
    if request.method == 'POST':
        program.faculty_id = request.form.get('faculty')
        program.name = request.form.get('name')
        db.session.commit()
        return redirect(url_for('manage_programs'))

    faculties = Faculty.query.all()
    return render_template('admin/program.html', program=program, faculties=faculties)

# Route for deleting a program
@app.route('/admin/delete_program/<int:id>')
def delete_program(id):
    program = Program.query.get(id)
    db.session.delete(program)
    db.session.commit()
    return redirect(url_for('manage_programs'))

# Route for managing subjects
@app.route('/admin/manage_subjects', methods=['GET', 'POST'])
def manage_subjects():
    if request.method == 'POST':
        program_id = request.form.get('program')
        name = request.form.get('name')
        credits = request.form.get('credits')
        year = request.form.get('year')
        semester = request.form.get('semester')
        if program_id and name and credits and year and semester:
            subject = Subject(program_id=program_id, name=name, credits=credits, year=year, semester=semester)
            db.session.add(subject)
            db.session.commit()
        return redirect(url_for('manage_subjects'))

    programs = Program.query.all()
    subjects = Subject.query.all()
    return render_template('admin/manage_subjects.html', subjects=subjects, programs=programs)

# Route for editing a subject
@app.route('/admin/edit_subject/<int:id>', methods=['GET', 'POST'])
def edit_subject(id):
    subject = Subject.query.get(id)
    if request.method == 'POST':
        subject.program_id = request.form.get('program')
        subject.name = request.form.get('name')
        subject.credits = request.form.get('credits')
        subject.year = request.form.get('year')
        subject.semester = request.form.get('semester')
        db.session.commit()
        return redirect(url_for('manage_subjects'))

    programs = Program.query.all()
    return render_template('admin/subject.html', subject=subject, programs=programs)

# Route for deleting a subject
@app.route('/admin/delete_subject/<int:id>')
def delete_subject(id):
    subject = Subject.query.get(id)
    db.session.delete(subject)
    db.session.commit()
    return redirect(url_for('manage_subjects'))
    