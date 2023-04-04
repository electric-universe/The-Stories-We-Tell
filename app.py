from flask import Flask, render_template, request
import openai

openai.api_key = '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'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    user_input = request.form['user_input']
    story = generate_story(user_input)  # Call the generate_story function
    return render_template('story.html', story=story)

def generate_story(user_input):
    prompt = f"Create a short story based on the user's input: {user_input}"
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
