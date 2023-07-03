from rest_framework import serializers
from .models import *
from datetime import datetime
from django.db.models import Q


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class NewsletterSerializer(serializers.ModelSerializer):
    # clients = ClientSerializer(many=True)

    class Meta:
        model = Newsletter
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class NewsletterWithClientsSerializer(serializers.ModelSerializer):
    clients = ClientSerializer(many=True)
    messages = MessageSerializer(source='messages_send', many=True)
    messages_len = serializers.SerializerMethodField('messages_len_func')
    messages_send = serializers.SerializerMethodField('messages_sended_func')
    messages_no_send = serializers.SerializerMethodField('messages_no_sended_func')

    def messages_len_func(self, newsletter):
        return newsletter.messages_send.all().count()

    def messages_sended_func(self, newsletter):
        return newsletter.messages_send.filter(status='OK').count()

    def messages_no_sended_func(self, newsletter):
        return newsletter.messages_send.filter(status='NO').count()

    class Meta:
        model = Newsletter
        fields = '__all__'


class StatistickAllSerializer(serializers.Serializer):
    total_sended_clients = serializers.SerializerMethodField('total_sended_clients_func')
    total_not_sended_clients = serializers.SerializerMethodField('total_not_sended_clients_func')
    newsletters = serializers.SerializerMethodField('total_newsletters_func')
    active_newsletters = serializers.SerializerMethodField('total_active_newsletters_func')
    noactive_newsletters = serializers.SerializerMethodField('total_no_active_newsletters_func')
    total_clients = serializers.SerializerMethodField('total_clients_func')

    def total_sended_clients_func(self, instance):
        return Message.objects.filter(status='OK').count()

    def total_not_sended_clients_func(self, instance):
        return Message.objects.filter(status='NO').count()

    def total_newsletters_func(self, instance):
        return instance.count()

    def total_active_newsletters_func(self, instance):
        current_date = datetime.now()
        return instance.filter(
            Q(start_date__lte=current_date) & Q(end_date__gte=current_date)
        ).count()

    def total_no_active_newsletters_func(self, instance):
        current_date = datetime.now()
        return instance.filter(
            Q(start_date__gte=current_date) & Q(end_date__lte=current_date)
        ).count()

    def total_clients_func(self, instance):
        return Client.objects.all().count()

