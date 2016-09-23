var ramColor = '#004000';
var romColor = '#000080';
var ioColor = '#800000';

var bankLayerNames = ['ram', 'basic', 'io', 'char', 'kernal'];
var lastBanks = { ram: true, basic: true, io: true, char: false, kernal: true };
var mapGraphics;



function mapSetup() {
	mapGraphics = {};
	for (var i=0; i<bankLayerNames.length; i++) {
		var g = createGraphics(512 * density, 512 * density);
		g.textAlign(CENTER, CENTER);
		g.textSize(12);
		mapGraphics[bankLayerNames[i]] = g;
	}

	function addrBlock(mg, color, desc) {
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

	hilbertBlock(8, 0x0000, 0x10000, addrBlock(mapGraphics.ram, ramColor, "RAM"))

	hilbertBlock(8, 0x0000, 0x0100, addrBlock(mapGraphics.ram, ramColor, "Zero page"));
	hilbertBlock(8, 0x0100, 0x0100, addrBlock(mapGraphics.ram, ramColor, "Stack"));

	hilbertBlock(8, 0x0400, 0x0400, addrBlock(mapGraphics.ram, ramColor, "Video memory"));

	hilbertBlock(8, 0xA000, 0x1000, addrBlock(mapGraphics.basic, romColor, "BASIC ROM"))
	hilbertBlock(8, 0xB000, 0x1000, addrBlock(mapGraphics.basic, romColor, "BASIC ROM"))

	hilbertBlock(8, 0xD000, 0x0400, addrBlock(mapGraphics.io, ioColor, "VIC-II"))
	hilbertBlock(8, 0xD400, 0x0400, addrBlock(mapGraphics.io, ioColor, "SID"))
	hilbertBlock(8, 0xD800, 0x0400, addrBlock(mapGraphics.io, ioColor, "Color RAM"))
	hilbertBlock(8, 0xDC00, 0x0100, addrBlock(mapGraphics.io, ioColor, "CIA #1"))
	hilbertBlock(8, 0xDD00, 0x0100, addrBlock(mapGraphics.io, ioColor, "CIA #2"))
	hilbertBlock(8, 0xDE00, 0x0100, addrBlock(mapGraphics.io, ioColor, "I/O #1"))
	hilbertBlock(8, 0xDF00, 0x0100, addrBlock(mapGraphics.io, ioColor, "I/O #2"))

	hilbertBlock(8, 0xD000, 0x1000, addrBlock(mapGraphics.char, romColor, "Character ROM"));

	hilbertBlock(8, 0xE000, 0x1000, addrBlock(mapGraphics.kernal, romColor, "KERNAL ROM"));
	hilbertBlock(8, 0xF000, 0x1000, addrBlock(mapGraphics.kernal, romColor, "KERNAL ROM"));
}

function hilbertBlock(maxLevel, location, sizeLinear, callback) {
	var level = Math.log2(sizeLinear) / 2;
	var size = 1 << (level - 1);

	var xy = hilbert.d2xy(maxLevel - level, location / sizeLinear);
	var x = xy[0] * size;
	var y = xy[1] * size;

	callback(x, y, size);
}

function updateMap(frameData) {
	for (var i = frameData.memoryValues.length - 1; i >= 0; i--) {
		var memoryValue = frameData.memoryValues[i];
		if ("1" in memoryValue) {
			var value = memoryValue["1"]
		    // https://www.c64-wiki.com/index.php/Bank_Switching
		    var loram = (value & 1) != 0;
		    var hiram = (value & 2) != 0;
		    var charen = (value & 4) != 0;
		    lastBanks.ram = true;
		    lastBanks.basic = hiram && loram;
		    lastBanks.io = charen && (hiram || loram);
		    lastBanks.char = !charen && (hiram || loram);
		    lastBanks.kernal = hiram;
		}
	}
}

function drawMap() {
	for (var i=0; i<bankLayerNames.length; i++) {
		var bankLayerName = bankLayerNames[i];
		if (lastBanks[bankLayerName]) {
			var bankLayer = mapGraphics[bankLayerName];
			image(bankLayer, 0, 0, 512 * density, 512 * density, 0, 0, 512, 512);
		}
	}
}