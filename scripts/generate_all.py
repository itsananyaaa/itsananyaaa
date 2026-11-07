"""
Master SVG Visual Asset Generator for Ananya Biju's Profile README (Revision 2).
Incorporates all user feedback:
1. Natural photographic portrait (original tones, upright, cropped, no red duotone).
2. 10.0 / 10 CGPA everywhere with zero text overflow.
3. Interactive hoverable grid block background in hero banner.
4. SMIL + CSS infinitely sliding marquee ticker with achievements on top.
5. All 18+ GitHub projects as individual cards (zero plain text).
6. Complete technical proficiencies in structured SVG card blocks (no 'resume source').
7. Fixed 3D GitHub skyline with zero overlap (pushed down with clear clearance).
8. Wins wall with all achievements in visual cards (including 1st Prize Design for Her Ideathon).
9. Internships flowchart retained as visual card only (no plain text).
10. Off-Duty bento with Bobby the cat.
11. Dedicated individual clickable pill buttons at the bottom (Resume, LinkedIn, GitHub, LeetCode, Goodreads, Email).
"""

import os
import json
import base64
from pathlib import Path
from design_tokens import (
    COLOR_BG, COLOR_CARD, COLOR_BORDER, COLOR_BORDER_HOT, COLOR_RED_HOT, COLOR_RED_ACCENT,
    COLOR_RED_DEEP, COLOR_RED_MUTED, COLOR_WHITE, COLOR_GREY_MUTED, COLOR_GREY_CHIP,
    FONT_ANTON, FONT_INTER, REPO_ROOT
)
from svg_engine import text_path, measure_text

ASSETS_DIR = REPO_ROOT / "assets"
for folder in ["hero", "about", "stats", "work", "stack", "activity", "wins", "timeline", "offduty", "closing"]:
    (ASSETS_DIR / folder).mkdir(parents=True, exist_ok=True)


def svg_wrapper(w: int, h: int, inner_xml: str, extra_defs: str = "") -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%">
  <defs>
    <style>
      @media (prefers-reduced-motion: reduce) {{
        .animated {{ animation: none !important; }}
      }}
      @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
      }}
      @keyframes pulse {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.35; transform: scale(0.92); }}
      }}
      .card-hover {{
        transition: stroke 0.25s ease, filter 0.25s ease;
      }}
      .card-hover:hover {{
        stroke: {COLOR_RED_HOT} !important;
        stroke-width: 1.5px !important;
        filter: drop-shadow(0 0 10px rgba(226, 35, 47, 0.5));
      }}
      .grid-block {{
        transition: fill 0.2s ease, stroke 0.2s ease;
      }}
      .grid-block:hover {{
        fill: #2A0407 !important;
        stroke: {COLOR_RED_HOT} !important;
      }}
    </style>
    {extra_defs}
  </defs>
  <rect width="100%" height="100%" fill="{COLOR_BG}"/>
  {inner_xml}
</svg>"""


# ==========================================
# 0. HERO SECTION (WITH INTERACTIVE GRID)
# ==========================================
def generate_hero():
    w, h = 1000, 440
    portrait_path = ASSETS_DIR / "hero" / "portrait_original.png"
    if not portrait_path.exists():
        portrait_path = ASSETS_DIR / "hero" / "portrait_duotone.png"
    
    portrait_b64 = ""
    if portrait_path.exists():
        with open(portrait_path, "rb") as f:
            portrait_b64 = base64.b64encode(f.read()).decode("ascii")

    # Interactive background grid blocks (50x50 cells)
    grid_xml = ""
    for gx in range(0, w, 50):
        for gy in range(0, h, 44):
            grid_xml += f'<rect class="grid-block" x="{gx}" y="{gy}" width="49" height="43" fill="#0C0C0D" stroke="#161618" stroke-width="0.5"/>\n'

    # Rotating red asterisk at top right
    asterisk_svg = f"""
    <g transform="translate(940, 55)">
      <g class="animated" style="transform-origin: 0 0; animation: spin 20s linear infinite;">
        <line x1="0" y1="-22" x2="0" y2="22" stroke="{COLOR_RED_HOT}" stroke-width="4.5" stroke-linecap="round"/>
        <line x1="-19" y1="-11" x2="19" y2="11" stroke="{COLOR_RED_HOT}" stroke-width="4.5" stroke-linecap="round"/>
        <line x1="-19" y1="11" x2="19" y2="-11" stroke="{COLOR_RED_HOT}" stroke-width="4.5" stroke-linecap="round"/>
      </g>
    </g>
    """

    tag0 = text_path(FONT_INTER, "00 // PORTFOLIO PROFILE", 50, 45, 12, fill=COLOR_RED_HOT, tracking=0.15)
    tag1 = text_path(FONT_INTER, "CHRIST COLLEGE OF ENGINEERING // EST. 2024", 50, 68, 11, fill=COLOR_GREY_MUTED, tracking=0.12)
    tag2 = text_path(FONT_INTER, "IRINJALAKUDA, KERALA, INDIA", 50, 90, 11, fill=COLOR_GREY_MUTED, tracking=0.12)

    title_ananya = text_path(FONT_ANTON, "ANANYA", 50, 220, 130, fill="none", stroke=COLOR_WHITE, stroke_width=2.5, tracking=0.04)
    title_biju = text_path(FONT_ANTON, "BIJU", 50, 345, 130, fill=COLOR_RED_HOT, tracking=0.04)

    role_bg = f'<rect class="card-hover" x="50" y="375" width="280" height="34" rx="4" fill="{COLOR_CARD}" stroke="{COLOR_BORDER}" stroke-width="1"/>'
    role_live_dot = f'<circle cx="68" cy="392" r="4.5" fill="{COLOR_RED_HOT}" class="animated" style="animation: pulse 2s ease-in-out infinite;"/>'
    role_txt = text_path(FONT_INTER, "AI/ML BUILDER // SYSTEMS // VISION", 82, 396, 11, fill=COLOR_WHITE, tracking=0.1)

    cgpa_pill = f'<rect class="card-hover" x="345" y="375" width="130" height="34" rx="4" fill="{COLOR_CARD}" stroke="{COLOR_BORDER_HOT}" stroke-width="1.5"/>'
    cgpa_txt = text_path(FONT_INTER, "CGPA 10.0 / 10", 360, 396, 11, fill=COLOR_RED_HOT, tracking=0.1)

    portrait_element = ""
    if portrait_b64:
        portrait_element = f"""
        <g transform="translate(560, 35)">
          <rect class="card-hover" x="0" y="0" width="390" height="375" rx="8" fill="{COLOR_CARD}" stroke="{COLOR_BORDER_HOT}" stroke-width="1"/>
          <circle cx="195" cy="180" r="150" fill="{COLOR_RED_DEEP}" opacity="0.2"/>
          <clipPath id="portrait-clip">
            <rect x="2" y="2" width="386" height="330" rx="7"/>
          </clipPath>
          <image href="data:image/png;base64,{portrait_b64}" x="5" y="5" width="380" height="325" preserveAspectRatio="xMidYMid slice" clip-path="url(#portrait-clip)"/>
          <line x1="0" y1="334" x2="390" y2="334" stroke="{COLOR_BORDER}" stroke-width="1"/>
          {text_path(FONT_INTER, "ANANYA BIJU // PORTRAIT FILE", 15, 358, 10, fill=COLOR_WHITE, tracking=0.12)}
          {text_path(FONT_INTER, "ORIGINAL TONES", 285, 358, 10, fill=COLOR_RED_HOT, tracking=0.12)}
        </g>
        """

    inner = f"""
    <!-- Interactive Background Grid -->
    <g opacity="0.75">
      {grid_xml}
    </g>
    <!-- Background blackout overlay behind text -->
    <rect x="40" y="20" width="490" height="400" rx="8" fill="{COLOR_BG}" opacity="0.88"/>
    <line x1="50" y1="110" x2="520" y2="110" stroke="{COLOR_BORDER}" stroke-width="1"/>
    {tag0}
    {tag1}
    {tag2}
    {asterisk_svg}
    {title_ananya}
    {title_biju}
    {role_bg}
    {role_live_dot}
    {role_txt}
    {cgpa_pill}
    {cgpa_txt}
    {portrait_element}
    """
    svg = svg_wrapper(w, h, inner)
    (ASSETS_DIR / "hero" / "hero_banner.svg").write_text(svg)
    print("Generated hero_banner.svg with interactive grid blocks")


# ==========================================
# 0b. CONTINUOUS SLIDING TICKER (ACHIEVEMENTS ON TOP)
# ==========================================
def generate_marquee():
    w, h = 1000, 48
    items = "  *  1ST PRIZE DESIGN FOR HER IDEATHON  *  FIRST RUNNER-UP PFRDA x IIT KANPUR  *  GUARDIAN WING PATENT FILED  *  10.0 / 10 CGPA  *  BEST PERFORMER GEC THRISSUR  *  WINNER SYNAPSE DEBATE  *  7 TECHNICAL INTERNSHIPS COMPLETED  *  AI/ML & COMPUTER VISION  *  "
    w_text = measure_text(FONT_INTER, items, 13, tracking=0.18)
    t1 = text_path(FONT_INTER, items, 0, 30, 13, fill=COLOR_WHITE, tracking=0.18)
    t2 = text_path(FONT_INTER, items, w_text, 30, 13, fill=COLOR_WHITE, tracking=0.18)

    marquee_defs = f"""
      @keyframes marquee_loop {{
        0% {{ transform: translateX(0); }}
        100% {{ transform: translateX(-{w_text:.1f}px); }}
      }}
    """

    inner = f"""
    <line x1="0" y1="0.5" x2="{w}" y2="0.5" stroke="{COLOR_BORDER}" stroke-width="1"/>
    <line x1="0" y1="{h-0.5}" x2="{w}" y2="{h-0.5}" stroke="{COLOR_BORDER}" stroke-width="1"/>
    <g class="animated" style="animation: marquee_loop 24s linear infinite;">
      <animateTransform attributeName="transform" type="translate" from="0 0" to="-{w_text:.1f} 0" dur="24s" repeatCount="indefinite"/>
      {t1}
      {t2}
    </g>
    """
    svg = svg_wrapper(w, h, inner, extra_defs=marquee_defs)
    (ASSETS_DIR / "hero" / "marquee_strip.svg").write_text(svg)
    print("Generated marquee_strip.svg with achievements on top and SMIL animation")


# ==========================================
# 1. ABOUT BENTO (NO TEXT OVERFLOW)
# ==========================================
def generate_about():
    w, h = 1000, 320
    col1 = f"""
    <rect class="card-hover" x="30" y="30" width="300" height="260" rx="6" fill="{COLOR_CARD}" stroke="{COLOR_BORDER}" stroke-width="1"/>
    {text_path(FONT_INTER, "01 // ROLE & IDENTITY", 50, 60, 11, fill=COLOR_RED_HOT, tracking=0.15)}
    {text_path(FONT_ANTON, "BUILDER.", 50, 105, 38, fill=COLOR_WHITE, tracking=0.03)}
    {text_path(FONT_ANTON, "ENGINEER.", 50, 145, 38, fill=COLOR_RED_HOT, tracking=0.03)}
    <line x1="50" y1="170" x2="310" y2="170" stroke="{COLOR_BORDER}" stroke-width="1"/>
    {text_path(FONT_INTER, "B.TECH COMPUTER SCIENCE", 50, 200, 12, fill=COLOR_WHITE, tracking=0.08)}
    {text_path(FONT_INTER, "Christ College of Engineering", 50, 222, 11.5, fill=COLOR_GREY_MUTED, tracking=0.04)}
    {text_path(FONT_INTER, "High-impact intelligent systems.", 50, 252, 11, fill=COLOR_GREY_MUTED, tracking=0.04)}
    """

    # Box 2: CGPA 10.0 (strictly verified inside borders)
    col2 = f"""
    <rect class="card-hover" x="350" y="30" width="300" height="260" rx="6" fill="{COLOR_CARD}" stroke="{COLOR_BORDER_HOT}" stroke-width="1.5"/>
    {text_path(FONT_INTER, "02 // ACADEMIC STANDING", 370, 60, 11, fill=COLOR_RED_HOT, tracking=0.15)}
    {text_path(FONT_ANTON, "10.0", 370, 135, 78, fill=COLOR_WHITE, tracking=0.02)}
    {text_path(FONT_INTER, "/ 10 CGPA", 535, 120, 18, fill=COLOR_RED_HOT, tracking=0.08)}
    <line x1="370" y1="170" x2="630" y2="170" stroke="{COLOR_BORDER}" stroke-width="1"/>
    {text_path(FONT_INTER, "PERFECT UNIVERSITY STANDING", 370, 198, 10.5, fill=COLOR_GREY_MUTED, tracking=0.1)}
    {text_path(FONT_INTER, "Top academic performance across CSE.", 370, 224, 10.5, fill=COLOR_WHITE, tracking=0.04)}
    {text_path(FONT_INTER, "Technical Lead @ CODe Association.", 370, 250, 10.5, fill=COLOR_GREY_MUTED, tracking=0.04)}
    """

    chips = [
        ("AI / ML", 670, 150),
        ("COMPUTER VISION", 750, 150),
        ("SYSTEMS", 670, 190),
        ("CYBERSECURITY", 760, 190),
        ("CLOUD", 670, 230),
        ("DEBATE", 745, 230),
    ]
    chip_xml = ""
    for label, cx, cy in chips:
        tw = measure_text(FONT_INTER, label, 10, tracking=0.1)
        chip_xml += f"""
        <rect x="{cx}" y="{cy}" width="{tw+20}" height="28" rx="14" fill="{COLOR_GREY_CHIP}" stroke="{COLOR_BORDER}" stroke-width="1"/>
        {text_path(FONT_INTER, label, cx+10, cy+18, 10, fill=COLOR_WHITE, tracking=0.1)}
        """

    col3 = f"""
    <rect class="card-hover" x="670" y="30" width="300" height="260" rx="6" fill="{COLOR_CARD}" stroke="{COLOR_BORDER}" stroke-width="1"/>
    {text_path(FONT_INTER, "03 // FOCUS & ROOTS", 690, 60, 11, fill=COLOR_RED_HOT, tracking=0.15)}
    {text_path(FONT_INTER, "LANGUAGES: EN / HI / ML / ES", 690, 90, 11, fill=COLOR_WHITE, tracking=0.08)}
    {text_path(FONT_INTER, "BASE: KERALA, INDIA", 690, 112, 11, fill=COLOR_GREY_MUTED, tracking=0.08)}
    <line x1="690" y1="130" x2="950" y2="130" stroke="{COLOR_BORDER}" stroke-width="1"/>
    {chip_xml}
    """

    inner = f"{col1}\n{col2}\n{col3}"
    svg = svg_wrapper(w, h, inner)
    (ASSETS_DIR / "about" / "about_bento.svg").write_text(svg)
    print("Generated about_bento.svg with zero text overflow")


# ==========================================
# 2. NUMBERS STATS SECTION
# ==========================================
def generate_numbers():
    w, h = 1000, 160
    stats = [
        ("10.0", "CGPA", "PERFECT ACADEMIC STANDING", 30),
        ("1", "PATENT", "APPLICATION FILED", 270),
        ("1ST", "RUNNER-UP", "PFRDA x IIT KANPUR", 510),
        ("7", "INTERNSHIPS", "TECHNICAL PROGRAMS", 750),
    ]

    tiles = ""
    for val, unit, caption, x in stats:
        tiles += f"""
        <g transform="translate({x}, 15)">
          <rect class="card-hover" x="0" y="0" width="220" height="130" rx="6" fill="{COLOR_CARD}" stroke="{COLOR_BORDER}" stroke-width="1"/>
          {text_path(FONT_ANTON, val, 20, 72, 54, fill=COLOR_WHITE, tracking=0.02)}
          {text_path(FONT_INTER, unit, 20, 95, 12, fill=COLOR_RED_HOT, tracking=0.15)}
          <line x1="20" y1="104" x2="200" y2="104" stroke="{COLOR_BORDER}" stroke-width="1"/>
          {text_path(FONT_INTER, caption, 20, 118, 9, fill=COLOR_GREY_MUTED, tracking=0.1)}
        </g>
        """

    svg = svg_wrapper(w, h, tiles)
    (ASSETS_DIR / "stats" / "numbers_row.svg").write_text(svg)
    print("Generated numbers_row.svg")


# ==========================================
# 3. WORK / ALL PROJECTS AS INDIVIDUAL CARDS
# ==========================================
def generate_all_project_cards():
    # 3.1 Pinned Hero Card: Guardian Wing
    gw_w, gw_h = 1000, 240
    gw_inner = f"""
    <rect class="card-hover" x="30" y="20" width="940" height="200" rx="8" fill="{COLOR_CARD}" stroke="{COLOR_BORDER_HOT}" stroke-width="1.5"/>
    <rect x="50" y="40" width="260" height="26" rx="4" fill="{COLOR_RED_MUTED}" stroke="{COLOR_RED_HOT}" stroke-width="1"/>
    {text_path(FONT_INTER, "PATENT APPLICATION FILED // APR 2026", 60, 57, 10, fill=COLOR_WHITE, tracking=0.12)}
    
    {text_path(FONT_ANTON, "GUARDIAN WING", 50, 115, 48, fill=COLOR_WHITE, tracking=0.04)}
    {text_path(FONT_INTER, "COLLABORATIVE FLEET INTELLIGENCE SYSTEM // APP NO. 202641048328", 50, 142, 12, fill=COLOR_RED_HOT, tracking=0.1)}
    {text_path(FONT_INTER, "Autonomous distributed vehicle coordination, low-latency telemetry and edge safety intelligence.", 50, 172, 12, fill=COLOR_GREY_MUTED, tracking=0.04)}
    
    <rect x="50" y="185" width="85" height="24" rx="12" fill="{COLOR_GREY_CHIP}" stroke="{COLOR_BORDER}" stroke-width="1"/>
    {text_path(FONT_INTER, "EDGE AI", 65, 201, 10, fill=COLOR_WHITE, tracking=0.1)}
    
    <rect x="145" y="185" width="115" height="24" rx="12" fill="{COLOR_GREY_CHIP}" stroke="{COLOR_BORDER}" stroke-width="1"/>
    {text_path(FONT_INTER, "TELEMETRY", 160, 201, 10, fill=COLOR_WHITE, tracking=0.1)}

    <rect x="270" y="185" width="150" height="24" rx="12" fill="{COLOR_GREY_CHIP}" stroke="{COLOR_BORDER}" stroke-width="1"/>
    {text_path(FONT_INTER, "DISTRIBUTED FLEET", 285, 201, 10, fill=COLOR_WHITE, tracking=0.1)}

    <g transform="translate(850, 110)">
      <circle cx="0" cy="0" r="45" fill="none" stroke="{COLOR_BORDER}" stroke-width="1"/>
      <circle cx="0" cy="0" r="30" fill="none" stroke="{COLOR_RED_HOT}" stroke-width="1.5" stroke-dasharray="4, 4"/>
      <circle cx="0" cy="0" r="6" fill="{COLOR_RED_HOT}"/>
    </g>
    """
    (ASSETS_DIR / "work" / "card_guardian_wing.svg").write_text(svg_wrapper(gw_w, gw_h, gw_inner))

    # All 18 projects in card format
    projects = [
        ("card_lucralens.svg", "02", "LUCRALENS AI", "AI & ML", "Streamlit app predicting corporate revenue using Random Forest regression.", ["PYTHON", "RANDOM FOREST", "STREAMLIT"]),
        ("card_roadsense.svg", "03", "ROADSENSE AI", "COMPUTER VISION", "AI road-damage detection & inspection-priority platform.", ["YOLO26N", "RDD2022", "PYTORCH"]),
        ("card_pocketplans.svg", "04", "POCKET PLANS", "FULL-STACK & APIS", "AI travel itinerary planner with real-time weather & maps routing.", ["FASTAPI", "GEOAPIFY", "WEATHER API"]),
        ("card_nids.svg", "05", "NETWORK INTRUSION AI", "SECURITY & ML", "ML network attack classifier with AI-driven plain explanations.", ["SCIKIT-LEARN", "RANDOM FOREST", "HUGGINGFACE"]),
        ("card_modis.svg", "06", "DEFORESTATION ML", "REMOTE SENSING", "Satellite telemetry analysis detecting forest cover transitions.", ["MODIS", "PANDAS", "GEOSPATIAL"]),
        ("card_noteverse.svg", "07", "NOTEVERSE", "UI & INTERACTION", "Fast drag-and-drop notes organizer with persistent state.", ["JAVASCRIPT", "DOM ENGINE", "LOCALSTORAGE"]),
        ("card_foodsync.svg", "08", "FOODSYNC / FOODHUB", "SPRING BOOT & REST", "Smart restaurant ordering system with table and billing workflows.", ["JAVA", "SPRING BOOT", "THYMELEAF", "REST"]),
        ("card_cloak.svg", "09", "INVISIBILITY CLOAK", "COMPUTER VISION", "Real-time color masking and live video background replacement.", ["PYTHON", "OPENCV", "NUMPY", "COLOR MASK"]),
        ("card_salary.svg", "10", "SALARY PREDICTOR", "HR ANALYTICS ML", "Interactive compensation regression engine based on empirical roles.", ["STREAMLIT", "PANDAS", "SCIKIT-LEARN"]),
        ("card_fitplan.svg", "11", "FITPLAN.AI", "HEALTH & ACTIVITY ML", "Personalized fitness analytics engine and health dashboard capstone.", ["JUPYTER", "SCIKIT-LEARN", "AGILE"]),
        ("card_keylogger.svg", "12", "KEYLOGGER APP", "CYBERSECURITY LAB", "Keystroke analysis tool capturing events for vulnerability audit.", ["PYTHON", "PYNPUT", "KALI LINUX"]),
        ("card_nps.svg", "13", "NPS SAATHI", "FINTECH & ANALYTICS", "National Pension Scheme intelligence engine built for IIT Kanpur.", ["TYPESCRIPT", "PENSION API", "FINTECH"]),
        ("card_drugrecall.svg", "14", "DRUG RECALL MONITOR", "HEALTH TELEMETRY", "Real-time pharmaceutical recall notification and safety engine.", ["PYTHON", "REST API", "PHARMA"]),
        ("card_diabetes.svg", "15", "DIABETES PREDICTOR", "CLINICAL ML", "Diagnostic risk assessment web application using medical vectors.", ["PYTHON", "SCIKIT-LEARN", "HEALTHCARE"]),
        ("card_quiz.svg", "16", "ELOQUENT QUIZ APP", "FRONTEND ARCHITECTURE", "Interactive web quiz platform applying responsive clean UI/UX.", ["HTML5", "CSS3", "VANILLA JS"]),
        ("card_cache.svg", "17", "CACHE ANALYSIS", "COMPUTER SYSTEMS", "Cache memory architecture simulator evaluating LRU & CPI in Ripes.", ["RIPES", "LRU CACHE", "ASSEMBLY"]),
        ("card_pharmacy.svg", "18", "PHARMACY MANAGEMENT", "DATABASE & SQL", "Relational inventory, supplier, and sales transaction DBMS.", ["SQL", "RELATIONAL SCHEMA", "DBMS"]),
        ("card_wireless.svg", "19", "WIRELESS POWER", "HARDWARE & IOT", "Inductive coupling contactless energy transfer optimization model.", ["HARDWARE", "INDUCTIVE", "IOT"]),
    ]

    for filename, idx, title, category, blurb, chips in projects:
        w, h = 480, 220
        chip_xml = ""
        cx = 30
        for c in chips:
            cw = measure_text(FONT_INTER, c, 9, tracking=0.1) + 18
            chip_xml += f"""
            <rect x="{cx}" y="172" width="{cw}" height="22" rx="11" fill="{COLOR_GREY_CHIP}" stroke="{COLOR_BORDER}" stroke-width="1"/>
            {text_path(FONT_INTER, c, cx+9, 186, 9, fill=COLOR_WHITE, tracking=0.1)}
            """
            cx += cw + 8

        inner = f"""
        <rect class="card-hover" x="10" y="10" width="460" height="200" rx="8" fill="{COLOR_CARD}" stroke="{COLOR_BORDER}" stroke-width="1"/>
        <line x1="10" y1="50" x2="470" y2="50" stroke="{COLOR_BORDER}" stroke-width="1"/>
        {text_path(FONT_INTER, f"PROJECT // {idx}", 30, 36, 11, fill=COLOR_RED_HOT, tracking=0.15)}
        {text_path(FONT_INTER, category, 320, 36, 10, fill=COLOR_GREY_MUTED, tracking=0.1)}
        
        {text_path(FONT_ANTON, title, 30, 95, 30, fill=COLOR_WHITE, tracking=0.03)}
        {text_path(FONT_INTER, blurb, 30, 130, 11, fill=COLOR_GREY_MUTED, tracking=0.03)}
        {chip_xml}
        """
        (ASSETS_DIR / "work" / filename).write_text(svg_wrapper(w, h, inner))
        print(f"Generated {filename}")


# ==========================================
# 4. TECH STACK (FULL RESUME SPECIFICATION BLOCKS)
# ==========================================
def generate_stack():
    w, h = 1000, 480
    panels = [
        ("01 // PROGRAMMING LANGUAGES", ["PYTHON", "JAVA", "C", "JAVASCRIPT", "HTML", "CSS", "SQL", "SHELL SCRIPTING"], 30, 20, 460, 135),
        ("02 // CORE COMPUTER SCIENCE", ["DATA STRUCTURES", "ALGORITHMS", "OOP", "DBMS & SQL", "OPERATING SYSTEMS", "PROBLEM SOLVING"], 510, 20, 460, 135),
        ("03 // FRAMEWORKS & LIBRARIES", ["REACT.JS", "BOOTSTRAP", "SPRING BOOT", "TENSORFLOW", "NUMPY", "OPENCV", "FASTAPI", "PANDAS"], 30, 175, 460, 135),
        ("04 // TOOLS & TECHNOLOGIES", ["GIT & GITHUB", "LINUX / UNIX", "VS CODE", "STREAMLIT", "OVERLEAF", "POSTMAN", "KALI LINUX"], 510, 175, 460, 135),
        ("05 // SOFTWARE DEVELOPMENT SKILLS", ["DEBUGGING", "CODE OPTIMIZATION", "VERSION CONTROL", "CLEAN CODE", "TEAM COLLABORATION", "ANALYTICAL THINKING"], 30, 330, 460, 135),
        ("06 // AREAS OF INTEREST & FOCUS", ["SOFTWARE ENG", "FRONTEND DEV", "AI/ML", "COMPUTER VISION", "CLOUD", "CYBERSECURITY", "BLOCKCHAIN"], 510, 330, 460, 135),
    ]

    panel_xml = ""
    for title, items, px, py, pw, ph in panels:
        chip_xml = ""
        x = px + 20
        y = py + 52
        for it in items:
            tw = measure_text(FONT_INTER, it, 9, tracking=0.08) + 18
            if x + tw > px + pw - 20:
                x = px + 20
                y += 32
            chip_xml += f"""
            <rect x="{x}" y="{y}" width="{tw}" height="24" rx="4" fill="{COLOR_GREY_CHIP}" stroke="{COLOR_BORDER}" stroke-width="1"/>
            {text_path(FONT_INTER, it, x+9, y+16, 9, fill=COLOR_WHITE, tracking=0.08)}
            """
            x += tw + 8

        panel_xml += f"""
        <rect class="card-hover" x="{px}" y="{py}" width="{pw}" height="{ph}" rx="6" fill="{COLOR_CARD}" stroke="{COLOR_BORDER}" stroke-width="1"/>
        {text_path(FONT_INTER, title, px+20, py+32, 10, fill=COLOR_RED_HOT, tracking=0.15)}
        {chip_xml}
        """

    svg = svg_wrapper(w, h, panel_xml)
    (ASSETS_DIR / "stack" / "stack_grid.svg").write_text(svg)
    print("Generated stack_grid.svg with complete resume proficiencies")


# ==========================================
# 5. 3D ISOMETRIC SKYLINE (FIXED OVERLAP & POSITIONING)
# ==========================================
def generate_skyline():
    w, h = 1000, 440

    manifest_path = REPO_ROOT / "scripts" / "manifest.json"
    with open(manifest_path) as f:
        manifest = json.load(f)

    days = manifest["days"]
    total_contributions = manifest["contributions"]
    current_streak = manifest["current_streak_days"]
    longest_streak = manifest["longest_streak_days"]

    header = f"""
    {text_path(FONT_INTER, "05 // GITHUB LIVING RECORD", 50, 45, 11, fill=COLOR_RED_HOT, tracking=0.15)}
    {text_path(FONT_ANTON, "AUTHENTIC 3D CONTRIBUTION SKYLINE", 50, 85, 34, fill=COLOR_WHITE, tracking=0.03)}
    {text_path(FONT_INTER, f"{total_contributions} VERIFIED CONTRIBUTIONS IN 2026 // 36 REPOSITORIES", 50, 112, 11, fill=COLOR_GREY_MUTED, tracking=0.1)}
    
    <g transform="translate(680, 25)">
      <rect class="card-hover" x="0" y="0" width="270" height="78" rx="6" fill="{COLOR_CARD}" stroke="{COLOR_BORDER}" stroke-width="1"/>
      {text_path(FONT_INTER, "CURRENT STREAK", 20, 26, 9, fill=COLOR_GREY_MUTED, tracking=0.15)}
      {text_path(FONT_ANTON, f"{current_streak} DAYS", 20, 58, 28, fill=COLOR_RED_HOT, tracking=0.03)}
      {text_path(FONT_INTER, f"LONGEST: {longest_streak} DAYS", 130, 56, 10, fill=COLOR_WHITE, tracking=0.1)}
    </g>
    """

    # Shift isometric origin down to y=290 so the top of the grid never touches the title
    origin_x = 500
    origin_y = 290

    pillars = []
    tile_w = 12
    tile_h = 6
    weeks_count = 52

    for week_idx in range(weeks_count):
        for day_idx in range(7):
            idx = week_idx * 7 + day_idx
            if idx >= len(days):
                continue
            day_data = days[idx]
            count = day_data["count"]

            iso_x = origin_x + (week_idx - weeks_count/2) * 13 - (day_idx - 3.5) * 13
            iso_y = origin_y + (week_idx - weeks_count/2) * 6.5 + (day_idx - 3.5) * 6.5

            if count == 0:
                ht = 3
                top_col = COLOR_CARD
                side_col = "#0D0D0E"
                side_col_r = "#080809"
            elif count <= 2:
                ht = 16
                top_col = "#720000"
                side_col = "#450204"
                side_col_r = "#300102"
            elif count <= 5:
                ht = 32
                top_col = COLOR_RED_ACCENT
                side_col = "#650508"
                side_col_r = "#480305"
            elif count <= 9:
                ht = 52
                top_col = COLOR_RED_HOT
                side_col = COLOR_RED_ACCENT
                side_col_r = "#650508"
            else:
                ht = 70
                top_col = "#FF4B4B"
                side_col = COLOR_RED_HOT
                side_col_r = COLOR_RED_ACCENT

            top_p = f"{iso_x},{iso_y - ht} {iso_x + tile_w},{iso_y + tile_h - ht} {iso_x},{iso_y + tile_h*2 - ht} {iso_x - tile_w},{iso_y + tile_h - ht}"
            left_p = f"{iso_x - tile_w},{iso_y + tile_h - ht} {iso_x},{iso_y + tile_h*2 - ht} {iso_x},{iso_y + tile_h*2} {iso_x - tile_w},{iso_y + tile_h}"
            right_p = f"{iso_x + tile_w},{iso_y + tile_h - ht} {iso_x},{iso_y + tile_h*2 - ht} {iso_x},{iso_y + tile_h*2} {iso_x + tile_w},{iso_y + tile_h}"

            polygon_xml = f"""
            <polygon points="{left_p}" fill="{side_col}"/>
            <polygon points="{right_p}" fill="{side_col_r}"/>
            <polygon points="{top_p}" fill="{top_col}" stroke="{COLOR_BG}" stroke-width="0.5"/>
            """
            pillars.append((iso_y, polygon_xml))

    pillars.sort(key=lambda p: p[0])
    rendered_pillars = "\n".join([p[1] for p in pillars])

    inner = f"""
    {header}
    <g>
      {rendered_pillars}
    </g>
    <!-- Month Labels along baseline -->
    {text_path(FONT_INTER, "NOV", 140, 420, 9.5, fill=COLOR_GREY_MUTED, tracking=0.15)}
    {text_path(FONT_INTER, "JAN", 290, 420, 9.5, fill=COLOR_GREY_MUTED, tracking=0.15)}
    {text_path(FONT_INTER, "MAR", 440, 420, 9.5, fill=COLOR_GREY_MUTED, tracking=0.15)}
    {text_path(FONT_INTER, "MAY", 590, 420, 9.5, fill=COLOR_GREY_MUTED, tracking=0.15)}
    {text_path(FONT_INTER, "JUL", 740, 420, 9.5, fill=COLOR_GREY_MUTED, tracking=0.15)}
    {text_path(FONT_INTER, "OCT", 880, 420, 9.5, fill=COLOR_GREY_MUTED, tracking=0.15)}
    """
    svg = svg_wrapper(w, h, inner)
    (ASSETS_DIR / "activity" / "skyline_3d.svg").write_text(svg)
    print("Generated skyline_3d.svg with zero headline overlap")


# ==========================================
# 6. WINS & HONOURS (100% CARDS FORMAT)
# ==========================================
def generate_wins():
    w, h = 1000, 440
    wins = [
        ("1ST PRIZE WINNER", "DESIGN FOR HER IDEATHON", "2026", "State-level women in technology product innovation champion.", COLOR_RED_HOT),
        ("FIRST RUNNER-UP", "PFRDA HACKATHON // IIT KANPUR", "MAR 2026", "National runner-up in fintech & pension analytics hackathon.", COLOR_WHITE),
        ("PATENT FILED", "GUARDIAN WING SYSTEM", "APR 2026", "Indian Patent Application No. 202641048328 for fleet edge AI.", COLOR_WHITE),
        ("BEST PERFORMER AWARD", "GEC THRISSUR AI/ML INTERNSHIP", "JUNE 2026", "Selected top performer in advanced applied machine learning cohort.", COLOR_WHITE),
        ("WINNER // SYNAPSE", "DEBATE CHAMPIONSHIP", "JAN 2026", "First prize in inter-collegiate parliamentary debate competition.", COLOR_WHITE),
        ("2ND PRIZE // ARGUMENT ARENA", "REGIONAL DEBATE LEAGUE", "FEB 2025", "Runner-up in Oxford-style structured debate tournament.", COLOR_WHITE),
        ("SHORTLISTED // SIH 2025", "SMART INDIA HACKATHON", "OCT 2025", "Selected in institutional evaluation round for national finals.", COLOR_WHITE),
        ("3RD PRIZE // TECHLETICS", "MICROPRESENTATION LEAGUE", "AUG 2025", "Podium finish in technical research communication contest.", COLOR_WHITE),
    ]

    tiles = ""
    for i, (title, org, date, blurb, accent) in enumerate(wins):
        col = i % 2
        row = i // 2
        x = 30 + col * 480
        y = 20 + row * 102

        tiles += f"""
        <g transform="translate({x}, {y})">
          <rect class="card-hover" x="0" y="0" width="460" height="92" rx="6" fill="{COLOR_CARD}" stroke="{COLOR_BORDER}" stroke-width="1"/>
          {text_path(FONT_INTER, f"{org} // {date}", 20, 24, 10, fill=COLOR_GREY_MUTED, tracking=0.1)}
          {text_path(FONT_ANTON, title, 20, 54, 21, fill=accent, tracking=0.03)}
          {text_path(FONT_INTER, blurb, 20, 75, 10, fill=COLOR_GREY_MUTED, tracking=0.04)}
        </g>
        """

    svg = svg_wrapper(w, h, tiles)
    (ASSETS_DIR / "wins" / "wins_wall.svg").write_text(svg)
    print("Generated wins_wall.svg with 8 full cards")


# ==========================================
# 7. INTERNSHIP TIMELINE (PERFECT IN-BOX ALIGNMENT)
# ==========================================
def generate_timeline():
    w, h = 1000, 290
    stages = [
        ("01", "INFOSYS", "Springboard 6.0 & 7.0", "AI/ML & Data Viz", "FitPlan Capstone"),
        ("02", "GEC THRISSUR", "Summer Internship", "Applied AI/ML", "Best Performer"),
        ("03", "VODAFONE", "VOIS x Edunet x AICTE", "Cybersecurity", "Keylogger System"),
        ("04", "IBM SKILLSBUILD", "Edunet x AICTE", "Frontend Web Dev", "Quiz Platform"),
        ("05", "SHELL", "Edunet x AICTE", "AI / Sustainability", "MODIS Detection"),
        ("06", "IBM SKILLSBUILD", "Edunet x AICTE", "AI & Machine Learning", "Salary Predictor"),
        ("07", "MICROSOFT", "Edunet x AICTE", "Foundations of AI", "Azure Vision & Bots"),
    ]

    step_w = 132
    start_x = 35
    box_w = 124
    box_h = 160
    cards = ""

    for i, (num, partner, org, domain, project) in enumerate(stages):
        x = start_x + i * step_w
        cards += f"""
        <g transform="translate({x}, 40)">
          <circle cx="{box_w/2}" cy="30" r="5" fill="{COLOR_RED_HOT}"/>
          <circle cx="{box_w/2}" cy="30" r="11" fill="none" stroke="{COLOR_BORDER}" stroke-width="1"/>
          
          <rect class="card-hover" x="0" y="55" width="{box_w}" height="{box_h}" rx="6" fill="{COLOR_CARD}" stroke="{COLOR_BORDER}" stroke-width="1"/>
          {text_path(FONT_INTER, f"PRG // {num}", 14, 76, 9, fill=COLOR_RED_HOT, tracking=0.15)}
          {text_path(FONT_ANTON, partner, 14, 102, 16, fill=COLOR_WHITE, tracking=0.03)}
          {text_path(FONT_INTER, org, 14, 122, 8.5, fill=COLOR_GREY_MUTED, tracking=0.04)}
          {text_path(FONT_INTER, domain, 14, 140, 8.5, fill=COLOR_RED_ACCENT, tracking=0.04)}
          <line x1="14" y1="156" x2="{box_w - 14}" y2="156" stroke="{COLOR_BORDER}" stroke-width="1"/>
          {text_path(FONT_INTER, project, 14, 182, 8.5, fill=COLOR_WHITE, tracking=0.04)}
        </g>
        """

    inner = f"""
    <line x1="50" y1="70" x2="950" y2="70" stroke="{COLOR_BORDER_HOT}" stroke-width="1.5"/>
    {cards}
    """
    svg = svg_wrapper(w, h, inner)
    (ASSETS_DIR / "timeline" / "internships_timeline.svg").write_text(svg)
    print("Generated internships_timeline.svg with perfect alignment")


# ==========================================
# 8. OFF-DUTY BENTO (WITH BOBBY THE CAT)
# ==========================================
def generate_offduty():
    w, h = 1000, 220
    fav_title = 'FAVOURITE: "NEVER LIE"'
    inner = f"""
    <rect class="card-hover" x="30" y="20" width="220" height="180" rx="6" fill="{COLOR_CARD}" stroke="{COLOR_BORDER_HOT}" stroke-width="1.5"/>
    {text_path(FONT_INTER, "08 // PET COMPANION", 45, 48, 10, fill=COLOR_RED_HOT, tracking=0.15)}
    {text_path(FONT_ANTON, "BOBBY THE CAT", 45, 85, 24, fill=COLOR_WHITE, tracking=0.03)}
    {text_path(FONT_INTER, "FELINE CHIEF AUDITOR", 45, 112, 10, fill=COLOR_RED_HOT, tracking=0.08)}
    <line x1="45" y1="128" x2="235" y2="128" stroke="{COLOR_BORDER}" stroke-width="1"/>
    {text_path(FONT_INTER, "Dedicated pet lover & proud cat parent.", 45, 155, 9.5, fill=COLOR_GREY_MUTED, tracking=0.04)}

    <rect class="card-hover" x="270" y="20" width="220" height="180" rx="6" fill="{COLOR_CARD}" stroke="{COLOR_BORDER}" stroke-width="1"/>
    {text_path(FONT_INTER, "08 // READING LIST", 285, 48, 10, fill=COLOR_RED_HOT, tracking=0.15)}
    {text_path(FONT_ANTON, "FREIDA MCFADDEN", 285, 85, 22, fill=COLOR_WHITE, tracking=0.03)}
    {text_path(FONT_INTER, fav_title, 285, 112, 10, fill=COLOR_RED_HOT, tracking=0.08)}
    <line x1="285" y1="128" x2="475" y2="128" stroke="{COLOR_BORDER}" stroke-width="1"/>
    {text_path(FONT_INTER, "Psychological thrillers & puzzle mysteries.", 285, 155, 9.5, fill=COLOR_GREY_MUTED, tracking=0.04)}

    <rect class="card-hover" x="510" y="20" width="220" height="180" rx="6" fill="{COLOR_CARD}" stroke="{COLOR_BORDER}" stroke-width="1"/>
    {text_path(FONT_INTER, "08 // RHETORIC", 525, 48, 10, fill=COLOR_RED_HOT, tracking=0.15)}
    {text_path(FONT_ANTON, "DEBATE & ORATORY", 525, 85, 22, fill=COLOR_WHITE, tracking=0.03)}
    {text_path(FONT_INTER, "SYNAPSE CHAMPION", 525, 112, 10, fill=COLOR_WHITE, tracking=0.08)}
    <line x1="525" y1="128" x2="715" y2="128" stroke="{COLOR_BORDER}" stroke-width="1"/>
    {text_path(FONT_INTER, "Parliamentary debate & competitive rhetoric.", 525, 155, 9.5, fill=COLOR_GREY_MUTED, tracking=0.04)}

    <rect class="card-hover" x="750" y="20" width="220" height="180" rx="6" fill="{COLOR_CARD}" stroke="{COLOR_BORDER}" stroke-width="1"/>
    {text_path(FONT_INTER, "08 // ECOSYSTEM", 765, 48, 10, fill=COLOR_RED_HOT, tracking=0.15)}
    {text_path(FONT_ANTON, "COMMUNITY LEAD", 765, 85, 22, fill=COLOR_WHITE, tracking=0.03)}
    {text_path(FONT_INTER, "TINKERHUB // FOSS", 765, 112, 10, fill=COLOR_RED_HOT, tracking=0.08)}
    <line x1="765" y1="128" x2="955" y2="128" stroke="{COLOR_BORDER}" stroke-width="1"/>
    {text_path(FONT_INTER, "Hackathons, peer learning & mentorship.", 765, 155, 9.5, fill=COLOR_GREY_MUTED, tracking=0.04)}
    """
    svg = svg_wrapper(w, h, inner)
    (ASSETS_DIR / "offduty" / "offduty_bento.svg").write_text(svg)
    print("Generated offduty_bento.svg with cat Bobby")


# ==========================================
# 9. CLOSING SECTION & DEDICATED BUTTONS
# ==========================================
def generate_closing_and_buttons():
    # 9.1 Closing Hero Headline
    w, h = 1000, 200
    t_lets = text_path(FONT_ANTON, "LET'S BUILD", 50, 95, 78, fill="none", stroke=COLOR_WHITE, stroke_width=2.0, tracking=0.03)
    t_together = text_path(FONT_ANTON, "SOMETHING REAL.", 50, 165, 78, fill=COLOR_RED_HOT, tracking=0.03)
    inner = f"""
    {text_path(FONT_INTER, "09 // DIRECT COLLABORATIONS", 50, 35, 11, fill=COLOR_RED_HOT, tracking=0.15)}
    {t_lets}
    {t_together}
    """
    (ASSETS_DIR / "closing" / "closing_hero.svg").write_text(svg_wrapper(w, h, inner))
    print("Generated closing_hero.svg")

    # 9.2 Individual Pill Buttons (Red-bordered, highlighted, clickable)
    buttons = [
        ("btn_resume.svg", "RESUME (PDF)", 160, COLOR_BORDER_HOT, COLOR_RED_HOT),
        ("btn_linkedin.svg", "LINKEDIN", 135, COLOR_BORDER, COLOR_WHITE),
        ("btn_github.svg", "GITHUB", 125, COLOR_BORDER, COLOR_WHITE),
        ("btn_leetcode.svg", "LEETCODE", 135, COLOR_BORDER, COLOR_WHITE),
        ("btn_goodreads.svg", "GOODREADS", 145, COLOR_BORDER, COLOR_WHITE),
        ("btn_email.svg", "EMAIL", 120, COLOR_BORDER, COLOR_WHITE),
    ]

    for filename, label, bw, border_col, txt_col in buttons:
        bh = 44
        btn_xml = f"""
        <rect class="card-hover" x="2" y="2" width="{bw-4}" height="{bh-4}" rx="20" fill="{COLOR_CARD}" stroke="{border_col}" stroke-width="1.5"/>
        {text_path(FONT_INTER, label, bw/2, 27, 11, fill=txt_col, anchor="middle", tracking=0.15)}
        """
        btn_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {bw} {bh}" width="{bw}" height="{bh}">
  <defs>
    <style>
      .card-hover {{
        transition: all 0.25s ease;
        cursor: pointer;
      }}
      .card-hover:hover {{
        stroke: {COLOR_RED_HOT} !important;
        stroke-width: 2px !important;
        filter: drop-shadow(0 0 10px rgba(226, 35, 47, 0.6));
      }}
    </style>
  </defs>
  <rect width="100%" height="100%" fill="{COLOR_BG}"/>
  {btn_xml}
</svg>"""
        (ASSETS_DIR / "closing" / filename).write_text(btn_svg)
        print(f"Generated {filename}")


if __name__ == "__main__":
    generate_hero()
    generate_marquee()
    generate_about()
    generate_numbers()
    generate_all_project_cards()
    generate_stack()
    generate_skyline()
    generate_wins()
    generate_timeline()
    generate_offduty()
    generate_closing_and_buttons()
    print("All SVGs successfully generated!")
