from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    #address = models.ForeignKey('Address', null=True, on_delete=models.SET_NULL)
    email = models.EmailField(max_length=100)


class Courier(models.Model):
    # init variables
    max_num_of_remaining_deliveries_var = 10
    # status variables
    available = 0
    full = 1

    # init columns
    courier_id = models.PositiveIntegerField()   # courier IDs are randomly generated, will not start from 0
    num_of_remaining_deliveries = models.PositiveIntegerField(default=10)
    date = models.DateField()
    status = models.PositiveIntegerField()

    def __str__(self):
        return "Courier ID: {}, date: {}".format(self.courier_id, self.date)


class Timeslot(models.Model):
    # status variables
    available = 0
    not_available = 1
    max_num_of_deliveries = 2
    deliveries_num_on_startup = 0

    # init columns
    courier = models.ForeignKey(Courier, null=True, on_delete=models.SET_NULL)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    num_of_scheduled_deliveries = models.PositiveIntegerField(default=deliveries_num_on_startup)
    status = models.PositiveIntegerField(default=available)
    supported_addresses = models.JSONField()    # list of supported cities

    def __str__(self):
        return "Start time: {}, end time: {}".format(self.start_time, self.end_time)


class Address(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    street = models.CharField(max_length=200)
    house_num = models.PositiveIntegerField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)


class Delivery(models.Model):
    # status variables
    scheduled = 0
    completed = 1
    # init columns
    timeslot = models.ForeignKey(Timeslot, null=True, on_delete=models.SET_NULL)
    status = models.PositiveIntegerField()
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
    courier = models.ForeignKey(Courier, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)