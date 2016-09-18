var microsecondsPerFrame = 20000;
var screenshotWidth = 384;
var screenshotHeight = 272;

var traceInfo;
var currentTimestamp;

function preload() {
	traceInfo = loadJSON("/info");
	setFrameRate(50);
	setupTraceGraphics();
}

function setup() {
	createCanvas(512 + screenshotWidth, 512);
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

	background(0);
	updateTraceGraphics(data);
	blendMode(ADD);
	drawTraceGraphics();
	blendMode(BLEND);
}