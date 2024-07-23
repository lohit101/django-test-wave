import praw
import pyttsx3
import os
import wave
import moviepy.editor as mpy
from moviepy.editor import *
import random
import ffmpeg
import assemblyai as aai
from PIL import Image, ImageFont
from pathlib import Path
import json
import time
import threading
import shutil
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

from django.shortcuts import render, redirect, HttpResponse
from django.templatetags.static import static
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import SignupForm, LoginForm
from .models import AllUploads

engine = pyttsx3.init()
aai.settings.api_key = "1e5580a285b54d92ba4127864d759415"
BASE_DIR = Path(os.path.dirname(__file__)).parent.absolute()

FFMPEG_PATH = os.path.join(BASE_DIR, "./static/bin/ffmpeg.exe")

reddit = praw.Reddit(
    client_id="knbUbBEc4z1gwkCsTgSqtA",
    client_secret="l82ipqXjyzttMwa5DwBs0EvfdkOwaA",
    user_agent="Window11:YTFaceless:v0.1 by u/Msfvenomm",
)

cloudinary.config( 
    cloud_name = "dk3pza4u4",
    api_key = "727187743436145",
    api_secret = "KiAwpyT7ZuiNRne4MFssLYyWwfA",
    secure=True
)

# Create your views here.
def home(request):
    return render(request, 'home.html')

def initiate_dirs(request):
    print("Checking directories...")
    
    REDDIT_VIDEO_USER_ROUTE = os.path.join(BASE_DIR, 'static', 'user', str(request.user), 'RedditVideo')
    
    if os.path.isdir(REDDIT_VIDEO_USER_ROUTE) and os.path.isdir(os.path.join(REDDIT_VIDEO_USER_ROUTE, 'Images')) and os.path.isdir(os.path.join(REDDIT_VIDEO_USER_ROUTE, 'Voiceovers')) and os.path.isdir(os.path.join(REDDIT_VIDEO_USER_ROUTE, 'Transcriptions')) and os.path.isdir(os.path.join(REDDIT_VIDEO_USER_ROUTE, 'Video')):
        print('All directories exist...')
    else:
        print('Building directory structure...')
        os.makedirs(os.path.join(REDDIT_VIDEO_USER_ROUTE, 'Images'))
        os.makedirs(os.path.join(REDDIT_VIDEO_USER_ROUTE, 'Voiceovers'))
        os.makedirs(os.path.join(REDDIT_VIDEO_USER_ROUTE, 'Transcriptions'))
        if not os.path.isdir(os.path.join(REDDIT_VIDEO_USER_ROUTE, 'Video')):
            os.makedirs(os.path.join(REDDIT_VIDEO_USER_ROUTE, 'Video'))

def manual_getstory(request, subreddit):
    print("Got a  call from: ", str(request.user))
    print("\nFetching data from reddit...")
    
    initiate_dirs(request)
    
    textlistfinal = []
    textlist = []
    n = 0
    for submission in reddit.subreddit(str(subreddit)).hot(limit = 3):
        textlist.append(submission.title)
        for top_level_comment in submission.comments:
            try:
                textlist.append(top_level_comment.body)
                n += 1
                if n >= 5:
                    break
            except AttributeError:
                break
        textlistfinal.append(textlist)
        textlist = []
        n = 0
    
    response = {
        'response' : textlistfinal
    }
    
    return JsonResponse(response)

def getstory(request):
    print("Got a  call from: ", str(request.user))
    print("\nFetching data from reddit...")
    
    initiate_dirs(request)
    
    textlistfinal = []
    textlist = []
    n = 0
    for submission in reddit.subreddit("askreddit").hot(limit = 3):
        textlist.append(submission.title)
        for top_level_comment in submission.comments:
            try:
                textlist.append(top_level_comment.body)
                n += 1
                if n >= 5:
                    break
            except AttributeError:
                break
        textlistfinal.append(textlist)
        textlist = []
        n = 0
        
    print(textlistfinal)
    
    textlisttemp = []
    textlistfinalfinal = []
    
    textlisttemp.append(random.choice(textlistfinal))
    textlistfinalfinal.append(textlisttemp[0][0])
    textlistfinalfinal.append(textlisttemp[0][random.randint(1,5)])
    
    res = create_text_image(request, textlistfinalfinal)
    return res
    
def wrap_text(text, font, max_width):
    lines = []
    words = text.split()
    while words:
        line = []
        while words and (font.getbbox(' '.join(line + [words[0]]))[2] <= max_width):
            line.append(words.pop(0))
        lines.append(' '.join(line))
    return lines

def create_text_image_js(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        textlist = data['data']
        
    res = create_text_image(request, textlist)
    return res
    
def create_text_image(request, textlist: list):
    print("Creating overlay image...")
    
    REDDIT_VIDEO_USER_ROUTE = os.path.join(BASE_DIR, 'static', 'user', str(request.user), 'RedditVideo')
    
    input_image_path = os.path.join(BASE_DIR, 'static', 'bin', 'RedditVideo', 'Background', 'banner.png')
    
    output_image_path = os.path.join(REDDIT_VIDEO_USER_ROUTE, 'Images', 'PostBanner.png')
        
    text = textlist[0]
    x = 60
    y = 230
    font_size = 80
    font_color = "white"
    font_file = os.path.join(BASE_DIR, 'static', 'bin', 'fonts', 'Verdana.ttf')

    image = Image.open(input_image_path)
    image_width, image_height = image.size
    
    font = ImageFont.truetype(font_file, font_size) if font_file else ImageFont.load_default()
    
    max_width = image_width - x * 2
    lines = wrap_text(text, font, max_width)
    
    stream = ffmpeg.input(input_image_path)
    
    for i, line in enumerate(lines):
        stream = stream.drawtext(
            text=line,
            x=x,
            y=y + i * (font_size + 10),
            fontsize=font_size,
            fontcolor=font_color,
            fontfile=font_file,
            box=1,
            boxcolor='black@0.5',
            boxborderw=5
        )
    
    stream = ffmpeg.output(stream, output_image_path)
    
    try:
        stream.run(overwrite_output=True, cmd=FFMPEG_PATH)
        print(f"Text added to image and saved as {output_image_path}")
    except ffmpeg.Error as e:
        print(f"Error occurred: {e.stderr}")
    
    final_text = ""
    
    for i in textlist:
        final_text += " " + str(i) + "."
        
    
    res = audio(request, final_text)
    return res
        
def audio(request, text):
    print("Creating audio file...")
    
    REDDIT_VIDEO_USER_ROUTE = os.path.join(BASE_DIR, 'static', 'user', str(request.user), 'RedditVideo')
    
    output_audio_path = os.path.join(REDDIT_VIDEO_USER_ROUTE, 'Voiceovers', 'title.wav')
    
    engine.save_to_file(text, output_audio_path)
    engine.runAndWait()
    
    res = get_duration(request)
    return res
    
def get_duration(request):
    REDDIT_VIDEO_USER_ROUTE = os.path.join(BASE_DIR, 'static', 'user', str(request.user), 'RedditVideo')
    
    durations = []
    
    for file_path in os.listdir(os.path.join(REDDIT_VIDEO_USER_ROUTE, 'Voiceovers')):
        with wave.open(os.path.join(REDDIT_VIDEO_USER_ROUTE, 'Voiceovers', file_path), 'r') as audio_file:
            frame_rate = audio_file.getframerate()
            n_frames = audio_file.getnframes()
            duration = n_frames / float(frame_rate)
            
            durations.append(duration + 1)
            
    res = create_video(request, sum(durations))
    return res
            
def create_video(request, audio_length):
    print("Creating video file...")
    
    REDDIT_VIDEO_USER_ROUTE = os.path.join(BASE_DIR, 'static', 'user', str(request.user), 'RedditVideo')
    
    start = random.randint(10, 300)
    end = start + audio_length
    
    # Load the video clip and trim to the desired duration
    clip = VideoFileClip(os.path.join(BASE_DIR, 'static', 'bin', 'RedditVideo', 'Background', 'Video.mp4'))
    clip = clip.subclip(start, end)
    clip = clip.volumex(0)
    
    # Load the image clip
    image_path = os.path.join(REDDIT_VIDEO_USER_ROUTE, 'Images', 'PostBanner.png')
    image_clip = ImageClip(image_path).set_duration(clip.duration)
    
    # Resize the image if needed
    image_width = clip.w * 0.90
    image_height = image_clip.h * (image_width / image_clip.w)
    image_clip = image_clip.resize(width=image_width)
    
    # Set margins and position the image
    horizontal_margin = 20  # Margin from left and right sides
    image_clip = image_clip.set_position((horizontal_margin, 'center'))
    
    # Create the composite video clip with the image overlay
    composite_clip = CompositeVideoClip([clip, image_clip])
    
    # Write the final video file
    output_path = os.path.join(REDDIT_VIDEO_USER_ROUTE, 'Video', f'Video{request.user}.mp4')
    composite_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
    
    res = get_captions(request)
    return res
    
def get_captions(request):
    print("Generating captions...")
    
    REDDIT_VIDEO_USER_ROUTE = os.path.join(BASE_DIR, 'static', 'user', str(request.user), 'RedditVideo')
    
    FILE_URL = os.path.join(REDDIT_VIDEO_USER_ROUTE, 'Voiceovers', 'title.wav')

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(FILE_URL)

    with open(os.path.join(REDDIT_VIDEO_USER_ROUTE, 'Transcriptions', 'subtitle.srt'), "w") as f:
        f.write(transcript.export_subtitles_srt(30))
    f.close()

    if transcript.status == aai.TranscriptStatus.error:
        print(transcript.error)
    
    res = add_captions(request)
    return res
    
def add_captions(request):
    print("Adding subtitles...")
    
    subtitle_file = f"./static/user/{request.user}/RedditVideo/Transcriptions/subtitle.srt"
    output_file = f"./static/user/{request.user}/RedditVideo/Video/VideoSubs.mp4"
    input_file = f"./static/user/{request.user}/RedditVideo/Video/Video{request.user}.mp4"
    
    (
        ffmpeg
        .input(input_file)
        .output(
            output_file, 
            vf=f'subtitles={subtitle_file}:force_style=\'FontSize=18,PrimaryColour=&H0000FFFF,OutlineColour=&H80000000,BackColour=&H40000000,BorderStyle=1,Outline=2,MarginV=80,Bold=1',
            vcodec='libx264',
            acodec='aac', 
            strict='-2'
        )
        .run(overwrite_output=True, cmd=FFMPEG_PATH)
    )
    
    res = add_audio(request)
    return res

def add_audio(request):
    print("Adding audio...")
    
    REDDIT_VIDEO_USER_ROUTE = os.path.join(BASE_DIR, 'static', 'user', str(request.user), 'RedditVideo')
    
    clip = mpy.VideoFileClip(os.path.join(REDDIT_VIDEO_USER_ROUTE, 'Video', 'VideoSubs.mp4'))
    title = AudioFileClip(os.path.join(REDDIT_VIDEO_USER_ROUTE, 'Voiceovers', 'title.wav'))
    videoclip = clip.set_audio(title)
    videoclip.write_videofile(os.path.join(REDDIT_VIDEO_USER_ROUTE, 'Video', f'VideoFinal{request.user}.mp4'), audio=True, codec='mpeg4', bitrate='3000k', audio_codec="aac", fps=30)
    
    res = upload_to_cdn(request)
    return res
    
def upload_to_cdn(request):
    print("Uploading to CDN...")
    
    REDDIT_VIDEO_USER_ROUTE = os.path.join(BASE_DIR, 'static', 'user', str(request.user), 'RedditVideo')
    
    upload_result = cloudinary.uploader.upload_large(os.path.join(REDDIT_VIDEO_USER_ROUTE, 'Video', f'VideoFinal{request.user}.mp4'), 
        resource_type = "video",
        public_id = f"RedditVideo{request.user}{random.randint(0,25550)}"
    )
    
    print(upload_result["secure_url"])

    res = save_project(request, upload_result["secure_url"])
    return res

def save_project(request, project):
    alluploads = AllUploads()
    alluploads.usernamefk = request.user
    alluploads.upload = str(project)
    alluploads.save()

    data = {
        'response' : project
    }
    return JsonResponse(data)

def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            messages.error(request, form.errors)
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('home')
        else:
            messages.error(request, form.errors)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')

def dashboard(request):
    return render(request, 'dashboard.html')

def dashboard_reddit(request):
    return render(request, 'dashboard_reddit.html')