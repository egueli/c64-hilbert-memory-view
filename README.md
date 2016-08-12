# c64-hilbert-memory-view
I want to see how my favorite 8-bit computer walks into its address space, represented as a Hilbert curve.

Something similar to https://xkcd.com/195/ (Map of the Internet), but for the Commodore 64's 64K of memory. And animated. In the future it will work in realtime alongside an emulator.

[![Inside the memory of a C64](http://i.imgur.com/AOoUg3l.png)](https://www.youtube.com/watch?v=NLeiEp-JWiE "Inside the memory of a C64")

The C64 memory map, showed as a Hilbert curve. The white spots are the data reads, writes, and instructions executed during typing and running a simple CBM BASIC program.




What you'll find in this repository:

* some Python scripts to record the activity of the VICE emulator;
* a P5.js sketch that will show the memory activiy of the 6510.


## How to build an animation

On Mac OS X (should work the same on Linux too):

1. Run VICE and enable remote monitor (or start from command line with `x64 -remotemonitor -remotemonitoraddress 127.0.0.1:6510`)
2. Load your favorite game, start recording some history in VICE (wait ~5s before starting playing), then stop recording. Take note of the recording length.
3. Type on a terminal (without pressing Enter) `./tracer.py -f 25 -e 35 > traces/output.trace` (replace 35 with the record duration, in seconds).
4. Re-run the recorded history, then quickly press Enter in the terminal.
5. Wait for the trace to be completed. It may take a while, 3-4 minutes for every *second* of recorded history. The resulting file will be around 21MB for every second of history. The tool will also create PNG screenshots in `/tmp`.
6. Once it's done, run `./compressor.py < traces/output.trace > traces/output.ctrace`. You can delete `output.ctrace`.
7. Open `imageGenerator/sketch.js`, edit the `traceFileName` variable to `output.ctrace`.
8. In the terminal, run `cd imageGenerator; python -m SimpleHTTPServer 8000`
9. In a browser, go to `http://localhost:8000`, wait the data to be loaded, then enjoy!

If you want to save the animation's screenshots:

10. ensure your browser can download files automatically, without opening the save dialog
11. in `sketch.js` set the variable `saveAllFrames` to `true`
12. Reload.

