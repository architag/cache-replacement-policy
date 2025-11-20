================================================================================
          Applying SRRIP to GPU L2 Cache for better Cache Performance
================================================================================

OVERVIEW
--------
This project implements and analyzes various GPU L2 cache replacement policies 
(FIFO, LRU, SRRIP-HP, SRRIP-FP) using the Accel-Sim framework. 
The code has been specifically verified and tested on an NVIDIA Titan V GPU.

CONTENTS
--------
1. System Requirements & Access
2. Environment Setup
3. Building the Simulator
4. (Optional) Building the Tracer Tool
5. Running a Simulation
6. Changing Cache Policies

================================================================================
1. SYSTEM REQUIREMENTS & ACCESS
================================================================================
This project requires an environment with an NVIDIA Titan V GPU.
If you are using the CIMS infrastructure, you must SSH into the 'cuda3' node.

    $ ssh to cuda3.cims.nyu.edu

================================================================================
2. ENVIRONMENT SETUP
================================================================================
Before compiling or running the simulator, you need to load the source code.
You must also load the appropriate CUDA module and set environment variables.

1. Clone repo
    $ git clone git@github.com:architag/cache-replacement-policy.git

2. Load CUDA 12.4:
    $ module load cuda-12.4

3. Set the CUDA install path:
    $ export CUDA_INSTALL_PATH=/usr/local/stow/cuda-12.4

4. Update your system PATH:
    $ export PATH=$CUDA_INSTALL_PATH/bin:$PATH

================================================================================
3. BUILDING THE SIMULATOR
================================================================================
To build the Accel-Sim simulator (required for performance testing):

1. Install Python dependencies:
    $ pip3 install -r requirements.txt

2. Source the setup script:
    $ source ./gpu-simulator/setup_environment.sh

3. Compile the simulator (using multiple threads for speed):
    $ make -j -C ./gpu-simulator/

================================================================================
4. (OPTIONAL) BUILDING THE TRACER TOOL
================================================================================
Note: This step is NOT required to run the simulations, as pre-generated traces 
for the tested problems are already provided in the `hw_run/` directory.

If you wish to generate new traces:
1. Install NVBit:
    $ ./util/tracer_nvbit/install_nvbit.sh

2. Compile the tracer:
    $ make -C ./util/tracer_nvbit/

================================================================================
5. RUNNING A SIMULATION
================================================================================
To trace an application and run the simulator, use the `accel-sim.out` binary.
Below is an example command to run the BFS benchmark from the Rodinia suite.

Command:
    ./gpu-simulator/bin/release/accel-sim.out \
    -config ./gpu-simulator/gpgpu-sim/configs/tested-cfgs/SM7_QV100/gpgpusim.config \
    -config ./gpu-simulator/configs/tested-cfgs/SM7_QV100/trace.config \
    -trace hw_run/rodinia_2.0-ft/11.0/bfs-rodinia-2.0-ft/__data_graph4096_txt___data_graph4096_result_txt/traces/kernelslist.g

Note on Traces:
The `kernelslist.g` files for other traced applications can be found within 
subdirectories of the `hw_run/rodinia_2.0-ft/11.0/` folder.

================================================================================
6. CHANGING CACHE POLICIES
================================================================================
To switch between the implemented cache replacement policies, you must edit the 
GPGPU-Sim configuration file.

File path:
    ./gpu-simulator/gpgpu-sim/configs/tested-cfgs/SM7_QV100/gpgpusim.config

Locate the line starting with `-gpgpu_cache:dl2`.
It will look similar to this:
    -gpgpu_cache:dl2 S:16:128:8,L:B:m:L:P,A:192:4,32:0,32

You need to change the 5th flag from the left (the letter 
after `8:` and before `:B` in this case).

Available Policy Codes:
    L  -> LRU (Least Recently Used) - [Default]
    F  -> FIFO (First In, First Out)
    S  -> SRRIP-HP (Static RRIP with High Priority)
    Z  -> SRRIP-FP (Static RRIP with Frequency Priority)

Example:
To change from LRU to SRRIP-HP, change:
    ...L:B:m:L:P...
To:
    ...S:B:m:L:P...