"""Build dist/Prajwal_Janbandhu_Resume.pdf. Run: uv run --with reportlab python resume.py

ATS rules kept here on purpose: single column, standard section headings,
real text (no images), and "•" bullets in an embedded TTF (built-in
Helvetica bullets extract as "(cid:127)").
"""
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle

# Arial matches Helvetica's metrics and embeds a Unicode map. ponytail: macOS font paths.
FONTS = "/System/Library/Fonts/Supplemental/"
pdfmetrics.registerFont(TTFont("Arial", FONTS + "Arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", FONTS + "Arial Bold.ttf"))
addMapping("Arial", 0, 0, "Arial")
addMapping("Arial", 1, 0, "Arial-Bold")

INK, MUTED, LINK = HexColor("#172033"), HexColor("#455164"), "#164e79"
body = ParagraphStyle("body", fontName="Arial", fontSize=9.4, leading=12.5, textColor=INK, leftIndent=6)
name = ParagraphStyle("name", body, fontName="Arial-Bold", fontSize=21, leading=26, alignment=TA_CENTER, leftIndent=0)
contact = ParagraphStyle("contact", body, fontSize=9, leading=13, alignment=TA_CENTER, textColor=MUTED, leftIndent=0)
heading = ParagraphStyle("heading", body, fontName="Arial-Bold", fontSize=10.2, leading=13, spaceBefore=9, spaceAfter=5)
bullet = ParagraphStyle("bullet", body, leftIndent=16, firstLineIndent=-7, spaceAfter=3)
sub = ParagraphStyle("sub", body, fontName="Arial-Bold", spaceAfter=3)
row_l = ParagraphStyle("row_l", body, fontName="Arial-Bold", fontSize=9.6, leftIndent=0)
row_r = ParagraphStyle("row_r", body, fontSize=9.1, textColor=MUTED, alignment=TA_RIGHT, leftIndent=0)


def a(url, text):
    return f'<a href="{url}" color="{LINK}">{text}</a>'


def pr(repo, n):
    return a(f"https://github.com/{repo}/pull/{n}", f"PR #{n}")


def h(text):
    return Paragraph(text, heading)


def row(left, when):
    t = Table([[Paragraph(left, row_l), Paragraph(when, row_r)]], colWidths=[380, None])
    t.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return t


def bullets(*items):
    return [Paragraph(f"•&nbsp;{i}", bullet) for i in items]


def project(title, *links):
    return Paragraph(f"{title}&nbsp;&nbsp;&nbsp;<font name='Arial'>{' | '.join(links)}</font>", sub)


FLEET, SUPERSERVE = "fleetdm/fleet", "superserve-ai/superserve"

story = [
    Paragraph("Prajwal Janbandhu", name),
    Paragraph("Navi Mumbai, India | Open to remote roles", contact),
    Paragraph(" | ".join([
        a("mailto:prajwal3274@gmail.com", "prajwal3274@gmail.com"), "+91 9511933274",
        a("https://github.com/Prajwal2246", "github.com/Prajwal2246"),
        a("https://linkedin.com/in/prajwaljanbandhu/", "linkedin.com/in/prajwaljanbandhu"),
    ]), contact),

    h("SUMMARY"),
    Paragraph(
        "Full Stack Developer at Envision Next LLP, building CRM features with Ruby on Rails, React, and PostgreSQL. "
        "Experience with REST API integrations, approval workflows, and database-backed applications, with 9 merged "
        "open-source pull requests to Fleet and Superserve.", body),

    h("SKILLS"),
    Paragraph("<b>Languages:</b> JavaScript, TypeScript, Ruby, SQL, Go", body),
    Paragraph("<b>Frontend:</b> React, Next.js, Tailwind CSS, Framer Motion", body),
    Paragraph("<b>Backend:</b> Ruby on Rails, Node.js, Express, REST APIs, JWT", body),
    Paragraph("<b>Data and tools:</b> PostgreSQL, MongoDB, Prisma, Firebase, Git, Claude Code", body),

    h("EXPERIENCE"),
    row("Envision Next LLP | Associate Full Stack Developer", "Apr 2026 - Present"),
    *bullets(
        "Develop and maintain an enterprise CRM used by 200+ employees, including incentives, HRMS, compliance, and "
        "automation features.",
        "Owned end-to-end development of the Incentive module: Rails APIs, database changes, calculation logic, employee "
        "and manager dashboards, approval workflows, filters, and exports.",
        "Built MahaRERA API integrations and Excel-driven automation for 1,000+ projects, implementing authentication, "
        "response processing, error handling, and project-information updates.",
    ),
    row("Tejas | Development Intern", "May 2025 - Oct 2025"),
    *bullets(
        "Built WebRTC signaling with Firestore for one-to-one video mentoring sessions, establishing peer-to-peer "
        "connections between students and tutors.",
        "Implemented real-time question and tutor-dashboard updates using Firestore onSnapshot listeners, and added UI "
        "transitions with Framer Motion.",
    ),

    h("SELECTED OPEN-SOURCE CONTRIBUTIONS"),
    *bullets(
        f"<b>Fleet - merged:</b> Made fleetctl apply reject incorrectly typed profile paths and labels ({pr(FLEET, 55097)}) "
        f"and stopped batch software uploads after the first failure ({pr(FLEET, 53407)}) in Go.",
        f"<b>Fleet - merged:</b> Fixed return navigation from live reports ({pr(FLEET, 54411)}), script-package search "
        f"({pr(FLEET, 53810)}), script timeout messages ({pr(FLEET, 54296)}), locked-host tooltips ({pr(FLEET, 54509)}), "
        f"and Observer+ policy runs ({pr(FLEET, 54726)}) in React and TypeScript.",
        f"<b>Superserve - merged:</b> Added MCP network-log pagination with cursor forwarding and regression tests "
        f"({pr(SUPERSERVE, 356)}); fixed development-watcher output deletion ({pr(SUPERSERVE, 330)}).",
    ),

    h("PROJECTS"),
    project("Drivly | Vehicle-sharing platform",
            a("https://drivly-mu.vercel.app/", "Live demo"), a("https://github.com/Prajwal2246/Drivly", "Source")),
    *bullets(
        "Built a peer-to-peer vehicle-sharing application with Next.js, TypeScript, Tailwind CSS, Prisma, and PostgreSQL, "
        "including JWT authentication and multi-user booking workflows.",
        "Implemented booking-conflict checks in a database transaction with vehicle-row locking, and calculated booking "
        "prices on the server from stored vehicle rates.",
    ),
    project("Blood Donor App | MERN", a("https://donar-app-frontend.vercel.app/", "Live demo")),
    *bullets("Built donor-management and authentication REST APIs with Node.js, Express, and MongoDB; connected a React "
             "frontend deployed on Vercel."),

    h("EDUCATION"),
    row("JSPM RSCOE | B.E. in Information Technology", "2020 - 2024"),
    Paragraph("CGPA: 8.3", body),
]

SimpleDocTemplate(
    "dist/Prajwal_Janbandhu_Resume.pdf", pagesize=A4, leftMargin=30, rightMargin=30, topMargin=28, bottomMargin=30,
    title="Prajwal Janbandhu - Full Stack Developer", author="Prajwal Janbandhu",
    keywords="Full Stack Developer, Ruby on Rails, React, TypeScript, JavaScript, PostgreSQL, Node.js, Next.js, REST APIs",
).build(story)
