from django.shortcuts import render
from django.http import HttpResponse
import google.generativeai as genai
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
import html
from PIL import Image
from io import BytesIO


# Create your views here.
def home(request):
    genai.configure(api_key=settings.GEMINI_API)
    chat = genai.GenerativeModel('gemini-pro').start_chat(history=[])
    chat_img = genai.GenerativeModel('gemini-pro-vision')
    globals()['chat_session'] = chat
    globals()['chat_session_img'] = chat_img
    return render(request,'home.html')

@api_view(['POST'])
def send_prompt(request):
    print("only prompt....")
    chat_session_text = globals()['chat_session']
    response = chat_session_text.send_message(request.POST['message'])
    return Response({'reply':html.unescape(response.text)})
   


@api_view(['POST'])
def send_image(request):
    print('Both') 

    chat_session_image = globals()['chat_session_img']
    name_format = request.FILES['file'].name.split('.')[-1]
    file_data = request.FILES['file'].read()
    file_data = Image.open(BytesIO(file_data))
    print(file_data)
    cookie_picture = [{
        'mime_type': name_format,
        'data': file_data
    }]
    prompt = request.POST['message']
    response = chat_session_image.generate_content(

            [prompt, file_data], stream=False
    )
    return Response({'reply':html.unescape(response.text)})

    


@api_view(['POST'])
def send_only_image(request): 

    chat_session_image = globals()['chat_session_img']
    name_format = request.FILES['file'].name.split('.')[-1]
    file_data = request.FILES['file'].read()
    file_data = Image.open(BytesIO(file_data))
    print(file_data)
    cookie_picture = [{
        'mime_type': name_format,
        'data': file_data
    }]

    response = chat_session_image.generate_content( file_data, stream=False )
    return Response({'reply':html.unescape(response.text)})