from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .forms import CustomUserChangeForm
from django.http import HttpResponse

from pytube import YouTube
import qrcode
import base64
from datetime import timedelta
from io import BytesIO
import requests
import string
import random
from PIL import Image
import os
import io
import re
import jsbeautifier
import speedtest
# import cv2
# import numpy as np

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            authenticate(username=username, password=password)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        if request.user.is_authenticated:
            return redirect('home')
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('edit_profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

# @login_required
# def yt_video_downloader(request):
#     return render(request, 'yt-video-downloader.html')

@login_required
def yt_video_downloader(request):
    try:
        if request.method == 'POST':
            link = request.POST['link']
            video = YouTube(link)

            # Get the selected format from the dropdown menu
            format = request.POST.get('format')
            if format == 'lowest':
                stream = video.streams.get_lowest_resolution()
            elif format == 'highest':
                stream = video.streams.get_highest_resolution()
            else:
                stream = video.streams.get_by_resolution(format)

            # Check if the stream is valid
            if not stream:
                messages.error(request, f"Video not available in '{format}' format.")
                return render(request, 'yt-video-downloader.html')

            # Generate the download link for the video stream
            download_url = stream.url
            filename = f"{video.title}.{stream.mime_type.split('/')[-1]}"
            format_name = stream.resolution
            
            # Convert duration to minutes
            duration = str(timedelta(seconds=video.length)).split(".")[0]
            duration_in_minutes = round(video.length / 60)

            thumbnail_url = video.thumbnail_url

            return render(request, 'yt-video-downloader.html', {'download_url': download_url,
                                                               'filename': filename,
                                                               'format': format_name,
                                                               'duration': duration,
                                                               'thumbnail_url': thumbnail_url})
        return render(request, 'yt-video-downloader.html')
    except:
        messages.error(request, 'Sorry something went wrong!')
        return render(request, "yt-video-downloader.html")

@login_required
def qr_code_generator(request):
    if request.method == 'POST':
        data = request.POST['qr-text']
        # version = int(request.POST.get('qr-version', '1'))
        box_size = int(request.POST.get('qr-box-size', '10'))
        border = int(request.POST.get('qr-border-size', '5'))
        fill_color = request.POST.get('qr-fill-color', 'black')
        back_color = request.POST.get('qr-back-color', 'white')
        qr = qrcode.QRCode(version=1, box_size=box_size, border=border)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        image_data = buffer.getvalue()
        qr_code = base64.b64encode(image_data).decode('utf-8')
        context = {'qr_code': qr_code}
        return render(request, 'qr-code-generator.html', context)
    return render(request, 'qr-code-generator.html')

# def get_youtube_thumbnail(video_url):
#     video_id = video_url.split('=')[-1]
#     thumbnail_url = f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'
#     return thumbnail_url

# def yt_thumbnail_downloader(request):
#     if request.method == 'POST':
#         video_url = request.POST['video_url']
#         try:
#             thumbnail_url = get_youtube_thumbnail(video_url)
#             context = {'thumbnail_url': thumbnail_url}
#         except:
#             context = {'error_message': 'Invalid URL'}
#         return render(request, 'yt-thumbnail-downloader.html', context)
#     else:
#         return render(request, 'yt-thumbnail-downloader.html')
    
def get_youtube_thumbnail(video_url):
    try:
        response = requests.get(video_url)
        video_id = response.text.split('"videoId":"')[1].split('"')[0]
        thumbnail_dict = {
            'Highest': f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg',
            'Standard': f'https://img.youtube.com/vi/{video_id}/sddefault.jpg',
            'High': f'https://img.youtube.com/vi/{video_id}/hqdefault.jpg',
            'Medium': f'https://img.youtube.com/vi/{video_id}/mqdefault.jpg',
            'Lowest': f'https://img.youtube.com/vi/{video_id}/default.jpg'
        }
        return thumbnail_dict
    except:
        return None
    
@login_required
def yt_thumbnail_downloader(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url', '').strip()
        if video_url:
            thumbnail_dict = get_youtube_thumbnail(video_url)
            if thumbnail_dict:
                context = {'thumbnail_dict': thumbnail_dict}
            else:
                context = {'error_message': 'Unable to get thumbnail'}
        else:
            context = {'error_message': 'Please enter a YouTube video URL'}
            messages.error(request, 'Please enter a YouTube video URL')
        return render(request, 'yt-thumbnail-downloader.html', context)
    else:
        return render(request, 'yt-thumbnail-downloader.html')

@login_required
def text_tools(request):
    output_text = ''
    input_text = ''
    if request.method == 'POST':
        input_text = request.POST.get('input_text')
        if request.POST.get('uppercase'):
            output_text = input_text.upper()
        elif request.POST.get('lowercase'):
            output_text = input_text.lower()
        elif request.POST.get('titlecase'):
            output_text = input_text.capitalize()
        elif request.POST.get('reverse'):
            output_text = input_text[::-1]
        elif request.POST.get('remove_punctuations'):
            output_text = input_text.translate(str.maketrans('', '', string.punctuation))
        elif request.POST.get('remove_extra_lines'):
            output_text = "\n".join([s.strip() for s in input_text.split("\n") if s.strip()])
        elif request.POST.get('count_words'):
            output_text = "The count of the words in the text is "+str(len(input_text.split()))
        elif request.POST.get('count_characters'):
            output_text = "The count of the characters in the text is "+str(len(input_text))
        elif request.POST.get('encode'):
            input_bytes = input_text.encode('utf-8')
            output_bytes = base64.b64encode(input_bytes)
            output_text = output_bytes.decode('utf-8')
        elif request.POST.get('decode'):
            input_bytes = input_text.encode('utf-8')
            output_bytes = base64.b64decode(input_bytes)
            output_text = output_bytes.decode('utf-8')
    
    context = {
        'output_text': output_text,
        'input_text': input_text,
    }
    return render(request, 'text-tools.html', context)

def password_generator(request):
    if request.method == 'POST':
        length = int(request.POST.get('length'))
        uppercase = request.POST.get('uppercase') == 'on'
        lowercase = request.POST.get('lowercase') == 'on'
        numbers = request.POST.get('numbers') == 'on'
        symbols = request.POST.get('symbols') == 'on'

        characters = ''
        if uppercase:
            characters += string.ascii_uppercase
        if lowercase:
            characters += string.ascii_lowercase
        if numbers:
            characters += string.digits
        if symbols:
            characters += string.punctuation

        if characters:
            password = ''.join(random.choice(characters) for i in range(length))
        else:
            password = ''

        context = {
            'password': password,
            'length': length,
            'uppercase': uppercase,
            'lowercase': lowercase,
            'numbers': numbers,
            'symbols': symbols,
        }
        return render(request, 'password-generator.html', context)
    else:
        return render(request, 'password-generator.html')

def png_to_webp_convertor(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')

        # Check if file is PNG
        if not image_file.name.endswith('.png'):
            return HttpResponse('Invalid file type')

        # Open the image using PIL
        image = Image.open(image_file)

        # Create an output buffer
        output = io.BytesIO()

        # Convert the image to WebP format and save it to the output buffer
        image.save(output, 'webp')

        # Create a response with the WebP image
        response = HttpResponse(output.getvalue(), content_type='image/webp')
        response['Content-Disposition'] = f'attachment; filename="{os.path.splitext(image_file.name)[0]}.webp"'

        return response

    return render(request, 'png-to-webp-convertor.html')

def webp_to_png_convertor(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')

        # Check if file is WebP
        if not image_file.name.endswith('.webp'):
            return HttpResponse('Invalid file type')

        # Open the image using PIL
        image = Image.open(image_file)

        # Create an output buffer
        output = io.BytesIO()

        # Convert the image to PNG format and save it to the output buffer
        image.save(output, 'png')

        # Create a response with the PNG image
        response = HttpResponse(output.getvalue(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{os.path.splitext(image_file.name)[0]}.png"'

        return response

    return render(request, 'webp-to-png-convertor.html')

def png_to_jpg_convertor(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')

        # Check if file is PNG
        if not image_file.name.endswith('.png'):
            return HttpResponse('Invalid file type')

        # Open the image using PIL
        image = Image.open(image_file)

        # Create an output buffer
        output = io.BytesIO()

        # Convert the image to JPEG format and save it to the output buffer
        image.convert('RGB').save(output, 'JPEG')

        # Create a response with the JPEG image
        response = HttpResponse(output.getvalue(), content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename="{os.path.splitext(image_file.name)[0]}.jpg"'

        return response

    return render(request, 'png-to-jpg-convertor.html')

def jpg_to_png_converter(request):
    if request.method == 'POST':
        # Get the uploaded file from the request object
        image_file = request.FILES.get('image')

        # Check if file is JPG
        if not image_file.name.endswith('.jpg') and not image_file.name.endswith('.jpeg'):
            return HttpResponse('Invalid file type')

        # Open the image using PIL
        image = Image.open(image_file)

        # Create an output buffer
        output = io.BytesIO()

        # Convert the image to PNG format and save it to the output buffer
        image.save(output, 'png')

        # Create a response with the PNG image
        response = HttpResponse(output.getvalue(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{os.path.splitext(image_file.name)[0]}.png"'

        return response

    return render(request, 'jpg-to-png-converter.html')

def jpg_to_webp_converter(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')

        # Check if file is JPEG
        if not image_file.name.endswith('.jpg'):
            return HttpResponse('Invalid file type')

        # Open the image using PIL
        image = Image.open(image_file)

        # Create an output buffer
        output = io.BytesIO()

        # Convert the image to WebP format and save it to the output buffer
        image.save(output, 'webp')

        # Create a response with the WebP image
        response = HttpResponse(output.getvalue(), content_type='image/webp')
        response['Content-Disposition'] = f'attachment; filename="{os.path.splitext(image_file.name)[0]}.webp"'

        return response

    return render(request, 'jpg-to-webp-converter.html')

def image_compressor(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')

        # Open the image using PIL
        image = Image.open(image_file)

        # Convert the image to RGB color mode
        image = image.convert('RGB')

        # Compress the image
        output = BytesIO()
        image.save(output, format='JPEG', quality=60)
        output.seek(0)

        # Create a response with the compressed image
        response = HttpResponse(output.read(), content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename="{image_file.name}"'

        return response

    return render(request, 'image-compressor.html')

def css_minifier(request):
    if request.method == 'POST':
        css = request.POST['css']
        # Remove whitespace and comments from the CSS
        minified_css = re.sub(r'\s*/\*.*?\*/\s*', '', css, flags=re.DOTALL)
        minified_css = re.sub(r'\s+', ' ', minified_css)
        context = {'minified_css': minified_css.strip()}
    else:
        context = {}

    return render(request, 'css-minifier.html', context)

def js_beautifier(request):
    if request.method == 'POST':
        js = request.POST['js']
        beautified_js = jsbeautifier.beautify(js)
        return render(request, 'js-beautifier.html', {'beautified_js': beautified_js})
    return render(request, 'js-beautifier.html')

def robots_txt_generator(request):
    # Get the website URL entered by the user
    website_url = request.POST.get('url')
    return render(request, 'robots-txt-generator.html', {'website_url': website_url})

def internet_speed_test(request):
    if request.method == 'POST':
        # Run a speed test
        st = speedtest.Speedtest()
        download_speed = st.download() / 10**6
        upload_speed = st.upload() / 10**6

        # Display the results
        return render(request, 'internet-speed-test.html', {'download_speed': download_speed, 'upload_speed': upload_speed})
    else:
        return render(request, 'internet-speed-test.html')

def ip_lookup(request):
    if request.method == 'POST':
        ip_address = request.POST.get('ip_address')
        url = f'https://ipinfo.io/{ip_address}/json'
        response = requests.get(url)
        data = response.json()

        context = {
            'ip_address': ip_address,
            'city': data.get('city'),
            'region': data.get('region'),
            'country': data.get('country'),
            'org': data.get('org'),
            'postal': data.get('postal'),
            'timezone': data.get('timezone'),
            'latitude': data.get('loc', '').split(',')[0],
            'longitude': data.get('loc', '').split(',')[1],
        }

        return render(request, 'ip-lookup.html', context)

    return render(request, 'ip-lookup.html')

def tools (request):
    return render(request, 'tools.html')

# def image_background_remover(request):
#     if request.method == 'POST':
#         # Get the uploaded image
#         image_file = request.FILES.get('image')
        
#         # Read the image using OpenCV
#         image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        
#         # Convert the image to BGRA
#         bgra_image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        
#         # Convert the image to grayscale
#         gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
#         # Threshold the grayscale image to create a mask
#         mask = cv2.threshold(gray_image, 250, 255, cv2.THRESH_BINARY)[1]
        
#         # Invert the mask
#         mask = cv2.bitwise_not(mask)
        
#         # Apply morphological operations to the mask to remove noise
#         kernel = np.ones((3, 3), np.uint8)
#         mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
#         mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
#         # Blur and stretch the mask
#         mask = cv2.GaussianBlur(mask, (0, 0), sigmaX=2, sigmaY=2, borderType=cv2.BORDER_DEFAULT)
#         mask = (2 * (mask.astype(np.float32)) - 255.0).clip(0, 255).astype(np.uint8)
        
#         # Apply the mask to the image
#         result_image = bgra_image.copy()
#         result_image[:, :, 3] = mask
        
#         # Convert the image back to BGR for display purposes
#         bgr_image = cv2.cvtColor(result_image, cv2.COLOR_BGRA2BGR)
        
#         # Convert the image to JPEG format and compress it
#         output = cv2.imencode('.jpg', bgr_image, [cv2.IMWRITE_JPEG_QUALITY, 80])[1].tobytes()
        
#         # Create a response with the compressed image
#         response = HttpResponse(output, content_type='image/jpeg')
#         response['Content-Disposition'] = f'attachment; filename="{image_file.name}"'
        
#         # Render the template with the uploaded and compressed images
#         return response

#     return render(request, 'image-background-remover.html')

# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect

# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             authenticate(username=username, password=password)
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'register.html', {'form': form})

# @login_required
# def dashboard(request):
#     return render(request, 'dashboard.html')

# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('dashboard')
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('dashboard')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})

# def logout_view(request):
#     logout(request)
#     return redirect('login')
