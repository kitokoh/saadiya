from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_report(downloads, mentions):
    c = canvas.Canvas("performance_report.pdf", pagesize=letter)
    c.drawString(100, 750, "Performance Report")
    c.drawString(100, 730, f"Total Downloads: {downloads}")
    c.drawString(100, 710, "Mentions:")
    for i, mention in enumerate(mentions, start=1):
        c.drawString(100, 710 - (i * 20), mention)
    c.save()

# Exécutez avec les données de suivi que vous avez obtenues
create_report(1200, ["@user1: Great software!", "@user2: Using it daily!"])
print("Rapport PDF généré.")
