#!/usr/bin/env python3
"""Generate a 30-question Digital SAT Reading & Writing practice test PDF."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
    HRFlowable,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Colors
NAVY = HexColor("#1a365d")
TEAL = HexColor("#2c7a7b")
LIGHT_GRAY = HexColor("#f7fafc")
MED_GRAY = HexColor("#e2e8f0")
DARK = HexColor("#1a202c")
ACCENT = HexColor("#c05621")

OUTPUT = "/workspace/sat-practice/SAT_Reading_Writing_Practice_Test_30.pdf"

# Unicode fonts (Turkish + English)
pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Serif", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Serif-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"))
# Oblique via regular for italic tags in Paragraph (reportlab <i> needs Italic font name)
pdfmetrics.registerFont(TTFont("DejaVu-Oblique", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily

registerFontFamily(
    "DejaVu",
    normal="DejaVu",
    bold="DejaVu-Bold",
    italic="DejaVu-Oblique",
    boldItalic="DejaVu-Bold",
)
registerFontFamily(
    "DejaVu-Serif",
    normal="DejaVu-Serif",
    bold="DejaVu-Serif-Bold",
    italic="DejaVu-Serif",
    boldItalic="DejaVu-Serif-Bold",
)


def make_styles():
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            fontName="DejaVu-Bold",
            fontSize=26,
            leading=32,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverSub",
            fontName="DejaVu",
            fontSize=14,
            leading=18,
            textColor=TEAL,
            alignment=TA_CENTER,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverMeta",
            fontName="DejaVu",
            fontSize=11,
            leading=15,
            textColor=DARK,
            alignment=TA_CENTER,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionHead",
            fontName="DejaVu-Bold",
            fontSize=13,
            leading=16,
            textColor=NAVY,
            spaceBefore=14,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TopicTag",
            fontName="DejaVu-Oblique",
            fontSize=8,
            leading=10,
            textColor=TEAL,
            spaceBefore=2,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="QNum",
            fontName="DejaVu-Bold",
            fontSize=11,
            leading=14,
            textColor=NAVY,
            spaceBefore=10,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Passage",
            fontName="DejaVu-Serif",
            fontSize=10,
            leading=13,
            textColor=DARK,
            alignment=TA_JUSTIFY,
            spaceBefore=4,
            spaceAfter=6,
            leftIndent=8,
            rightIndent=8,
            borderPadding=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Stem",
            fontName="DejaVu",
            fontSize=10,
            leading=13,
            textColor=DARK,
            alignment=TA_JUSTIFY,
            spaceBefore=2,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Choice",
            fontName="DejaVu",
            fontSize=10,
            leading=13,
            textColor=DARK,
            leftIndent=14,
            spaceBefore=1,
            spaceAfter=1,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Instr",
            fontName="DejaVu",
            fontSize=10,
            leading=14,
            textColor=DARK,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="AnsHead",
            fontName="DejaVu-Bold",
            fontSize=14,
            leading=18,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="AnsLine",
            fontName="DejaVu",
            fontSize=10,
            leading=14,
            textColor=DARK,
            spaceBefore=2,
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="FooterNote",
            fontName="DejaVu",
            fontSize=8,
            leading=10,
            textColor=HexColor("#718096"),
            alignment=TA_CENTER,
        )
    )
    return styles


# ---------------------------------------------------------------------------
# 30 questions — early Digital SAT R&W topics
# ---------------------------------------------------------------------------
QUESTIONS = [
    # ---- Words in Context (1–5) ----
    {
        "topic": "Craft and Structure · Words in Context",
        "passage": (
            "Although the museum’s new exhibit was widely advertised, attendance "
            "remained <b>tepid</b> throughout the opening week. Curators had expected "
            "crowds; instead, galleries were often empty by midafternoon."
        ),
        "stem": "As used in the text, <b>tepid</b> most nearly means",
        "choices": [
            "A) lukewarm or unenthusiastic.",
            "B) unexpectedly expensive.",
            "C) carefully planned.",
            "D) highly controversial.",
        ],
        "answer": "A",
        "explain": "Context of empty galleries and unmet expectations points to weak/unenthusiastic attendance.",
    },
    {
        "topic": "Craft and Structure · Words in Context",
        "passage": (
            "The biologist’s explanation of the experiment was so <b>lucid</b> that "
            "even students with little background in genetics could follow each step "
            "of the procedure."
        ),
        "stem": "As used in the text, <b>lucid</b> most nearly means",
        "choices": [
            "A) brightly lit.",
            "B) clear and easy to understand.",
            "C) overly technical.",
            "D) brief and incomplete.",
        ],
        "answer": "B",
        "explain": "Students with little background could follow — so lucid = clear.",
    },
    {
        "topic": "Craft and Structure · Words in Context",
        "passage": (
            "Critics argued that the mayor’s plan to revitalize downtown was "
            "<b>ambitious</b> but unrealistic, citing the city’s limited budget and "
            "the project’s enormous scope."
        ),
        "stem": "As used in the text, <b>ambitious</b> most nearly means",
        "choices": [
            "A) dishonest.",
            "B) large in scale or intent.",
            "C) popular with voters.",
            "D) carefully researched.",
        ],
        "answer": "B",
        "explain": "Paired with “enormous scope,” ambitious means large in scale/intent.",
    },
    {
        "topic": "Craft and Structure · Words in Context",
        "passage": (
            "Rather than offering a single explanation, the historian presents several "
            "<b>competing</b> theories about the city’s sudden decline in the 1800s."
        ),
        "stem": "As used in the text, <b>competing</b> most nearly means",
        "choices": [
            "A) athletic.",
            "B) rival or alternative.",
            "C) outdated.",
            "D) incomplete.",
        ],
        "answer": "B",
        "explain": "Several theories that vie as explanations = rival/alternative.",
    },
    {
        "topic": "Craft and Structure · Words in Context",
        "passage": (
            "The committee’s report was <b>concise</b>: in fewer than ten pages it "
            "summarized years of research and recommended three specific actions."
        ),
        "stem": "As used in the text, <b>concise</b> most nearly means",
        "choices": [
            "A) brief yet complete.",
            "B) confusing.",
            "C) harshly critical.",
            "D) outdated.",
        ],
        "answer": "A",
        "explain": "Few pages covering years of research = brief yet complete.",
    },
    # ---- Central Ideas & Details (6–9) ----
    {
        "topic": "Information and Ideas · Central Ideas and Details",
        "passage": (
            "Honeybees communicate the location of food through a “waggle dance.” "
            "The angle of the dance relative to the sun indicates direction, while "
            "the duration of the waggle indicates distance. Researchers have shown "
            "that other bees can use this information to fly directly to the food source."
        ),
        "stem": "Which choice best states the main idea of the text?",
        "choices": [
            "A) Honeybees produce honey by dancing near flowers.",
            "B) Honeybees use a dance to tell others where food is located.",
            "C) The sun’s position confuses honeybees searching for food.",
            "D) Researchers taught honeybees a new form of communication.",
        ],
        "answer": "B",
        "explain": "The whole passage explains how the waggle dance conveys food location.",
    },
    {
        "topic": "Information and Ideas · Central Ideas and Details",
        "passage": (
            "In the 1960s, many cities replaced streetcars with buses, arguing that "
            "buses were more flexible and cheaper to operate. Decades later, some of "
            "those same cities began rebuilding rail lines, citing congestion and "
            "the desire for more reliable transit."
        ),
        "stem": "According to the text, why did some cities later rebuild rail lines?",
        "choices": [
            "A) Buses had become more expensive than streetcars.",
            "B) Streetcars were considered more flexible than buses.",
            "C) Cities faced traffic problems and wanted more reliable transit.",
            "D) The federal government required all cities to use rail.",
        ],
        "answer": "C",
        "explain": "The text explicitly cites congestion and desire for reliable transit.",
    },
    {
        "topic": "Information and Ideas · Central Ideas and Details",
        "passage": (
            "Mangrove forests protect coastal communities by absorbing wave energy "
            "during storms. They also serve as nurseries for fish and store large "
            "amounts of carbon. Despite these benefits, mangrove areas continue to "
            "shrink due to coastal development."
        ),
        "stem": "Which detail from the text best supports the idea that mangroves help people?",
        "choices": [
            "A) Mangrove areas continue to shrink.",
            "B) Mangroves absorb wave energy during storms.",
            "C) Coastal development is increasing.",
            "D) Fish live in many ocean habitats.",
        ],
        "answer": "B",
        "explain": "Absorbing wave energy during storms directly protects communities.",
    },
    {
        "topic": "Information and Ideas · Central Ideas and Details",
        "passage": (
            "Ada Lovelace, writing in the 1840s about Charles Babbage’s proposed "
            "Analytical Engine, described a method for calculating Bernoulli numbers. "
            "Her notes are often cited as an early example of what would later be "
            "called a computer program."
        ),
        "stem": "The text most strongly suggests that Lovelace’s notes were notable because they",
        "choices": [
            "A) proved that Babbage’s machine could never be built.",
            "B) contained an early form of computer programming.",
            "C) were the first books printed about mathematics.",
            "D) criticized the use of Bernoulli numbers.",
        ],
        "answer": "B",
        "explain": "The text says her notes are cited as an early computer program.",
    },
    # ---- Inferences (10–12) ----
    {
        "topic": "Information and Ideas · Inferences",
        "passage": (
            "When the library announced evening hours three nights a week, "
            "student visits increased sharply. Staff also noted that the number of "
            "books checked out after 6 p.m. rose more than daytime checkouts."
        ),
        "stem": "Based on the text, which statement is most strongly supported?",
        "choices": [
            "A) Students prefer to study only in the morning.",
            "B) Extended evening hours made the library more useful to students.",
            "C) The library should eliminate daytime hours.",
            "D) Book checkouts always decline when libraries stay open later.",
        ],
        "answer": "B",
        "explain": "Visits and evening checkouts rose after evening hours were added.",
    },
    {
        "topic": "Information and Ideas · Inferences",
        "passage": (
            "The chef insisted on buying produce from nearby farms, even when "
            "imported options were cheaper. She told reporters that freshness and "
            "supporting local growers mattered more to her than cutting costs."
        ),
        "stem": "It can reasonably be inferred that the chef",
        "choices": [
            "A) values local, fresh ingredients over the lowest price.",
            "B) refuses to cook with any vegetables.",
            "C) believes imported food is always unsafe.",
            "D) plans to close her restaurant soon.",
        ],
        "answer": "A",
        "explain": "She prioritizes freshness and local growers over cost.",
    },
    {
        "topic": "Information and Ideas · Inferences",
        "passage": (
            "Although the novel received mixed reviews when it was first published, "
            "it has remained continuously in print for over a century and is now "
            "widely taught in high school literature courses."
        ),
        "stem": "Which inference is best supported by the text?",
        "choices": [
            "A) The novel was immediately a bestseller.",
            "B) Early mixed reviews did not prevent the novel’s lasting importance.",
            "C) High schools only teach recently published books.",
            "D) The author never wrote another novel.",
        ],
        "answer": "B",
        "explain": "Despite mixed early reviews, it stayed in print and is widely taught.",
    },
    # ---- Command of Evidence (13–15) ----
    {
        "topic": "Information and Ideas · Command of Evidence",
        "passage": (
            "A study compared two groups of office workers. Group A took a "
            "ten-minute walk outdoors at midday; Group B remained indoors. "
            "In the afternoon, Group A completed a focus task 18% faster on average "
            "than Group B."
        ),
        "stem": "Which finding, if true, would most weaken the claim that outdoor walks improve afternoon focus?",
        "choices": [
            "A) Group A workers reported enjoying the weather that day.",
            "B) Group A and Group B had identical workloads in the morning.",
            "C) Group A had already scored higher on focus tests before the study began.",
            "D) The outdoor route was approximately half a mile long.",
        ],
        "answer": "C",
        "explain": "Pre-existing higher focus scores would explain the result without the walk.",
    },
    {
        "topic": "Information and Ideas · Command of Evidence",
        "passage": (
            "City planners claim that adding bike lanes on Main Street will increase "
            "the number of people who bicycle to work. They point to a survey in which "
            "62% of residents said they would bike more if dedicated lanes existed."
        ),
        "stem": "Which piece of evidence would best support the planners’ claim?",
        "choices": [
            "A) A nearby city saw bicycle commuting rise after installing similar lanes.",
            "B) Main Street currently has heavy car traffic at rush hour.",
            "C) Some residents prefer buses to bicycles.",
            "D) Bike lanes are less expensive than building new parking garages.",
        ],
        "answer": "A",
        "explain": "A comparable city that saw increased bike commuting is direct supporting evidence.",
    },
    {
        "topic": "Information and Ideas · Command of Evidence",
        "passage": (
            "Dr. Kim argues that reading fiction improves empathy. She cites a "
            "laboratory experiment in which participants who read a short story "
            "scored higher on an empathy questionnaire than those who read a "
            "nonfiction article of the same length."
        ),
        "stem": "Which choice best describes the function of the cited experiment in the text?",
        "choices": [
            "A) It provides evidence offered in support of Dr. Kim’s argument.",
            "B) It contradicts Dr. Kim’s main claim.",
            "C) It explains how empathy questionnaires are scored.",
            "D) It summarizes the plot of the short story.",
        ],
        "answer": "A",
        "explain": "The experiment is presented as evidence for her claim.",
    },
    # ---- Text Structure / Purpose (16–17) ----
    {
        "topic": "Craft and Structure · Text Structure and Purpose",
        "passage": (
            "Most people assume that deserts are lifeless. In fact, deserts host "
            "specialized plants and animals adapted to extreme heat and scarce water. "
            "Understanding these adaptations can help scientists design better "
            "water-conservation technologies."
        ),
        "stem": "Which choice best describes the overall structure of the text?",
        "choices": [
            "A) It presents a common belief, then challenges it and notes a practical benefit.",
            "B) It lists desert animals and then describes a scientific experiment.",
            "C) It argues that deserts should be converted into farmland.",
            "D) It compares two competing theories about climate change.",
        ],
        "answer": "A",
        "explain": "Common assumption → correction → practical implication.",
    },
    {
        "topic": "Craft and Structure · Text Structure and Purpose",
        "passage": (
            "The following text is from a museum brochure: “Visitors are invited "
            "to explore the sculpture garden before entering the main galleries. "
            "Maps are available at the entrance, and guided tours begin every hour.”"
        ),
        "stem": "The main purpose of the text is to",
        "choices": [
            "A) criticize the museum’s layout.",
            "B) provide practical information for visitors.",
            "C) compare sculpture to painting.",
            "D) argue that guided tours are unnecessary.",
        ],
        "answer": "B",
        "explain": "It gives visitor guidance: where to go, maps, tour times.",
    },
    # ---- Transitions (18–20) ----
    {
        "topic": "Expression of Ideas · Transitions",
        "passage": (
            "Many students prefer digital textbooks because they are searchable and "
            "often cheaper. ______ some learners say they concentrate better when "
            "reading from printed pages."
        ),
        "stem": "Which choice completes the text with the most logical transition?",
        "choices": [
            "A) Therefore,",
            "B) For example,",
            "C) However,",
            "D) Likewise,",
        ],
        "answer": "C",
        "explain": "The second sentence contrasts with the first → However.",
    },
    {
        "topic": "Expression of Ideas · Transitions",
        "passage": (
            "The research team collected water samples from twelve lakes. ______ "
            "they tested each sample for microplastic particles."
        ),
        "stem": "Which choice completes the text with the most logical transition?",
        "choices": [
            "A) Meanwhile,",
            "B) Next,",
            "C) In contrast,",
            "D) Nevertheless,",
        ],
        "answer": "B",
        "explain": "Sequential process: collect, then test → Next.",
    },
    {
        "topic": "Expression of Ideas · Transitions",
        "passage": (
            "Solar panels have become significantly less expensive over the past decade. "
            "______ more households can now afford to install them."
        ),
        "stem": "Which choice completes the text with the most logical transition?",
        "choices": [
            "A) As a result,",
            "B) On the other hand,",
            "C) For instance,",
            "D) Regardless,",
        ],
        "answer": "A",
        "explain": "Lower cost causes more affordability → As a result.",
    },
    # ---- Rhetorical Synthesis (21) ----
    {
        "topic": "Expression of Ideas · Rhetorical Synthesis",
        "passage": (
            "While researching a local park for a class presentation, a student "
            "takes these notes:<br/>"
            "• Park opened in 1924<br/>"
            "• Designed by landscape architect Elena Ruiz<br/>"
            "• Features a rose garden and a lake<br/>"
            "• Hosts free summer concerts<br/>"
            "• Listed on the National Register of Historic Places in 1998"
        ),
        "stem": (
            "The student wants to emphasize the park’s historical significance. "
            "Which choice most effectively uses relevant information from the notes?"
        ),
        "choices": [
            "A) The park, which opened in 1924 and was listed on the National Register of Historic Places in 1998, was designed by Elena Ruiz.",
            "B) The park has a rose garden and a lake and hosts free summer concerts.",
            "C) Elena Ruiz designed parks in several cities.",
            "D) Summer concerts at the park are free for visitors.",
        ],
        "answer": "A",
        "explain": "Opening date + historic register listing best emphasize historical significance.",
    },
    # ---- Boundaries / Punctuation (22–25) ----
    {
        "topic": "Standard English Conventions · Boundaries",
        "passage": None,
        "stem": (
            "Which choice completes the text so that it conforms to the conventions "
            "of Standard English?<br/><br/>"
            "The scientist presented her findings at the conference ______ the audience "
            "asked many detailed questions."
        ),
        "choices": [
            "A) ; and",
            "B) , and",
            "C) : and",
            "D) and,",
        ],
        "answer": "B",
        "explain": "Two independent clauses joined by coordinating conjunction need a comma before and.",
    },
    {
        "topic": "Standard English Conventions · Boundaries",
        "passage": None,
        "stem": (
            "Which choice completes the text so that it conforms to the conventions "
            "of Standard English?<br/><br/>"
            "My favorite novel ______ <i>To Kill a Mockingbird</i>, is required reading "
            "in many schools."
        ),
        "choices": [
            "A) ,",
            "B) ;",
            "C) :",
            "D) .",
        ],
        "answer": "A",
        "explain": "An appositive (the book title) is set off with commas on both sides.",
    },
    {
        "topic": "Standard English Conventions · Boundaries",
        "passage": None,
        "stem": (
            "Which choice completes the text so that it conforms to the conventions "
            "of Standard English?<br/><br/>"
            "The recipe requires three ingredients ______ flour, sugar, and butter."
        ),
        "choices": [
            "A) ;",
            "B) ,",
            "C) :",
            "D) —",
        ],
        "answer": "C",
        "explain": "A colon introduces a list after an independent clause.",
    },
    {
        "topic": "Standard English Conventions · Boundaries",
        "passage": None,
        "stem": (
            "Which choice completes the text so that it conforms to the conventions "
            "of Standard English?<br/><br/>"
            "Because the bridge was closed for repairs ______ drivers had to take "
            "a longer route."
        ),
        "choices": [
            "A) ;",
            "B) ,",
            "C) :",
            "D) —",
        ],
        "answer": "B",
        "explain": "Dependent clause before independent clause → comma.",
    },
    # ---- Form, Structure, and Sense (26–30) ----
    {
        "topic": "Standard English Conventions · Form, Structure, and Sense",
        "passage": None,
        "stem": (
            "Which choice completes the text so that it conforms to the conventions "
            "of Standard English?<br/><br/>"
            "The pair of shoes ______ on the porch all night."
        ),
        "choices": [
            "A) were left",
            "B) was left",
            "C) are left",
            "D) have been leaving",
        ],
        "answer": "B",
        "explain": "Subject is “pair” (singular), so “was left.”",
    },
    {
        "topic": "Standard English Conventions · Form, Structure, and Sense",
        "passage": None,
        "stem": (
            "Which choice completes the text so that it conforms to the conventions "
            "of Standard English?<br/><br/>"
            "Neither the coach nor the players ______ ready to leave the stadium."
        ),
        "choices": [
            "A) was",
            "B) is",
            "C) were",
            "D) has been",
        ],
        "answer": "C",
        "explain": "With neither/nor, verb agrees with nearer subject “players” (plural) → were.",
    },
    {
        "topic": "Standard English Conventions · Form, Structure, and Sense",
        "passage": None,
        "stem": (
            "Which choice completes the text so that it conforms to the conventions "
            "of Standard English?<br/><br/>"
            "Last summer, the museum ______ a special exhibit on ancient pottery."
        ),
        "choices": [
            "A) hosts",
            "B) hosted",
            "C) will host",
            "D) hosting",
        ],
        "answer": "B",
        "explain": "“Last summer” requires past tense → hosted.",
    },
    {
        "topic": "Standard English Conventions · Form, Structure, and Sense",
        "passage": None,
        "stem": (
            "Which choice completes the text so that it conforms to the conventions "
            "of Standard English?<br/><br/>"
            "Walking through the old market, ______."
        ),
        "choices": [
            "A) the spices smelled wonderful to Maya",
            "B) wonderful spices were smelled by Maya",
            "C) Maya smelled the wonderful spices",
            "D) smelling wonderful spices was Maya",
        ],
        "answer": "C",
        "explain": "Modifier “Walking…” must modify Maya (the walker), not spices.",
    },
    {
        "topic": "Standard English Conventions · Form, Structure, and Sense",
        "passage": None,
        "stem": (
            "Which choice completes the text so that it conforms to the conventions "
            "of Standard English?<br/><br/>"
            "The scholarship rewards students who excel in academics, contribute "
            "to their communities, and ______ leadership skills."
        ),
        "choices": [
            "A) demonstrating",
            "B) to demonstrate",
            "C) demonstrate",
            "D) demonstration of",
        ],
        "answer": "C",
        "explain": "Parallel structure: excel, contribute, and demonstrate.",
    },
]


def add_header_footer(canvas, doc):
    canvas.saveState()
    page = canvas.getPageNumber()
    if page > 1:
        canvas.setStrokeColor(MED_GRAY)
        canvas.setLineWidth(0.5)
        canvas.line(0.75 * inch, letter[1] - 0.55 * inch, letter[0] - 0.75 * inch, letter[1] - 0.55 * inch)
        canvas.setFont("DejaVu", 8)
        canvas.setFillColor(NAVY)
        canvas.drawString(0.75 * inch, letter[1] - 0.45 * inch, "SAT Reading & Writing Practice Test")
        canvas.drawRightString(letter[0] - 0.75 * inch, letter[1] - 0.45 * inch, "30 Questions")
        canvas.setStrokeColor(MED_GRAY)
        canvas.line(0.75 * inch, 0.55 * inch, letter[0] - 0.75 * inch, 0.55 * inch)
        canvas.setFillColor(HexColor("#718096"))
        canvas.drawCentredString(letter[0] / 2, 0.35 * inch, f"Page {page}")
    canvas.restoreState()


def build_pdf():
    styles = make_styles()
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title="SAT Reading & Writing Practice Test — 30 Questions",
        author="SAT Practice",
    )

    story = []

    # Cover
    story.append(Spacer(1, 1.4 * inch))
    story.append(Paragraph("DIGITAL SAT® STYLE", styles["CoverSub"]))
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("Reading and Writing", styles["CoverTitle"]))
    story.append(Paragraph("Practice Test", styles["CoverTitle"]))
    story.append(Spacer(1, 0.25 * inch))
    story.append(
        HRFlowable(width="60%", thickness=2, color=TEAL, spaceBefore=4, spaceAfter=4, hAlign="CENTER")
    )
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("30 Soruluk Alıştırma Sınavı", styles["CoverSub"]))
    story.append(Paragraph("İlk / Temel Konular · Beginner–Foundational Topics", styles["CoverMeta"]))
    story.append(Spacer(1, 0.45 * inch))

    meta_data = [
        [Paragraph("<b>Soru sayısı / Questions:</b> 30", styles["CoverMeta"])],
        [Paragraph("<b>Süre önerisi / Suggested time:</b> 32 dakika (yaklaşık)", styles["CoverMeta"])],
        [Paragraph("<b>Seçenekler / Choices:</b> A · B · C · D", styles["CoverMeta"])],
        [Paragraph("<b>Cevap anahtarı / Answer key:</b> PDF sonunda", styles["CoverMeta"])],
    ]
    meta_table = Table(meta_data, colWidths=[5.5 * inch])
    meta_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
                ("BOX", (0, 0), (-1, -1), 1, TEAL),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 16),
            ]
        )
    )
    story.append(meta_table)

    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("Konu Dağılımı / Topic Breakdown", styles["SectionHead"]))
    topics_text = (
        "1–5 Words in Context · 6–9 Central Ideas &amp; Details · 10–12 Inferences · "
        "13–15 Command of Evidence · 16–17 Text Structure &amp; Purpose · "
        "18–20 Transitions · 21 Rhetorical Synthesis · 22–25 Boundaries (punctuation) · "
        "26–30 Form, Structure &amp; Sense (grammar)"
    )
    story.append(Paragraph(topics_text, styles["Instr"]))
    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Paragraph(
            "Bu test resmi College Board sınavı değildir; Digital SAT Reading &amp; Writing "
            "formatına benzer alıştırma sorularıdır. Her soruda doğru seçeneği daire içine alın.",
            styles["Instr"],
        )
    )
    story.append(
        Paragraph(
            "This is an unofficial practice set modeled on Digital SAT Reading &amp; Writing. "
            "Circle the best answer for each question.",
            styles["Instr"],
        )
    )

    story.append(PageBreak())

    # Instructions page
    story.append(Paragraph("Directions / Yönergeler", styles["SectionHead"]))
    story.append(
        Paragraph(
            "Each question has one best answer. For passage-based items, read the short text "
            "carefully, then choose the option that best answers the question. For Standard "
            "English Conventions items, choose the option that corrects the blank or completes "
            "the sentence correctly.",
            styles["Instr"],
        )
    )
    story.append(
        Paragraph(
            "Her sorunun bir doğru cevabı vardır. Metinli sorularda kısa paragrafı okuyup "
            "en uygun seçeneği işaretleyin. Dilbilgisi / noktalama sorularında cümleyi "
            "Standart İngilizce kurallarına göre tamamlayan seçeneği seçin.",
            styles["Instr"],
        )
    )
    story.append(Spacer(1, 0.15 * inch))
    story.append(
        HRFlowable(width="100%", thickness=1, color=MED_GRAY, spaceBefore=6, spaceAfter=10)
    )

    # Questions
    for i, q in enumerate(QUESTIONS, start=1):
        block = []
        block.append(Paragraph(f"Question {i}", styles["QNum"]))
        block.append(Paragraph(q["topic"], styles["TopicTag"]))
        if q.get("passage"):
            block.append(Paragraph(f"<i>{q['passage']}</i>", styles["Passage"]))
        block.append(Paragraph(q["stem"], styles["Stem"]))
        for ch in q["choices"]:
            block.append(Paragraph(ch, styles["Choice"]))
        block.append(Spacer(1, 6))
        block.append(
            HRFlowable(width="100%", thickness=0.4, color=MED_GRAY, spaceBefore=2, spaceAfter=2)
        )
        story.append(KeepTogether(block))

    # Answer key
    story.append(PageBreak())
    story.append(Paragraph("Answer Key / Cevap Anahtarı", styles["AnsHead"]))
    story.append(
        Paragraph(
            "Aşağıda doğru cevaplar ve kısa açıklamalar yer alır.",
            styles["Instr"],
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    # Answer grid
    grid_rows = []
    row = []
    for i, q in enumerate(QUESTIONS, start=1):
        cell = Paragraph(f"<b>{i}.</b> {q['answer']}", styles["AnsLine"])
        row.append(cell)
        if len(row) == 5:
            grid_rows.append(row)
            row = []
    if row:
        while len(row) < 5:
            row.append(Paragraph("", styles["AnsLine"]))
        grid_rows.append(row)

    grid = Table(grid_rows, colWidths=[1.3 * inch] * 5)
    grid.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
                ("BOX", (0, 0), (-1, -1), 1, TEAL),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, MED_GRAY),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.append(grid)
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("Explanations / Açıklamalar", styles["SectionHead"]))

    for i, q in enumerate(QUESTIONS, start=1):
        story.append(
            Paragraph(
                f"<b>{i}. {q['answer']}</b> — {q['explain']}",
                styles["AnsLine"],
            )
        )

    story.append(Spacer(1, 0.4 * inch))
    story.append(
        HRFlowable(width="100%", thickness=1, color=MED_GRAY, spaceBefore=8, spaceAfter=8)
    )
    story.append(
        Paragraph(
            "Unofficial practice material · Digital SAT® is a trademark of College Board, "
            "which was not involved in the production of this document.",
            styles["FooterNote"],
        )
    )

    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build_pdf()
