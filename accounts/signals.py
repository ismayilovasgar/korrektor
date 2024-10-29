# from django.contrib.auth.signals import user_logged_in
# from django.dispatch import receiver
# from django.utils import timezone
# from .models import User


# @receiver(user_logged_in)
# def track_daily_login(sender, request, user, **kwargs):
#     # Mövcud tarixi alın
#     today = timezone.now().date()

#     # Əgər istifadəçinin son girişi bugündürsə, daily_session-i artırın
#     if user.last_login and user.last_login.date() == today:
#         user.daily_session += 1
#     else:
#         # Əgər ilk girişdirsə və ya son girişi dünəndirsə, günlük sayını sıfırlayın
#         user.daily_session = 1

#     user.save()
