from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from ..decorators import student_required
from ..models import Classroom, Enrollment, Test, Question, Answer, testTaken
import datetime
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfTransformer
import nltk, string, numpy, math
from sklearn.feature_extraction.text import TfidfVectorizer
import google.generativeai as genai
import json
import logging
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from django.shortcuts import get_object_or_404, redirect
from ..models import Test, Question, Answer, testTaken
from django.contrib.auth.decorators import login_required
from ..decorators import student_required

# Configure chatbot API
genai.configure(api_key="AIzaSyA6t6yawckjVx4zDWorU8rTpWYYgACm6pk")  # Replace with correct API key
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from django.shortcuts import get_object_or_404, redirect
from ..models import Test, Question, Answer, testTaken
from django.contrib.auth.decorators import login_required
from ..decorators import student_required

# Configure chatbot API
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import json
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..models import Test, Question, Answer, testTaken
from ..decorators import student_required

logger = logging.getLogger(__name__)

genai.configure(api_key="AIzaSyA6t6yawckjVx4zDWorU8rTpWYYgACm6pk")
chatbot_model = genai.GenerativeModel("gemini-2.0-flash")
bert_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

def chatbot_evaluate(question, student_answer, max_marks):
    prompt = (
        f"You are an AI evaluator. Given a question, a student's response, and total marks, "
        f"assign a score as follows: "
        f"1. Full marks for correct response. "
        f"2. Partial marks for partially correct answers. "
        f"3. Zero marks for incorrect or irrelevant answers. "
        f"Format your output as a number: <marks> (e.g., 5). "
        f"For unrelated prompts, return 0. "
        f"Strictly respond with a number only.\n\n"
        f"Question: {question}\n"
        f"Student Response: {student_answer}\n"
        f"Total Marks: {max_marks}"
    )
    logger.debug(f"Sending request to Chatbot API with prompt:\n{prompt}")
    
    response = chatbot_model.generate_content(prompt)
    logger.debug(f"Raw Chatbot Response: {response.text.strip()}")
    
    try:
        chatbot_score = int(response.text.strip())
    except ValueError:
        chatbot_score = 0
    
    logger.debug(f"Final Chatbot Score after conversion: {chatbot_score}")
    return max(0, min(chatbot_score, max_marks))

@login_required(login_url='login')
@student_required
def submit_test(request, test_id):
    logger.debug("Using the correct submit_test function!")
    logger.debug(f"POST Data Received: {json.dumps(request.POST.dict(), indent=4)}")
    
    test = get_object_or_404(Test, id=test_id)
    student = request.user 
    
    if testTaken.objects.filter(test=test, student=request.user).exists():
        logger.debug("Test already taken, redirecting...")
        return redirect('review_test', test_id)
    
    tt = testTaken(test=test, student=student, actual_score=0, ml_score=0)
    tt.save()
    logger.debug("New testTaken entry created")
    
    for key, value in request.POST.items():
        if key.isdigit():  # Check if key is a question ID
            question_id = int(key)
            ans_text = value.strip()
            question = get_object_or_404(Question, id=question_id)
            model_answer = question.key.strip()
            max_marks = question.max_score
            
            logger.debug(f"Processing Question {question_id}: {question.qn_text}")
            logger.debug(f"Student Answer: {ans_text}")
            logger.debug(f"Max Marks for this question: {max_marks}")
            
            # Compute embeddings
            embeddings = bert_model.encode([model_answer, ans_text])
            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            
            # Apply stricter threshold and non-linear cubic scaling
            min_similarity = 0.6
            if similarity < min_similarity:
                bert_score = 0
            else:
                normalized_similarity = (similarity - min_similarity) / (1 - min_similarity)
                bert_score = round((normalized_similarity ** 3) * max_marks)
                bert_score = max(0, min(bert_score, max_marks))
            
            logger.debug(f"BERT Score Calculated: {bert_score}")
            
            # Keyword boosting - reward answers containing exact key terms
            model_words = set(nltk.word_tokenize(model_answer.lower()))
            ans_words = set(nltk.word_tokenize(ans_text.lower()))
            common_words = model_words.intersection(ans_words)
            if len(common_words) > 2:
                bert_score = min(max_marks, bert_score + int(max_marks * 0.1))
            
            # Answer Length Penalty - Penalize very short answers
            min_length_ratio = 0.45
            if len(ans_text) < min_length_ratio * len(model_answer):
                bert_score = round(bert_score * 0.5)
            
            logger.debug(f"Final Adjusted BERT Score: {bert_score}")
            
            # Get chatbot evaluation score
            logger.debug(f"Calling chatbot_evaluate with: {question.qn_text}, {ans_text}, {max_marks}")
            chatbot_score = chatbot_evaluate(question.qn_text, ans_text, max_marks)
            logger.debug(f"Chatbot Returned: {chatbot_score}")
            
            # Average the two scores
            final_score = round((bert_score + chatbot_score) / 2)
            
            logger.debug(f"Final Computed Score: {final_score}")
            
            ans = Answer(student=student, question=question, answer_text=ans_text, actual_score=final_score, ml_score=final_score)
            ans.save()
            tt.actual_score += final_score
            tt.ml_score += final_score
    
    tt.save()
    logger.debug("Test submission completed, redirecting...")
    return redirect('view_class', test.belongs.id)















########################################################################################
@login_required(login_url='login')
@student_required
def join_class(request):
	if request.method == "POST":
		code = request.POST['code']
		user = request.user 

		try:
			room = Classroom.objects.get(code=code)
		except Classroom.DoesNotExist:
			messages.warning(request, "There's no such Classroom")
			return redirect('join_class')

		if Enrollment.objects.filter(room=room, student=user).exists():
			messages.info(request, 'You Already Enrolled {}'.format(room))
		else: 
			Enrollment(room=room, student=user).save() 
			messages.success(request, '{} Class Enrolled'.format(room))

		return redirect('dashboard')

	return render(request, 'students/join_class.html')


@login_required(login_url='login')
@student_required
def attend_test(request, test_id):
	test = get_object_or_404(Test, id=test_id)

	if testTaken.objects.filter(test=test, student=request.user).exists():
		return redirect('review_test', test_id)

	qns = Question.objects.filter(test=test_id)
	return render(request, 'students/attend_test.html', { 'qns' : qns, 'test' : test } )


bert_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')




@login_required(login_url='login')
@student_required
def review_test(request, test_id):
	test = get_object_or_404(Test, id=test_id)
	qns = Question.objects.filter(test=test_id)
	student = request.user 
	ans = []
	tot = 0
	act = 0  
	for i in range(len(qns)) :
		d = {} 
		d['qns'] = qns[i] 
		d['ans'] = get_object_or_404(Answer, student=student, question=qns[i]) # Answer.objects.filter(student=student, question=qns[i]) 
		ans.append(d)
		act += d['ans'].actual_score  
		tot += qns[i].max_score 

	mark = "{} / {}".format(act, tot)
	return render(request, 'students/review_test.html', { 'test' : test, 'ans' : ans, 'mark' : mark })


@login_required(login_url='login')
@student_required
def assigned_test(request, class_id):
	test = Test.objects.filter(belongs=class_id)

	tests = []
	for t in test:
		if(testTaken.objects.filter(test=t, student=request.user).exists()):
			continue 
		elif ( t.start_time == None or t.start_time < timezone.now()) and ( t.end_time == None or t.end_time > timezone.now()):
			t.status = "Assigned"
			tests.append(t)

	# Search
	search = request.GET.get('search')

	if search != "" and search is not None:
		tests = Test.objects.filter(belongs=class_id, name__icontains=search).order_by('-create_time')


	# paginator 
	paginator = Paginator(tests, 5)
	page = request.GET.get('page', 1)

	try:
		tests = paginator.page(page)
	except PageNotAnInteger:
		tests = paginator.page(1)
	except EmptyPage:
		tests = paginator.page(paginator.num_pages)

		
	room = get_object_or_404(Classroom, id=class_id)
	return render(request, 'classroom/view_class.html', {'tests' : tests, 'room' : room } )


@login_required(login_url='login')
@student_required
def missing_test(request, class_id):
	test = Test.objects.filter(belongs=class_id)

	tests = []
	for t in test:
		if(testTaken.objects.filter(test=t, student=request.user).exists()):
			continue 
		elif ( t.start_time == None or t.start_time < timezone.now()) and ( t.end_time == None or t.end_time > timezone.now()):
			t.status = "Assigned"
			tests.append(t)
		elif(t.start_time and t.start_time > timezone.now()): # test is not yet started
			t.status = "not"
		else:
			t.status = "late"
			tests.append(t)

	# Search
	search = request.GET.get('search')

	if search != "" and search is not None:
		tests = Test.objects.filter(belongs=class_id, name__icontains=search).order_by('-create_time')


	# paginator 
	paginator = Paginator(tests, 5)
	page = request.GET.get('page', 1)

	try:
		tests = paginator.page(page)
	except PageNotAnInteger:
		tests = paginator.page(1)
	except EmptyPage:
		tests = paginator.page(paginator.num_pages)

	room = get_object_or_404(Classroom, id=class_id)
	return render(request, 'classroom/view_class.html', {'tests' : tests, 'room' : room } )


@login_required(login_url='login')
@student_required
def done_test(request, class_id):
	taken = list(testTaken.objects.filter(student=request.user).values("test"))

	d = []
	for t in taken: 
		d.append( t['test'] )
	tests = Test.objects.filter(pk__in=d, belongs=class_id)

	# Search
	search = request.GET.get('search')

	if search != "" and search is not None:
		tests = Test.objects.filter(belongs=class_id, name__icontains=search).order_by('-create_time')


	# paginator 
	paginator = Paginator(tests, 5)
	page = request.GET.get('page', 1)

	try:
		tests = paginator.page(page)
	except PageNotAnInteger:
		tests = paginator.page(1)
	except EmptyPage:
		tests = paginator.page(paginator.num_pages)


	for t in tests:
		t.status = "done"
		
	room = get_object_or_404(Classroom, id=class_id)
	return render(request, 'classroom/view_class.html', {'tests' : tests, 'room' : room } )