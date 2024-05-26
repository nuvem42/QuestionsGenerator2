from flask import Flask, request, jsonify, render_template
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from transformers import pipeline
import nltk

nltk.download('punkt')

app = Flask(__name__)

# Load the pre-trained T5 model and tokenizer
print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained("valhalla/t5-small-e2e-qg", model_max_length=512, legacy=False)
model = AutoModelForSeq2SeqLM.from_pretrained("valhalla/t5-small-e2e-qg")
print("Model and tokenizer loaded.")

# Define a function to generate questions
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

    # Replace the separator token with a newline character
    gen_text = gen_text.replace('<sep>', '\n')

    # Use nltk's sent_tokenize to split questions
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
from flask import Flask, request, jsonify, render_template
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline

app = Flask(__name__)

# Load the pre-trained T5 model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("valhalla/t5-small-e2e-qg", model_max_length=512, legacy=False)
model = AutoModelForSeq2SeqLM.from_pretrained("valhalla/t5-small-e2e-qg")

# Define a function to generate questions
def generate_questions(text_data, num_questions):
    # Prepare the input for the model
    input_text = f"generate questions: {text_data}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    # Generate questions
    questions = []
    for _ in range(num_questions):
        # Generate a question
        gen_ids = model.generate(
            input_ids,
            max_length=512,  # Set max_length here if needed
            num_beams=5,
            early_stopping=True,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
            length_penalty=1.0,
            no_repeat_ngram_size=2,
            bad_words_ids=[[tokenizer.unk_token_id]],
            num_return_sequences=1,
        )

        # Decode the generated question
        gen_text = tokenizer.decode(gen_ids[0], skip_special_tokens=True)

        # Append the decoded question to the list
        questions.append(gen_text)

    return questions

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    text_data = request.form['text_data']
    num_questions = int(request.form['num_questions'])
    questions = generate_questions(text_data, num_questions)
    return jsonify({'questions': questions})

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)
    print("Flask app is running.")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text_data = request.form['text_data']
        num_questions = int(request.form['num_questions'])
        questions = generate_questions(text_data, num_questions)
        return jsonify({'questions': questions})

        <h1>T5 Question Generator</h1>
        <form action="" method="post">
            <label for="text_data">Enter a paragraph text:</label><br>
            <textarea id="text_data" name="text_data" rows="10" cols="50"></textarea><br>
            <label for="num_questions">Enter the number of questions to generate:</label><br>
            <input type="number" id="num_questions" name="num_questions" value="5"><br>
            <input type="submit" value="Generate Questions">
        </form>
'''