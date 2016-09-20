var microsecondsPerFrame = 200;
var oneStepOnly = true;

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
	mapSetup();
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
	if (!oneStepOnly) {
		needData = true;
	}
	currentTimestamp += microsecondsPerFrame;
	if (currentTimestamp >= traceInfo.lastTimestamp)
		reset();

	updateMap(data)
	updateTraceGraphics(data);

	background(0);
	drawMap();
	blendMode(ADD);
	drawTraceGraphics();
	blendMode(BLEND);
}