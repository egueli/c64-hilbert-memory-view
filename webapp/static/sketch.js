var currentTimestamp;
var microsecondsPerFrame = 20000;

var traceInfo;

function preload() {
	traceInfo = loadJSON("/info");
	setFrameRate(50);
}

function setup() {
	console.log(traceInfo);
	currentTimestamp = traceInfo.firstTimestamp;
}

var needData = true;

function draw() {
	if (needData) {
		loadJSON("/trace?from=" + currentTimestamp + "&to=" + (currentTimestamp + microsecondsPerFrame), onDataForFrame);
		needData = false;
	}
}

function onDataForFrame(data) {
	needData = true;
	console.log(data);
}