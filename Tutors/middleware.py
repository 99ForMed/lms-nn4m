from django.http import JsonResponse, HttpResponseRedirect
from pyzoom import refresh_tokens
import os
from .models import Tutor
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from dotenv import load_dotenv
from django.utils import timezone

load_dotenv()

class TutorsZoomTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                tutor = Tutor.objects.get(user=user)
                if tutor.zoom_access_token is None:  
                    return HttpResponseRedirect(reverse('zoom_authorize'))  # Redirect to zoom authorization page
                elif self.access_token_has_expired(tutor):  
                    try:
                        new_tokens = refresh_tokens(os.getenv("APP_CLIENT_ID"), os.getenv("APP_CLIENT_SECRET"), tutor.zoom_refresh_token)
                        tutor.zoom_access_token = new_tokens['access_token']
                        tutor.zoom_refresh_token = new_tokens['refresh_token']
                        tutor.zoom_token_expiration = timezone.now() + timezone.timedelta(hours=1)  # set expiration date to 1 hour from now
                        tutor.save()
                    except Exception as e:
                        # Handle token refresh error, e.g., log the error
                        pass
            except Tutor.DoesNotExist:
                # Handle the case when the user is not a tutor
                pass

        response = self.get_response(request)

        return response

    def access_token_has_expired(self, tutor):
        """
        Checks whether the access token of a tutor has expired.
        
        Arguments:
        - tutor: a Tutor instance.
        
        Returns:
        - Boolean: True if the token has expired, False otherwise.
        """
        now = timezone.now()
        # return tutor.zoom_token_expiration <= now
        return True
