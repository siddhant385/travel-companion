
console.log(marked)

function closeChat() {
  document.querySelector('.chat-box').style.display = 'none';
}

function sendMessage() {
  const userInput = document.getElementById('user-input').value;
  if (userInput.trim()) {
      const userMessage = document.createElement('div');
      userMessage.classList.add('message', 'user-message');
      
      // Convert user input (Markdown) to HTML using marked.js
      userMessage.innerHTML = `<p>${marked.parse(userInput)}</p>`;
      document.getElementById('chat-content').appendChild(userMessage);

      // Send message to Flask API
      fetch("/chat", {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          body: JSON.stringify({ message: userInput })
      })
      .then(response => response.json())
      .then(data => {
          const botMessage = document.createElement('div');
          botMessage.classList.add('message', 'bot-message');
          
          // Convert bot's response (Markdown) to HTML using marked.js
          botMessage.innerHTML = `<p>${marked.parse(data.response)}</p>`;
          document.getElementById('chat-content').appendChild(botMessage);

          // Scroll to the bottom
          document.getElementById('chat-content').scrollTop = document.getElementById('chat-content').scrollHeight;
      })
      .catch(error => {
          console.error("Error:", error);
      });

      // Clear input field
      document.getElementById('user-input').value = '';
  }
}

