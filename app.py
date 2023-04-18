from flask import Flask, render_template, request
import os
import subprocess
import speech_recognition as sr
#import locale
#import unicodedata

app = Flask(__name__)

def transcribe(audio_path, language="en-GB, en-US, en-AU, nl, ru"):
    """
    This function transcribes the audio content
    
    Args:
        audio_path: string variable - the path to a specific audio to analyze any speech in it
        language: string variable - language helping to identify which one is used in audios
    
    Returns:
        A text of the audio to search function
        
    Raises:
        RequestError, UnknownValueError
    """
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

@app.route('/')
def index():
    """
    This function launches the index.html file of the website

    Returns:
        An index.html file render template
    """
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search(): 
    """
    This function provides a list of videos as a result according to user's video names and/or keywords from the search bars
    
    Args:
        video_name: string requested by POST method
        keywords: string requested by POST method
    
    Returns:
        A list of video names which will be used in order to show specific videos. In case of using keywords this list will be sorted by the amount of keywords in audio content
    """
    video_name = request.form['video_name'].lower() 
    keywords = request.form['keywords'].lower()
    #video_name = 'database' 
    #keywords = 'database'
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
                    #print(count)
                    if count >= 0: 
                        results[video] = count 
        videos = [k for k, v in sorted(results.items(), key=lambda item: item[1], reverse=True)] 
        #print(videos)
    else: 
        if video_name: 
            videos = [f for f in os.listdir('./videos') if video_name in f.lower()] 
        else: 
            videos = [f for f in os.listdir('./videos')] 
         
        if keywords: 
            results = {} 
            for video in videos: 
                audio_path = os.path.join('./audios', os.path.splitext(video)[0] + '.flac') 
                if os.path.exists(audio_path): 
                    text = transcribe(audio_path, language="en-GB, en-US, en-AU, nl, ru") 
                    count = text.lower().count(keywords) 
                    if count > 0: 
                        results[video] = count 
            videos = [k for k, v in sorted(results.items(), key=lambda item: item[1], reverse=True)] 
     
    return render_template('index.html', videos=videos)


if __name__ == '__main__':
    app.run(debug=True)