const http = require('http');
const websocket = require('ws');

const server = http.createServer((_, res) => {
    res.end("I am connected");
});

const wss = new websocket.Server({ server });

wss.on('connection', (ws, _) => {
    ws.on('message', (msg) => {
        console.log(msg.toString());
        wss.clients.forEach(client => {
            client.send(msg.toString());
        });
    });
});

server.listen(7001);