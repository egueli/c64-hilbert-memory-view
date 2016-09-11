var hilbert = (function() {
  // From Mike Bostock: http://bl.ocks.org/597287
  // Adapted from Nick Johnson: http://bit.ly/biWkkq
  var pairs = [
    [[0, 3], [1, 0], [3, 1], [2, 0]],
    [[2, 1], [1, 1], [3, 0], [0, 2]],
    [[2, 2], [3, 3], [1, 2], [0, 1]],
    [[0, 0], [3, 2], [1, 3], [2, 3]]
  ];
  // d2xy and rot are from:
  // http://en.wikipedia.org/wiki/Hilbert_curve#Applications_and_mapping_algorithms
  function rot(n, x, y, rx, ry) {
    if (ry === 0) {
      if (rx === 1) {
        x = n - 1 - x;
        y = n - 1 - y;
      }
      return [y, x];
    }
    return [x, y];
  }
  return {
    xy2d: function(x, y, z) {
      var quad = 0,
          pair,
          i = 0;
      while (--z >= 0) {
        pair = pairs[quad][(x & (1 << z) ? 2 : 0) | (y & (1 << z) ? 1 : 0)];
        i = (i << 2) | pair[0];
        quad = pair[1];
      }
      return i;
    },
    d2xy: function(z, t) {
      var n = 1 << z,
          x = 0,
          y = 0;
      for (var s = 1; s < n; s *= 2) {
        var rx = 1 & (t / 2),
            ry = 1 & (t ^ rx);
        var xy = rot(s, x, y, rx, ry);
        x = xy[0] + s * rx;
        y = xy[1] + s * ry;
        t /= 4;
      }
      return [x, y];
    }
  };
})();

/*
function hilbertCurve(level) {
  return d3.range(1 << (level * 2)).map(
    function(i) { return hilbert.d2xy(level, i);
  });
}

var w = 500,
    level = 6,
    x = d3.scale.linear().domain([0, 1 << level]).range([0, w]),
    colours = false;

var vis = d3.select("#vis").append("svg")
    .attr("width", w+10)
    .attr("height", w+10)
  .append("g")
    .attr("transform", "translate(5,5)");

var line = d3.svg.line()
    .x(function(d) { return x(d[0]); })
    .y(function(d) { return x(d[1]); });

vis.append("path").attr("d", "M0,0");

for (var i=1; i<=6; i++) {
  $('#level').append('<option value="' + i + '"' + ((i === level) ? ' selected="selected"' : '') + '>' + i + '</option>');
}

$('#level').change(function() { level = parseInt($(this).val()); })
$('#colours').change(function() { colours = $(this).attr('checked'); });

$('#level, #colours').change(function() {
  x.domain([-.5, 1 << level]);
  var curve = hilbertCurve(level);
  vis.select("path")
      .attr("d", line(curve));
  var square = vis.selectAll("rect")
      .data(colours ? curve : []);
  square.enter().append("rect");
  square.exit().remove();
  vis.selectAll("rect")
      .style("fill", function(d, i) {
        return d3.hsl(~~(i * 360 / (1<<(level*2))), 1, .5).rgb();
      })
      .attr("x", function(d) { return x(d[0] - .5); })
      .attr("y", function(d) { return x(d[1] - .5); })
      .attr("width", x(1) - x(0) + 1)
      .attr("height", x(1) - x(0) + 1);
}).change();
*/