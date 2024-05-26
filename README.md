# QuestionsGenerator2


# Step 1: create and activate enviroment
python -m venv venv
source venv/bin/activate
pip install sentencepiece protobuf torch transformers flask nltk


# Step 2: Create a new Flask project

mkdir t5-question-generator
cd t5-question-generator

# step 3: Create a new file app.py and add the following code:
'''
from flask import Flask, request, jsonify, render_template
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from transformers import pipeline
import nltk
nltk.download('punkt')
app = Flask(__name__)
'''Load the pre-trained T5 model and tokenizer'''
print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained("valhalla/t5-small-e2e-qg", model_max_length=512, legacy=False)
model = AutoModelForSeq2SeqLM.from_pretrained("valhalla/t5-small-e2e-qg")
print("Model and tokenizer loaded.")
'''Define a function to generate questions'''
def generate_questions(text_data):
    input_text = f"generate questions: {text_data}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    gen_ids = model.generate(
        input_ids,
        max_length=512,
        num_beams=5,
        early_stopping=True,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
        length_penalty=1.0,
        no_repeat_ngram_size=2,
        bad_words_ids=[[tokenizer.unk_token_id]],
        num_return_sequences=1,
    )
    gen_text = tokenizer.decode(gen_ids[0], skip_special_tokens=True)

    '''Replace the separator token with a newline character'''
    gen_text = gen_text.replace('<sep>', '\n')

    '''Use nltk's sent_tokenize to split questions'''
    questions = nltk.sent_tokenize(gen_text)
    return questions

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    text_data = request.form['text_data']
    questions = generate_questions(text_data)
    return jsonify({'questions': questions})

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)
    print("Flask app is running.")

'''

# Step 4: Create a folder called "templates" and add a html file called "index.html"
'''
<!DOCTYPE html>
<html>
<head>
  <title>T5 Question Generator</title>
  <style>
    form {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    label {
      margin-bottom: 10px;
    }
    textarea {
      margin-bottom: 10px;
    }
    #questions {
      max-width: 50%; /* adjust the width to your liking */
      margin: 20px auto; /* add some margin to create space around the questions */
      padding: 20px; /* add some padding to create space between the questions and the border */
      border: 1px solid #ccc; /* add a border to visually separate the questions */
      border-radius: 10px; /* add some rounded corners to the border */
    }
    .container {
  text-align: center;
  padding: 20px;
  

    }
    .container > * {
      width: 100%; /* make all child elements take up the full width */
    }
    .container > h1 {
      margin-bottom: 20px; /* add some margin to create space between the title and the form */
    }
  </style>
</head>
<body style="background-image: url('static/Design sem nome.jpg'); background-size: cover; background-repeat: no-repeat; background-attachment: fixed; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
  <div class="container">
    <h1>T5 Question Generator</h1>
    <form id="question-form">
      <label for="text_data">Enter a paragraph text:</label>
      <textarea id="text_data" name="text_data" rows="10" cols="50"></textarea>
      <button type="submit">Generate Questions</button>
    </form>
    <div id="questions">
      <h2>Generated Questions:</h2>
      <ul id="questions-list"></ul>
    </div>
  </div>
  <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>
'''

# Step 5: creat a folder called "static" and add your background image and a js file called "script.js"
'''
document.getElementById('question-form').addEventListener('submit', function(event) {
  event.preventDefault();
  const formData = new FormData(this);
  fetch('/generate', {
    method: 'POST',
    body: formData
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok ' + response.statusText);
    }
    return response.json();
  })
  .then(data => {
    const questionsList = document.getElementById('questions-list');
    questionsList.innerHTML = '';
    data.questions.forEach(question => {
      const listItem = document.createElement('li');
      listItem.textContent = question;
      questionsList.appendChild(listItem);
    });
  })
  .catch(error => {
    console.error('Error:', error);
  });
});
'''
