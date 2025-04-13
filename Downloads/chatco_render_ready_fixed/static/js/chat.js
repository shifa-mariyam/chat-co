
function getCurrentTime() {
  return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}
function sendMessage() {
  const input = document.getElementById("userInput");
  const chatBox = document.getElementById("chatBox");
  const question = input.value.trim();
  if (question === "") return;

  const userMsg = document.createElement("div");
  userMsg.classList.add("message", "you");
  userMsg.innerHTML = `<strong>You:</strong><br>${question}<div class="timestamp">${getCurrentTime()}</div>`;
  chatBox.appendChild(userMsg);
  chatBox.scrollTop = chatBox.scrollHeight;

  const typing = document.createElement("div");
  typing.classList.add("message", "bot");
  typing.innerHTML = \`
    <img src="/static/logooo.png" alt="Bot Logo" />
    <span class="typing-indicator"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span>\`;
  chatBox.appendChild(typing);
  chatBox.scrollTop = chatBox.scrollHeight;

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: question }),
  })
    .then((response) => response.json())
    .then((data) => {
      typing.remove();
      const botMsg = document.createElement("div");
      botMsg.classList.add("message", "bot");
      botMsg.innerHTML = \`
        <img src="/static/logooo.png" alt="Bot Logo" />
        \${data.response}
        <div class="timestamp">\${getCurrentTime()}</div>
      \`;
      const emojiBox = document.createElement("div");
      emojiBox.classList.add("emoji-reactions");
      emojiBox.innerHTML = \`
        <button onclick="reactEmoji(this)">👍</button>
        <button onclick="reactEmoji(this)">❤️</button>
        <button onclick="reactEmoji(this)">😂</button>
      \`;
      botMsg.appendChild(emojiBox);
      chatBox.appendChild(botMsg);
      chatBox.scrollTop = chatBox.scrollHeight;
    });
  input.value = "";
}
function reactEmoji(button) {
  button.style.transform = "scale(1.3)";
  setTimeout(() => (button.style.transform = "scale(1)"), 200);
}
