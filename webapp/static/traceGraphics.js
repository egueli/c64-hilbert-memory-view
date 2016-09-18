var traceGraphics;
var density = window.devicePixelRatio; // happens to be 2 on os x with retina display

function setupTraceGraphics() {
  traceGraphics = createGraphics(512 * density, 512 * density);
}

function updateTraceGraphics(frameData) {
	
}

function drawTraceGraphics() {
	image(traceGraphics, 0, 0, 512 * density, 512 * density, 0, 0, 512, 512);
}