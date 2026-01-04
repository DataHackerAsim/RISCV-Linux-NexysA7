# From Logic Gates to Linux: RISC-V SoC on FPGA

**Authors:** Asim Ahmed, Shawaiz Zafar, Abdullah Mustafa
**Supervisor:** Tanvyr Ahmed
**Institution:** NUST Chip Design Centre (NCDC), SINES
**Date:** December 2025

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 1. Project Overview
[cite_start]This project demonstrates the complete design and implementation of a Linux-capable System-on-Chip (SoC) on a Digilent Nexys A7-100T FPGA[cite: 22, 26]. [cite_start]We integrated a VexRiscv (RV32IMA) processor, DDR2 memory controller, and essential peripherals to boot **Linux Kernel 6.9.0** in approximately 11 seconds[cite: 24, 29].

### [cite_start]System Specifications [cite: 2541, 2554, 3256]
* **FPGA Board:** Digilent Nexys A7-100T (Artix-7 XC7A100T)
* **CPU:** VexRiscv (RV32IMA) @ 50 MHz (5-stage pipeline, Sv32 MMU)
* **Memory:** 128 MB DDR2 RAM (@ 200 MT/s)
* **Storage:** MicroSD Card (SPI Mode)
* **OS:** Linux 6.9.0 + BusyBox 1.37.0 Userland

---

## 2. Repository Structure
[cite_start]This repository contains the source scripts and pre-compiled binaries required to reproduce our results[cite: 3564, 3841].

| File/Folder | Description |
| :--- | :--- |
| `make.py` | [cite_start]Main Python script to build the SoC and Software[cite: 2650]. |
| `soc_linux.py` | Defines the SoC architecture (CPU, RAM, Peripherals). |
| `boards.py` | Board definitions for Nexys A7. |
| `litex_setup.py` | [cite_start]Installer script for the LiteX framework dependencies[cite: 2834]. |
| `sd_card_files/` | [cite_start]**REQUIRED:** Contains the 5 boot files (`Image`, `rootfs.cpio`, `rv32.dtb`, `boot.json`, `opensbi.bin`)[cite: 3841]. |
| `prebuilt/` | [cite_start]Contains the synthesized bitstream (`nexys4ddr.bit`) for immediate testing[cite: 3845]. |
| `ESP_Report...pdf`| Full project documentation and technical details. |

---

## 3. Quick Start: Verify the Project (No Compilation)
*Use this method to verify the system functionality immediately without waiting for synthesis.*

### Prerequisites
* **Hardware:** Digilent Nexys A7-100T Board, Micro USB Cable, MicroSD Card.
* **Software:** Vivado Hardware Manager (Lab Edition or Full) or OpenOCD.
* **Terminal:** PuTTY, TeraTerm, or `screen` (Linux).

### Steps
1.  **Prepare the SD Card:**
    * [cite_start]Format your MicroSD card to **FAT32**[cite: 3177].
    * [cite_start]Copy **ALL 5 FILES** from the `sd_card_files/` folder to the **root** of the SD card[cite: 3202].
    * *Files required:* `boot.json`, `Image`, `rv32.dtb`, `rootfs.cpio`, `opensbi.bin`.
    * Insert the SD card into the Nexys A7 board.

2.  **Program the FPGA:**
    * Connect the Nexys A7 to your PC via USB.
    * Open Vivado Hardware Manager.
    * [cite_start]Program the device using the bitstream located in `prebuilt/nexys4ddr.bit`[cite: 3224].

3.  **Connect Serial Console:**
    * Open your terminal program (e.g., PuTTY).
    * [cite_start]**Port:** Select your device's COM port (Windows) or `/dev/ttyUSBx` (Linux)[cite: 3232].
    * [cite_start]**Baud Rate:** `115200`[cite: 3239].
    * **Settings:** 8 Data bits, No Parity, 1 Stop bit (8N1).

4.  **Boot Linux:**
    * Press the red **CPU_RESET** button on the FPGA board.
    * Watch the boot logs. The login prompt will appear in ~11 seconds.
    * [cite_start]**Login:** `root` (No password required)[cite: 3247].

---

## 4. Full Reproduction: Build from Source
*Use these steps to rebuild the entire project (Bitstream + Linux images) from scratch.*

### [cite_start]Environment Requirements [cite: 2689]
* **OS:** Ubuntu 22.04 LTS (Native or WSL2).
* **Tools:** Xilinx Vivado 2023.2, Python 3.10+.
* **Packages:** `git`, `build-essential`, `python3-pip`, `verilator`, `libevent-dev`, `libjson-c-dev`.

### Build Instructions
**1. Setup Dependencies:**
```bash
# Install system packages
sudo apt update && sudo apt install -y build-essential python3-pip git device-tree-compiler

# Install LiteX framework using the provided script
chmod +x litex_setup.py
./litex_setup.py --init --install --user --tag 2024.04  # [cite: 2648]


2. Build Hardware (SoC Bitstream): This step synthesizes the Verilog into a bitstream. Takes ~45 minutes.
python3 make.py --board=nexys4ddr --build  # [cite: 2650]
# Output: build/nexys4ddr/gateware/nexys4ddr.bit
3. Build Software (Linux & RootFS): This compiles the Kernel, OpenSBI, and Buildroot. Takes ~60 minutes.
python3 make.py --board=nexys4ddr --buildroot  # [cite: 2653]
# Output: buildroot/output/images/

4. Generate Configuration:
python3 make.py --board=nexys4ddr --dtb   # Generates rv32.dtb [cite: 3129]
python3 make.py --board=nexys4ddr --json  # Generates boot.json [cite: 3142]

5. Troubleshooting

Garbled Serial Output: Ensure your baud rate is set strictly to 115200.
SD Card Not Detected: Ensure the card is formatted as FAT32 and files are in the root directory (not a subfolder).
Memory Test Failed: Check that the FPGA is receiving stable power; try a different USB port or powered hub.

License & Acknowledgments
This project is based on the linux-on-litex-vexriscv project by LiteX-Hub.
Report & Implementation: © 2025 Asim Ahmed, Shawaiz Zafar, Abdullah Mustafa.
Open Source Components: VexRiscv, LiteX, Buildroot, Linux Kernel.
