from config.db_config import get_db_connection
from psycopg2.extras import RealDictCursor


def verificar_usuario(correo, contraseña):

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT 
            u.id,
            u.primer_nombre,
            u.primer_apellido,
            u.id_rol,
            p.nombre AS programa
        FROM usuario u
        LEFT JOIN programa p ON u.id_programa = p.id
        WHERE u.correo_institucional = %s
        AND u.contraseña = %s;
    """, (correo, contraseña))

    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    return usuario