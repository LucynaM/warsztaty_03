from django.shortcuts import render, redirect
from .models import Room, Reservation
from django.views import View
from datetime import datetime, date


class ShowRooms(View):
    """Show all rooms with reservation state for current day"""
    def get(self, request):
        rooms = Room.objects.all()
        for room in rooms:
            if room.reservations.filter(reservation_date=date.today()):
                room.reserved = "Reserved"
            else:
                room.reserved = "Open"
        context = {"rooms": rooms}
        return render(request, 'room_booking/index.html', context)


class RoomDetails(View):
    """Show selected room details"""
    def get(self, request, id):
        room = Room.objects.get(id=id)
        room.reserved = []
        for reservation in room.reservations.filter(reservation_date__gte=date.today()).order_by("reservation_date"):
            room.reserved.append(reservation.reservation_date)
        context = {"room": room}
        return render(request, 'room_booking/room_details.html', context)


class RoomNew(View):
    """Add new room"""
    def get(self, request):
        return render(request, 'room_booking/room_new.html')

    def post(self, request):
        err_msg = ""
        if not "name" in request.POST or request.POST["name"] == "":
            err_msg += "Name is required field "
        else:
            name = (request.POST["name"]).title()
        if not "capacity" in request.POST or request.POST["capacity"] == "":
            err_msg += "Capacity is required field "
        else:
            try:
                capacity = int(request.POST["capacity"])
            except ValueError:
                err_msg += "Capacity must be a number "
        if err_msg != "":
            context = {"err_msg": err_msg}
            return render(request, 'room_booking/room_new.html', context)
        else:
            if "projector" in request.POST:
                projector = True
            else:
                projector = False
            Room.objects.create(name=name, capacity=capacity, projector=projector)
            return redirect('room_booking:all_rooms')


class DeleteRoom(View):
    """Delete selected room"""
    def get(self, request, id):
        room = Room.objects.get(id=id)
        context = {"room": room}
        return render(request, 'room_booking/room_delete.html', context)

    def post(self, request, id):
        room = Room.objects.get(id=id)
        room.delete()
        return redirect('room_booking:all_rooms')


class EditRoom(View):
    """Edit selected room"""

    def get(self, request, id):
        room = Room.objects.get(id=id)
        context = {"room": room}
        return render(request, 'room_booking/room_edit.html', context)

    def post(self, request, id):
        err_msg = ""
        room = Room.objects.get(id=id)
        if not "name" in request.POST or request.POST["name"] == "":
            err_msg += "Name is required field <br>"
        else:
            room.name = request.POST["name"]
        if not "capacity" in request.POST or request.POST["capacity"] == "":
            err_msg += "Capacity is required field "
        else:
            try:
                room.capacity = int(request.POST["capacity"])
            except ValueError:
                err_msg += "Capacity must be a number "

        if err_msg != "":
            context = {"room": room, "err_msg": err_msg}
            return render(request, 'room_booking/room_edit.html', context)
        else:
            if "projector" in request.POST:
                room.projector = True
            else:
                room.projector = False
            room.save()
            return redirect('room_booking:all_rooms')


class ReserveRoom(View):
    """Reserve selected room"""

    @staticmethod
    def getting_reserved(room):
        room.reserved = []
        for reservation in room.reservations.filter(reservation_date__gte=date.today()).order_by("reservation_date"):
            room.reserved.append(reservation.reservation_date)
        return {"room": room}

    def get(self, request, id):
        room = Room.objects.get(id=id)
        context = ReserveRoom.getting_reserved(room)
        if "reservation_date" in request.session:
            context["reservation_date"] = request.session["reservation_date"]
            del request.session["reservation_date"]
        return render(request, 'room_booking/room_reserve.html', context)

    def post(self, request, id):
        room = Room.objects.get(id=id)
        err_msg = ""
        if not "reservation_date" in request.POST or request.POST["reservation_date"] == "":
            err_msg += "Please select date "
        else:
            reservation_date = datetime.strptime(request.POST["reservation_date"], '%Y-%m-%d').date()
            if room.reservations.filter(reservation_date=reservation_date):
                err_msg += "Room's already been reserved. Please select another date "
            elif reservation_date < date.today():
                err_msg += "Please select correct date "

        if err_msg != "":
            context = {"room": room, "err_msg": err_msg}
            return render(request, 'room_booking/room_reserve.html', context)
        else:
            reservation = Reservation.objects.create(reservation_date=reservation_date, room=room)
            if request.POST["comment"] != "":
                reservation.comment = request.POST["comment"]
                reservation.save()
            context = ReserveRoom.getting_reserved(room)
            return render(request, 'room_booking/room_reserve.html', context)


class SearchRoom(View):
    """Search room for selected date"""
    def get(self, request):
        return render(request, 'room_booking/room_search.html')

    def post(self, request):
        err_msg = ""
        if not "reservation_date" in request.POST or request.POST["reservation_date"] == "":
            err_msg += "Please select date "
        else:
            reservation_date = datetime.strptime(request.POST["reservation_date"], '%Y-%m-%d').date()
            if request.POST["capacity"] == "":
                capacity = False
            else:
                try:
                    capacity = int(request.POST["capacity"])
                except ValueError:
                    err_msg += "Capacity must be a number "

        if err_msg != "":
            context = {"err_msg": err_msg}
            return render(request, 'room_booking/room_search.html', context)
        else:
            if "projector" in request.POST:
                projector = True
            else:
                projector = False

            if reservation_date and capacity and projector:
                open_rooms = Room.objects.filter(capacity__gte=capacity, projector=True).exclude(
                    reservations__reservation_date=reservation_date)
            elif reservation_date and capacity:
                open_rooms = Room.objects.filter(capacity__gte=capacity).exclude(
                    reservations__reservation_date=reservation_date)
            elif reservation_date and projector:
                open_rooms = Room.objects.filter(projector=True).exclude(
                    reservations__reservation_date=reservation_date)
            elif reservation_date:
                open_rooms = Room.objects.exclude(
                    reservations__reservation_date=reservation_date)

            request.session["reservation_date"] = str(reservation_date)

            context = {"open_rooms": open_rooms}
            return render(request, 'room_booking/room_search.html', context)
