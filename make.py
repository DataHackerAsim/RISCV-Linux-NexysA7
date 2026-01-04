#!/usr/bin/env python3

import os
import sys
import re
import argparse
import shutil

from litex.soc.integration.builder import Builder
from litex.soc.cores.cpu.vexriscv_smp import VexRiscvSMP
from litex.build.generic_platform import *

from boards import *
from soc_linux import SoCLinux

# --- HELPER FUNCTIONS ---
def camel_to_snake(name):
    name = re.sub(r'(?<=[a-z])(?=[A-Z])', '_', name)
    return name.lower()

def get_supported_boards():
    board_classes = {}
    for name, obj in globals().items():
        name = camel_to_snake(name)
        if isinstance(obj, type) and issubclass(obj, Board) and obj is not Board:
            board_classes[name] = obj
    return board_classes

supported_boards = get_supported_boards()
# ------------------------

def main():
    parser = argparse.ArgumentParser(description="Linux on LiteX-VexRiscv")
    parser.add_argument("--board", required=True, help="FPGA board")
    parser.add_argument("--build", action="store_true", help="Build bitstream")
    parser.add_argument("--load", action="store_true", help="Load bitstream")
    parser.add_argument("--flash", action="store_true", help="Flash bitstream")
    parser.add_argument("--remote-ip", default="192.168.1.100", help="Remote IP")
    parser.add_argument("--rootfs", default="ram0", choices=["ram0", "mmcblk0p2"], help="RootFS location")

    VexRiscvSMP.args_fill(parser)
    args = parser.parse_args()

    # Get Board Class
    board_class = supported_boards[args.board]
    board = board_class()

    soc_kwargs = Board.soc_kwargs
    soc_kwargs.update(board.soc_kwargs)

    # ============================================================
    # MASTER SETTING 1: FORCE 50 MHz (Stable RAM)
    # ============================================================
    soc_kwargs["sys_clk_freq"] = int(50e6)

    VexRiscvSMP.args_read(args)
    soc = SoCLinux(board.soc_cls, **soc_kwargs)
    board.platform = soc.platform

    for k, v in board.soc_constants.items():
        soc.add_constant(k, v)

    # ============================================================
    # MASTER SETTING 2: MANUAL SPI SD CARD DEFINITION
    # CRITICAL FIX: Corrected pin mapping for Nexys A7-100T
    # ============================================================
    if "sdcard" in board.soc_capabilities:
        # CORRECT Nexys A7-100T SD Card Pinout (from Digilent schematic):
        #   SD_CLK   = B1  (was incorrectly E2 which is SD_RESET!)
        #   SD_CMD   = C1  (MOSI)
        #   SD_D0    = C2  (MISO) 
        #   SD_D3    = D2  (CS_N)
        #   SD_RESET = E2  (directly active, directly connects SD)
        spi_sd_pins = [
            ("spisdcard", 0,
                Subsignal("clk",  Pins("B1")),   # SD_CLK - FIXED!
                Subsignal("mosi", Pins("C1")),   # SD_CMD
                Subsignal("miso", Pins("C2")),   # SD_D0
                Subsignal("cs_n", Pins("D2")),   # SD_D3
                IOStandard("LVCMOS33"),
                Misc("SLEW=SLOW"),               # Improve signal integrity
            )
        ]
        board.platform.add_extension(spi_sd_pins)
        
        # CRITICAL FIX: Lower SPI clock for stability with Class 10 cards
        # 5 MHz is conservative but reliable
        soc.add_spi_sdcard(name="spisdcard", spi_clk_freq=5e6)
        
        print("=" * 60)
        print("SD Card Mode: SPI @ 5 MHz (Conservative/Stable)")
        print("Pin Mapping: CLK=B1, MOSI=C1, MISO=C2, CS=D2")
        print("=" * 60)
    # ============================================================

    if "ethernet" in board.soc_capabilities:
        soc.configure_ethernet(remote_ip=args.remote_ip)

    # Build
    build_dir = os.path.join("build", args.board)
    builder = Builder(soc, output_dir=build_dir, 
                      csr_json=os.path.join(build_dir, "csr.json"), 
                      csr_csv=os.path.join(build_dir, "csr.csv"))
    builder.build(run=args.build, build_name=args.board)

    # DTB
    soc.generate_dts(args.board, args.rootfs)
    soc.compile_dts(args.board)
    soc.combine_dtb(args.board)

    # Boot Config
    shutil.copyfile(f"images/boot_{args.rootfs}.json", "images/boot.json")

    if args.load:
        board.load(filename=builder.get_bitstream_filename(mode="sram"))
    if args.flash:
        board.flash(filename=builder.get_bitstream_filename(mode="flash"))

if __name__ == "__main__":
    main()
