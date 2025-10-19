from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_rfq_pdf(rfq):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 80

    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width / 2, y, "Request for Quotation (RFQ)")
    y -= 40

    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"RFQ Number: {rfq.id}")
    y -= 20
    p.drawString(50, y, f"Title: {rfq.title}")
    y -= 20
    p.drawString(50, y, f"Description: {rfq.description}")
    y -= 40

    if rfq.user:
        p.drawString(50, y, f"Created by: {rfq.user.full_name} ({rfq.user.email})")
        y -= 20
        p.drawString(50, y, f"Phone: {rfq.user.phone}")
        y -= 20

    p.drawString(50, y, f"Due Date: {rfq.due_date}")
    y -= 20
    p.drawString(50, y, f"Status: {rfq.status}")
    y -= 20
    p.drawString(50, y, f"Estimated Cost: ${rfq.estimated_cost}")
    y -= 40

    if hasattr(rfq, "subcontractor") and rfq.subcontractor:
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Subcontractor Information")
        y -= 20
        p.setFont("Helvetica", 12)
        p.drawString(50, y, f"Name: {rfq.subcontractor.name}")
        y -= 20
        p.drawString(50, y, f"Contact: {rfq.subcontractor.contact_person}")
        y -= 20
        p.drawString(50, y, f"Phone: {rfq.subcontractor.phone}")
        y -= 20
        p.drawString(50, y, f"Email: {rfq.subcontractor.email}")
        y -= 20
        p.drawString(50, y, f"Address: {rfq.subcontractor.address}")

    p.showPage()
    p.save()
    buffer.seek(0)

    return buffer
