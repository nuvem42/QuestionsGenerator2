# QuestionsGenerator
This project used t5-small-e2e-qg model to generate questions based on an input text
Read this article to understand more about how the project works and the idea behind it: https://medium.com/insights-of-nature/ed-ai-question-generation-ai-models-and-how-you-can-build-one-115e3df8825c 

References that I used to relicate this project:
    - https://huggingface.co/valhalla/t5-small-e2e-qg/tree/main
    - generating questions with transformers - https://github.com/patil-suraj/question_generation/blob/master/README.md
    - hugging face transformers - https://huggingface.co/docs/transformers/main/en/index
    - end to end question generation - https://arxiv.org/pdf/2005.01107v1.pdf


## Create the following files and organize them this way:
    | Question generator
      | app.py
      | templates
         | index.html
      | static
         | script.js
         | background image.jpg

## Remember to create and activate a virtual enviroment

    python -m venv venv

    source venv/bin/activate

    pip install sentencepiece protobuf torch transformers flask nltk

### Remember that to run the app.py in your codespace you need to activate the virtual enviroment 
