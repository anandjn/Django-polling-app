import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question
from django.urls import reverse
# Create your tests here.

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for question whose pub_date is in future"""

        time = timezone.now() + datetime.timedelta(days = 30)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_past_question(self):
        """was_published_recently() returns Flase for question whose pub_date is older than 1 day"""

        time = timezone.now() - datetime.timedelta(days = 1, seconds=1)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.was_published_recently(), False)
    
    def test_was_published_recently_with_recent_question(self):
        """was_published_recently returns True for question whose pub_date is within the last day"""
        time = timezone.now() - datetime.timedelta(hours = 23 , minutes=59, seconds=59)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(), True)

def createQuestion(question_text, days):
    """Creates a question with given 'question_text' and with offset with current time. (positve days = future, negatice days = past)"""
    time = timezone.now() + datetime.timedelta(days = days)
    return Question.objects.create(question_text= question_text, pub_date = time)

class QuestionIndexViewTests(TestCase):

    def test_no_question(self):
        """if No question is published, an appropriate message is displayed on index page"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_past_question(self):
        """Question with pub_date in the past are displayed on index page"""
        question = createQuestion("Past Question", -30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])

    def test_future_question(self):
        """Question with pub_date in the future is not displayed on the index page and an appropriate message is displayed"""
        question = createQuestion("Future Question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
    
    def test_future_question_and_past_question(self):
        """Even both future and past question exist, only past question is diasplayed"""
        question = createQuestion("Past Question", -5)
        createQuestion("Future Question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])

    def test_two_past_question(self):
        """The index page will display multiple question"""
        question_one = createQuestion("Question One?", -5)
        question_two = createQuestion("Question Two?", -10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question_one, question_two])

class QuestionDetailView(TestCase):
    def test_future_question(self):
        """The detail view of a question with pub_date in future return 404 not found"""
        future_question = createQuestion("Future Question", 5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """The detail view of question with pub_date in past is displays the question text"""
        past_question = createQuestion("Past Question?", -5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionResultView(TestCase):
    def test_future_question(self):
        """Result View of question with pub_date in future return 404 not found"""
        future_question = createQuestion("Future Question", 5)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_past_question(self):
        """Result view of question with pub_date in past displays the question text"""
        past_question = createQuestion("Past Question?", -5)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
