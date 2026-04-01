#!/usr/bin/env python3
"""
Brown CS Course Flowchart Generator (v2)
Grid layout: columns = pathways, rows = levels.
Within each (pathway × level) cell, courses wrap into ≤MAX_COLS sub-columns.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from math import ceil
from collections import defaultdict

# ─── PATHWAYS ──────────────────────────────────────────────────────────────────
PATHWAYS = {
    "intro":    ("Intro / Gateway",       "#BEBEBE"),
    "theory":   ("Theory",                "#7FB3D3"),
    "systems":  ("Systems",               "#76C893"),
    "security": ("Security",              "#E07070"),
    "ai":       ("AI / Machine Learning", "#F0C040"),
    "compbio":  ("Computational Biology", "#B07FCC"),
    "visual":   ("Visual Computing",      "#F0A040"),
    "design":   ("Design / HCI",          "#50BCA8"),
    "misc":     ("Independent Study",     "#9AA8B0"),
}

PATHWAY_ORDER = ["intro", "theory", "systems", "security", "ai", "compbio", "visual", "design", "misc"]

# ─── COURSES ───────────────────────────────────────────────────────────────────
# cid -> (display_code, short_name, pathway, level)
# levels: 0=intro  1=gateway  2=core-1000  3=upper-1000  4=grad-2000

COURSES = {
    # INTRO (level 0)
    "0111":  ("CSCI 0111",  "Computing Foundations: Data",         "intro",    0),
    "0150":  ("CSCI 0150",  "Intro OOP & CS",                      "intro",    0),
    "0170":  ("CSCI 0170",  "CS: An Integrated Intro",             "intro",    0),
    "0190":  ("CSCI 0190",  "Accelerated Intro to CS",             "intro",    0),

    # GATEWAY (level 1)
    "0200":  ("CSCI 0200",  "Program Design & Data Structures",    "intro",    1),
    "0220":  ("CSCI 0220",  "Discrete Structures & Probability",   "theory",   1),
    "0300":  ("CSCI 0300",  "Fundamentals of Computer Systems",    "systems",  1),
    "0320":  ("CSCI 0320",  "Intro Software Engineering",          "systems",  1),
    "0330":  ("CSCI 0330",  "Intro to Computer Systems",           "systems",  1),

    # CORE 1000-LEVEL (level 2)
    "1010":  ("CSCI 1010",  "Theory of Computation",               "theory",   2),
    "1040":  ("CSCI 1040",  "Basics of Cryptographic Systems",     "security", 2),
    "1440":  ("CSCI 1440",  "Algorithmic Game Theory",             "theory",   2),
    "1510":  ("CSCI 1510",  "Introduction to Cryptography",        "security", 2),
    "1550":  ("CSCI 1550",  "Probabilistic Methods in CS",         "theory",   2),
    "1570":  ("CSCI 1570",  "Design & Analysis of Algorithms",     "theory",   2),
    "1710":  ("CSCI 1710",  "Logic for Systems",                   "theory",   2),
    "1260":  ("CSCI 1260",  "Compilers & Program Analysis",        "systems",  2),
    "1270":  ("CSCI 1270",  "Database Management Systems",         "systems",  2),
    "1320":  ("CSCI 1320",  "Modern Web & Mobile Apps",            "systems",  2),
    "1380":  ("CSCI 1380",  "Distributed Computer Systems",        "systems",  2),
    "1390":  ("CSCI 1390",  "Systems for Machine Learning",        "systems",  2),
    "1600":  ("CSCI 1600",  "Real-Time & Embedded Software",       "systems",  2),
    "1650":  ("CSCI 1650",  "Software Security & Exploitation",    "security", 2),
    "1660":  ("CSCI 1660",  "Computer Systems Security",           "security", 2),
    "1670":  ("CSCI 1670",  "Operating Systems",                   "systems",  2),
    "1680":  ("CSCI 1680",  "Computer Networks",                   "systems",  2),
    "1730":  ("CSCI 1730",  "Programming Languages",               "systems",  2),
    "1760":  ("CSCI 1760",  "Multiprocessor Synchronization",      "systems",  2),
    "1360":  ("CSCI 1360",  "Human Factors in Cybersecurity",      "security", 2),
    "1410":  ("CSCI 1410",  "Artificial Intelligence",             "ai",       2),
    "1450":  ("CSCI 1450",  "Probability for Computing",           "ai",       2),
    "1580":  ("CSCI 1580",  "Information Retrieval",               "ai",       2),
    "1810":  ("CSCI 1810",  "Computational Molecular Biology",     "compbio",  2),
    "1230":  ("CSCI 1230",  "Computer Graphics",                   "visual",   2),
    "1250":  ("CSCI 1250",  "Intro Computer Animation",            "visual",   2),
    "1290":  ("CSCI 1290",  "Computational Photography",           "visual",   2),
    "1370":  ("CSCI 1370",  "VR Design for Science",               "visual",   2),
    "1300":  ("CSCI 1300",  "Interaction Design (UI/UX)",          "design",   2),
    "1302":  ("CSCI 1302",  "Sociotechnical Systems & HCI",        "design",   2),
    "1377":  ("CSCI 1377",  "Tools for Thought",                   "design",   2),
    "1900":  ("CSCI 1900",  "csciStartup",                         "design",   2),

    # UPPER 1000-LEVEL (level 3)
    "1950H": ("CSCI 1950H", "Computational Topology",              "theory",   3),
    "1951G": ("CSCI 1951G", "Optimization Methods in Finance",     "theory",   3),
    "1951W": ("CSCI 1951W", "Sublinear Algorithms",                "theory",   3),
    "1951X": ("CSCI 1951X", "Formal Proof & Verification",         "theory",   3),
    "1675":  ("CSCI 1675",  "High-Perf Network Systems",           "systems",  3),
    "1951Q": ("CSCI 1951Q", "Topics in Programming Languages",     "systems",  3),
    "1951U": ("CSCI 1951U", "Software Eng of Large Systems",       "systems",  3),
    "1951V": ("CSCI 1951V", "Hypertext / Hypermedia",              "systems",  3),
    "1952Y": ("CSCI 1952Y", "Computer Architecture",               "systems",  3),
    "1515":  ("CSCI 1515",  "Applied Cryptography",                "security", 3),
    "1800":  ("CSCI 1800",  "Cybersecurity & Intl Relations",      "security", 3),
    "1805":  ("CSCI 1805",  "Computers, Freedom & Privacy",        "security", 3),
    "1860":  ("CSCI 1860",  "Cybersecurity Law & Policy",          "security", 3),
    "1870":  ("CSCI 1870",  "Cybersecurity Ethics",                "security", 3),
    "1951L": ("CSCI 1951L", "Blockchains & Cryptocurrencies",      "security", 3),
    "1953A": ("CSCI 1953A", "Accessible & Incl Cybersecurity",     "security", 3),
    "1420":  ("CSCI 1420",  "Machine Learning",                    "ai",       3),
    "1430":  ("CSCI 1430",  "Computer Vision",                     "ai",       3),
    "1460":  ("CSCI 1460",  "Computational Linguistics",           "ai",       3),
    "1470":  ("CSCI 1470",  "Deep Learning",                       "ai",       3),
    "1520":  ("CSCI 1520",  "Algorithmic Aspects of ML",           "ai",       3),
    "1640":  ("CSCI 1640",  "AI and Security",                     "ai",       3),
    "1951A": ("CSCI 1951A", "Data Science",                        "ai",       3),
    "1951C": ("CSCI 1951C", "Humanity-Centered Robots",            "ai",       3),
    "1951O": ("CSCI 1951O", "Design of Robotic Systems",           "ai",       3),
    "1951R": ("CSCI 1951R", "Introduction to Robotics",            "ai",       3),
    "1951Z": ("CSCI 1951Z", "Fairness in Automated Decision",      "ai",       3),
    "1952I": ("CSCI 1952I", "Language Processing",                 "ai",       3),
    "1952Z": ("CSCI 1952Z", "Robots as a Medium",                  "ai",       3),
    "1820":  ("CSCI 1820",  "Algorithmic Foundations of CompBio",  "compbio",  3),
    "1850":  ("CSCI 1850",  "Deep Learning in Genomics",           "compbio",  3),
    "1280":  ("CSCI 1280",  "Intermediate 3D Animation",           "visual",   3),
    "1950N": ("CSCI 1950N", "2D Game Engines",                     "visual",   3),
    "1950T": ("CSCI 1950T", "Advanced Animation Production",       "visual",   3),
    "1950U": ("CSCI 1950U", "3D Game Engine Development",          "visual",   3),
    "1951S": ("CSCI 1951S", "Virtual Reality Software Review",     "visual",   3),
    "1951T": ("CSCI 1951T", "Surveying VR Data Visualization",     "visual",   3),
    "1952A": ("CSCI 1952A", "Human-AI Interaction",                "design",   3),
    "1952B": ("CSCI 1952B", "Responsible CS in Practice",          "design",   3),
    "1952V": ("CSCI 1952V", "Algorithms for the People",           "design",   3),
    "1951I": ("CSCI 1951I", "CS for Social Change",                "design",   3),
    "1951B": ("CSCI 1951B", "Virtual Citizens or Subjects?",       "design",   3),
    "1970":  ("CSCI 1970",  "Independent Study (Capstone)",        "misc",     3),

    # GRADUATE 2000-LEVEL (level 4)
    "2440":  ("CSCI 2440",  "Adv Algorithmic Game Theory",         "theory",   4),
    "2500A": ("CSCI 2500A", "Advanced Algorithms",                 "theory",   4),
    "2500B": ("CSCI 2500B", "Opt Algorithms for Planar Graphs",    "theory",   4),
    "2510":  ("CSCI 2510",  "Approximation Algorithms",            "theory",   4),
    "2540":  ("CSCI 2540",  "Adv Probabilistic Methods",           "theory",   4),
    "2730":  ("CSCI 2730",  "Programming Language Theory",         "theory",   4),
    "2750":  ("CSCI 2750",  "Parallel & Distributed Computing",    "theory",   4),
    "2950E": ("CSCI 2950E", "Stochastic Optimization",             "theory",   4),
    "2950K": ("CSCI 2950K", "Special Topics: Comp Linguistics",    "theory",   4),
    "2951Q": ("CSCI 2951Q", "Topics in Advanced Algorithms",       "theory",   4),
    "2952M": ("CSCI 2952M", "Works in Machine Learning",           "theory",   4),
    "2952T": ("CSCI 2952T", "An Algorithmist's Toolkit",           "theory",   4),
    "2952U": ("CSCI 2952U", "Beyond Worst Case Algorithms",        "theory",   4),
    "2270":  ("CSCI 2270",  "Topics in Database Management",       "systems",  4),
    "2330":  ("CSCI 2330",  "Programming Environments",            "systems",  4),
    "2340":  ("CSCI 2340",  "Software Engineering",                "systems",  4),
    "2680":  ("CSCI 2680",  "Computer Networks & Internet",        "systems",  4),
    "2690":  ("CSCI 2690",  "Datacenter & Cloud OS",               "systems",  4),
    "2950X": ("CSCI 2950X", "Programming Languages & Systems",     "systems",  4),
    "2951H": ("CSCI 2951H", "Algorithms for Big Data",             "systems",  4),
    "2951O": ("CSCI 2951O", "Foundations of Prescriptive Analytics","systems", 4),
    "2952E": ("CSCI 2952E", "Network Management Topics",           "systems",  4),
    "2952F": ("CSCI 2952F", "Distributed Systems at Scale",        "systems",  4),
    "2952J": ("CSCI 2952J", "Computing w/ Emerging Technologies",  "systems",  4),
    "2952R": ("CSCI 2952R", "Systems Transforming Systems",        "systems",  4),
    "2950U2":("CSCI 2950U", "Networking & Distributed Systems",    "systems",  4),
    "2390":  ("CSCI 2390",  "Privacy-Conscious CS",                "security", 4),
    "2590":  ("CSCI 2590",  "Advanced Topics in Cryptography",     "security", 4),
    "2950V": ("CSCI 2950V", "Topics in Applied Cryptography",      "security", 4),
    "2951E": ("CSCI 2951E", "Topics in CS Security",               "security", 4),
    "2951U": ("CSCI 2951U", "Topics in Software Security",         "security", 4),
    "2402C": ("CSCI 2402C", "Reading the Large Language Models",   "ai",       4),
    "2410":  ("CSCI 2410",  "Statistical Models in NLU",           "ai",       4),
    "2420":  ("CSCI 2420",  "Probabilistic Graphical Models",      "ai",       4),
    "2640":  ("CSCI 2640",  "AI & Cybersecurity Policy",           "ai",       4),
    "2951C": ("CSCI 2951C", "Autonomous Agents & Market Design",   "ai",       4),
    "2951F": ("CSCI 2951F", "Learning & Sequential Decision",      "ai",       4),
    "2951K": ("CSCI 2951K", "Topics in Collaborative Robotics",    "ai",       4),
    "2951W": ("CSCI 2951W", "Creative AI for Comp Graphics",       "ai",       4),
    "2951X": ("CSCI 2951X", "Reintegrating AI",                    "ai",       4),
    "2951Z": ("CSCI 2951Z", "Advanced Algorithmic Game Theory",    "ai",       4),
    "2952C": ("CSCI 2952C", "Learning w/ Limited Labeled Data",    "ai",       4),
    "2952D": ("CSCI 2952D", "Computational Semantics",             "ai",       4),
    "2952L": ("CSCI 2952L", "Robotics and Choreography",           "ai",       4),
    "2952N": ("CSCI 2952N", "Advanced Deep Learning",              "ai",       4),
    "2952O": ("CSCI 2952O", "3D Robot Perception",                 "ai",       4),
    "2952P": ("CSCI 2952P", "Coordinated Mobile Robotics",         "ai",       4),
    "2952Q": ("CSCI 2952Q", "Robust Algorithms for ML",            "ai",       4),
    "2952W": ("CSCI 2952W", "Critical Data & ML Studies",          "ai",       4),
    "2952X": ("CSCI 2952X", "Research in Self-Supervised Learning","ai",       4),
    "2955":  ("CSCI 2955",  "Design & Analysis of Trading Agents", "ai",       4),
    "2820":  ("CSCI 2820",  "Adv Algorithms in Comp Biology",      "compbio",  4),
    "2952G": ("CSCI 2952G", "Deep Learning in Genomics (Grad)",    "compbio",  4),
    "2240":  ("CSCI 2240",  "Interactive Computer Graphics",       "visual",   4),
    "2370":  ("CSCI 2370",  "Interdisciplinary Sci Visualization", "visual",   4),
    "2950J": ("CSCI 2950J", "Cognition, HCI & Visual Analysis",    "visual",   4),
    "2950Q": ("CSCI 2950Q", "Topics in Computer Vision",           "visual",   4),
    "2951I": ("CSCI 2951I", "CV for Graphics & Interaction",       "visual",   4),
    "2952K": ("CSCI 2952K", "3D Computer Vision & Deep Learning",  "visual",   4),
    "2300":  ("CSCI 2300",  "HCI Seminar",                         "design",   4),
    "2952V": ("CSCI 2952V", "Algorithms for the People (Grad)",    "design",   4),
    "2952Y": ("CSCI 2952Y", "Computational Design & Fabrication",  "design",   4),
    "2890":  ("CSCI 2890",  "Graduate Independent Study",          "misc",     4),
}

# ─── PREREQS ───────────────────────────────────────────────────────────────────
PREREQS = [
    # Intro → Gateway
    ("0111","0200"),("0150","0200"),("0170","0200"),("0190","0200"),
    ("0200","0220"),("0200","0300"),("0200","0320"),("0200","0330"),
    # Theory
    ("0220","1010"),("0220","1440"),("0220","1510"),("0220","1550"),
    ("0220","1570"),("0220","1710"),("0220","1040"),
    ("1550","2540"),("1570","2500A"),("1570","2500B"),("1570","2510"),
    ("1510","1515"),("1510","2590"),("1510","1951L"),("1510","2950V"),
    ("1710","1951X"),("1710","2730"),
    ("1440","2440"),("1440","2951Z"),("1440","2955"),
    ("1550","2950E"),("1010","1951W"),
    ("1570","1951G"),("1570","2952T"),("2500A","2952U"),("2500A","2951Q"),
    ("1570","2750"),("1570","2950K"),
    # Systems
    ("0300","1670"),("0320","1670"),("0330","1670"),
    ("0300","1680"),("0320","1680"),("0330","1680"),
    ("0300","1600"),("0320","1600"),("0330","1600"),
    ("0300","1650"),("0320","1650"),("0330","1650"),
    ("0300","1660"),("0320","1660"),("0330","1660"),
    ("0320","1270"),("0330","1270"),
    ("0320","1260"),("0330","1260"),
    ("0320","1320"),("0330","1320"),
    ("0320","1380"),("0330","1380"),
    ("0300","1390"),("0320","1390"),
    ("0220","1730"),("0320","1730"),
    ("1670","1760"),("1670","1675"),("1680","1675"),
    ("1670","1952Y"),("1670","2690"),("1680","2680"),
    ("1270","2270"),("1660","2390"),("1670","2390"),
    ("1380","2952F"),("1380","2952R"),("1380","2950U2"),
    ("0320","1951U"),("0320","2340"),("0220","2330"),
    ("1730","1951Q"),("1730","2730"),("1730","2950X"),
    ("1260","2330"),("1260","2950X"),
    ("1380","2951H"),("1380","2952E"),("1380","2952J"),
    ("1660","2951E"),("1650","2951U"),
    ("1270","2951O"),
    # AI/ML
    ("0200","1410"),("0200","1450"),("0200","1580"),
    ("1410","1420"),("1450","1420"),
    ("1420","1430"),("1420","1470"),("1420","1520"),
    ("1420","1640"),("1420","1951Z"),("1420","2420"),
    ("1420","2951F"),("1420","2952Q"),
    ("1410","1460"),("1460","2410"),("1460","1952I"),("1460","2952D"),
    ("1470","1850"),("1850","2952G"),
    ("1430","2952K"),("1470","2952N"),
    ("1420","2952W"),("1420","2640"),
    ("1450","1951A"),
    ("1410","1951R"),("1951R","1951C"),("1951R","1951O"),
    ("1420","1952A"),("1420","2951X"),
    ("1470","2402C"),("1470","2951K"),
    ("1440","2951C"),
    ("1420","2952L"),("1420","2952P"),("1420","2952O"),
    ("1420","2952X"),("1420","2952C"),
    ("1420","2951W"),("1420","2952N"),
    ("1420","2955"),
    # CompBio
    ("0200","1810"),("1810","1820"),("1820","2820"),
    ("1470","1850"),
    # Visual
    ("0200","1230"),("0200","1250"),("0200","1290"),("0200","1370"),
    ("1230","1280"),("1230","2240"),("1230","1950N"),("1230","1950U"),
    ("1250","1950T"),("2240","2370"),
    ("1430","2950Q"),("1430","2951I"),
    ("1470","2952K"),("1230","2952K"),
    ("2240","2950J"),("1951S","1951T"),
    # Design
    ("0200","1300"),("0200","1302"),("0200","1377"),("0200","1900"),
    ("1300","2300"),("1302","1952A"),("1302","1952B"),
    ("0200","1951I"),
    # Security extras
    ("0200","1360"),("0200","1800"),("0200","1805"),
    ("1510","1860"),("1510","1870"),
    ("1800","2640"),
]

# ─── LAYOUT ENGINE ─────────────────────────────────────────────────────────────
BOX_W    = 2.10   # inches
BOX_H    = 0.58   # inches
GAP_X    = 0.12   # horizontal gap within a cell
GAP_Y    = 0.10   # vertical gap within a cell
BAND_GAP = 0.55   # gap between pathway bands
LEVEL_GAP = 1.30  # extra vertical gap between levels (room for arrows)

MAX_COLS = 3      # max sub-columns per (pathway × level) cell


def build_layout(courses, pathway_order):
    cells = defaultdict(list)
    for cid, (code, name, pw, lv) in courses.items():
        cells[(lv, pw)].append(cid)
    for k in cells:
        cells[k].sort(key=lambda c: courses[c][0])  # sort by code

    cell_rows = {}  # (lv, pw) -> number of rows in that cell
    for (lv, pw), cids in cells.items():
        cell_rows[(lv, pw)] = ceil(len(cids) / MAX_COLS)

    # Height of each level row (max rows across all pathways at that level)
    level_row_count = {}
    for lv in range(5):
        level_row_count[lv] = max(
            (cell_rows.get((lv, pw), 0) for pw in pathway_order),
            default=1
        )

    # Cumulative Y positions — level 0 (intro) at LARGEST y (top of plot).
    # We first compute each level's height, then assign y top-down.
    cell_heights = {}
    for lv in range(5):
        cell_heights[lv] = level_row_count[lv] * (BOX_H + GAP_Y) - GAP_Y

    total_height = sum(cell_heights[lv] + LEVEL_GAP for lv in range(5)) - LEVEL_GAP

    # level_y[lv] = y coordinate of the TOP edge of that level's region
    # Level 0 is at the TOP → highest y value
    level_y = {}
    y_top = total_height
    for lv in range(5):
        level_y[lv] = y_top - cell_heights[lv]   # top edge stored; we'll use cy = top+row*(BOX_H+GAP_Y)
        y_top = level_y[lv] - LEVEL_GAP

    # X positions for each pathway band
    band_x = {}    # pw -> x of LEFT edge of band
    x_cursor = 0.0
    for pw in pathway_order:
        band_x[pw] = x_cursor
        # Width = MAX_COLS columns (use actual max courses per level for tighter fit)
        max_cols_used = max(
            (min(len(cells.get((lv, pw), [])), MAX_COLS) for lv in range(5)),
            default=0
        )
        if max_cols_used == 0:
            band_x[pw] = x_cursor  # still reserve space for label
            max_cols_used = 1
        band_w = max_cols_used * (BOX_W + GAP_X) - GAP_X
        x_cursor += band_w + BAND_GAP

    total_width = x_cursor - BAND_GAP

    # Assign positions to each course
    positions = {}  # cid -> (cx, cy)  center of box
    for (lv, pw), cids in cells.items():
        bx = band_x[pw]
        by = level_y[lv]
        for idx, cid in enumerate(cids):
            col = idx % MAX_COLS
            row = idx // MAX_COLS
            cx = bx + col * (BOX_W + GAP_X) + BOX_W / 2
            # level_y[lv] is the TOP edge of the level band; rows go downward
            cy = by - row * (BOX_H + GAP_Y) - BOX_H / 2
            positions[cid] = (cx, cy)

    return positions, band_x, level_y, level_row_count, total_width, total_height, cells


def main():
    positions, band_x, level_y, level_row_count, TW, TH, cells = \
        build_layout(COURSES, PATHWAY_ORDER)

    MARGIN = 1.2
    fig_w = TW + 2 * MARGIN + 1.5   # +1.5 for level labels on left
    fig_h = TH + 2 * MARGIN + 1.8   # +1.8 for title + legend

    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=130)
    ox = MARGIN + 1.5   # x origin offset (left side for level labels)
    oy = MARGIN + 1.2   # y origin offset (bottom, title at top)

    ax.set_xlim(-ox, fig_w - MARGIN)
    ax.set_ylim(-oy, fig_h - oy - MARGIN * 0.3)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#F6F6F6')
    ax.set_facecolor('#F6F6F6')

    # ── Pathway band backgrounds ───────────────────────────────────────────
    y_bottom = -LEVEL_GAP * 0.4
    y_top_bg = TH + 0.15
    for pw in PATHWAY_ORDER:
        color = PATHWAYS[pw][1]
        xs = [positions[cid][0] for cid, (_, _, cpw, _) in COURSES.items()
              if cpw == pw and cid in positions]
        if not xs:
            continue
        x0 = min(xs) - BOX_W / 2 - 0.08
        x1 = max(xs) + BOX_W / 2 + 0.08
        rect = mpatches.FancyBboxPatch(
            (x0, y_bottom), x1 - x0, y_top_bg - y_bottom,
            boxstyle="round,pad=0.05",
            facecolor=color, edgecolor='#888888',
            linewidth=0.6, alpha=0.20, zorder=0
        )
        ax.add_patch(rect)
        mid_x = (x0 + x1) / 2
        ax.text(mid_x, y_top_bg + 0.25, PATHWAYS[pw][0],
                ha='center', va='bottom', fontsize=6.8,
                fontweight='bold', color='#222222', zorder=5)

    # ── Level row dividers and labels ──────────────────────────────────────
    level_labels = {
        0: "Intro\nSequence",
        1: "Gateway\nCourses",
        2: "Core\n1000-Level",
        3: "Upper\n1000-Level",
        4: "Graduate\n2000-Level",
    }
    for lv in range(5):
        top_edge = level_y[lv]   # top edge of this level
        cell_h = level_row_count[lv] * (BOX_H + GAP_Y) - GAP_Y
        bot_edge = top_edge - cell_h
        mid_y = (top_edge + bot_edge) / 2
        ax.text(-0.35, mid_y, level_labels[lv],
                ha='right', va='center', fontsize=6.5,
                fontweight='bold', color='#444444', linespacing=1.35)
        # Divider line between levels (below the bottom of this level)
        ax.axhline(bot_edge - LEVEL_GAP / 2, color='#CCCCCC',
                   linewidth=0.45, linestyle='--', zorder=0)

    # ── Prerequisite arrows ────────────────────────────────────────────────
    valid = set(COURSES.keys()) & set(positions.keys())
    for (src, dst) in PREREQS:
        if src not in valid or dst not in valid:
            continue
        sx, sy = positions[src]
        dx, dy = positions[dst]
        # Arrow from bottom of src to top of dst (or side if same level)
        src_lv = COURSES[src][3]
        dst_lv = COURSES[dst][3]
        if src_lv < dst_lv:
            # Higher level → lower level visually (level 0 has highest y)
            # Arrow from BOTTOM of src (lower y) to TOP of dst (higher y relative within its level)
            start = (sx, sy - BOX_H / 2)   # bottom of src box
            end   = (dx, dy + BOX_H / 2)   # top of dst box
            rad   = 0.05 if abs(sx - dx) < 2 else 0.20
        else:
            # Same level sideways arrow
            if sx < dx:
                start = (sx + BOX_W / 2, sy)
                end   = (dx - BOX_W / 2, dy)
            else:
                start = (sx - BOX_W / 2, sy)
                end   = (dx + BOX_W / 2, dy)
            rad   = 0.25
        ax.annotate(
            "", xy=end, xytext=start,
            arrowprops=dict(
                arrowstyle="-|>",
                color='#555555',
                lw=0.55,
                mutation_scale=6,
                connectionstyle=f"arc3,rad={rad}",
            ),
            zorder=1
        )

    # ── Course boxes ───────────────────────────────────────────────────────
    for cid, (code, name, pw, lv) in COURSES.items():
        if cid not in positions:
            continue
        cx, cy = positions[cid]
        color = PATHWAYS[pw][1]

        # Slightly lighten fill color for readability
        box = mpatches.FancyBboxPatch(
            (cx - BOX_W / 2, cy - BOX_H / 2), BOX_W, BOX_H,
            boxstyle="round,pad=0.04",
            facecolor=color, edgecolor='#2A2A2A',
            linewidth=0.90, zorder=2
        )
        ax.add_patch(box)

        # Course code — bold top
        ax.text(cx, cy + BOX_H * 0.20, code,
                ha='center', va='center',
                fontsize=5.4, fontweight='bold',
                color='#0A0A0A', zorder=3)
        # Course name — wrap at ~26 chars
        n = name
        if len(n) > 26:
            split = n[:26].rfind(' ')
            split = split if split > 10 else 26
            line1, line2 = n[:split], n[split:].strip()
            ax.text(cx, cy - BOX_H * 0.05, line1,
                    ha='center', va='center',
                    fontsize=4.1, color='#1A1A1A', zorder=3)
            ax.text(cx, cy - BOX_H * 0.38, line2,
                    ha='center', va='center',
                    fontsize=4.1, color='#1A1A1A', zorder=3)
        else:
            ax.text(cx, cy - BOX_H * 0.20, n,
                    ha='center', va='center',
                    fontsize=4.3, color='#1A1A1A', zorder=3)

    # ── Title ──────────────────────────────────────────────────────────────
    title_y = TH + 1.05
    ax.text(TW / 2, title_y,
            "Brown University CS — Course Flowchart (2020 Pathway Requirements)",
            ha='center', va='center', fontsize=11.5, fontweight='bold',
            color='#111111')
    ax.text(TW / 2, title_y - 0.45,
            "Arrows = prerequisites  •  Color = primary pathway  •  "
            "Source: cs.brown.edu pathways page  •  2020 requirements (for classes 2024 and earlier)",
            ha='center', va='center', fontsize=6.2, color='#555555')

    # ── Legend ─────────────────────────────────────────────────────────────
    patches = [
        mpatches.Patch(facecolor=PATHWAYS[pw][1], edgecolor='#555555',
                       linewidth=0.7, label=PATHWAYS[pw][0])
        for pw in PATHWAY_ORDER
    ]
    leg = ax.legend(handles=patches,
                    loc='lower left',
                    bbox_to_anchor=(-0.35 / fig_w, -oy / (fig_h - oy)),
                    ncol=len(PATHWAY_ORDER),
                    fontsize=6.2, framealpha=0.85,
                    edgecolor='#AAAAAA',
                    title="Pathway Legend",
                    title_fontsize=7)

    out = "/Users/francoisleutou/Desktop/CodingSpace/cs1970KF Projects/brown_cs_course_flowchart.png"
    fig.savefig(out, dpi=130, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    plt.close(fig)

    total = len([c for c in COURSES if c in positions])
    print(f"Saved: {out}")
    print(f"Canvas: {fig_w:.1f}\" × {fig_h:.1f}\"  @130 DPI → "
          f"{int(fig_w*130)} × {int(fig_h*130)} px")
    print(f"Courses plotted: {total}")


if __name__ == "__main__":
    main()
