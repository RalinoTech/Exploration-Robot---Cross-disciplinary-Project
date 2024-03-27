const validKeys = ['q', 's', 'd', 'z'];
const display = document.getElementById('keyPressed');
let pressedKeys = []; // Liste des touches actuellement enfoncées

document.addEventListener('keydown', function (event) {
    const key = event.key.toLowerCase();
    if (validKeys.includes(key) && !pressedKeys.includes(key)) {
        pressedKeys.push(key); // Ajoute la touche actuellement enfoncée à la liste
        document.getElementById('key' + key.toUpperCase()).classList.add('key-pressed');
        sendData(key); // Envoie la touche enfoncée au serveur Flask
    }
});

document.addEventListener('keyup', function (event) {
    const key = event.key.toLowerCase();
    if (pressedKeys.includes(key)) {
        pressedKeys = pressedKeys.filter(k => k !== key); // Retire la touche relâchée de la liste
        display.style.color = '#333';
        document.getElementById('key' + key.toUpperCase()).classList.remove('key-pressed');
    }
});

function sendData(key) {
    const xhr = new XMLHttpRequest();
    const url = '/input?inp=' + key;
    xhr.open('GET', url, true);
    xhr.send();
}
