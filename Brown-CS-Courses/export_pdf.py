#!/usr/bin/env python3
"""
Tiles brown_cs_course_flowchart.png across A4 landscape pages and saves as PDF.
The pages can be printed and assembled into a poster.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as mpatches
import numpy as np
from PIL import Image
from math import ceil

# ── Config ──────────────────────────────────────────────────────────────────
IMG_PATH    = "/Users/francoisleutou/Desktop/CodingSpace/cs1970KF Projects/brown_cs_course_flowchart.png"
PDF_PATH    = "/Users/francoisleutou/Desktop/CodingSpace/cs1970KF Projects/brown_cs_course_flowchart.pdf"

PAGE_W      = 11.693   # A4 landscape width  (inches)
PAGE_H      =  8.268   # A4 landscape height (inches)
MARGIN      =  0.25    # margin on all sides (inches)
DPI         = 130

# Target grid: scale the image so it fits across this many tiles
TARGET_COLS = 3
TARGET_ROWS = 2

# ── Load and scale image ─────────────────────────────────────────────────────
img = Image.open(IMG_PATH).convert("RGB")
orig_w_px, orig_h_px = img.size
orig_w_in = orig_w_px / DPI
orig_h_in = orig_h_px / DPI

content_w = PAGE_W - 2 * MARGIN
content_h = PAGE_H - 2 * MARGIN

# Scale image so it fits within TARGET_COLS × TARGET_ROWS tiles
target_w_in = TARGET_COLS * content_w
target_h_in = TARGET_ROWS * content_h
scale = min(target_w_in / orig_w_in, target_h_in / orig_h_in)

new_w_px = int(orig_w_px * scale)
new_h_px = int(orig_h_px * scale)
img = img.resize((new_w_px, new_h_px), Image.LANCZOS)

img_w_px, img_h_px = img.size
img_w_in = img_w_px / DPI
img_h_in = img_h_px / DPI

n_cols = ceil(img_w_in / content_w)
n_rows = ceil(img_h_in / content_h)
total  = n_cols * n_rows

tile_w_px = int(content_w * DPI)
tile_h_px = int(content_h * DPI)

print(f"Original : {orig_w_px}×{orig_h_px} px  ({orig_w_in:.2f}\" × {orig_h_in:.2f}\")")
print(f"Scaled   : {img_w_px}×{img_h_px} px  ({img_w_in:.2f}\" × {img_h_in:.2f}\")  [scale={scale:.2f}]")
print(f"Tile     : {tile_w_px}×{tile_h_px} px  ({content_w:.2f}\" × {content_h:.2f}\")")
print(f"Grid     : {n_cols} cols × {n_rows} rows = {total} A4 landscape pages")
print()

# ── Build PDF ────────────────────────────────────────────────────────────────
with PdfPages(PDF_PATH) as pdf:

    # ── Cover page ──────────────────────────────────────────────────────────
    fig_c, ax_c = plt.subplots(figsize=(PAGE_W, PAGE_H))
    fig_c.patch.set_facecolor('#F6F6F6')
    ax_c.set_facecolor('#F6F6F6')
    ax_c.axis('off')

    ax_c.text(PAGE_W / 2, PAGE_H * 0.72,
              "Brown University",
              ha='center', va='center', fontsize=22, color='#222222',
              fontweight='bold')
    ax_c.text(PAGE_W / 2, PAGE_H * 0.62,
              "CS Course Flowchart",
              ha='center', va='center', fontsize=18, color='#333333',
              fontweight='bold')
    ax_c.text(PAGE_W / 2, PAGE_H * 0.53,
              "2020 Pathway Requirements",
              ha='center', va='center', fontsize=13, color='#555555')
    ax_c.text(PAGE_W / 2, PAGE_H * 0.42,
              f"This document tiles the full flowchart across {total} A4 landscape pages\n"
              f"({n_cols} columns × {n_rows} rows).  Print all pages and assemble into a poster.",
              ha='center', va='center', fontsize=9, color='#666666',
              linespacing=1.6)
    ax_c.text(PAGE_W / 2, PAGE_H * 0.29,
              "Arrows indicate prerequisite relationships\n"
              "Color indicates primary pathway\n"
              "Source: cs.brown.edu — concentration-requirements-2020/pathways-for-undergraduate-and-masters-students",
              ha='center', va='center', fontsize=8, color='#777777',
              linespacing=1.7)

    # Assembly guide grid
    GX = MARGIN + 0.5
    GY = PAGE_H * 0.08
    cell_gw = (PAGE_W - GX - MARGIN - 0.3) / n_cols
    cell_gh = (PAGE_H * 0.14) / n_rows
    for r in range(n_rows):
        for c in range(n_cols):
            pg = r * n_cols + c + 2   # +2 because cover is page 1
            rect = mpatches.FancyBboxPatch(
                (GX + c * cell_gw, GY + (n_rows - 1 - r) * cell_gh),
                cell_gw - 0.04, cell_gh - 0.03,
                boxstyle="round,pad=0.02",
                facecolor='#DDEEFF', edgecolor='#888888', linewidth=0.6
            )
            ax_c.add_patch(rect)
            ax_c.text(GX + c * cell_gw + cell_gw / 2,
                      GY + (n_rows - 1 - r) * cell_gh + cell_gh / 2,
                      f"p.{pg}", ha='center', va='center', fontsize=7)

    ax_c.text(PAGE_W / 2, GY - 0.15,
              "Assembly guide — page numbers shown in each tile",
              ha='center', va='top', fontsize=7, color='#888888')

    pdf.savefig(fig_c, dpi=DPI)
    plt.close(fig_c)
    print("  [cover]  page 1")

    # ── Tile pages ──────────────────────────────────────────────────────────
    page_num = 2
    for row in range(n_rows):
        for col in range(n_cols):
            x0 = col * tile_w_px
            y0 = row * tile_h_px
            x1 = min(x0 + tile_w_px, img_w_px)
            y1 = min(y0 + tile_h_px, img_h_px)

            tile = np.array(img.crop((x0, y0, x1, y1)))

            fig, ax = plt.subplots(figsize=(PAGE_W, PAGE_H), dpi=DPI)
            fig.patch.set_facecolor('white')
            ax.set_facecolor('white')
            ax.axis('off')

            # Draw the tile — imshow with extent maps image into content area
            # The tile may be smaller than content area on right/bottom edges
            tile_h_in = (y1 - y0) / DPI
            tile_w_in = (x1 - x0) / DPI

            ax.imshow(
                tile, aspect='auto', interpolation='lanczos',
                extent=[MARGIN, MARGIN + tile_w_in,
                        PAGE_H - MARGIN - tile_h_in, PAGE_H - MARGIN],
                origin='upper'
            )
            ax.set_xlim(0, PAGE_W)
            ax.set_ylim(0, PAGE_H)

            # Thin border around content area
            border = mpatches.Rectangle(
                (MARGIN, PAGE_H - MARGIN - content_h), content_w, content_h,
                linewidth=0.4, edgecolor='#AAAAAA', facecolor='none'
            )
            ax.add_patch(border)

            # Corner tick marks for alignment when cutting/assembling
            tick = 0.12
            for (tx, ty) in [(MARGIN, PAGE_H - MARGIN),
                             (MARGIN + content_w, PAGE_H - MARGIN),
                             (MARGIN, PAGE_H - MARGIN - content_h),
                             (MARGIN + content_w, PAGE_H - MARGIN - content_h)]:
                ax.plot([tx - tick, tx + tick], [ty, ty],
                        color='#BBBBBB', lw=0.35, zorder=10)
                ax.plot([tx, tx], [ty - tick, ty + tick],
                        color='#BBBBBB', lw=0.35, zorder=10)

            # Footer: page number + position label
            label = (f"Page {page_num} of {total + 1}  "
                     f"[col {col + 1}/{n_cols}, row {row + 1}/{n_rows}]  —  "
                     "Brown CS Course Flowchart (2020 requirements)")
            ax.text(PAGE_W / 2, MARGIN * 0.45, label,
                    ha='center', va='center', fontsize=5.5, color='#999999')

            pdf.savefig(fig, dpi=DPI)
            plt.close(fig)
            print(f"  [tile]   page {page_num}  (col {col + 1}/{n_cols}, row {row + 1}/{n_rows})")
            page_num += 1

print()
print(f"Saved: {PDF_PATH}")
print(f"Total pages: {total + 1}  (1 cover + {total} tiles)")
