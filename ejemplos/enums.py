from enum import Enum


class TIPOS_COCHE(Enum):
    STANDAR = 1
    AUTOMATICO = 2


class DIAS_SEMANA(Enum):
    LUNES = "lunes"
    MARTES = "martes"
    MIERCOLES = "miercoles"
    JUEVES = "jueves"
    VIERNES = "viernes"
    SABADO = "sabado"
    DOMINGO = "domingo"


class Coche:
    def __init__(self, tipo, dia_compra) -> None:
        self.tipo = tipo
        self.dia_compra = dia_compra


# Esto es codigo limpio y es mas entendible que
coche1 = Coche(TIPOS_COCHE.STANDAR, DIAS_SEMANA.LUNES)
# aqui pueden existir multiples errores puesto que lunes se puede escrbir de distintas formas
coche2 = Coche(1, "lunes")

print(coche1.tipo.value, coche2.tipo)
print(coche1.dia_compra.value, coche2.dia_compra)

# Enum puede funcioanr como un identificardor no siempre puede retornace el valor
# Por ejemplo
COCHES = {DIAS_SEMANA.LUNES: [coche1, coche2]}
print(COCHES)
print(COCHES[DIAS_SEMANA.LUNES])
