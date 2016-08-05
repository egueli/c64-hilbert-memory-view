# c64-hilbert-memory-view
I want to see how my favorite 8-bit computer walks into its address space, represented as a Hilbert curve.

Something similar to https://xkcd.com/195/ (Map of the Internet), but for the Commodore 64's 64K of memory. And  animated. In the future it will work in realtime alongside an emulator.

![The C64 memory map, showed as a Hilbert curve](/imageGenerator/example_map.png?raw=true)

The C64 memory map, showed as a Hilbert curve. The white spots are the instructions executed during the startup.




What you'll find in this repository:

* a Python script to record the activity of the VICE emulator;
* a P5.js sketch that will show the memory activiy of the 6510.
* an execution trace of the C64 startup sequence.

## tracer.py

Open a VICE emulator, set up remote monitoring (localhost port 6510), then

    ./tracer.py -r > trace.txt

The emulator will reset, and the trace file will be written then. VICE will become A LOT slower, so take into account 10 minutes before the initialization ends.

Omit the -r to avoid resetting the C64. Then you can see how the C64 reads its memory while playing your own favorite game.


## imageGenerator

Will show the contents of trace.txt with some animation.

Run it in a local server (e.g. `cd imageGenerator; python -m SimpleHTTPServer 8000`) to see it working.