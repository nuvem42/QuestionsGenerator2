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
