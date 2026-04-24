from fastapi import APIRouter
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from config.db_config import get_db_connection
from reportlab.lib import colors

router = APIRouter(prefix="/reporte", tags=["Reporte"])


@router.get("/eventos")
def generar_reporte(estado: str = None, fecha: str = None, modalidad: str = None):

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT nombre, fecha, hora, modalidad, estado
        FROM evento
        WHERE 1=1
    """

    params = []

    if estado:
        query += " AND estado = %s"
        params.append(estado)

    if fecha:
        query += " AND fecha = %s"
        params.append(fecha)

    if modalidad:
        query += " AND modalidad = %s"
        params.append(modalidad)

    cursor.execute(query, params)
    eventos = cursor.fetchall()

    cursor.close()
    conn.close()

    # CREAR PDF
    file_path = "reporte_eventos.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # 🔵 ENCABEZADO
    c.setFillColor(colors.blue)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(150, 750, "REPORTE DE EVENTOS CUL")

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)

    y = 700

    # 🔶 TITULOS
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Nombre")
    c.drawString(200, y, "Fecha")
    c.drawString(280, y, "Hora")
    c.drawString(350, y, "Modalidad")
    c.drawString(450, y, "Estado")

    y -= 20
    c.setFont("Helvetica", 10)

    # 🔽 DATOS
    for e in eventos:
        c.drawString(50, y, str(e[0]))
        c.drawString(200, y, str(e[1]))
        c.drawString(280, y, str(e[2]))
        c.drawString(350, y, str(e[3]))
        c.drawString(450, y, str(e[4]))

        y -= 20

        if y < 50:
            c.showPage()
            y = 750

    # 🔴 PIE DE PAGINA
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(180, 30, "Sistema de Gestión de Eventos - CUL")

    c.save()

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename="reporte_eventos.pdf"
    )