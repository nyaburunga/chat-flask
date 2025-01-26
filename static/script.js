const socket = io();
const messages = document.getElementById('messages');
const sendBtn = document.getElementById('send-btn');
const messageInput = document.getElementById('message-input');
const themeToggle = document.getElementById('theme-toggle');
const disconnectBtn = document.getElementById('disconnectBtn');
const messageSound = new Audio('/static/notification.mp3');

let username = prompt('Entrez votre nom :') || 'Anonyme';

socket.emit('chatMessage', { sender: 'System', message: `${username} a rejoint le chat.` });

sendBtn.addEventListener('click', () => {
    const message = messageInput.value.trim();
    if (message) {
        socket.emit('chatMessage', { sender: username, message });
        messageInput.value = '';
    }
});

socket.on('message', (data) => {
    addMessage(data.sender, data.message, data.sender === username);
    if (data.sender !== username) {
        messageSound.play();
    }
});

socket.on('deleteMessage', (data) => {
    alert('Un message a été supprimé par un administrateur.');
});

disconnectBtn.addEventListener('click', () => {
    socket.disconnect();
    alert('Vous avez quitté le chat.');
    location.reload();
});

themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark');
});

document.querySelectorAll('.reaction').forEach((button) => {
    button.addEventListener('click', () => {
        if (username) {
            const reaction = button.textContent;
            socket.emit('chatMessage', { sender: username, message: reaction });
        }
    });
});

function addMessage(sender, message, isMyMessage) {
    const div = document.createElement('div');
    div.classList.add(isMyMessage ? 'my-message' : 'other-message');
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    div.innerHTML = `<strong>${sender}</strong> <span class="timestamp">${time}</span>: ${message}`;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}
