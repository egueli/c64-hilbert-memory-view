# c64-hilbert-memory-view
I want to see how my favorite 8-bit computer walks into its address space, represented as a Hilbert curve.

There are two things here:

* a Python script to record the activity of the VICE emulator;
* a P5.js sketch that will show the memory activiy of the 6510.

## client.py

Open a VICE emulator, set up remote monitoring (localhost port 6510), then

    ./client.py > trace.txt

The emulator will reset, and the trace file will be written then. VICE will become A LOT slower, so take into account 10 minutes before the initialization ends.


## imageGenerator

Will show the contents of trace.txt with some animation.
For now, it displays the memory map of the Commodore 64 using a Hilbert curve.
