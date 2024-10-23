const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

// Create an Express application
const app = express();

// Create a HTTP server and bind it with Express
const server = http.createServer(app);

// Bind Socket.IO to the server
const io = socketIo(server);

// Utility function for delay
function sleepFor(sleepDuration){
  var now = new Date().getTime();
  while(new Date().getTime() < now + sleepDuration){ 
      /* Do nothing */ 
  }
}

// When a client connects
io.on('connection', (socket) => {
  console.log('A user connected');

  // Simulate a big process
  const simulateBigProcess = () => {
    console.log('Simulating a big process...');
    let progress = 0;

    while (progress < 100) {
      // Simulate work
      progress += 10;
      socket.emit('progress', { progress });
      console.log("Progress: ", progress);
      sleepFor(3000);
    }

    socket.emit('complete', { message: 'Process complete!' });
  };

  // Listen for a custom event from the client
  socket.on('execute_command', (data) => {
    socket.emit('server_response', { message: 'Message received' });
      simulateBigProcess();
      console.log(`Received message from client: ${data.message}`);
      // Optionally, send a response back to the client
  });

  // When the client disconnects
  socket.on('disconnect', () => {
    console.log('A user disconnected');
  });
});

// Start the server
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
