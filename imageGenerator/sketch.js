var mapScale = 2;
var timeScale = 30;
var trace;
var frames = [];

var frameRate = 15;
var microsecsPerFrame = Math.floor(1000000 / frameRate);

var traceGraphics;

function preload() {
  trace = loadStrings('assets/trace_reset.txt');
}

function setup() {
  createCanvas(512, 512);
  traceGraphics = createGraphics(512, 512);
  setFrameRate(frameRate);

  printMap();

  processTrace();

  // Uncomment this to save the map to PNG.
  //save('map.png');
}

function processTrace() {
  for (var i=0; i<trace.length; i++) {
    var line = trace[i];
    var tokens = line.split(" ");
    var timestamp = tokens[0];

    var frame = Math.floor(timestamp / microsecsPerFrame * timeScale);
    var reads;
    if (!frames[frame]) {
      reads = [];
      frames[frame] = {
        time: timestamp / 1000000,
        reads: reads
      };
    }
    else {
      reads = frames[frame].reads;
    }

    var addressHex = tokens[1];
    var address = parseInt(addressHex, 16);
    if (reads[address] === undefined) {
      reads[address] = 1;
    }
    else {
      reads[address]++;
    }
  }

  trace = null;
  console.log(frames.length);
}

function printMap() {
  rect(0, 0, 256, 256);

  function addrBlock(color, desc) {
    return function(x, y, size) {
      x *= mapScale;
      y *= mapScale;
      size *= mapScale;
      fill(color);
      rect(x, y, size, size);

      fill(128);
      textAlign(CENTER, CENTER);
      text(desc, x, y, size, size);
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
  var size = 1 << level;

  var xy = hilbert.d2xy(maxLevel - level, location / sizeLinear);
  var x = xy[0] * size;
  var y = xy[1] * size;

  callback(x, y, size);
}


var frameNum = 50; //jump after memory test cycle
function draw() {
  console.log(frameNum);
  frameNum++;

  var frameData = frames[frameNum];

  background(0);
  updateTraceGraphics(frameData);
  image(traceGraphics, 0, 0);

  if (frameData) {
    stroke(255);
    fill(255);
    textSize(40);
    textAlign(LEFT, TOP);
    text(frameData.time, 0, 0, 288, 288)
  }
}

function updateTraceGraphics(frameData) {
  var tg = traceGraphics;

  tg.background(0, 64);

  if (!frameData)
    return;

  var reads = frameData.reads;
  console.log("instructions: " + reads.length);

  for (address in reads) {
    var xy = hilbert.d2xy(8, address);
    tg.noStroke();
    tg.fill(255);
    tg.rect(xy[0], xy[1], 1, 1);
  }
}