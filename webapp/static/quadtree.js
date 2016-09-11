'use strict';

class Quadtree {
	static doTree(range, maxDepth, callback) {
		Quadtree.doTreeRecursive(range, maxDepth, callback, 1, 1, 0);
	}

	static doTreeRecursive(rangeToTest, maxDepth, callback, depth, scale, offset) {
		for (var i = 0; i < 1; i += 0.25) {
			var quadrant = range(i, i + 0.25).times(scale).add(offset);
			var result = rangeToTest.overlapTest(quadrant);

			if (result == 1) {
				callback(depth, scale, quadrant);
			}
			else if (result > 0) {
				if (depth <= maxDepth) {
					Quadtree.doTreeRecursive(rangeToTest, maxDepth, callback, depth + 1, scale / 4, quadrant.from);
				}
				else if (result >= 0.5) {
					callback(depth, scale, quadrant);
				}
			}
		}
	}

}
