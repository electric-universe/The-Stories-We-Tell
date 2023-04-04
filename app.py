from flask import Flask, render_template, request
import openai
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
    # process the form data and generate the story
    title, story = generate_story(story_type, user_input)

    return render_template('story.html', title=title, story=story, user_input=user_input)


def generate_story(story_type, user_input):
    if story_type == 'sad':
        prompt = f"Write a sad story based on the user's input: {user_input}"
    elif story_type == 'funny':
        prompt = f"Write a funny story based on the user's input: {user_input}"
    else:
        prompt = f"Write a horror story based on the user's input: {user_input}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    story = response.choices[0].text.strip()
    title = response.choices[0].text.strip().split('.')[0]  # Extract first sentence as title
    return title, story

if __name__ == '__main__':
    app.run(debug=True)
