from django.shortcuts import get_object_or_404, HttpResponseRedirect
from interview.models import InterviewStudent
from pyzoom import refresh_tokens
from django.core.exceptions import ObjectDoesNotExist
import os
from dotenv import load_dotenv
from django.urls import reverse
from django.utils import timezone

load_dotenv()

class ZoomTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.

        # user = request.user
        # if user.is_authenticated:
        #     try:
        #         interview_student = InterviewStudent.objects.get(user=user)
        #         if interview_student.zoom_access_token is None:  
        #             return HttpResponseRedirect(reverse('zoom_authorize'))  # Redirect to zoom authorization page
        #         elif self.access_token_has_expired(interview_student):
        #             try:
        #                 new_tokens = refresh_tokens(os.getenv("APP_CLIENT_ID"), os.getenv("APP_CLIENT_SECRET"), interview_student.zoom_refresh_token)
        #                 interview_student.zoom_access_token = new_tokens['access_token']
        #                 interview_student.zoom_refresh_token = new_tokens['refresh_token']
        #                 interview_student.zoom_token_expiration = timezone.now() + timezone.timedelta(hours=1)  # set expiration date to 1 hour from now
        #                 interview_student.save()
        #             except Exception as e:
        #                 # Handle token refresh error, e.g., log the error
        #                 pass
        #     except InterviewStudent.DoesNotExist:
        #         # Handle the case when the user is not an interview student
        #         pass

        response = self.get_response(request)

        # Code to be executed for each request/response after the view is called.

        return response

    def access_token_has_expired(self, student):
        """
        Checks whether the access token of a student has expired.
        
        Arguments:
        - student: a InterviewStudent instance.
        
        Returns:
        - Boolean: True if the token has expired, False otherwise.
        """
        now = timezone.now()
        # return student.zoom_token_expiration <= now
        return False