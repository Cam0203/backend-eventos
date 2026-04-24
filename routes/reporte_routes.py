from fastapi import APIRouter
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from config.db_config import get_db_connection

router = APIRouter(prefix="/reporte", tags=["Reporte"])


@router.get("/eventos")
def generar_reporte(
    estado: str = None,
    fecha: str = None,
    modalidad: str = None,
    cupo_max: int = None
):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT nombre, fecha, hora, modalidad, estado, cupo_max
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

    if cupo_max:
        query += " AND cupo_max = %s"
        params.append(cupo_max)

    query += " ORDER BY fecha ASC"

    cursor.execute(query, params)
    eventos = cursor.fetchall()

    cursor.close()
    conn.close()

    file_path = "reporte_eventos.pdf"

    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # Encabezado
    c.setFillColor(colors.HexColor("#0b2c5f"))
    c.rect(0, height - 80, width, 80, fill=True, stroke=False)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(170, height - 45, "REPORTE DE EVENTOS CUL")

    c.setFont("Helvetica", 9)
    c.drawString(50, height - 65, "Sistema de Gestión de Eventos Académicos")

    # Filtros usados
    y = height - 110

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Filtros aplicados:")

    y -= 18
    c.setFont("Helvetica", 9)

    filtros = [
        f"Estado: {estado if estado else 'Todos'}",
        f"Fecha: {fecha if fecha else 'Todas'}",
        f"Modalidad: {modalidad if modalidad else 'Todas'}",
        f"Cupo máximo: {cupo_max if cupo_max else 'Todos'}"
    ]

    for filtro in filtros:
        c.drawString(50, y, filtro)
        y -= 14

    y -= 10

    # Encabezado tabla
    c.setFillColor(colors.HexColor("#f59e0b"))
    c.rect(40, y - 5, 530, 22, fill=True, stroke=False)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(45, y, "Nombre")
    c.drawString(185, y, "Fecha")
    c.drawString(250, y, "Hora")
    c.drawString(310, y, "Modalidad")
    c.drawString(390, y, "Estado")
    c.drawString(470, y, "Cupo")

    y -= 25
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.black)

    if not eventos:
        c.drawString(50, y, "No se encontraron eventos con los filtros seleccionados.")
    else:
        for e in eventos:
            if y < 60:
                c.showPage()
                y = height - 70

                c.setFillColor(colors.HexColor("#f59e0b"))
                c.rect(40, y - 5, 530, 22, fill=True, stroke=False)

                c.setFillColor(colors.white)
                c.setFont("Helvetica-Bold", 9)
                c.drawString(45, y, "Nombre")
                c.drawString(185, y, "Fecha")
                c.drawString(250, y, "Hora")
                c.drawString(310, y, "Modalidad")
                c.drawString(390, y, "Estado")
                c.drawString(470, y, "Cupo")

                y -= 25
                c.setFont("Helvetica", 8)
                c.setFillColor(colors.black)

            c.drawString(45, y, str(e[0])[:28])
            c.drawString(185, y, str(e[1]))
            c.drawString(250, y, str(e[2]))
            c.drawString(310, y, str(e[3]))
            c.drawString(390, y, str(e[4]))
            c.drawString(470, y, str(e[5]))

            y -= 18

    # Pie de página
    c.setFillColor(colors.HexColor("#0b2c5f"))
    c.rect(0, 0, width, 35, fill=True, stroke=False)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(190, 15, "Sistema de Gestión de Eventos - Universidad CUL")

    c.save()

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename="reporte_eventos.pdf"
    )