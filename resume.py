"""Build dist/Prajwal_Janbandhu_Resume.pdf. Run: uv run --with reportlab python resume.py

Layout follows the Google Docs template (Calibri look, small-caps headings
with a rule, bold keywords, ● bullets). ATS rules kept on purpose: single
column, real text only (no icons), headings at one font size so they extract
as words ("WORK EXPERIENCE", not "W E / ORK XPERIENCE"), embedded TTF with a
Unicode map, and every URL written out in full.
"""
from pathlib import Path

from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

# Carlito is metric-compatible with Calibri (OFL, see fonts/OFL.txt).
FONTS = Path(__file__).parent / "fonts"
pdfmetrics.registerFont(TTFont("Carlito", FONTS / "Carlito-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Carlito-Bold", FONTS / "Carlito-Bold.ttf"))
addMapping("Carlito", 0, 0, "Carlito")
addMapping("Carlito", 1, 0, "Carlito-Bold")

body = ParagraphStyle("body", fontName="Carlito", fontSize=12, leading=14.6)
name = ParagraphStyle("name", body, fontSize=22.5, leading=27, alignment=TA_CENTER)
contact = ParagraphStyle("contact", body, fontSize=11, leading=16, alignment=TA_CENTER)
heading = ParagraphStyle("heading", body, fontSize=13.5, leading=17, leftIndent=8, spaceBefore=10)
skill = ParagraphStyle("skill", body, fontName="Carlito-Bold", leftIndent=14)
bullet = ParagraphStyle("bullet", body, leftIndent=36, bulletIndent=18, bulletFontName="Carlito", bulletFontSize=10)
right = ParagraphStyle("right", body, alignment=TA_RIGHT)


def a(url, text=None):
    return f'<a href="{url}"><u>{text or url.removeprefix("https://").removeprefix("mailto:")}</u></a>'


def h(text):
    # One font size: mixed-size small caps extract as "W E / ORK XPERIENCE".
    return [Paragraph(text.upper(), heading), HRFlowable(width="100%", thickness=1, color="black", spaceBefore=1, spaceAfter=10)]


def row(left, when="", indent=8, space_after=10):
    t = Table([[Paragraph(left, ParagraphStyle("l", body, leftIndent=indent)), Paragraph(when, right)]],
              colWidths=["72%", "28%"])
    t.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                           ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), space_after)]))
    return t


def bullets(*items):
    return [Paragraph(i, bullet, bulletText="●") for i in items] + [Spacer(1, 12)]


story = [
    Paragraph("Prajwal Janbandhu", name),
    Paragraph(" | ".join([a("https://github.com/Prajwal2246"), a("https://linkedin.com/in/prajwaljanbandhu/"),
                          a("https://leetcode.com/u/Prajwal_2246/")]), contact),
    Paragraph(f"{a('mailto:prajwal3274@gmail.com')} | +91 9511933274", contact),

    *h("Summary"),
    Paragraph(
        "Full Stack Developer experienced with <b>Ruby on Rails</b> and <b>React</b>, with a strong foundation in "
        "<b>JavaScript</b>, <b>TypeScript</b>, <b>Node.js</b>, and <b>Next.js</b>. Experienced in building <b>APIs</b>, "
        "automation, integrations, and database-driven applications using AI-assisted development with <b>Claude Code</b>, "
        "with <b>9 merged pull requests</b> to open-source projects.", body),

    *h("Skills"),
    Paragraph("Languages: JavaScript, TypeScript, Ruby, SQL, Go", skill),
    Paragraph("Frontend: React.js, Next.js, Tailwind CSS", skill),
    Paragraph("Backend: Node.js, Express.js, Ruby on Rails, REST APIs", skill),
    Paragraph("Databases: PostgreSQL, MongoDB, Prisma ORM", skill),
    Paragraph("AI &amp; Tools: Claude Code, Git, Firebase", skill),

    *h("Work Experience"),
    row("<b>Envision Next LLP — Associate Full Stack Developer</b>", "<b>Apr 2026 - Present</b>"),
    *bullets(
        "Develop and maintain an enterprise CRM platform used by 200+ employees, working across HRMS, Incentives, "
        "Compliance Records, Automation, Scraping, Extensions, and Corrections modules.",
        "Owned end-to-end development of the Incentive module, building dashboards, employee and manager views, "
        "calculation logic, <b>Rails APIs</b>, database changes, filters, reports/exports, and approval workflows.",
        "Developed <b>MahaRERA API</b> integrations and automation for 1,000+ projects, implementing authentication, "
        "response processing, error handling, and Excel-driven workflows to automatically update project information.",
        "Built and enhanced production features across frontend UI, APIs, databases, authentication, permissions, "
        "integrations, and exports, investigating existing code and data flows to deliver end-to-end fixes and improvements.",
        "Used <b>Claude Code</b> as an AI-assisted development tool for codebase exploration, implementation, debugging, "
        "refactoring, and iterative development while reviewing and validating generated changes.",
    ),
    row("<b>Tejas — Development Intern</b>", "<b>May 2025 - Oct 2025</b>"),
    *bullets(
        "Engineered a custom <b>WebRTC</b> signaling mechanism using <b>Firestore</b>, establishing peer-to-peer video "
        "connections in under 2 seconds for 1-on-1 remote mentoring sessions.",
        "Implemented zero-polling real-time data synchronization with <b>Firestore onSnapshot</b> listeners, processing "
        "student questions and updating tutor dashboards with sub-500ms latency.",
        "Integrated <b>Framer Motion</b> for fluid UI transitions and optimized frontend asset delivery for improved "
        "application performance.",
    ),

    *h("Projects"),
    row("<b>Drivly P2P Vehicle-Sharing Platform</b>", a("https://drivly-mu.vercel.app/", "Live Link")),
    *bullets(
        "Built a peer-to-peer vehicle-sharing platform for residential communities using <b>Next.js</b>, "
        "<b>TypeScript</b>, and <b>Tailwind CSS</b>.",
        "Integrated <b>Prisma ORM</b> with <b>PostgreSQL</b> and implemented custom <b>JWT</b> authentication, database "
        "schemas, and realistic multi-user seed data.",
        "Implemented <b>Next.js</b> streaming, loading states, and optimized UI patterns to improve perceived performance "
        "and user experience.",
    ),
    row("<b>Blood Donor App - MERN Stack</b>", a("https://donar-app-frontend.vercel.app/", "Live Link")),
    *bullets(
        "Developed a full-stack blood donor management application using <b>MongoDB</b>, <b>Express.js</b>, "
        "<b>React.js</b> and <b>Node.js</b>.",
        "Built <b>RESTful APIs</b> for user authentication, donor management, and data retrieval, with the frontend "
        "deployed on <b>Vercel</b> and secure cross-origin communication configured with the backend.",
    ),

    *h("Open Source Contributions"),
    row("<b>Fleet — Contributor (7 merged PRs)</b>"),
    *bullets(
        "Contributed fixes across policy execution, software inventory, script handling, navigation, and batch "
        "operations in a large-scale <b>Go</b> and <b>TypeScript/React</b> codebase.",
        "Made <b>fleetctl apply</b> reject incorrectly typed profile paths and labels, and stopped batch software uploads "
        "after the first package failure using a cancellable errgroup context.",
        "Collaborated with maintainers through pull requests, code reviews, CI validation, and iterative changes.",
    ),
    row("<b>Superserve AI — Contributor (2 merged PRs)</b>"),
    *bullets("Contributed to <b>MCP</b> functionality, including network-log pagination with cursor forwarding and "
             "regression tests, and a development watcher fix."),
    row("<b>Vitest — Contributor</b>"),
    *bullets("Opened a pull request adding <b>Temporal.Instant</b> and <b>Temporal.ZonedDateTime</b> support to "
             "<b>vi.setSystemTime()</b>, currently in review."),

    *h("Education"),
    row("B.E. in Information Technology, JSPM RSCOE - CGPA: 8.3", "2020 - 2024", indent=6),
]

SimpleDocTemplate(
    "dist/Prajwal_Janbandhu_Resume.pdf", pagesize=A4, leftMargin=16, rightMargin=24, topMargin=24, bottomMargin=28,
    title="Prajwal Janbandhu - Full Stack Developer", author="Prajwal Janbandhu",
    keywords="Full Stack Developer, Ruby on Rails, React, TypeScript, JavaScript, Node.js, Next.js, PostgreSQL, REST APIs",
).build(story)
