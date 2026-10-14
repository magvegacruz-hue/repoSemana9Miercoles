class Pila:
    def __init__(self, capacidad: int):
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")
        self.capacidad = capacidad
        self.elementos: list = []

    def esta_vacia(self) -> bool:
        return len(self.elementos) == 0

    def esta_llena(self) -> bool:
        return len(self.elementos) == self.capacidad

    def apilar(self, item) -> dict:
        if self.esta_llena():
            return {"exito": False, "mensaje": "La pila está llena."}
        self.elementos.append(item)
        return {"exito": True, "mensaje": f"Elemento '{item}' apilado."}

    def desapilar(self) -> dict:
        if self.esta_vacia():
            return {"exito": False, "mensaje": "La pila está vacía."}
        item = self.elementos.pop()
        return {"exito": True, "mensaje": f"Elemento '{item}' desapilado."}

    def ver_tope(self) -> dict:
        if self.esta_vacia():
            return {"exito": False, "mensaje": "La pila está vacía."}
        return {"exito": True, "tope": self.elementos[-1]}

    def mostrar(self) -> list:
        return list(reversed(self.elementos))