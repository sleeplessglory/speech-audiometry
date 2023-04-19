from flask import Flask, render_template, request
import os
import subprocess
import speech_recognition as sr
#import locale
#import unicodedata

def transcribe(audio_path, language="en-GB, en-US, en-AU, nl, ru"):
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language=language)
        return text
    except sr.UnknownValueError:
        return "Unable to recognize speech"
    except sr.RequestError as e:
        return f"Error: {e}"

def search(video_name, keywords): 
    video_name = video_name.lower() 
    keywords = keywords.lower()

    videos = [] 
     
    if video_name and keywords: 
        results = {} 
        for video in os.listdir('./videos'): 
            if video_name in video.lower(): 
                audio_path = os.path.join('./audios', os.path.splitext(video)[0] + '.flac') 
                if os.path.exists(audio_path): 
                    #print(audio_path)
                    text = transcribe(audio_path, language="en-GB, en-US, en-AU, nl, ru") 
                    #print(text)
                    count = text.lower().count(keywords) 
                    print("Video:", video, "\nAmount of keywords:", count)
                    if count >= 0: 
                        results[video] = count 
        videos = [k for k, v in sorted(results.items(), key=lambda item: item[1], reverse=True)] 
        print("List of videos by name and keywords:", videos, "\n")

    else: 
        if video_name: 
            videos = [f for f in os.listdir('./videos') if video_name in f.lower()] 
            print("List of videos by name:", videos, "\n")

        else: 
            videos = [f for f in os.listdir('./videos')] 
         
        if keywords: 
            results = {} 
            for video in videos: 
                audio_path = os.path.join('./audios', os.path.splitext(video)[0] + '.flac') 
                if os.path.exists(audio_path): 
                    text = transcribe(audio_path, language="en-GB, en-US, en-AU, nl, ru") 
                    count = text.lower().count(keywords) 
                    print("Video:", video, "\nAmount of keywords:", count)
                    if count > 0: 
                        results[video] = count 
            videos = [k for k, v in sorted(results.items(), key=lambda item: item[1], reverse=True)]
            print("List of videos by keywords:", videos, "\n") 



examples=["matrix", "mAtRIX", "MATRIX", "Matrix", #checking capitalized letters
          "matrices", "determinant", "database", "relational", "определитель",
          "😍😍🍦🔑😎", "🎡👓💾💿🎥🎵🎶💎🥇🔒🔑🔋📲🎬📽⏰🍕🍟🍦🚑✈🌏💚💙💜🖤💖💘🟥", #checking emojis
          "хранилище", "хранилища", "лекция", "архитектура", "модель", "базы данных", "база", "data", 
          "SDuifpdfg930=2*/", "123kndsf*456", #checking random requests
          "++++++++++_____", "1245@$$@%&()(*)(())", "/**-@:!!!!&&@???xsine",
          "($$)@()(___#%*!!!/*-*-*--\\\||||??DSklIFOIE)3/*7/-88))_________---@)#$@999900@#98235&#ybjdsfgaef6WD#&#"] #checking longer random requests
def test_name():
    print("_______________________________________________\n         Tests by only video names")
    keywords=""
    for i in range(len(examples)):
        video_name=examples[i]
        print("Test for a video name: ", video_name)
        search(video_name, keywords)
def test_keywords():
    print("_______________________________________________\n            Tests by only keywords")
    video_name=""
    for i in range(len(examples)):
        keywords=examples[i]
        print("Test for keywords: ", keywords)
        search(video_name, keywords)
def test_name_keywords():
    print("_______________________________________________\n       Tests by video names and keywords")
    for i in range(len(examples)):
        video_name=examples[i]
        keywords=examples[i]
        print("Test for a video name:", video_name, "and keywords:", keywords)
        search(video_name, keywords)
test_name()
test_keywords()
test_name_keywords()
