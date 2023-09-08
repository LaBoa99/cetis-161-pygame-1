# Variables
"""
    Las variables no necesitan un tipo y 
    siempre se le pueden asignar cualquier tipo de dato
"""
variable = 1        # Enteros
variable = "Hola"   # Strings
variable = 1.0      # Punto Flotante
variable = []       # Arrays / Listas
variable = {}       # Diccionarios
variable = None     # Null o vacio
variable = True     # Verdadero
variable = False    # Falso

# Operadores Aritmeticos
# Estos funcionan siempre y cuando la variable tenga asignado un numero
variable = 1
variableB = -2
variable -= 1 # variable = variable - 1
variable += 1 # variable = variable + 1
variable /= 1 # variable = variable / 1
variable *= 1 # variable = variable * 1

variable = 2 * variableB
variable = 0.5 + 1
variable = (300 - 20) / 10
variable = 10 // 3 # Elimina la parte decimal y retorna un numero entero

# Saludos
persona = "Gael"
saludo = "Hola, "
final = "!"
print(saludo, persona, final)

import random 

numeroAadivinar = random.randint(1, 10)
numeroEntrada = input("dame un numero del 1 al 10: ")
if numeroEntrada == numeroAadivinar:
    print("ganaste")
else:
    print("perdiste")