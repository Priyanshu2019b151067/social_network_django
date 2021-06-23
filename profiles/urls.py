from django.urls import path
from .views import *
urlpatterns = [
  path('myprofile/',my_profile_view,name="my-profile"),
  path("my-invites/",invatation_received_view, name="my-invites-view"),
  path("invite/",invite_profiles_list_view, name="invite-view"),
  path("send-invite/",send_invatation, name ="send-invite"),
  path("<slug>", ProfilesDetailView.as_view(), name="profile-detail-view"),
  path("",ProfileListView.as_view(), name="all-profiles"),
  path("remove-friend/",remove_from_friends, name="remove-friend"),
  path("my-invites/accept/",accept_invatation, name="accept-invite"),
  path("my-invites/reject/",reject_invatation, name="reject-invite")
]
