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

body = ParagraphStyle("body", fontName="Carlito", fontSize=10.4, leading=12.4)
name = ParagraphStyle("name", body, fontSize=20, leading=24, alignment=TA_CENTER)
contact = ParagraphStyle("contact", body, fontSize=10.3, leading=13.5, alignment=TA_CENTER)
heading = ParagraphStyle("heading", body, fontSize=12, leading=14, leftIndent=8, spaceBefore=5)
skill = ParagraphStyle("skill", body, leftIndent=14)
bullet = ParagraphStyle("bullet", body, leftIndent=34, bulletIndent=18, bulletFontName="Carlito", bulletFontSize=9)
right = ParagraphStyle("right", body, alignment=TA_RIGHT)


def a(url, text=None):
    return f'<a href="{url}"><u>{text or url.removeprefix("https://").removeprefix("mailto:")}</u></a>'


def pr(repo, n):
    return a(f"https://github.com/{repo}/pull/{n}", f"#{n}")


def h(text):
    # One font size: mixed-size small caps extract as "W E / ORK XPERIENCE".
    return [Paragraph(text.upper(), heading), HRFlowable(width="100%", thickness=1, color="black", spaceBefore=1, spaceAfter=5)]


def row(left, when="", indent=8):
    t = Table([[Paragraph(left, ParagraphStyle("l", body, leftIndent=indent)), Paragraph(when, right)]],
              colWidths=["60%", "40%"])
    t.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                           ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return t


def bullets(*items):
    return [Paragraph(i, bullet, bulletText="●") for i in items] + [Spacer(1, 4)]


FLEET, SUPERSERVE = "fleetdm/fleet", "superserve-ai/superserve"

story = [
    Paragraph("Prajwal Janbandhu", name),
    Paragraph(f"Navi Mumbai, India | +91 9511933274 | {a('mailto:prajwal3274@gmail.com')}", contact),
    Paragraph(" | ".join([a("https://github.com/Prajwal2246"), a("https://linkedin.com/in/prajwaljanbandhu/"),
                          a("https://leetcode.com/u/Prajwal_2246/")]), contact),

    *h("Summary"),
    Paragraph(
        "Full Stack Developer building an enterprise CRM with <b>Ruby on Rails</b>, <b>React</b>, and <b>PostgreSQL</b>, "
        "with a strong foundation in <b>JavaScript</b>, <b>TypeScript</b>, <b>Node.js</b>, and <b>Next.js</b>. Builds "
        "<b>REST APIs</b>, third-party integrations, automation, and database-driven features end to end, with "
        "<b>9 merged pull requests</b> to open-source projects including Fleet.", body),

    *h("Skills"),
    Paragraph("<b>Languages:</b> JavaScript, TypeScript, Ruby, SQL, Go, HTML, CSS", skill),
    Paragraph("<b>Frontend:</b> React.js, Next.js, Tailwind CSS", skill),
    Paragraph("<b>Backend:</b> Ruby on Rails, Node.js, Express.js, REST APIs, JWT", skill),
    Paragraph("<b>Databases:</b> PostgreSQL, MongoDB, Prisma ORM", skill),
    Paragraph("<b>AI &amp; Tools:</b> Claude Code, Git, Firebase, Vercel", skill),

    *h("Work Experience"),
    row("<b>Envision Next LLP — Associate Full Stack Developer</b>", "<b>Apr 2026 - Present</b>"),
    *bullets(
        "Develop and maintain an enterprise CRM platform used by 200+ employees, working across HRMS, Incentives, "
        "Compliance Records, Automation, Scraping, Extensions, and Corrections modules.",
        "Owned end-to-end development of the Incentive module, building dashboards, employee and manager views, "
        "calculation logic, <b>Rails APIs</b>, database changes, filters, reports/exports, and approval workflows.",
        "Developed <b>MahaRERA API</b> integrations and automation for 1,000+ projects, implementing authentication, "
        "response processing, error handling, and Excel-driven workflows to automatically update project information.",
    ),
    row("<b>Tejas — Development Intern</b>", "<b>Jan 2026 - Feb 2026</b>"),
    *bullets(
        "Engineered a custom <b>WebRTC</b> signaling mechanism using <b>Firestore</b>, establishing peer-to-peer video "
        "connections in under 2 seconds for 1-on-1 remote mentoring sessions.",
        "Implemented zero-polling real-time data synchronization with <b>Firestore onSnapshot</b> listeners, processing "
        "student questions and updating tutor dashboards with sub-500ms latency, with <b>Framer Motion</b> UI transitions.",
    ),
    row("<b>Hackveda — Web Development Intern</b>", "<b>Jan 2024 - Jun 2024</b>"),
    *bullets(
        "Implemented UI updates and <b>HTML/CSS</b> changes across company web pages based on design and content requests.",
        "Fixed layout and styling issues on <b>Day Trade Insight</b>, a trading-insights web platform built at Hackveda.",
    ),

    *h("Open Source Contributions"),
    row("<b>Fleet — Contributor (7 merged PRs)</b>", a("https://github.com/fleetdm/fleet", "github.com/fleetdm/fleet")),
    *bullets(
        "Merged fixes across policy execution, software inventory, script handling, and navigation in a large-scale "
        f"<b>Go</b> and <b>TypeScript/React</b> codebase ({pr(FLEET, 54411)}, {pr(FLEET, 53810)}, {pr(FLEET, 54296)}, "
        f"{pr(FLEET, 54509)}, {pr(FLEET, 54726)}).",
        f"Made <b>fleetctl apply</b> reject incorrectly typed profile paths and labels instead of silently dropping them "
        f"({pr(FLEET, 55097)}), and stopped batch software uploads after the first failure using a cancellable "
        f"<b>errgroup</b> context ({pr(FLEET, 53407)}).",
    ),
    row("<b>Superserve AI — Contributor (2 merged PRs)</b>",
        a("https://github.com/superserve-ai/superserve", "github.com/superserve-ai/superserve")),
    *bullets(f"Added <b>MCP</b> network-log pagination with cursor forwarding and regression tests ({pr(SUPERSERVE, 356)}), "
             f"and fixed a development watcher that deleted the HTTP build output ({pr(SUPERSERVE, 330)})."),
    row("<b>Vitest — Contributor</b>", a("https://github.com/vitest-dev/vitest", "github.com/vitest-dev/vitest")),
    *bullets(f"Opened a pull request adding <b>Temporal.Instant</b> and <b>Temporal.ZonedDateTime</b> support to "
             f"<b>vi.setSystemTime()</b> ({pr('vitest-dev/vitest', 11321)}, in review)."),

    *h("Projects"),
    row("<b>Drivly — P2P Vehicle-Sharing Platform</b>", a("https://drivly-mu.vercel.app/", "Live Link")),
    *bullets(
        "Built a peer-to-peer vehicle-sharing platform for residential communities with <b>Next.js</b>, "
        "<b>TypeScript</b>, <b>Tailwind CSS</b>, <b>Prisma ORM</b>, and <b>PostgreSQL</b>, including custom <b>JWT</b> "
        "authentication and multi-user booking workflows.",
        "Prevented double bookings by running conflict checks inside a <b>database transaction</b> with "
        "<b>row-level locking</b>, and calculated booking prices on the server from stored vehicle rates.",
    ),
    row("<b>Blood Donor App — MERN Stack</b>", a("https://donar-app-frontend.vercel.app/", "Live Link")),
    *bullets("Built <b>RESTful APIs</b> for authentication and donor management with <b>Node.js</b>, <b>Express.js</b>, "
             "and <b>MongoDB</b>, connected to a <b>React.js</b> frontend deployed on <b>Vercel</b>."),

    *h("Education"),
    row("B.E. in Information Technology, JSPM RSCOE - CGPA: 8.3", "2020 - 2024", indent=6),
]

SimpleDocTemplate(
    "dist/Prajwal_Janbandhu_Resume.pdf", pagesize=A4, leftMargin=16, rightMargin=24, topMargin=16, bottomMargin=14,
    title="Prajwal Janbandhu - Full Stack Developer", author="Prajwal Janbandhu",
    keywords="Full Stack Developer, Ruby on Rails, React, TypeScript, JavaScript, Node.js, Next.js, PostgreSQL, REST APIs",
).build(story)
