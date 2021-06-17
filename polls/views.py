from . models import Question, Choice

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import F



# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last 5 published questions(not including those set to be published in future)"""

        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'

    def get_queryset(self):
        """Return the Question only its not in future"""
        return Question.objects.filter(pub_date__lte = timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """Return the Question only its not in future"""
        return Question.objects.filter(pub_date__lte = timezone.now())

def vote(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    
    # first -> dictionary error, second = django error for data not in model Choice
    except (KeyError, Choice.DoesNotExist):
        # redisplay the question's voting from with error
        return render(request, 'polls/details.html', {'question': question, 'error_message' : "You didn't select a choice"})
    
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # always return HttpResponseRedirect after successfully
        # dealing with POST data. This prevents data from 
        #being posted twice, if user hits back button.
    return HttpResponseRedirect(reverse('polls:results', args = (question.id,)))
