from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from ..decorators import teacher_required
from ..models import Classroom, Enrollment, Test, Question, Answer, testTaken
from ..forms import CreateTestForm, CreateQnForm, CreateClassForm
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Classroom, Test
from ..forms import CreateTestForm
import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..decorators import teacher_required
from ..models import Classroom, Test, Question

import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..decorators import teacher_required
from ..models import Classroom, Test, Question

import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..decorators import teacher_required
from ..models import Classroom, Test, Question

import pandas as pd
import os
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..decorators import teacher_required
from ..models import Classroom, Test, Question
import openpyxl

def download_excel_template(request):
    # Create an Excel workbook and sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Question Template"
    
    # Add headers
    ws.append(["Question", "Answer", "Marks"])
    
    # Prepare response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=question_template.xlsx'
    wb.save(response)
    return response

def process_excel(file_path, test):
    try:
        print("process_excel() function called")
        print("Checking file existence:", os.path.exists(file_path))
        
        df = pd.read_excel(file_path)
        print("Extracted Data:\n", df)
        required_columns = {'Question', 'Answer', 'Marks'}
        
        if not required_columns.issubset(df.columns):
            return False, "Invalid file format. Ensure columns are: Question, Answer, Marks."
        
        for _, row in df.iterrows():
            print(f"Adding Question: {row['Question']}, Answer: {row['Answer']}, Marks: {row['Marks']}")
            q = Question(
                test=test,
                qn_text=row['Question'],
                key=row['Answer'],
                max_score=row['Marks']
            )
            q.save()
            print("Saved:", q)
        
        return True, "Questions successfully added."
    except Exception as e:
        return False, f"Error processing file: {str(e)}"

@login_required(login_url='login')
@teacher_required
def submit_question_paper(request, class_id):
    room = get_object_or_404(Classroom, pk=class_id)
    tests = Test.objects.filter(belongs=room)
    
    print("FILES RECEIVED:", request.FILES)
    print("POST DATA RECEIVED:", request.POST)
    
    if request.method == "POST" and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        test_id = request.POST.get('test_id')
        
        if not test_id:
            messages.error(request, "Please select a test.")
            return redirect('view_class', class_id)
        
        test = get_object_or_404(Test, pk=test_id, belongs=room)
        
        if not uploaded_file.name.endswith(('.xlsx', '.xls')):
            messages.error(request, "Invalid file type. Please upload an Excel file (.xlsx or .xls).")
            return redirect('view_class', class_id)
        
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        
        print("File saved at:", file_path)
        
        success, message = process_excel(file_path, test)
        
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
        
        return redirect('view_class', class_id)
    
    messages.error(request, "No file uploaded.")
    return redirect('view_class', class_id)


@login_required(login_url='login')
@teacher_required
def submit_question_paper(request, class_id):
    room = get_object_or_404(Classroom, pk=class_id)
    tests = Test.objects.filter(belongs=room)
    
    print("FILES RECEIVED:", request.FILES)
    print("POST DATA RECEIVED:", request.POST)
    
    if request.method == "POST" and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        test_id = request.POST.get('test_id')
        
        if not test_id:
            messages.error(request, "Please select a test.")
            return redirect('view_class', class_id)
        
        test = get_object_or_404(Test, pk=test_id, belongs=room)
        
        if not uploaded_file.name.endswith(('.xlsx', '.xls')):
            messages.error(request, "Invalid file type. Please upload an Excel file (.xlsx or .xls).")
            return redirect('view_class', class_id)
        
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        
        print("Saved file path:", file_path)
        
        success, message = process_excel(file_path, test)
        
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
        
        return redirect('view_class', class_id)
    
    messages.error(request, "No file uploaded.")
    return redirect('view_class', class_id)

@login_required(login_url='login')
@teacher_required
def submit_question_paper(request, class_id):
    room = get_object_or_404(Classroom, pk=class_id)
    tests = Test.objects.filter(belongs=room)
    
    print("FILES RECEIVED:", request.FILES)
    print("POST DATA RECEIVED:", request.POST)
    
    if request.method == "POST" and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        test_id = request.POST.get('test_id')
        
        if not test_id:
            messages.error(request, "Please select a test.")
            return redirect('view_class', class_id)
        
        test = get_object_or_404(Test, pk=test_id, belongs=room)
        
        if not uploaded_file.name.endswith(('.xlsx', '.xls')):
            messages.error(request, "Invalid file type. Please upload an Excel file (.xlsx or .xls).")
            return redirect('view_class', class_id)
        
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        
        print("Saved file path:", file_path)
        
        success, message = process_excel(file_path, test)
        
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
        
        return redirect('view_class', class_id)
    
    messages.error(request, "No file uploaded.")
    return redirect('view_class', class_id)



@login_required(login_url='login')
@teacher_required
def create_class(request):
	form = CreateClassForm(request.POST or None, request.FILES or None)
	if request.method == "POST":
		form = CreateClassForm(request.POST)

		if form.is_valid():
			name = form.cleaned_data.get('name')
			desc = form.cleaned_data.get('desc')
			code = form.cleaned_data.get('code')
			user = request.user 
			room = Classroom(owner=user, name=name, code=code, desc=desc)
			room.save()
			messages.success(request, '{} Class is Created'.format(room))
			return redirect('dashboard')
		else:
			messages.error(request, form.errors)
	return render(request, 'teachers/create_class.html', {'form': form})

@login_required(login_url='login')
@teacher_required
def update_class(request, class_id):
	room = get_object_or_404(Classroom, pk=class_id)
	if request.method == "POST":
		form = CreateClassForm(request.POST, instance=room)

		if form.is_valid():
			form.save()
			messages.success(request, '{} Class is Updated'.format(room))
			return redirect('view_class', class_id)
		else:
			messages.error(request, form.errors)
	else:
		form = CreateClassForm(instance=room)
	return render(request, 'teachers/create_class.html', {'form': form, 'room':room})

@login_required(login_url='login')
@teacher_required
def delete_class(request, class_id):
	room = get_object_or_404(Classroom, pk=class_id)
	messages.success(request, '{} is deleted'.format(room))
	room.delete()
	return redirect('dashboard')
	

@login_required(login_url='login')
@teacher_required
def create_test(request, class_id):
	form = CreateTestForm(request.POST or None, request.FILES or None)
	if request.method == "POST":
		form=CreateTestForm(request.POST)

		if form.is_valid():
			name = form.cleaned_data.get('name')
			desc = form.cleaned_data.get('desc')
			start_time = form.cleaned_data.get('start_time')
			end_time = form.cleaned_data.get('end_time')
			
			belongs = get_object_or_404(Classroom, id=class_id)

			test = Test(belongs=belongs, name=name, desc=desc, start_time=start_time, end_time=end_time)
			test.save()

			return redirect('view_class', class_id)
		else: 
			messages.error(request, form.errors)

	return render(request, 'teachers/create_test.html', {'form': form })

@login_required(login_url='login')
@teacher_required
def update_test(request, test_id):
	test = get_object_or_404(Test, pk=test_id)

	if request.method == "POST":
		form = CreateTestForm(request.POST, instance=test)

		if form.is_valid():
			form.save()
			messages.success(request, '{}  is Updated'.format(test))
			return redirect('view_test', test.id)
		else: 
			messages.error(request, form.errors)
	else:
		form = CreateTestForm(instance=test)
	return render(request, 'teachers/create_test.html', {'form': form, 'test' : test })

@login_required(login_url='login')
@teacher_required
def delete_test(request, test_id):
	test = get_object_or_404(Test, pk=test_id)
	room = test.belongs
	messages.success(request, '{} is deleted'.format(test))
	test.delete()
	return redirect('view_class', room.id)



@login_required(login_url='login')
@teacher_required
def view_test(request, test_id):
	qns = Question.objects.filter(test=test_id)
	test = get_object_or_404(Test, pk=test_id)

	# Search
	search = request.GET.get('search')

	if search != "" and search is not None:
		qns = Question.objects.filter(test=test_id, qn_text__icontains=search)

	# paginator 
	paginator = Paginator(qns, 5)
	page = request.GET.get('page', 1)

	try:
		qns = paginator.page(page)
	except PageNotAnInteger:
		qns = paginator.page(1)
	except EmptyPage:
		qns = paginator.page(paginator.num_pages)

	return render(request, 'teachers/view_test.html', { 'qns' : qns, 'test' : test } )


@login_required(login_url='login')
@teacher_required
def students_work(request, test_id):
	test = get_object_or_404(Test, pk=test_id)
	student = Enrollment.objects.filter(room=test.belongs).values('student')
	attended_s = testTaken.objects.filter(test=test_id).values('student')
	missed_s = [item for item in student if item not in attended_s]

	d = [] 
	for s in missed_s:
		d.append(s['student'])

	attended_s = User.objects.filter(pk__in=attended_s).values()
	missed_s = User.objects.filter(pk__in=d).values()

	for a in attended_s:
		a['ml_score'] = get_object_or_404(testTaken, test=test_id, student=a['id']).ml_score
		a['actual_score'] = get_object_or_404(testTaken, test=test_id, student=a['id']).actual_score


	qns = Question.objects.filter(test=test_id)
	test.max_score = 0 
	
	for q in qns:
		test.max_score += q.max_score

	values = {
		'test': test,
		'attended_s':attended_s,
		'missed_s': missed_s,
	}

	return render(request, 'teachers/students_work.html', values )


@login_required(login_url='login')
@teacher_required
def individual_work(request, test_id, student_id):	
	test = get_object_or_404(Test, pk=test_id)
	student = Enrollment.objects.filter(room=test.belongs).values('student')
	attended_s = testTaken.objects.filter(test=test_id).values('student')
	missed_s = [item for item in student if item not in attended_s]

	d = [] 
	for s in missed_s:
		d.append(s['student'])

	
	attended_s = User.objects.filter(pk__in=attended_s).values()
	missed_s = User.objects.filter(pk__in=d).values()
	
	for a in attended_s:
		a['ml_score'] = get_object_or_404(testTaken, test=test_id, student=a['id']).ml_score
		a['actual_score'] = get_object_or_404(testTaken, test=test_id, student=a['id']).actual_score

	test.max_score = 0 
	qns = Question.objects.filter(test=test_id)
	student = get_object_or_404(User, pk=student_id) 
	ans = []
	for q in qns :
		d = {} 
		d['qns'] = q 
		d['ans'] = get_object_or_404(Answer, student=student, question=q)
		ans.append(d)
		test.max_score += q.max_score
	

	values = {
		'ans' : ans, 
		'test': test,
		'student': student, 
		'attended_s':attended_s,
		'missed_s': missed_s,
	}

	return render(request, 'teachers/students_work.html', values )


@login_required(login_url='login')
@teacher_required
def update_work(request, qn_id, student_id):
	if request.method == "POST":
		ac = int(request.POST['actual_score'])
		student = get_object_or_404(User, pk=student_id) 
		qn = get_object_or_404(Question, pk=qn_id)
		ans = get_object_or_404(Answer, student=student, question=qn)
		tt = get_object_or_404(testTaken, student=student, test=qn.test)
		tt.actual_score -= ans.actual_score 
		tt.actual_score += ac 
		ans.actual_score = ac 
		ans.save()
		tt.save() 
	return redirect('individual_work', qn.test.id, student.id)


@login_required(login_url='login')
@teacher_required
def create_qn(request, test_id):
	form = CreateQnForm(request.POST or None, request.FILES or None)
	if request.method == "POST":
		form = CreateQnForm(request.POST)

		if form.is_valid():
			text = form.cleaned_data.get('qn_text')
			key = form.cleaned_data.get('key')
			max_score = form.cleaned_data.get('max_score')
			
			test = get_object_or_404(Test, id=test_id)

			qn = Question(test=test, qn_text=text, key=key, max_score=max_score)
			qn.save()

			return redirect('view_test', test_id)
		else: 
			messages.error(request, form.errors)

	return render(request, 'teachers/create_qn.html', {'form': form})

@login_required(login_url='login')
@teacher_required
def update_qn(request, qn_id):
	qn = get_object_or_404(Question, pk=qn_id)

	if request.method == "POST":
		form = CreateQnForm(request.POST, instance=qn)

		if form.is_valid():
			form.save()
			messages.success(request, 'Question is Updated')
			return redirect('view_test', qn.test.id)
		else: 
			messages.error(request, form.errors)
	else:
		form = CreateQnForm(instance=qn)
	return render(request, 'teachers/create_qn.html', {'form': form, 'qn' : qn })

@login_required(login_url='login')
@teacher_required
def delete_qn(request, qn_id):
	qn = get_object_or_404(Question, pk=qn_id)
	test = qn.test
	messages.success(request, 'Question is deleted')
	qn.delete()
	return redirect('view_test', test.id)