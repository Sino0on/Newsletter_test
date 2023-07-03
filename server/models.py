from django.db import models


class Client(models.Model):
    number = models.IntegerField()
    code = models.CharField(max_length=123)
    tag = models.CharField(max_length=50)
    timezone = models.CharField(max_length=123)

    def __str__(self):
        return f'{self.code} {self.number}'

    def get_number(self):
        return int(str(self.code) + str(self.number))

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Newsletter(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    clients = models.ManyToManyField(Client)

    def __str__(self):
        return f'{self.start_date} {self.text}'


class Message(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    newsletter = models.ForeignKey(Newsletter, models.CASCADE, related_name='messages_send')
    client = models.ForeignKey(Client, models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.created_date} {self.newsletter}'



