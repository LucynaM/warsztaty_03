from django.conf.urls import url
from .views import ShowRooms, RoomDetails, RoomNew, DeleteRoom, EditRoom, ReserveRoom, SearchRoom

urlpatterns = [
    #all rooms site
    url(r'^$', ShowRooms.as_view(), name='all_rooms'),
    #showing room details site
    url(r'^room/(?P<id>(\d)+)/$', RoomDetails.as_view(), name='room_details'),
    #adding new room site
    url(r'^room/new/$', RoomNew.as_view(), name='room_new'),
    # deleting selected room site
    url(r'^room/delete/(?P<id>(\d)+)/$', DeleteRoom.as_view(), name='room_delete'),
    # editing existing room details site
    url(r'^room/edit/(?P<id>(\d)+)/$', EditRoom.as_view(), name='room_edit'),
    # room reservation site
    url(r'^room/reserve/(?P<id>(\d)+)/$', ReserveRoom.as_view(), name='room_reserve'),
    # room searching site
    url(r'^room/search/$', SearchRoom.as_view(), name='room_search'),
]
