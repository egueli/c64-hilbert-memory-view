function setup() {
  createCanvas(512, 512);

  printMap();

  // Uncomment this to save the map to PNG.
  //save('map.png');
}

function printMap() {
  rect(0, 0, 256, 256);

  function addrBlock(color, desc) {
    return function(x, y, size) {
      x *= 2;
      y *= 2;
      size *= 2;
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
  console.log(sizeLinear);
  var level = Math.log2(sizeLinear) / 2;
  var size = 1 << level;

  var xy = hilbert.d2xy(maxLevel - level, location / sizeLinear);
  var x = xy[0] * size;
  var y = xy[1] * size;

  callback(x, y, size);
}

function draw() {
  // if (mouseIsPressed) {
  //   fill(0);
  // } else {
  //   fill(255);
  // }
  // ellipse(mouseX, mouseY, 80, 80);
}