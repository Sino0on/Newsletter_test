from django.shortcuts import render
from .models import *
from rest_framework import generics
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from .tasks import *


class NewsletterListView(generics.ListAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer


class NewsletterCreateView(generics.CreateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        print(serializer.data)
        for i in serializer.data['clients']:
            client = Client.objects.get(id=i)
            message = Message.objects.create(status="NO", client=client, newsletter_id=serializer.data['id'])
            payload = {
              "id": message.pk,
              "phone": client.get_number(),
              "text": serializer.data['text']
            }
            print(serializer.data['end_date'])
            start_newsletter.apply_async(args=(payload, serializer.data['end_date']), eta=serializer.data['start_date'])
            print('end')
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NewsletterUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer


class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientCreateView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class StatistikDetail(generics.RetrieveAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterWithClientsSerializer
    lookup_field = 'pk'


class StatistickAllView(generics.GenericAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = StatistickAllSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

