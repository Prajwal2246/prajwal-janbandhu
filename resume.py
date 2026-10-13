"""Build dist/Prajwal_Janbandhu_Resume.pdf. Run: uv run --with reportlab python resume.py

ATS rules kept here on purpose: single column, standard section headings,
real text (no images/tables), "•" bullets in an embedded TTF (built-in
Helvetica bullets extract as "(cid:127)"), and every URL written out in full.
"""
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

# Embedded TTF so every glyph (incl. bullets) has a Unicode mapping. ponytail: macOS font paths.
FONTS = "/System/Library/Fonts/Supplemental/"
pdfmetrics.registerFont(TTFont("Arial", FONTS + "Arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", FONTS + "Arial Bold.ttf"))
pdfmetrics.registerFont(TTFont("CourierNew", FONTS + "Courier New.ttf"))
addMapping("Arial", 0, 0, "Arial")
addMapping("Arial", 1, 0, "Arial-Bold")

INK, MUTED, LINK = HexColor("#1b2230"), HexColor("#4a5160"), HexColor("#1f4e8c")
base = ParagraphStyle("base", fontName="Arial", fontSize=9.7, leading=12.6, textColor=INK)
name = ParagraphStyle("name", base, fontName="Arial-Bold", fontSize=21, leading=25, alignment=TA_CENTER)
center = ParagraphStyle("center", base, alignment=TA_CENTER, textColor=MUTED, fontSize=9.4)
heading = ParagraphStyle("heading", base, fontName="Arial-Bold", fontSize=11, leading=14, spaceBefore=8, spaceAfter=3)
bullet = ParagraphStyle("bullet", base, leftIndent=11, firstLineIndent=-8, spaceAfter=1)
right = ParagraphStyle("right", base, alignment=2, textColor=MUTED)


def a(url, text=None):
    return f'<a href="{url}" color="#1f4e8c">{text or url.removeprefix("https://").removeprefix("mailto:")}</a>'


def row(left, when=""):
    if not when:
        return Paragraph(f"<b>{left}</b>", ParagraphStyle("sub", base, spaceBefore=2, spaceAfter=1))
    t = Table([[Paragraph(f"<b>{left}</b>", base), Paragraph(when, right)]], colWidths=["72%", "28%"])
    t.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
    return t


def bullets(*items):
    return [Paragraph(f"•&nbsp;&nbsp;{i}", bullet) for i in items]


def h(text):
    return Paragraph(text.upper(), heading)


GH = "https://github.com/Prajwal2246"
PR = lambda repo, n: a(f"https://github.com/{repo}/pull/{n}", f"#{n}")

story = [
    Paragraph("Prajwal Janbandhu", name),
    Paragraph("Full Stack Developer | Ruby on Rails, React, TypeScript, PostgreSQL", center),
    Paragraph("Navi Mumbai, India | Open to remote roles | +91 9511933274 | " + a("mailto:prajwal3274@gmail.com"), center),
    Paragraph(" | ".join([a(GH), a("https://linkedin.com/in/prajwaljanbandhu"), a("https://prajwal-janbandhu.vercel.app")]), center),

    h("Summary"),
    Paragraph(
        "Full Stack Developer at Envision Next LLP building an enterprise CRM with Ruby on Rails, React, and PostgreSQL. "
        "Experienced in REST API development, third-party API integrations, approval workflows, and database-backed web "
        "applications. Open-source contributor with 9 merged pull requests to Fleet (Go, TypeScript, React) and "
        "Superserve (TypeScript, MCP).", base),

    h("Skills"),
    Paragraph("<b>Languages:</b> JavaScript, TypeScript, Ruby, SQL, Go, HTML, CSS", base),
    Paragraph("<b>Frontend:</b> React, Next.js, Tailwind CSS, Framer Motion", base),
    Paragraph("<b>Backend:</b> Ruby on Rails, Node.js, Express.js, REST APIs, JWT Authentication, WebRTC", base),
    Paragraph("<b>Databases:</b> PostgreSQL, MongoDB, Prisma ORM, Firebase Firestore", base),
    Paragraph("<b>Tools:</b> Git, GitHub, Vercel, Claude Code", base),

    h("Experience"),
    row("Associate Full Stack Developer | Envision Next LLP", "Apr 2026 - Present"),
    *bullets(
        "Develop and maintain an enterprise CRM used by 200+ employees, covering incentives, HRMS, compliance, and automation modules.",
        "Owned end-to-end development of the Incentive module: Ruby on Rails APIs, PostgreSQL schema changes, calculation logic, "
        "employee and manager dashboards, approval workflows, filters, and exports.",
        "Built MahaRERA API integrations and Excel-driven automation for 1,000+ projects, implementing authentication, "
        "response processing, error handling, and project-information updates.",
    ),
    row("Development Intern | Tejas", "May 2025 - Oct 2025"),
    *bullets(
        "Built WebRTC signaling with Firebase Firestore for one-to-one video mentoring sessions, establishing peer-to-peer "
        "connections between students and tutors.",
        "Implemented real-time question and tutor-dashboard updates with Firestore onSnapshot listeners in React, and added "
        "UI transitions with Framer Motion.",
    ),

    h("Open-Source Contributions"),
    row(f"Fleet (open-source device management) | 7 merged PRs | {a('https://github.com/fleetdm/fleet', 'github.com/fleetdm/fleet')}"),
    *bullets(
        f"Made <font face='CourierNew'>fleetctl apply</font> reject incorrectly typed profile paths and labels instead of silently "
        f"dropping them and reporting success (Go) {PR('fleetdm/fleet', 55097)}.",
        f"Stopped batch software uploads after the first package failure using a cancellable errgroup context (Go) "
        f"{PR('fleetdm/fleet', 53407)}.",
        f"Fixed return navigation from live reports and policies, script-package identification and search, script timeout "
        f"messages, locked-host tooltips, and policy permissions for Observer+ (React, TypeScript) "
        f"{PR('fleetdm/fleet', 54411)} {PR('fleetdm/fleet', 53810)} {PR('fleetdm/fleet', 54296)} "
        f"{PR('fleetdm/fleet', 54509)} {PR('fleetdm/fleet', 54726)}.",
    ),
    row(f"Superserve (sandbox infrastructure for AI agents) | 2 merged PRs | {a('https://github.com/superserve-ai/superserve', 'github.com/superserve-ai/superserve')}"),
    *bullets(
        f"Added MCP network-log pagination with cursor forwarding and regression tests (TypeScript) {PR('superserve-ai/superserve', 356)}; "
        f"fixed development-watcher output deletion {PR('superserve-ai/superserve', 330)}.",
    ),

    h("Projects"),
    row(f"Drivly | Vehicle-Sharing Platform | {a('https://drivly-mu.vercel.app')}"),
    *bullets(
        "Built a peer-to-peer vehicle-sharing web application with Next.js, TypeScript, Tailwind CSS, Prisma, and PostgreSQL, "
        "including JWT authentication and multi-user booking workflows.",
        "Prevented double bookings with conflict checks inside a database transaction using row-level locking, and calculated "
        "booking prices on the server from stored vehicle rates.",
    ),
    row(f"Blood Donor App | MERN Stack | {a('https://donar-app-frontend.vercel.app')}"),
    *bullets("Built donor-management and authentication REST APIs with Node.js, Express.js, and MongoDB, connected to a React "
             "frontend deployed on Vercel."),

    h("Education"),
    row("B.E. in Information Technology | JSPM's RSCOE, Pune", "2020 - 2024"),
    Paragraph("CGPA: 8.3 / 10", base),
]

doc = SimpleDocTemplate(
    "dist/Prajwal_Janbandhu_Resume.pdf", pagesize=A4, leftMargin=40, rightMargin=40, topMargin=28, bottomMargin=24,
    title="Prajwal Janbandhu - Full Stack Developer Resume", author="Prajwal Janbandhu", subject="Resume",
    keywords="Full Stack Developer, Ruby on Rails, React, TypeScript, JavaScript, PostgreSQL, Node.js, Next.js, Go, REST APIs",
)
doc.build(story)
