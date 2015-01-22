#Useage

##Create
Create a new streamer: `var streamer = new Streamer();`

##Start
Start it: `streamer.connect();`

##Use
make a request to the server: `streamer.request('AF3') or streamer.request(['AF3', 'AF4']);`

On a response from the server, the Streamer triggers an event 'bufferUpdated' on the body.

Data can be consumed from the streamer by: `streamer.consumeData()`