'use strict';

class Range {
	constructor(from, to) {
		if (to < from) {
			throw new Error("invalid range: [" + from + ", " + to + ")");
		}
		this.from = from;
		this.to = to;
	}

	get length() {
		return this.to - this.from;
	}

	times(n) {
		return new Range(this.from * n, this.to * n);
	}

	add(offset) {
		return new Range(this.from + offset, this.to + offset);
	}

	overlapTest(reference) {
		if (reference.to <= this.from) // this is fully on the right of ref
			return 0;
		if (reference.from >= this.to) // this is fully on the left of ref
			return 0;
		var beforeRef = Math.max(0, this.from - reference.from);
		var afterRef = Math.max(0, reference.to - this.to);
		var outsideRef = beforeRef + afterRef;
		return 1 - (outsideRef / reference.length);

	}

	toString() {
		return "[" + this.from + ", " + this.to + ")";
	}
}

function range(from, to) {
	return new Range(from, to);
}

/*
var rangeToTest = range(0.2, 0.4);

console.log(rangeToTest.overlapTest(range(0.0, 0.1)) == 0);
console.log(rangeToTest.overlapTest(range(0.1, 0.2)) == 0);
console.log(rangeToTest.overlapTest(range(0.1, 0.3)) == 0.5); // TODO fix float comparison
console.log(rangeToTest.overlapTest(range(0.1, 0.4)) == 1);
console.log(rangeToTest.overlapTest(range(0.1, 0.5)) == 1);
console.log(rangeToTest.overlapTest(range(0.2, 0.5)) == 1);
console.log(rangeToTest.overlapTest(range(0.3, 0.5)) == 0.5);
console.log(rangeToTest.overlapTest(range(0.4, 0.5)) == 0);
console.log(rangeToTest.overlapTest(range(0.2, 0.4)) == 1);
console.log(rangeToTest.overlapTest(range(0.203125, 0.21875)) == 1);
*/

