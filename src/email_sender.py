"""Send formatted newsletter via Gmail SMTP."""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.arxiv_client import ArxivPaper


def _format_paper_html(paper: ArxivPaper, reason: str) -> str:
    return (
        f'<li style="margin-bottom:12px;">'
        f'<a href="{paper.pdf_url}" style="font-weight:bold;color:#1a0dab;">{paper.title}</a><br>'
        f'<span style="color:#666;font-size:0.9em;">Relevance: {reason}</span>'
        f'</li>'
    )


def _build_html(
    grouped_papers: dict[str, list[ArxivPaper]],
    scores: dict[str, dict],
    sections: dict[str, str],
    date_str: str,
) -> str:
    total = sum(len(ps) for ps in grouped_papers.values())
    parts = [
        f"<h2>Paper Newsletter — {date_str}</h2>",
        f"<p>{total} relevant papers across {len(grouped_papers)} categories</p>",
    ]

    for category, papers in grouped_papers.items():
        emoji = sections.get(category, "📄")
        parts.append(f"<h3>{emoji} {category} ({len(papers)})</h3>")
        parts.append("<ul>")
        for paper in papers:
            reason = scores.get(paper.arxiv_id, {}).get("reason", "")
            parts.append(_format_paper_html(paper, reason))
        parts.append("</ul>")

    return "\n".join(parts)


def send_email(
    email_to: str,
    app_password: str,
    grouped_papers: dict[str, list[ArxivPaper]],
    scores: dict[str, dict],
    sections: dict[str, str],
    date_str: str,
) -> None:
    total = sum(len(ps) for ps in grouped_papers.values())
    html = _build_html(grouped_papers, scores, sections, date_str)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Paper Newsletter — {date_str} ({total} papers)"
    msg["From"] = email_to
    msg["To"] = email_to
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_to, app_password)
        server.sendmail(email_to, email_to, msg.as_string())
