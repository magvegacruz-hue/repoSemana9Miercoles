import base64
import uuid
from pathlib import Path


class GestorFotos:
    def __init__(self, carpeta: str):
        self.carpeta = Path(carpeta)
        self.carpeta.mkdir(parents=True, exist_ok=True)

    def guardar_base64(self, imagen_base64: str) -> dict:
        if not imagen_base64:
            return {
                "exito": False,
                "mensaje": "No se recibió ninguna imagen."
            }

        try:
            if "," in imagen_base64:
                imagen_base64 = imagen_base64.split(",")[1]

            datos = base64.b64decode(imagen_base64, validate=True)

            if len(datos) == 0:
                return {
                    "exito": False,
                    "mensaje": "La imagen está vacía."
                }

            nombre = f"foto_{uuid.uuid4().hex}.jpg"
            ruta = self.carpeta / nombre

            with ruta.open("wb") as archivo:
                archivo.write(datos)

            return {
                "exito": True,
                "nombre": nombre,
                "mensaje": "Foto guardada correctamente."
            }

        except Exception:
            return {
                "exito": False,
                "mensaje": "No se pudo guardar la imagen."
            }

    def eliminar(self, nombre: str) -> None:
        ruta = self.carpeta / nombre

        if ruta.exists():
            ruta.unlink()