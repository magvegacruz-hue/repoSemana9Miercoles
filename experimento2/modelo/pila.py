class Pila:
    def __init__(self, capacidad: int):
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")

        self.capacidad = capacidad
        self.elementos: list[str] = []

    def esta_vacia(self) -> bool:
        return len(self.elementos) == 0

    def esta_llena(self) -> bool:
        return len(self.elementos) == self.capacidad

    def apilar(self, elemento: str) -> dict:
        if self.esta_llena():
            return {
                "exito": False,
                "mensaje": "La pila está llena."
            }

        self.elementos.append(elemento)

        return {
            "exito": True,
            "mensaje": f"Foto apilada: {elemento}"
        }

    def desapilar(self) -> dict:
        if self.esta_vacia():
            return {
                "exito": False,
                "mensaje": "La pila está vacía."
            }

        elemento = self.elementos.pop()

        return {
            "exito": True,
            "mensaje": f"Foto desapilada: {elemento}",
            "elemento": elemento
        }

    def ver_tope(self) -> dict:
        if self.esta_vacia():
            return {
                "exito": False,
                "mensaje": "La pila está vacía."
            }

        return {
            "exito": True,
            "elemento": self.elementos[-1]
        }

    def mostrar(self) -> list[str]:
        return list(reversed(self.elementos))