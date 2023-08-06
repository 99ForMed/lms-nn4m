from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
from interview.models import InterviewClass
from django.contrib.auth import get_user_model
from Tutors.models import Tutor

User = get_user_model()

from django.db.models.signals import pre_save

from django.db.models import JSONField
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()

class LessonPlan(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    tutors = models.ManyToManyField(Tutor, related_name="tutors")

    def __str__(self):
        return str(self.title)

class LiveClass(models.Model):
    initiator = models.ForeignKey(User, on_delete=models.CASCADE)
    currently_presenting = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='presenting_classes')

    interview_class = models.ForeignKey(InterviewClass, on_delete=models.CASCADE)
    lesson_plan = models.ForeignKey(LessonPlan, on_delete=models.CASCADE, null=True, blank=True) # reference to lesson plan
    lesson_data = JSONField(null=True, blank=True) # JSON field to store the lesson plan data
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    url = models.URLField(max_length=200)
    current_question = models.CharField(max_length=200, blank=True, null=True)  # stores the current question being answered

    @property
    def scheduled_end_time(self):
        """ This property calculates the scheduled end time which is 100 minutes after the start """
        return self.start_time + timedelta(minutes=100)

    @property
    def time_left(self):
        """ This property calculates the time left to the end of the class """
        if self.is_active:
            return max(timedelta(0), self.scheduled_end_time - timezone.now())
        else:
            return timedelta(0)

    def end_class(self):
        """ This method sets the actual end time of the class and sets the class as inactive """
        self.end_time = timezone.now()
        self.is_active = False
        # Send message to the group
        async_to_sync(channel_layer.group_send)(
            "live_class",  # group name
            {
                "type": "class.ended",
            }
        )
        self.save()
    
    def get_grouped_questions(self):
        # Initialize an empty list to hold the processed scenarios and questions.
        grouped_questions = []

        # Iterate over the items in lesson_data. Each item is a scenario with its associated questions.
        for scenario, questions in self.lesson_data.items():
            # Initialize an empty list to hold the processed questions for this scenario.
            scenario_questions = []

            # Iterate over the questions in this scenario.
            for question_data in questions:
                # Each question_data item is a dictionary with a single key-value pair.
                # The key is the question text and the value is the question's status.
                for question_text, question_status in question_data.items():
                    # Append the processed question to scenario_questions.
                    scenario_questions.append({
                        'text': question_text,
                        'status': question_status,
                        'locked': question_status != 'unlocked',
                        'label': f'Question {len(scenario_questions) + 1}',
                    })

            # Append the processed scenario and its associated questions to grouped_questions.
            grouped_questions.append({
                'scenario': scenario,
                'questions': scenario_questions,
            })

        # Return the processed scenarios and questions.
        return grouped_questions





@receiver(pre_save, sender=LiveClass)
def fill_lesson_data(sender, instance, **kwargs):
    if instance.lesson_plan and not instance.lesson_data:
        # Fetching scenarios and questions related to the lesson plan
        scenarios = list(instance.lesson_plan.scenarios.values('description')) # use .values() to get dicts
        questions = list(instance.lesson_plan.questions.values('question_text', 'scenario__description')) # use double underscore to get scenario description

        # Creating the dict
        lesson_data = {}
        for scenario in scenarios:
            lesson_data[scenario['description']] = []
        lesson_data[None] = []

        for question in questions:
            if question['scenario__description']:
                lesson_data[question['scenario__description']].append({question['question_text']: 'locked'})
            else:
                lesson_data[None].append({question['question_text']: 'locked'})
                
        instance.lesson_data = lesson_data


class Scenario(models.Model):
    lesson_plan = models.ForeignKey(LessonPlan, on_delete=models.CASCADE, related_name="scenarios")
    description = models.TextField()

    def __str__(self):
        return str(self.description)

class Question(models.Model):
    lesson_plan = models.ForeignKey(LessonPlan, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return str(self.question_text)

class Task(models.Model):
    lesson_plan = models.ForeignKey(LessonPlan, on_delete=models.CASCADE, related_name="tasks")
    description = models.TextField()
    is_for_group = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.description)

class Feedback(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_feedbacks')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_feedbacks')
    Question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_feedbacks', blank=True, null=True)
    LiveClass = models.ForeignKey(LiveClass, on_delete=models.CASCADE, related_name='live_class', blank=True, null=True)
    text = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback from {self.sender} to {self.receiver}'

class Timer(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    @property
    def duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        else:
            return timezone.now() - self.start_time







