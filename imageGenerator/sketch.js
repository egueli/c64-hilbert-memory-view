// configuration
var traceFileName = 'simple_basic.ctrace';
var mapScale = 2;
var timeScale = 1;
var startAtTime = 0;
var stopAtTime = 100000;
var saveAllFrames = false;
var showText = true;
var fps = 60;
var traceClearAlpha = 20;


// global variables
var endFrameNum = 0;
var firstLoop = true;
var frames = [];
var firstFrameNum;

var microsecsPerFrame = Math.floor(1000000 / fps);

var traceGraphics;
var mapGraphics;

var density = window.devicePixelRatio; // happens to be 2 on os x with retina display

var screenshotWidth = 384;
var screenshotHeight = 272;
var executeColor = '#ffffff';
var readColor = '#00ff00';
var writeColor = '#ff0000';

function preload() {
  trace = loadStrings('assets/traces/' + traceFileName);
}

function setup() {
  createCanvas(512 + screenshotWidth, 512);
  traceGraphics = createGraphics(512 * density, 512 * density);
  mapGraphics = createGraphics(512 * density, 512 * density);
  setFrameRate(fps);

  printMap();

  processTrace();

  // Uncomment this to save the map to PNG.
  //save('map.png');
}

function processTrace() {
  console.log("will read " + trace.length + " lines")
  for (var i=0; i<trace.length; i++) {
    var line = trace[i];
    var tokens = line.split(" ");
    var timestamp = tokens[0];


    var frameNum = Math.floor(timestamp / microsecsPerFrame * timeScale);
    var frame;
    if (!frames[frameNum]) {
      frame = {
        timestamp: timestamp,
        time: timestamp / 1000000,
        reads: [],
        writes: [],
        executes: []
      };
      frames[frameNum] = frame;
      endFrameNum = frameNum;
      if (firstFrameNum === undefined)
        firstFrameNum = frameNum
    }
    else {
      frame = frames[frameNum];
    }

    if (tokens[1] == 'screenshot') {
      frame.screenshot = tokens[2];
    }
    else {
      var nGroups = 0, nAccesses = 0;
      for (var t = 1; t < tokens.length; t++, nGroups++) {
        var accessFields = tokens[t].split(':')
        var accessTypes = accessFields[0];
        var accesses;
        switch(accessTypes) {
          case 'r': accesses = frame.reads; break;
          case 'w': accesses = frame.writes; break;
          case 'x': accesses = frame.executes; break;
        }
        var rangeStart = parseInt(accessFields[1])
        var rangeLen = parseInt(accessFields[2])
        for (var a = 0; a < rangeLen; a++, nAccesses++) {
          accesses[rangeStart + a] = 1
        }
      }
    }
  }

  trace = null;
  console.log(frames.length);
}

function printMap() {
  var mg = mapGraphics;

  mg.textAlign(CENTER, CENTER);
  mg.textSize(12);

  function addrBlock(color, desc) {
    return function(x, y, size) {
      x *= mapScale * density;
      y *= mapScale * density;
      size *= mapScale * density;
      mg.fill(color);
      mg.rect(x, y, size, size);

      mg.fill(128);
      mg.text(desc, x, y, size, size);
    };
  }
  var ramColor = '#004000';
  var romColor = '#000080';
  var ioColor = '#800000';

  hilbertBlock(8, 0x0000, 0x10000, addrBlock(ramColor, "RAM"))

  hilbertBlock(8, 0x0000, 0x0100, addrBlock(ramColor, "System vars"));
  hilbertBlock(8, 0x0100, 0x0100, addrBlock(ramColor, "Stack"));
  hilbertBlock(8, 0x0200, 0x0100, addrBlock(ramColor, "System vars"));
  hilbertBlock(8, 0x0300, 0x0100, addrBlock(ramColor, "System vars"));
  
  hilbertBlock(8, 0x0400, 0x0400, addrBlock(ramColor, "Video memory"));

  hilbertBlock(8, 0xA000, 0x1000, addrBlock(romColor, "BASIC ROM"))
  hilbertBlock(8, 0xB000, 0x1000, addrBlock(romColor, "BASIC ROM"))
    
  hilbertBlock(8, 0xD000, 0x0400, addrBlock(ioColor, "VIC-II"))
  hilbertBlock(8, 0xD400, 0x0400, addrBlock(ioColor, "SID"))
  hilbertBlock(8, 0xD800, 0x0400, addrBlock(ioColor, "Color RAM"))
  hilbertBlock(8, 0xDC00, 0x0100, addrBlock(ioColor, "CIA #1"))
  hilbertBlock(8, 0xDD00, 0x0100, addrBlock(ioColor, "CIA #2"))
  hilbertBlock(8, 0xDE00, 0x0100, addrBlock(ioColor, "I/O #1"))
  hilbertBlock(8, 0xDF00, 0x0100, addrBlock(ioColor, "I/O #2"))
  
  hilbertBlock(8, 0xE000, 0x1000, addrBlock(romColor, "KERNAL ROM"));
  hilbertBlock(8, 0xF000, 0x1000, addrBlock(romColor, "KERNAL ROM"));
}

function hilbertBlock(maxLevel, location, sizeLinear, callback) {
  var level = Math.log2(sizeLinear) / 2;
  var size = 1 << (level - 1);

  var xy = hilbert.d2xy(maxLevel - level, location / sizeLinear);
  var x = xy[0] * size;
  var y = xy[1] * size;

  callback(x, y, size);
}


var startFrameNum = startAtTime * fps * timeScale;
var frameNum = startFrameNum;
var currentScreenshotImage;
var loadingScreenshot;
var saveFrameSeq = 0;

function draw() {
  if (frameNum > endFrameNum - firstFrameNum) {
    console.log("end of trace, looping");
    frameNum = startFrameNum;
    firstLoop = false;
    return;
  }

  var frameData = frames[firstFrameNum + frameNum];

  if (!frameData) {
    console.log("empty frame " + frameNum);
    return;
  }

  if (frameData.time >= stopAtTime) {
    console.log("reached stopAtTime, looping");
    frameNum = startFrameNum;
    firstLoop = false;
    return;
  }

  if (frameData.screenshot) {
    if (loadingScreenshot) {
      if (currentScreenshotImage.width == 1) {
        console.log("screenshot loading in progress, waiting");
        return;
      }
      else {
        loadingScreenshot = false;
      }
    }
    else {
      currentScreenshotImage = loadImage("assets/traces/" + frameData.screenshot);
      loadingScreenshot = true;
      return;
    }
  }

  background(0);
  image(mapGraphics, 0, 0, 512 * density, 512 * density, 0, 0, 512, 512);
  updateTraceGraphics(frameData);
  blendMode(ADD);
  image(traceGraphics, 0, 0, 512 * density, 512 * density, 0, 0, 512, 512);
  blendMode(BLEND);

  image(currentScreenshotImage, 512, 0);

  if (showText) {
    stroke(255);
    fill(255);
    textSize(40);
    textAlign(RIGHT, BOTTOM);
    text(frameNum, width, height - 40);
    text(frameData.timestamp, 0, 0, width, height);
  }

  if (saveAllFrames && firstLoop) {
    saveCanvas("frame" + saveFrameSeq, "png");
    saveFrameSeq++;
  }

  frameNum++;
}

function updateTraceGraphics(frameData) {
  var tg = traceGraphics;

  tg.background(0, traceClearAlpha);

  if (!frameData)
    return;

  tg.noStroke();
  tg.fill(readColor);
  drawAccesses(tg, frameData.reads);
  tg.fill(writeColor);
  drawAccesses(tg, frameData.writes);
  tg.fill(executeColor);
  drawAccesses(tg, frameData.executes);
}

function drawAccesses(tg, accesses) {
  for (address in accesses) {
    var xy = hilbert.d2xy(8, address);
    tg.rect(xy[0] * mapScale, xy[1] * mapScale, mapScale, mapScale);
  }
}