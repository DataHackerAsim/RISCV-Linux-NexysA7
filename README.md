# From Logic Gates to Linux: RISC-V SoC on FPGA

**Authors:**  
- Asim Ahmed  
- Shawaiz Zafar  
- Abdullah Mustafa  

**Supervisor:** Tanvyr Ahmed  
**Institution:** NUST Chip Design Centre (NCDC), SINES  
**Date:** December 2025  

---

## License
See the **License & Acknowledgments** section at the end of this document.

---

## 1. Project Overview

This project demonstrates the complete design and implementation of a **Linux-capable System-on-Chip (SoC)** on a **Digilent Nexys A7-100T FPGA**.  
A **VexRiscv (RV32IMA)** processor, **DDR2 memory controller**, and essential peripherals are integrated to successfully boot **Linux Kernel 6.9.0** in approximately **11 seconds**.

### System Specifications

- **FPGA Board:** Digilent Nexys A7-100T (Artix-7 XC7A100T)  
- **CPU:** VexRiscv (RV32IMA) @ 50 MHz  
  - 5-stage pipeline  
  - Sv32 MMU  
- **Memory:** 128 MB DDR2 RAM (@ 200 MT/s)  
- **Storage:** MicroSD Card (SPI Mode)  
- **Operating System:**  
  - Linux Kernel 6.9.0  
  - BusyBox 1.37.0 userland  

---

## 2. Repository Structure

This repository contains all source scripts and pre-compiled binaries required to reproduce the results.

| File / Folder | Description |
|---------------|------------|
| `make.py` | Main Python script to build the SoC and software |
| `soc_linux.py` | Defines the SoC architecture (CPU, RAM, peripherals) |
| `boards.py` | Board definitions for Nexys A7 |
| `litex_setup.py` | Installer script for LiteX framework dependencies |
| `sd_card_files/` | **REQUIRED**: Contains the 5 boot files |
| `prebuilt/` | Pre-synthesized FPGA bitstream for immediate testing |
| `ESP_Report_*.pdf` | Full project documentation and technical details |

### Required SD Card Files
The following files must exist in the **root** of the SD card:
- `boot.json`
- `Image`
- `rv32.dtb`
- `rootfs.cpio`
- `opensbi.bin`

---

## 3. Quick Start: Verify the Project (No Compilation)

Use this method to verify system functionality **without rebuilding** the project.

### Prerequisites

**Hardware**
- Digilent Nexys A7-100T FPGA board  
- Micro-USB cable  
- MicroSD card  

**Software**
- Vivado Hardware Manager (Lab Edition or Full) **or** OpenOCD  

**Terminal**
- PuTTY / TeraTerm (Windows)  
- `screen` or `minicom` (Linux)

---

### Steps

#### 1. Prepare the SD Card
1. Format the MicroSD card as **FAT32**
2. Copy **all 5 files** from `sd_card_files/` to the **root directory**
3. Insert the SD card into the Nexys A7 board

#### 2. Program the FPGA
1. Connect the Nexys A7 to your PC via USB  
2. Open **Vivado Hardware Manager**  
3. Program the device using:
