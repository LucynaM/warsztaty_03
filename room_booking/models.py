from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=128)
    capacity = models.IntegerField()
    projector = models.BooleanField(default=True)

    def __str__(self):
        return "Room: {}, capacity: {}, projector: {}".format(self.name, self.capacity, 'Yes' if self.projector else 'No')

class Reservation(models.Model):
    reservation_date = models.DateField()
    room = models.ForeignKey(Room, related_name='reservations')
    comment = models.TextField(null=True)

    def __str__(self):
        return "Date: {}, room: {}".format(self.reservation_date, self.room.name)
