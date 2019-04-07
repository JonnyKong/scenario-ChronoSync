ChronoSync Simulation Scenario in Ad-hoc Network
=============

### Prerequisites

* NS-3 (branch `ndnSIM-v2.5`)
* ndnSIM 2.6 (tagged as `ndnSIM-2.6`)
  * Note that you have to remove all `DummyIOService` in NFD 0.6.2 and ndn-cxx 0.6.2.

### Compiling ns-3
To configure in optimized mode without logging **(default)**:

    ./waf configure

To configure in optimized mode with scenario logging enabled (logging in NS-3 and ndnSIM modules will
still be disabled, but you can see output from NS_LOG* calls from your scenarios and extensions):

    ./waf configure --logging

To configure in debug mode with all logging enabled

    ./waf configure --debug

### Running
You can run the ping scenario by:

    ./waf --run chronosync-mobile
    # or
    # ./build/chronosync-mobile
