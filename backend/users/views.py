from django.contrib.auth import get_user_model
from rest_framework import viewsets
from users.serializers import UserSerializer
from payments.models import BillingInfo, Address

from rest_framework.decorators import api_view, parser_classes
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import json
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.shortcuts import render

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ("email",)

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class SignUp(generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@api_view(['GET'])
def get_address(request):
    user = request.user

    try:
        billing_info = BillingInfo.objects.get(customer=user)
        address = billing_info.delivery_address
        to_send = address.to_json()
    except:
        to_send = ''

    return JsonResponse(to_send, safe=False)

@api_view(['POST'])
def set_address(request):
    current_user = request.user
    address_json = json.loads(request.POST.get('address_json'))
    line_1 = address_json['line_1']
    line_2 = address_json['line_2']
    city = address_json['city']
    state = address_json['state']
    zip = address_json['zip']
    country = address_json['country']

    if line_1 is '':
        return HttpResponse(status=403)

    new_address = Address(line_1=line_1, line_2=line_2, city=city, state=state, zip=zip, country=country)
    new_address.save()

    try:
        billing_info = BillingInfo.objects.get(customer=current_user)

        # Delete Old Address
        if billing_info.delivery_address is not None:
            billing_info.delivery_address.delete()

        billing_info.delivery_address = new_address
        billing_info.save()
    except:
        billing_info = BillingInfo(customer=current_user, delivery_address=new_address)
        billing_info.save()

    return JsonResponse(new_address.to_json())