#!/usr/bin/env python3
"""Generate a CEFR A1–A2 English Level Placement Test PDF."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)

OUTPUT = Path(__file__).resolve().parents[1] / "exams" / "A1-A2_English_Level_Placement_Test.pdf"

PAGE_W, PAGE_H = A4
MARGIN = 1.8 * cm

NAVY = colors.HexColor("#1B2A4A")
TEAL = colors.HexColor("#0D7377")
LIGHT = colors.HexColor("#F4F7FA")
LINE = colors.HexColor("#C5CED9")
SOFT = colors.HexColor("#E8EEF4")
MUTED = colors.HexColor("#5A6A7A")
WHITE = colors.white
BLACK = colors.HexColor("#1A1A1A")


def build_styles():
    base = getSampleStyleSheet()
    styles = {
        "cover_title": ParagraphStyle(
            "cover_title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=28,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=12,
            leading=16,
            textColor=TEAL,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "section": ParagraphStyle(
            "section",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=WHITE,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=0,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            textColor=NAVY,
            spaceBefore=8,
            spaceAfter=4,
        ),
        "h3": ParagraphStyle(
            "h3",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=14,
            textColor=TEAL,
            spaceBefore=6,
            spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=BLACK,
            alignment=TA_JUSTIFY,
            spaceAfter=4,
        ),
        "body_left": ParagraphStyle(
            "body_left",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=BLACK,
            alignment=TA_LEFT,
            spaceAfter=4,
        ),
        "instruction": ParagraphStyle(
            "instruction",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=9.5,
            leading=13,
            textColor=MUTED,
            spaceAfter=6,
        ),
        "q": ParagraphStyle(
            "q",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=BLACK,
            spaceBefore=3,
            spaceAfter=2,
        ),
        "opt": ParagraphStyle(
            "opt",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            textColor=BLACK,
            leftIndent=14,
            spaceAfter=1,
        ),
        "passage": ParagraphStyle(
            "passage",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14.5,
            textColor=BLACK,
            alignment=TA_JUSTIFY,
            spaceAfter=4,
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11,
            textColor=MUTED,
        ),
        "footer": ParagraphStyle(
            "footer",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
        "center": ParagraphStyle(
            "center",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=BLACK,
            alignment=TA_CENTER,
        ),
        "rubric": ParagraphStyle(
            "rubric",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=BLACK,
            spaceAfter=2,
        ),
        "answer": ParagraphStyle(
            "answer",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            textColor=BLACK,
            spaceAfter=2,
        ),
        "bold_body": ParagraphStyle(
            "bold_body",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=14,
            textColor=BLACK,
            spaceAfter=4,
        ),
        "line_label": ParagraphStyle(
            "line_label",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=16,
            textColor=BLACK,
        ),
    }
    return styles


def section_banner(text, styles):
    data = [[Paragraph(text, styles["section"])]]
    t = Table(data, colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, -1), WHITE),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    return t


def info_box(items, styles, col_widths=None):
    rows = []
    for label, blank in items:
        rows.append(
            [
                Paragraph(f"<b>{label}</b>", styles["line_label"]),
                Paragraph(blank, styles["line_label"]),
            ]
        )
    if col_widths is None:
        col_widths = [4.2 * cm, PAGE_W - 2 * MARGIN - 4.2 * cm]
    t = Table(rows, colWidths=col_widths)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    return t


def writing_lines(n=8):
    rows = [["_" * 95] for _ in range(n)]
    t = Table(rows, colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(
        TableStyle(
            [
                ("TEXTCOLOR", (0, 0), (-1, -1), LINE),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return t


def checkbox_row(label, styles):
    return Paragraph(f"☐  {label}", styles["opt"])


def add_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, PAGE_H - 1.2 * cm, PAGE_W - MARGIN, PAGE_H - 1.2 * cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN, PAGE_H - 1.0 * cm, "CEFR A1–A2 English Level Placement Test")
    # Pages 1–N candidate paper; examiner pack begins after speaking brief.
    # Label stays neutral so mixed candidate/examiner PDFs remain accurate.
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 1.0 * cm, "Official Test Paper")
    canvas.line(MARGIN, 1.3 * cm, PAGE_W - MARGIN, 1.3 * cm)
    canvas.drawCentredString(PAGE_W / 2, 0.8 * cm, f"Page {doc.page}")
    canvas.restoreState()


def build_document():
    styles = build_styles()
    story = []

    # ========== COVER ==========
    story.append(Spacer(1, 0.5 * cm))
    story.append(
        Table(
            [[Paragraph("THE LANGUAGE LAB", styles["cover_sub"])]],
            colWidths=[PAGE_W - 2 * MARGIN],
        )
    )
    story.append(Spacer(1, 0.25 * cm))
    story.append(Paragraph("English Level Placement Test", styles["cover_title"]))
    story.append(Paragraph("CEFR Levels A1 and A2", styles["cover_sub"]))
    story.append(Spacer(1, 0.15 * cm))
    story.append(
        HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceBefore=2, spaceAfter=8)
    )

    meta = Table(
        [
            [
                Paragraph("<b>Skills assessed</b><br/>Reading · Writing · Speaking", styles["center"]),
                Paragraph("<b>Total time</b><br/>Approximately 55–65 minutes", styles["center"]),
                Paragraph("<b>Purpose</b><br/>Place candidates at A1 or A2", styles["center"]),
            ]
        ],
        colWidths=[(PAGE_W - 2 * MARGIN) / 3] * 3,
    )
    meta.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.8, TEAL),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.append(meta)
    story.append(Spacer(1, 0.35 * cm))

    story.append(Paragraph("Candidate Information", styles["h2"]))
    story.append(
        info_box(
            [
                ("Full name:", "_" * 55),
                ("Date of birth:", "_" * 20 + "    Date of test: " + "_" * 20),
                ("Candidate ID (if any):", "_" * 25 + "    Examiner: " + "_" * 25),
                ("Native language:", "_" * 30 + "    Centre: " + "_" * 25),
            ],
            styles,
        )
    )
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("Overview of the Test", styles["h2"]))
    overview = [
        ["Part", "Skill", "Tasks", "Time", "Marks"],
        ["1", "Reading", "20 questions (vocabulary, grammar, texts)", "25 min", "40"],
        ["2", "Writing", "2 tasks (personal form + short paragraph)", "20 min", "20"],
        ["3", "Speaking", "3 stages (interview, description, dialogue)", "8–10 min", "20"],
        ["", "", "Total", "≈ 55–65 min", "80"],
    ]
    ot = Table(overview, colWidths=[1.4 * cm, 2.6 * cm, 7.2 * cm, 2.4 * cm, 1.8 * cm])
    ot.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -2), "Helvetica"),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BACKGROUND", (0, 1), (-1, -2), WHITE),
                ("BACKGROUND", (0, -1), (-1, -1), SOFT),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("ALIGN", (2, 1), (2, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.4, LINE),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(ot)
    story.append(Spacer(1, 0.25 * cm))

    story.append(Paragraph("General Instructions for Candidates", styles["h2"]))
    instructions = [
        "Write all answers in <b>English</b> using a blue or black pen.",
        "Do <b>not</b> use a dictionary, phone, or translation tool.",
        "For multiple-choice questions, circle <b>one</b> letter only (A, B, C, or D).",
        "If you change an answer, cross out the old one clearly and circle the new one.",
        "Manage your time: leave a few minutes to check Part 1 and Part 2.",
        "In the Speaking test, listen carefully and answer in full sentences when you can.",
        "There is no negative marking. Attempt every question.",
    ]
    for i, text in enumerate(instructions, 1):
        story.append(Paragraph(f"{i}. {text}", styles["body_left"]))

    story.append(Spacer(1, 0.2 * cm))
    note = Table(
        [
            [
                Paragraph(
                    "<b>Level decision:</b> Scores place you at <b>Below A1</b>, <b>A1</b>, or <b>A2</b>. "
                    "This test is designed for beginner and elementary placement only. "
                    "It does not certify B1 or higher.",
                    styles["rubric"],
                )
            ]
        ],
        colWidths=[PAGE_W - 2 * MARGIN],
    )
    note.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SOFT),
                ("BOX", (0, 0), (-1, -1), 0.6, TEAL),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(note)

    # ========== PART 1 READING ==========
    story.append(PageBreak())
    story.append(section_banner("PART 1 — READING  ·  25 minutes  ·  40 marks", styles))
    story.append(Spacer(1, 0.35 * cm))
    story.append(
        Paragraph(
            "Answer all questions. Each question is worth <b>2 marks</b> unless stated otherwise.",
            styles["instruction"],
        )
    )

    # Section A
    story.append(Paragraph("Section A — Everyday English (Questions 1–8)", styles["h2"]))
    story.append(
        Paragraph(
            "Choose the best word or phrase to complete each sentence. Circle A, B, C, or D.",
            styles["instruction"],
        )
    )

    section_a = [
        (
            "1. My name _____ Anna. I am from Poland.",
            ["am", "is", "are", "be"],
        ),
        (
            "2. _____ is your phone number?",
            ["Who", "Where", "What", "When"],
        ),
        (
            "3. I usually _____ coffee in the morning.",
            ["drink", "drinks", "drinking", "to drink"],
        ),
        (
            "4. There _____ two books on the table.",
            ["is", "are", "be", "am"],
        ),
        (
            "5. Excuse me, _____ is the train station?",
            ["who", "what", "where", "how"],
        ),
        (
            "6. She _____ to work by bus every day.",
            ["go", "goes", "going", "gone"],
        ),
        (
            "7. Can you _____ the window, please? It is hot in here.",
            ["open", "opens", "opening", "opened"],
        ),
        (
            "8. I _____ to the cinema yesterday.",
            ["go", "goes", "went", "going"],
        ),
    ]
    letters = ["A", "B", "C", "D"]
    for q, opts in section_a:
        story.append(Paragraph(q, styles["q"]))
        opt_line = "     ".join(f"{letters[i]}) {opts[i]}" for i in range(4))
        story.append(Paragraph(opt_line, styles["opt"]))

    # Section B
    story.append(Paragraph("Section B — Vocabulary (Questions 9–12)", styles["h2"]))
    story.append(
        Paragraph(
            "Choose the word that best completes each sentence. Circle A, B, C, or D.",
            styles["instruction"],
        )
    )
    section_b = [
        (
            "9. I need to buy bread, milk, and eggs. I am going to the _____.",
            ["hospital", "supermarket", "cinema", "station"],
        ),
        (
            "10. My brother is a _____. He works in a school.",
            ["teacher", "driver", "waiter", "pilot"],
        ),
        (
            "11. It is very _____ outside. Please take an umbrella.",
            ["sunny", "windy", "rainy", "snowy"],
        ),
        (
            "12. We live in a small _____ near the park.",
            ["apple", "apartment", "animal", "answer"],
        ),
    ]
    for q, opts in section_b:
        story.append(Paragraph(q, styles["q"]))
        opt_line = "     ".join(f"{letters[i]}) {opts[i]}" for i in range(4))
        story.append(Paragraph(opt_line, styles["opt"]))

    # Section C — Matching (compact; keep together so it does not split awkwardly)
    notices = Table(
        [
            [
                Paragraph("<b>Notices</b>", styles["bold_body"]),
                Paragraph("<b>Meanings</b>", styles["bold_body"]),
            ],
            [
                Paragraph(
                    "13. PLEASE DO NOT FEED THE ANIMALS<br/>"
                    "14. STAFF ONLY<br/>"
                    "15. NO PARKING<br/>"
                    "16. QUIET PLEASE — EXAM IN PROGRESS",
                    styles["body_left"],
                ),
                Paragraph(
                    "A. You must not leave your car here.<br/>"
                    "B. Only workers can enter this area.<br/>"
                    "C. Do not give food to the animals.<br/>"
                    "D. Speak softly; people are taking a test.<br/>"
                    "E. Buy your tickets before 6 p.m.",
                    styles["body_left"],
                ),
            ],
        ],
        colWidths=[(PAGE_W - 2 * MARGIN) / 2] * 2,
    )
    notices.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), SOFT),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    ans_boxes = Table(
        [
            [
                Paragraph("13 → ____", styles["center"]),
                Paragraph("14 → ____", styles["center"]),
                Paragraph("15 → ____", styles["center"]),
                Paragraph("16 → ____", styles["center"]),
            ]
        ],
        colWidths=[(PAGE_W - 2 * MARGIN) / 4] * 4,
    )
    ans_boxes.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(
        KeepTogether(
            [
                Paragraph("Section C — Notices and Signs (Questions 13–16)", styles["h2"]),
                Paragraph(
                    "Match each notice (13–16) with the correct meaning (A–E). "
                    "There is one extra meaning you do not need. Write the letter in the box.",
                    styles["instruction"],
                ),
                notices,
                Spacer(1, 0.15 * cm),
                ans_boxes,
            ]
        )
    )

    # Section D+E on a fresh page so passage questions stay with their texts
    story.append(PageBreak())
    story.append(section_banner("PART 1 — READING (continued)", styles))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph("Section D — Short Message (Questions 17–18)", styles["h2"]))
    story.append(Paragraph("Read the message. Then answer the questions.", styles["instruction"]))

    msg_box = Table(
        [
            [
                Paragraph(
                    "<b>Hi Sara,</b><br/>"
                    "Would you like to come to my house on Saturday? "
                    "We can watch a film and have pizza. "
                    "Please arrive at 6 o'clock. "
                    "My address is 14 Green Street, near the big supermarket. "
                    "Call me if you cannot come.<br/>"
                    "Love, Maya",
                    styles["passage"],
                )
            ]
        ],
        colWidths=[PAGE_W - 2 * MARGIN],
    )
    msg_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.8, TEAL),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(msg_box)
    story.append(Spacer(1, 0.15 * cm))

    story.append(Paragraph("17. What does Maya want to do on Saturday?", styles["q"]))
    for i, t in enumerate(
        [
            "Go shopping with Sara",
            "Watch a film and eat pizza at home",
            "Visit the supermarket",
            "Call Sara at 6 o'clock",
        ]
    ):
        story.append(Paragraph(f"{letters[i]}) {t}", styles["opt"]))

    story.append(Paragraph("18. Where does Maya live?", styles["q"]))
    for i, t in enumerate(
        [
            "Near a cinema",
            "At Sara's house",
            "At 14 Green Street",
            "Next to a school",
        ]
    ):
        story.append(Paragraph(f"{letters[i]}) {t}", styles["opt"]))

    # Section E — Longer reading
    story.append(Paragraph("Section E — Reading Text (Questions 19–20)", styles["h2"]))
    story.append(Paragraph("Read the text. Then answer the questions.", styles["instruction"]))

    long_text = Table(
        [
            [
                Paragraph(
                    "<b>A Day in My Life</b><br/><br/>"
                    "My name is Tom. I am 28 and I live in Manchester with my wife, Lisa. "
                    "I work in a bookshop in the city centre from nine to five. "
                    "I like my job because I love books and I meet interesting people. "
                    "In the evening we often cook together. On Fridays we sometimes go to a restaurant. "
                    "At the weekend I play football with friends; Lisa prefers to stay at home and read. "
                    "Next month we want to visit London for three days. We are both excited about the trip.",
                    styles["passage"],
                )
            ]
        ],
        colWidths=[PAGE_W - 2 * MARGIN],
    )
    long_text.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.8, TEAL),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(long_text)
    story.append(Spacer(1, 0.12 * cm))

    end_r = Table(
        [
            [
                Paragraph(
                    "<b>End of Part 1.</b> Check your answers. Then go on to Part 2 — Writing.",
                    styles["center"],
                )
            ]
        ],
        colWidths=[PAGE_W - 2 * MARGIN],
    )
    end_r.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SOFT),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    q19_opts = [
        "Because he finishes work early",
        "Because he loves books and meets interesting people",
        "Because the bookshop is near his house",
        "Because Lisa works with him",
    ]
    q20_opts = [
        "Play football in the park",
        "Open a restaurant",
        "Visit London for three days",
        "Move to Manchester",
    ]
    story.append(
        KeepTogether(
            [
                Paragraph("19. Why does Tom like his job?", styles["q"]),
                *[Paragraph(f"{letters[i]}) {t}", styles["opt"]) for i, t in enumerate(q19_opts)],
                Paragraph("20. What do Tom and Lisa want to do next month?", styles["q"]),
                *[Paragraph(f"{letters[i]}) {t}", styles["opt"]) for i, t in enumerate(q20_opts)],
                Spacer(1, 0.25 * cm),
                end_r,
            ]
        )
    )

    # ========== PART 2 WRITING ==========
    story.append(PageBreak())
    story.append(section_banner("PART 2 — WRITING  ·  20 minutes  ·  20 marks", styles))
    story.append(Spacer(1, 0.35 * cm))
    story.append(
        Paragraph(
            "Complete both tasks. Write clearly. Spelling and grammar are part of the mark.",
            styles["instruction"],
        )
    )

    story.append(Paragraph("Task 1 — Personal Information Form (8 marks)", styles["h2"]))
    story.append(
        Paragraph(
            "Complete the form about yourself. Write short answers in English. "
            "Use full words (not only numbers) where possible.",
            styles["instruction"],
        )
    )

    form_rows = [
        ["Question", "Your answer"],
        ["1. What is your full name?", ""],
        ["2. How old are you?", ""],
        ["3. Where do you live? (city / country)", ""],
        ["4. What is your job or what do you study?", ""],
        ["5. What languages do you speak?", ""],
        ["6. What do you like doing in your free time?", ""],
        ["7. Why are you learning English?", ""],
        ["8. Write one sentence about your family.", ""],
    ]
    ft = Table(form_rows, colWidths=[7.5 * cm, PAGE_W - 2 * MARGIN - 7.5 * cm], rowHeights=[0.7 * cm] * 9)
    ft.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("BACKGROUND", (0, 1), (0, -1), LIGHT),
            ]
        )
    )
    story.append(ft)

    story.append(Paragraph("Task 2 — Short Paragraph (12 marks)", styles["h2"]))
    story.append(
        Paragraph(
            "Write <b>40–60 words</b> about your typical day. Include information about:",
            styles["instruction"],
        )
    )
    for bullet in [
        "when you get up",
        "what you do in the morning",
        "what you do in the afternoon or evening",
        "something you like about your day",
    ]:
        story.append(Paragraph(f"• {bullet}", styles["opt"]))

    story.append(Spacer(1, 0.15 * cm))
    story.append(
        Paragraph(
            "<i>Write your paragraph below. Count your words at the end.</i>",
            styles["instruction"],
        )
    )
    story.append(writing_lines(10))
    story.append(Spacer(1, 0.2 * cm))
    story.append(
        Paragraph(
            "Word count: __________     Examiner use only — Task 1: ____ / 8     Task 2: ____ / 12     Total Writing: ____ / 20",
            styles["small"],
        )
    )

    tip = Table(
        [
            [
                Paragraph(
                    "<b>Tips:</b> Use present simple for routines (I get up, I go, I eat). "
                    "Use capital letters and full stops. Check subject–verb agreement "
                    "(he/she + -s).",
                    styles["rubric"],
                )
            ]
        ],
        colWidths=[PAGE_W - 2 * MARGIN],
    )
    tip.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SOFT),
                ("BOX", (0, 0), (-1, -1), 0.5, TEAL),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.append(Spacer(1, 0.25 * cm))
    story.append(tip)

    # ========== PART 3 SPEAKING (candidate brief) ==========
    story.append(PageBreak())
    story.append(section_banner("PART 3 — SPEAKING  ·  8–10 minutes  ·  20 marks", styles))
    story.append(Spacer(1, 0.35 * cm))
    story.append(
        Paragraph(
            "This part is a face-to-face interview with an examiner. "
            "You may look at the picture prompt when the examiner shows it. "
            "Speak clearly. It is better to give a short answer than to say nothing.",
            styles["instruction"],
        )
    )

    story.append(Paragraph("What will happen", styles["h2"]))
    stages = [
        ["Stage", "Focus", "Time", "What you do"],
        [
            "1",
            "Personal interview",
            "3 min",
            "Answer questions about yourself, home, work/study, free time.",
        ],
        [
            "2",
            "Picture description",
            "3 min",
            "Describe a picture. Say who/what you see and what people are doing.",
        ],
        [
            "3",
            "Short dialogue",
            "2–4 min",
            "Ask and answer simple questions on an everyday topic.",
        ],
    ]
    st = Table(stages, colWidths=[1.5 * cm, 3.4 * cm, 1.8 * cm, PAGE_W - 2 * MARGIN - 6.7 * cm])
    st.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("BACKGROUND", (0, 1), (-1, -1), WHITE),
            ]
        )
    )
    story.append(st)

    story.append(Paragraph("Useful language you may use", styles["h2"]))
    story.append(
        Paragraph(
            "• My name is … / I live in … / I work as … / I am a student.<br/>"
            "• In my free time I … / I like … because …<br/>"
            "• In the picture I can see … / There is / There are … / He is …-ing.<br/>"
            "• Could you repeat that, please? / Sorry, I do not understand.<br/>"
            "• What about you? / Do you …? / Where do you …?",
            styles["body_left"],
        )
    )

    story.append(Paragraph("Picture prompt (Stage 2) — Candidate view", styles["h2"]))
    story.append(
        Paragraph(
            "The examiner will show you a picture similar to the description below. "
            "Practise describing scenes like this.",
            styles["instruction"],
        )
    )

    picture = Table(
        [
            [
                Paragraph(
                    "<b>Scene description (for reference / practice)</b><br/><br/>"
                    "A café on a sunny day. Two people are sitting at a table outside. "
                    "A woman is drinking coffee. A man is reading a newspaper. "
                    "A waiter is carrying a tray with sandwiches. "
                    "A child is playing with a dog near a tree. "
                    "There are flowers on the table and bicycles in front of the café.",
                    styles["passage"],
                )
            ]
        ],
        colWidths=[PAGE_W - 2 * MARGIN],
    )
    picture.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("BOX", (0, 0), (-1, -1), 1.2, TEAL),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    story.append(picture)

    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("Candidate self-check (optional, before the interview)", styles["h2"]))
    for item in [
        "I can say my name, age, and where I live.",
        "I can talk about my job or studies in simple sentences.",
        "I can say what I like doing in my free time.",
        "I can describe people and actions in a picture (There is… / He is …-ing).",
        "I can ask simple questions (Do you…? / Where…? / What…?).",
    ]:
        story.append(checkbox_row(item, styles))

    story.append(Spacer(1, 0.5 * cm))
    end_c = Table(
        [
            [
                Paragraph(
                    "<b>End of the candidate paper.</b> Please wait for the examiner for Part 3 — Speaking. "
                    "Do not write on the Examiner Pack pages.",
                    styles["center"],
                )
            ]
        ],
        colWidths=[PAGE_W - 2 * MARGIN],
    )
    end_c.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, -1), WHITE),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    # Need white text - Paragraph with white color
    end_c = Table(
        [
            [
                Paragraph(
                    "<font color='white'><b>End of the candidate paper.</b> Please wait for the examiner for "
                    "Part 3 — Speaking. Do not write on the Examiner Pack pages.</font>",
                    styles["center"],
                )
            ]
        ],
        colWidths=[PAGE_W - 2 * MARGIN],
    )
    end_c.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(end_c)

    # ========== EXAMINER PACK ==========
    story.append(PageBreak())
    # Switch footer via onPage later - we'll use multi-build approach
    # Actually SimpleDocTemplate uses one onPage. I'll mark examiner pages in header text within content
    # and use a custom page template... Simpler: include "Examiner Pack" banner and use examiner footer
    # for whole doc after break by rebuilding... Best approach: use two onPage handlers with
    # doc.afterFlowable or just one generic footer "Placement Test" without candidate/examiner split.
    # I'll update add_header_footer to be generic, and put "Examiner Pack" in section banners.

    story.append(section_banner("EXAMINER PACK — CONFIDENTIAL", styles))
    story.append(Spacer(1, 0.3 * cm))
    story.append(
        Paragraph(
            "Do not give these pages to candidates. Use them for administration, scoring, and the speaking interview.",
            styles["instruction"],
        )
    )

    story.append(Paragraph("Answer Key — Part 1 Reading (40 marks)", styles["h2"]))
    story.append(Paragraph("Award <b>2 marks</b> for each correct answer.", styles["instruction"]))

    key_data = [
        ["Q", "Answer", "Q", "Answer", "Q", "Answer", "Q", "Answer"],
        ["1", "B (is)", "6", "B (goes)", "11", "C (rainy)", "16", "D"],
        ["2", "C (What)", "7", "A (open)", "12", "B (apartment)", "17", "B"],
        ["3", "A (drink)", "8", "C (went)", "13", "C", "18", "C"],
        ["4", "B (are)", "9", "B (supermarket)", "14", "B", "19", "B"],
        ["5", "C (where)", "10", "A (teacher)", "15", "A", "20", "C"],
    ]
    kt = Table(key_data, colWidths=[1.0 * cm, 3.8 * cm] * 4)
    kt.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("GRID", (0, 0), (-1, -1), 0.4, LINE),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("BACKGROUND", (0, 1), (-1, -1), WHITE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]),
            ]
        )
    )
    story.append(kt)
    story.append(Spacer(1, 0.2 * cm))
    story.append(
        Paragraph(
            "Extra meaning in Section C (not used): <b>E</b>.",
            styles["answer"],
        )
    )

    story.append(Paragraph("Writing Mark Scheme — Part 2 (20 marks)", styles["h2"]))
    story.append(Paragraph("Task 1 — Form (8 marks)", styles["h3"]))
    story.append(
        Paragraph(
            "Award <b>1 mark</b> per item if the answer is understandable and relevant in English. "
            "Accept minor spelling errors if meaning is clear. Award 0 if blank, in another language only, "
            "or completely off-topic. Maximum: 8.",
            styles["rubric"],
        )
    )

    story.append(Paragraph("Task 2 — Paragraph (12 marks)", styles["h3"]))
    rubric_rows = [
        ["Band", "Marks", "Descriptor"],
        [
            "Strong A2",
            "10–12",
            "Clear routine description; mostly accurate present simple; linked ideas; 40+ words; message fully achieved.",
        ],
        [
            "A2",
            "7–9",
            "Adequate description; some errors but meaning usually clear; mostly on topic; about 40 words.",
        ],
        [
            "A1",
            "4–6",
            "Simple sentences or phrases; limited control of present simple; meaning partly clear; may be short.",
        ],
        [
            "Below A1",
            "1–3",
            "Very little English; isolated words; message hard to follow.",
        ],
        [
            "No attempt",
            "0",
            "Blank or not in English.",
        ],
    ]
    rt = Table(rubric_rows, colWidths=[2.4 * cm, 1.6 * cm, PAGE_W - 2 * MARGIN - 4.0 * cm])
    rt.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), TEAL),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("BACKGROUND", (0, 1), (-1, -1), WHITE),
            ]
        )
    )
    story.append(rt)

    # Speaking script
    story.append(PageBreak())
    story.append(section_banner("SPEAKING — EXAMINER SCRIPT  ·  20 marks", styles))
    story.append(Spacer(1, 0.3 * cm))
    story.append(
        Paragraph(
            "Conduct the interview in a friendly, supportive way. Allow brief thinking time. "
            "You may rephrase a question once. Do not teach during the test.",
            styles["instruction"],
        )
    )

    story.append(Paragraph("Stage 1 — Personal interview (about 3 minutes)", styles["h2"]))
    story.append(Paragraph("<b>Examiner says:</b>", styles["bold_body"]))
    story.append(
        Paragraph(
            "“Hello. My name is _____. What’s your name?”<br/>"
            "“Nice to meet you. How are you today?”<br/>"
            "“Where do you live?” / “Who do you live with?”<br/>"
            "“Do you work or are you a student?” → follow up: “What do you do?” / “What do you study?”<br/>"
            "“What do you like doing in your free time?”<br/>"
            "“Tell me about a typical day in your week.”",
            styles["body_left"],
        )
    )
    story.append(
        Paragraph(
            "<i>Prompt if needed:</i> “What time do you get up?” “What do you eat for breakfast?” "
            "“When do you finish work/school?”",
            styles["instruction"],
        )
    )

    story.append(Paragraph("Stage 2 — Picture description (about 3 minutes)", styles["h2"]))
    story.append(
        Paragraph(
            "<b>Examiner says:</b> “Look at this picture of a café. Tell me what you can see.”",
            styles["body_left"],
        )
    )
    story.append(
        Paragraph(
            "If the candidate is silent after 10–15 seconds, ask support questions:",
            styles["instruction"],
        )
    )
    for q in [
        "How many people are there?",
        "What is the woman doing?",
        "What is the man doing?",
        "What is the waiter carrying?",
        "Is it a sunny day or a rainy day?",
        "Would you like to go to this café? Why / Why not?",
    ]:
        story.append(Paragraph(f"• {q}", styles["opt"]))

    story.append(Paragraph("Stage 3 — Short dialogue (2–4 minutes)", styles["h2"]))
    story.append(
        Paragraph(
            "<b>Topic card — Food and meals</b> (give orally; do not require reading)",
            styles["bold_body"],
        )
    )
    story.append(
        Paragraph(
            "<b>Examiner says:</b> “Let’s talk about food. I will ask you some questions, "
            "and then you ask me two questions.”",
            styles["body_left"],
        )
    )
    story.append(Paragraph("<b>Ask the candidate:</b>", styles["bold_body"]))
    for q in [
        "What do you usually eat for breakfast?",
        "What is your favourite meal?",
        "Do you like cooking? Why / Why not?",
        "Where do you usually have lunch?",
    ]:
        story.append(Paragraph(f"• {q}", styles["opt"]))
    story.append(
        Paragraph(
            "<b>Then say:</b> “Now please ask me two questions about food or meals.”",
            styles["body_left"],
        )
    )
    story.append(
        Paragraph(
            "Accept any relevant questions (e.g. “Do you like pizza?” “What do you eat for dinner?”). "
            "Answer briefly and naturally.",
            styles["instruction"],
        )
    )

    story.append(Paragraph("Speaking Mark Scheme (20 marks)", styles["h2"]))
    speak_rows = [
        ["Criterion", "Marks", "A1 indicators", "A2 indicators"],
        [
            "Interaction &\nfluency",
            "0–5",
            "Short answers; long pauses; needs heavy support",
            "Keeps going with short turns; occasional hesitation",
        ],
        [
            "Vocabulary",
            "0–5",
            "Basic personal words only",
            "Everyday vocabulary for home, work, free time, food",
        ],
        [
            "Grammar",
            "0–5",
            "Isolated phrases; little sentence control",
            "Simple present / present continuous with frequent but clear errors",
        ],
        [
            "Pronunciation &\ntask success",
            "0–5",
            "Hard to follow; task only partly done",
            "Mostly intelligible; describes picture and asks simple questions",
        ],
    ]
    sp = Table(speak_rows, colWidths=[2.8 * cm, 1.4 * cm, 5.0 * cm, 5.2 * cm])
    sp.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 7.5),
                ("GRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("BACKGROUND", (0, 1), (-1, -1), WHITE),
            ]
        )
    )
    story.append(
        KeepTogether(
            [
                sp,
                Spacer(1, 0.15 * cm),
                Paragraph(
                    "Total Speaking = sum of four criteria (maximum 20). "
                    "Half marks are allowed (e.g. 3.5) if your local policy permits; "
                    "otherwise round to the nearest whole mark.",
                    styles["rubric"],
                ),
            ]
        )
    )

    # Score sheet & level decision
    story.append(PageBreak())
    story.append(section_banner("SCORE SHEET & LEVEL DECISION", styles))
    story.append(Spacer(1, 0.2 * cm))

    story.append(
        info_box(
            [
                ("Candidate name:", "_" * 50),
                ("Examiner name:", "_" * 30 + "    Date: " + "_" * 20),
            ],
            styles,
        )
    )
    story.append(Spacer(1, 0.2 * cm))

    score_rows = [
        ["Component", "Raw score", "Maximum"],
        ["Part 1 Reading", "________", "40"],
        ["Part 2 Writing", "________", "20"],
        ["Part 3 Speaking", "________", "20"],
        ["TOTAL", "________", "80"],
    ]
    sc = Table(score_rows, colWidths=[6 * cm, 5 * cm, 4.4 * cm])
    sc.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.5, LINE),
                ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("BACKGROUND", (0, -1), (-1, -1), SOFT),
                ("BACKGROUND", (0, 1), (-1, -2), WHITE),
            ]
        )
    )
    story.append(sc)

    story.append(Paragraph("Official level placement (total out of 80)", styles["h2"]))
    level_rows = [
        ["Total score", "Placement", "Typical profile"],
        [
            "0–24",
            "Below A1",
            "Needs pre-A1 / absolute beginner support before an A1 course.",
        ],
        [
            "25–49",
            "A1",
            "Can handle basic personal information with support; limited connected text.",
        ],
        [
            "50–80",
            "A2",
            "Can manage simple everyday reading, short writing, and basic spoken interaction.",
        ],
    ]
    lv = Table(level_rows, colWidths=[2.8 * cm, 2.6 * cm, PAGE_W - 2 * MARGIN - 5.4 * cm])
    lv.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), TEAL),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#FDECEC")),
                ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#FFF8E7")),
                ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#E7F6F0")),
            ]
        )
    )
    story.append(lv)

    story.append(
        Paragraph(
            "<b>Borderline:</b> within 3 marks of a cut-off (22–27 or 47–52), place higher only if "
            "at least two skills match that level; if one skill is much weaker (e.g. Speaking ≤ 6/20), place lower.",
            styles["rubric"],
        )
    )

    story.append(Paragraph("Final placement", styles["h2"]))
    final = Table(
        [
            [
                Paragraph("☐ Below A1", styles["center"]),
                Paragraph("☐ A1", styles["center"]),
                Paragraph("☐ A2", styles["center"]),
            ]
        ],
        colWidths=[(PAGE_W - 2 * MARGIN) / 3] * 3,
    )
    final.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.8, NAVY),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
            ]
        )
    )
    story.append(final)

    story.append(Paragraph("Examiner comments / recommended next steps", styles["h2"]))
    story.append(writing_lines(2))
    story.append(
        Paragraph(
            "Examiner signature: _________________________     Date: _______________",
            styles["body_left"],
        )
    )
    story.append(Spacer(1, 0.12 * cm))
    cefr = Table(
        [
            [
                Paragraph(
                    "<b>CEFR alignment note.</b> This test samples A1–A2 can-do statements for short texts, "
                    "basic personal writing, and simple spoken interaction. "
                    "It is a placement tool, not an official CEFR certificate.",
                    styles["rubric"],
                )
            ]
        ],
        colWidths=[PAGE_W - 2 * MARGIN],
    )
    cefr.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SOFT),
                ("BOX", (0, 0), (-1, -1), 0.6, TEAL),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(cefr)

    # Build PDF
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=1.6 * cm,
        bottomMargin=1.7 * cm,
        title="CEFR A1–A2 English Level Placement Test",
        author="The Language Lab",
        subject="English placement test covering Reading, Writing, and Speaking for A1/A2",
    )
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    return OUTPUT


if __name__ == "__main__":
    path = build_document()
    print(f"Created: {path}")
