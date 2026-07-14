import os
import uuid
from datetime import datetime
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
from app.core.config import settings

class ReportGenerator:
    def __init__(self):
        self.output_dir = os.path.join(settings.UPLOAD_DIR, "reports")
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_pdf(self, scan_results: list, health_score: float, username: str = "Guest"):
        filename = f"report_{uuid.uuid4().hex[:8]}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        if not REPORTLAB_AVAILABLE:
            # Fallback for systems that cannot install reportlab (like Python 3.14)
            with open(filepath, 'w') as f:
                f.write("PDF Generation unavailable on this Python version without ReportLab.\n")
                f.write(f"Health Score: {health_score}\n")
            return f"/reports/{filename}"
        
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                                rightMargin=40, leftMargin=40,
                                topMargin=40, bottomMargin=18)
        
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        title_style.alignment = 1 # Center
        h2_style = styles['Heading2']
        normal_style = styles['Normal']
        
        elements = []
        
        # Header
        elements.append(Paragraph("FarmGuardian AI - Field Health Report", title_style))
        elements.append(Spacer(1, 12))
        
        # Meta Info
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elements.append(Paragraph(f"<b>Generated For:</b> {username}", normal_style))
        elements.append(Paragraph(f"<b>Date:</b> {date_str}", normal_style))
        elements.append(Spacer(1, 20))
        
        # Health Score
        score_color = colors.green if health_score >= 80 else colors.orange if health_score >= 50 else colors.red
        score_text = f"<font color='{score_color}'><b>Overall Field Health Score: {health_score:.1f}%</b></font>"
        elements.append(Paragraph(score_text, h2_style))
        elements.append(Spacer(1, 20))
        
        # Table of Scans
        elements.append(Paragraph("<b>Scan Details</b>", h2_style))
        data = [['Image #', 'Disease Detected', 'Confidence', 'Severity', 'Risk Level']]
        
        for i, scan in enumerate(scan_results, 1):
            data.append([
                str(i),
                scan.get('disease', 'Unknown'),
                f"{scan.get('confidence', 0)*100:.1f}%",
                scan.get('severity_level', 'N/A'),
                scan.get('risk_level', 'N/A')
            ])
            
        t = Table(data, colWidths=[60, 200, 80, 80, 80])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#16a34a')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8fafc')),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0'))
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 30))
        
        # Priority Actions
        elements.append(Paragraph("<b>Priority Actions Recommended</b>", h2_style))
        # Find the worst case for recommendations
        worst_scan = min(scan_results, key=lambda x: x.get('severity_score', 0)) if scan_results else None
        
        if worst_scan and 'recommendations' in worst_scan:
            recs = worst_scan['recommendations']
            if 'immediate_actions' in recs:
                elements.append(Paragraph("<b>Immediate Actions:</b>", normal_style))
                for action in recs['immediate_actions']:
                    elements.append(Paragraph(f"• {action}", normal_style))
                elements.append(Spacer(1, 10))
                
        doc.build(elements)
        
        # Return the public URL path
        return f"/reports/{filename}"

report_generator = ReportGenerator()
