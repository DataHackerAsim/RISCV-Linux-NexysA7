# From Logic Gates to Linux: RISC-V SoC on FPGA

**Authors:**
- Asim Ahmed
- Shawaiz Zafar
- Abdullah Mustafa

**Supervisor:** Tanveer Ahmed
**Institution:** School of Interdisciplinary Engineering and Sciences (SINES), NUST
**Collaboration:** NUST Chip Design Centre (NCDC)
**Date:** December 2025

---

> **ℹ️ About this repository**
> This is a **results and reproduction package** — it contains the pre-synthesized
> bitstream, boot images, and build scripts needed to verify or fully rebuild the project.
> The complete RTL source (LiteX/VexRiscv SoC definition, Verilog netlists, Vivado
> project) is generated at build time by the LiteX framework from the Python SoC
> description in `soc_linux.py`; it is not committed here as it is hundreds of megabytes
> of tool-generated output. Everything needed to reproduce the full design from scratch
> is in **Section 4** below.

---

## 📄 Technical Report

A comprehensive **100+ page technical report** covering the full design flow — from
digital logic fundamentals through SoC architecture, memory hierarchy, Linux bring-up,
and performance analysis — is included in this repository:

**[`ESP_Report_RISCV_Linux_FPGA.pdf`](ESP_Report_RISCV_Linux_FPGA.pdf)**

This document is the primary reference for understanding the design decisions, synthesis
results, and implementation details of this project.

---

## 1. Project Overview

This project demonstrates the complete design and implementation of a **Linux-capable
System-on-Chip (SoC)** on a **Digilent Nexys A7-100T FPGA**.

A **VexRiscv (RV32IMA)** processor, **DDR2 memory controller**, and essential peripherals
are integrated to successfully boot **Linux Kernel 6.9.0** in approximately **11 seconds**.

### System Specifications

| Component | Details |
|---|---|
| **FPGA Board** | Digilent Nexys A7-100T (Artix-7 XC7A100T) |
| **CPU** | VexRiscv (RV32IMA) @ 50 MHz — 5-stage pipeline, Sv32 MMU |
| **Memory** | 128 MB DDR2 RAM @ 200 MT/s |
| **Storage** | MicroSD Card (SPI Mode) |
| **OS** | Linux Kernel 6.9.0 + BusyBox 1.37.0 userland |
| **Boot time** | ~11 seconds |

---

## 2. Repository Structure

This repository contains all scripts and pre-compiled binaries required to reproduce
the results.

| File / Folder | Description |
|---|---|
| `make.py` | Main Python script to build the SoC and software |
| `soc_linux.py` | Defines the SoC architecture (CPU, RAM, peripherals) |
| `boards.py` | Board definitions for Nexys A7 |
| `litex_setup.py` | Installer script for LiteX framework dependencies |
| `sim.py` | Simulation script |
| `sd_card_files/` | **REQUIRED** — the 5 boot files for the SD card |
| `prebuilt/` | Pre-synthesized FPGA bitstream for immediate testing |
| `HOWTO.md` | Supplementary setup notes |
| `ESP_Report_RISCV_Linux_FPGA.pdf` | **100+ page full technical report** |

### Required SD Card Files

The following 5 files must be present in the **root** of the SD card:

- `boot.json`
- `Image`
- `rv32.dtb`
- `rootfs.cpio`
- `opensbi.bin`

---

## 3. Quick Start: Verify the Project (No Compilation)

Use the pre-synthesized bitstream to verify system functionality **without rebuilding**
anything.

### Prerequisites

**Hardware**
- Digilent Nexys A7-100T FPGA board
- Micro-USB cable
- MicroSD card

**Software**
- Vivado Hardware Manager (Lab Edition or Full) or OpenOCD

**Terminal**
- PuTTY / TeraTerm (Windows)
- `screen` or `minicom` (Linux)

### Steps

**1. Prepare the SD Card**
1. Format the MicroSD card as **FAT32**
2. Copy **all 5 files** from `sd_card_files/` to the **root directory**
3. Insert the SD card into the Nexys A7 board

**2. Program the FPGA**
1. Connect the Nexys A7 to your PC via USB
2. Open **Vivado Hardware Manager**
3. Program the device using:
```
   prebuilt/nexys4ddr.bit
```

**3. Connect the Serial Console**

| Setting | Value |
|---|---|
| Port | `COMx` (Windows) / `/dev/ttyUSBx` (Linux) |
| Baud Rate | `115200` |
| Mode | `8N1` |

**4. Boot Linux**
1. Press the **red CPU_RESET** button on the FPGA board
2. Observe boot logs in the serial terminal
3. Login prompt appears in ~11 seconds

```
login: root
password: (none)
```

---

## 4. Full Reproduction: Build from Source

These steps rebuild **everything from scratch** — the FPGA bitstream, Linux kernel, and
root filesystem.

### Environment Requirements

- **OS:** Ubuntu 22.04 LTS (native or WSL2)
- **Tools:** Xilinx Vivado 2023.2, Python 3.10+
- **Packages:** `git`, `build-essential`, `python3-pip`, `verilator`,
  `libevent-dev`, `libjson-c-dev`, `device-tree-compiler`

### Build Instructions

**1. Setup Dependencies**
```bash
sudo apt update && sudo apt install -y \
    build-essential python3-pip git device-tree-compiler \
    verilator libevent-dev libjson-c-dev

chmod +x litex_setup.py
./litex_setup.py --init --install --user --tag 2024.04
```

**2. Build Hardware (SoC Bitstream)** ⏱️ ~45 minutes
```bash
python3 make.py --board=nexys4ddr --build
```
Output: `build/nexys4ddr/gateware/nexys4ddr.bit`

**3. Build Software (Linux & RootFS)** ⏱️ ~60 minutes
```bash
python3 make.py --board=nexys4ddr --buildroot
```
Output: `buildroot/output/images/`

**4. Generate Configuration Files**
```bash
python3 make.py --board=nexys4ddr --dtb
python3 make.py --board=nexys4ddr --json
```

---

## 5. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Garbled serial output | Wrong baud rate | Set baud rate to exactly `115200` |
| SD card not detected | Wrong format or file location | Format as FAT32; files must be in the **root** directory, not a subfolder |
| Memory test failed | Unstable USB power | Try a different USB port or a powered hub |

---

## 6. Contributions & Upstream Attribution

This project is built on top of the open-source
**[linux-on-litex-vexriscv](https://github.com/litex-hub/linux-on-litex-vexriscv)**
framework by LiteX-Hub. The following table clarifies what is upstream and what was
contributed by this project:

| File | Origin | Notes |
|------|--------|-------|
| `soc_linux.py` | Upstream (LiteX-Hub) | Unmodified SoC class definition |
| `boards.py` | Upstream (LiteX-Hub) | Unmodified board definitions |
| `litex_setup.py` | Upstream (LiteX-Hub) | Unmodified dependency installer |
| `sim.py` | Upstream (LiteX-Hub) | Unmodified simulation script |
| `HOWTO.md` | Upstream (LiteX-Hub) | Adapted with Nexys A7 notes |
| **`make.py`** | **Modified** | SD card pin fix (B1/E2), 50 MHz clock, 5 MHz SPI |
| **`prebuilt/nexys4ddr.bit`** | **Generated** | Synthesised bitstream for Nexys A7-100T |
| **`sd_card_files/`** | **Generated** | Linux kernel, OpenSBI, DTB, rootfs built by team |
| **`README.md`** | **Written** | Project documentation |
| **`ESP_Report_RISCV_Linux_FPGA.pdf`** | **Written** | 100+ page technical report |

### Key Technical Contributions

1. **SD Card Pin Mapping Fix** — The upstream Nexys A7 configuration mapped `SD_CLK`
   to pin `E2`, which is actually `SD_RESET` on the Nexys A7-100T schematic. This
   project corrects it to pin `B1` (the actual `SD_CLK`), along with verified mappings
   for `CMD=C1`, `D0=C2`, `D3=D2`. Without this fix, the SD card is not detected.

2. **Clock Stability** — System clock forced to 50 MHz (down from the upstream default)
   to ensure stable DDR2 memory operation on the Nexys A7-100T.

3. **SPI Clock Tuning** — SPI SD card clock reduced to 5 MHz for reliable operation
   with Class 10 MicroSD cards.

4. **Complete Build & Verification** — Full synthesis (Vivado 2023.2), Linux kernel
   6.9.0 + BusyBox 1.37.0 cross-compilation, OpenSBI build, device tree generation,
   and verified boot on physical hardware.

---

## 7. Boot Evidence

Successful Linux boot is documented in the technical report
([`ESP_Report_RISCV_Linux_FPGA.pdf`](ESP_Report_RISCV_Linux_FPGA.pdf)), which
includes full serial console boot logs, timing measurements, and photographs of the
running system.

Expected boot output (serial console at 115200 baud):

```
--============= Boot ==================--
Copying Image to 0x40000000...
Copying rv32.dtb to 0x40ef0000...
Copying rootfs.cpio to 0x41000000...
Copying opensbi.bin to 0x40f00000...
Executing booted program at 0x40f00000

...

[    0.000000] Linux version 6.9.0 (...)
[    0.000000] Machine model: LiteX SoC on Nexys4DDR

...

Welcome to Buildroot
buildroot login: root
#
```

Boot time: approximately 11 seconds from CPU reset to login prompt.

---

## License & Acknowledgments

- Based on **linux-on-litex-vexriscv** by LiteX-Hub
- **Report & Implementation:** © 2025 — Asim Ahmed, Shawaiz Zafar, Abdullah Mustafa
- **Open Source Components:** VexRiscv · LiteX · Buildroot · Linux Kernel

[BSD-2-Clause License](LICENSE)
