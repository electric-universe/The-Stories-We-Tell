from flask import Flask, render_template, request, url_for

import openai
import requests
from io import BytesIO
import os

openai.api_key = os.environ.get('OPENAI_API_KEY')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    user_input = request.form['user_input']
    story_type = request.form['story_type']
    # process the form data and generate the story and image
    title, story, image_url = generate_story_and_image(story_type, user_input)

    return render_template('story.html', title=title, story=story, user_input=user_input, image_url=image_url)

@app.route('/share', methods=['GET', 'POST'])
def share():
    if request.method == 'POST':
        title = request.form['title']
        story = request.form['story']
        image_url = request.form['image_url']
        return render_template('share.html', title=title, story=story, image_url=image_url, url=request.url)
    else:
        title = request.args.get('title')
        story = request.args.get('story')
        image_url = request.args.get('image_url')
        return render_template('share.html', title=title, story=story, image_url=image_url)

@app.route('/story')
def story():
    title = request.args.get('title')
    story = request.args.get('story')
    user_input = request.args.get('user_input')
    image_url = request.args.get('image_url')
    return render_template('story.html', title=title, story=story, user_input=user_input, image_url=image_url)

def generate_story_and_image(story_type, user_input):
    if story_type == 'sad':
        prompt = f"Write a sad story based on the user's input: {user_input}"
        title = 'Sad Story'
    elif story_type == 'funny':
        prompt = f"Write a funny story based on the user's input: {user_input}"
        title = 'Funny Story'
    else:
        prompt = f"Write a horror story based on the user's input: {user_input}"
        title = 'Horror Story'
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    story = response.choices[0].text.strip()
    
    # generate image based on the story
    response = openai.Image.create(
        prompt=story,
        n=1,
        size="512x512",
        response_format="url"
    )
    image_url = response['data'][0]['url']
    
    return title, story, image_url

if __name__ == '__main__':
    app.run(debug=True)
