from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from .models import Question
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    page = request.GET.get('page','1')
    # 질문 목록 데이터, 역순으로 정렬
    question_list = Question.objects.order_by('-create_date')
    
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {'question_list':page_obj}
    
    # context = {'question_list':question_list}
    # render -> 파이썬 데이터를 HTML로 반환
    # 리액트랑 같이 쓸때는 redirect 로 옮겨 주면 될듯하다
    return render(request,'pybo/question_list.html',context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question':question}
    return render(request,'pybo/question_detail.html',context)

def answer_create(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail',question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question':question, 'form':form}
    return render(request,'pybo/question_detail.html',context)


def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)