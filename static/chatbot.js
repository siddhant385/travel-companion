function closeChat() {
  document.querySelector('.chat-box').style.display = 'none';
}

function sendMessage() {
  const userInput = document.getElementById('user-input').value;
  if (userInput.trim()) {
      const userMessage = document.createElement('div');
      userMessage.classList.add('message', 'user-message');
      userMessage.innerHTML = `<p>${userInput}</p>`;
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
          botMessage.innerHTML = `<p>${data.response}</p>`;
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
