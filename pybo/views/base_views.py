from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count

from ..models import Question


def index(request):
    """
    pybo 목록 출력
    """
    # print(request.GET) == <QueryDict: {'page': ['4']}>
    page = request.GET.get('page','1')
    kw = request.GET.get('kw','')
    so = request.GET.get('so','recent')

    """
    annotate 함수는 Question 모델의 기존 필드인
     author, subject, content, create_date, modify_date, voter에 질문의 
     추천 수에 해당하는 num_voter 필드를 임시로 추가해 주는 함수이다. 
     이렇게 annotate 함수로 num_voter 필드를 추가하면 filter 함수나 order_by 함수에서 num_voter 필드를 사용할 수 있게 된다.
      여기서 num_voter는 Count('voter')와 같이 Count 함수를 사용하여 만들었다.
    """
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter','-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer','-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')

    """
    localhost:8000/pybo/?page=1
    get('page', '1')에서 '1'은 /pybo/ URL처럼 page 파라미터가 없는 URL을 위해 기본값으로 1을 지정한 것이다
    """
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw)|
            Q(content__icontains=kw)|
            Q(author__username__icontains=kw)|
            Q(answer__author__username__icontains=kw)
            ).distinct()
        

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    
   

    context = {'question_list':page_obj, 'page':page, 'kw':kw, 'so':so}
    
    return render(request, 'pybo/question_list.html',context)

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question':question}
    
    return render(request, 'pybo/question_detail.html',context)