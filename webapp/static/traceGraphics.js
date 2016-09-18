var traceClearAlpha = 20;
var executeColor = '#ffffff';
var readColor = '#00ff00';
var writeColor = '#ff0000';
var mapScale = 2;

var traceGraphics;
var density = window.devicePixelRatio; // happens to be 2 on os x with retina display

function setupTraceGraphics() {
	traceGraphics = createGraphics(512 * density, 512 * density);
}

function updateTraceGraphics(frameData) {
	var tg = traceGraphics;

	tg.background(0, traceClearAlpha);

	if (!frameData)
		return;

	tg.noStroke();
	tg.fill(readColor);
	drawAccesses(tg, frameData.accesses.read);
	tg.fill(writeColor);
	drawAccesses(tg, frameData.accesses.write);
	tg.fill(executeColor);
	drawAccesses(tg, frameData.accesses.execute);
}

function drawAccesses(tg, accesses) {
	console.log('drawAccesses', accesses)
	for (var i = 0; i < accesses.length; i++) {
		var address = accesses[i];
		var xy = hilbert.d2xy(8, address);
		tg.rect(xy[0] * mapScale, xy[1] * mapScale, mapScale, mapScale);
	}
}

function drawTraceGraphics() {
	image(traceGraphics, 0, 0, 512 * density, 512 * density, 0, 0, 512, 512);
}