var currentTimestamp;
var microsecondsPerFrame = 20000;

var traceInfo;

function preload() {
	traceInfo = loadJSON("/info");
	setFrameRate(50);
}

function setup() {
	console.log(traceInfo);
	reset();
}

var needData = true;

function draw() {
	if (needData) {
		loadJSON("/trace?from=" + currentTimestamp + "&to=" + (currentTimestamp + microsecondsPerFrame), onDataForFrame);
		needData = false;
	}
}

function reset() {
	currentTimestamp = traceInfo.firstTimestamp;
	
}

function onDataForFrame(data) {
	// needData = true;
	console.log(data);
	currentTimestamp += microsecondsPerFrame;
	if (currentTimestamp >= traceInfo.lastTimestamp)
		reset();

	updateTraceGraphics(data);
	blendMode(ADD);
	drawTraceGraphics();
	blendMode(BLEND);
}