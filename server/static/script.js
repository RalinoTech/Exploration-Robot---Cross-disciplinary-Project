// Gestion des touches Q, S, D et Z
const arrowKeys = ['q', 's', 'd', 'z'];
let arrowPressedKeys = []; // Liste des touches Q, S, D et Z actuellement enfoncées

document.addEventListener('keydown', function (event) {
    const key = event.key.toLowerCase();
    if (arrowKeys.includes(key) && !arrowPressedKeys.includes(key)) {
        arrowPressedKeys.push(key); // Ajoute la touche actuellement enfoncée à la liste
        document.getElementById('key' + key.toUpperCase()).classList.add('key-pressed');
    }
});

document.addEventListener('keyup', function (event) {
    const key = event.key.toLowerCase();
    if (arrowKeys.includes(key)) {
        const index = arrowPressedKeys.indexOf(key);
        if (index > -1) {
            arrowPressedKeys.splice(index, 1); // Retire la touche relâchée de la liste
            document.getElementById('key' + key.toUpperCase()).classList.remove('key-pressed');
        }
    }
});

// Fonction pour envoyer les touches enfoncées au serveur Flask
function sendPressedKeys() {
    arrowPressedKeys.forEach(function (key) {
        sendData(key); // Envoie la touche enfoncée au serveur Flask
    });
}

// Envoie les touches enfoncées toutes les 100 millisecondes
setInterval(sendPressedKeys, 100);


const speedKeys = ['k', 'l', 'm'];
let activeSpeed = null;

document.addEventListener('keydown', function (event) {
    const key = event.key;
    if (speedKeys.includes(key)) {
        // Si la touche actuelle est déjà active, la désactiver
        if (activeSpeed === key) {
            document.getElementById('key' + key).classList.remove('key-pressed');
            activeSpeed = null;
        } else { // Sinon, activer la touche actuelle et désactiver la touche précédemment activée
            if (activeSpeed) {
                document.getElementById('key' + activeSpeed).classList.remove('key-pressed');
            }
            document.getElementById('key' + key).classList.add('key-pressed');
            activeSpeed = key;
            sendData(key); // Envoie la touche enfoncée au serveur Flask
        }
    }
});

function sendData(key) {
    const xhr = new XMLHttpRequest();
    const url = '/input?inp=' + key;
    xhr.open('GET', url, true);
    xhr.send();
}
