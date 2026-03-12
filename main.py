#EJERCICIO GENERALA     
import random

def tirar_dados(cantidad_dados):
    dados= []
    for i in range(cantidad_dados):
        dado=random.randint(1,6)
        dados.append(dado)
    return dados

def jugada(dados):
    
    contadores = [0,0,0,0,0,0]

    # contar cuantas veces aparece cada dado
    for dado in dados:
        contadores[dado-1] += 1

    # GENERALA
    for c in contadores:
        if c == 5:
            return "Generala"

    # POKER
    for c in contadores:
        if c == 4:
            return "Poker"

    # FULL
    hay_tres = False
    hay_dos = False

    for c in contadores:
        if c == 3:
            hay_tres = True
        if c == 2:
            hay_dos = True

    if hay_tres and hay_dos:
        return "Full"

    # ESCALERA
    dados_ordenados = sorted(dados)

    if dados_ordenados == [1,2,3,4,5] or dados_ordenados == [2,3,4,5,6]:
        return "Escalera"

    return "Nada"
    
def puntaje_numero(dados, numero):
    
    suma = 0

    for dado in dados:
        if dado == numero:
            suma += dado

    return suma

def reroll(dados, indices):
    nuevos = dados[:]  # copia
    for i in indices:
        nuevos[i] = random.randint(1, 6)
    return nuevos

def pedir_indices_a_retirar():
    
    while True:

        s = input("Qué dados querés volver a tirar? (1-5 separados por espacio, Enter=ninguno): ").strip()

        if s == "":
            return []

        partes = s.split()

        # verificar que todos sean numeros
        for p in partes:
            if not p.isdigit():
                print("Error: solo se permiten números.")
                break
        else:
            numeros = []
            for p in partes:
                k = int(p)

                if not (1 <= k <= 5):
                    print("Error: los números deben estar entre 1 y 5.")
                    break

                if k in numeros:
                    print("Error: no puede haber números repetidos.")
                    break

                numeros.append(k)

            else:
                # convertir a índices de python
                indices = []
                for k in numeros:
                    indices.append(k - 1)

                return indices


def turno():
    dados = tirar_dados(5)
    print("Tirada 1:", dados)

    resultado_primera_tirada = jugada(dados)

    if resultado_primera_tirada == "Generala":
        return dados, 1, True, resultado_primera_tirada

    nro_tirada_final = 1

    for nro_tirada in range(2, 4):
        indices = pedir_indices_a_retirar()

        if len(indices) == 0:
            break

        dados = reroll(dados, indices)
        print(f"Tirada {nro_tirada}:", dados)

        nro_tirada_final = nro_tirada

    return dados, nro_tirada_final, False, resultado_primera_tirada

CATEGORIAS = ["E","F","P","G","1","2","3","4","5","6"]
def crear_planilla():
    planilla = {}
    for c in CATEGORIAS:
        planilla[c] = None
    return planilla

def categorias_disponibles(planilla):
    disp = []
    for c in planilla:
        if planilla[c] is None:
            disp.append(c)
    return disp

def pedir_categoria(planilla):
    disp = categorias_disponibles(planilla)
    print("Categorías disponibles:", disp)

    while True:
        c = input("Elegí categoría: ").upper()
        if c in disp:
            return c
        print("Categoría inválida o ya usada.")
        
def calcular_puntaje(dados, categoria, nro_tirada_final, resultado_primera_tirada):
    
    if categoria in ["1","2","3","4","5","6"]:
        return puntaje_numero(dados, int(categoria))

    resultado = jugada(dados)

    if categoria == "E" and resultado == "Escalera":
        if nro_tirada_final == 1 and resultado_primera_tirada == "Escalera":
            return 25
        return 20

    if categoria == "F" and resultado == "Full":
        if nro_tirada_final == 1 and resultado_primera_tirada == "Full":
            return 35
        return 30

    if categoria == "P" and resultado == "Poker":
        if nro_tirada_final == 1 and resultado_primera_tirada == "Poker":
            return 45
        return 40

    if categoria == "G" and resultado == "Generala":
        return 50

    return 0
        
def anotar_puntaje(planilla, categoria, puntos):
    planilla[categoria] = puntos
    

def turno_jugador(planilla, nombre):
    print("\nTurno de", nombre)

    dados, nro_tirada_final, generala_real, resultado_primera_tirada = turno()
    print("Dados finales:", dados)
    print("Terminó en la tirada:", nro_tirada_final)

    resultado = jugada(dados)
    print("Jugada obtenida:", resultado)

    if generala_real:
        anotar_puntaje(planilla, "G", 80)
        print("GENERALA REAL")
        print(nombre, "gana automáticamente")
        print("Planilla actual:", planilla)
        return True

    categoria = pedir_categoria(planilla)
    puntos = calcular_puntaje(dados, categoria, nro_tirada_final, resultado_primera_tirada)

    anotar_puntaje(planilla, categoria, puntos)

    print("Se anotaron", puntos, "puntos en la categoría", categoria)
    print("Planilla actual:", planilla)
    return False
    
def planilla_completa(planilla): #RECORRE LA PLANILLA Y SE FIJA SI ESTA COMPLETA O NO
    for categoria in planilla:
        if planilla[categoria] is None:
            return False
    return True

def total_puntos(planilla):
    total = 0
    for categoria in planilla:
        total += planilla[categoria]
    return total

def guardar_csv(planilla_j1, planilla_j2):
    with open("jugadas.csv", "w") as archivo:

        archivo.write("jugada,j1,j2\n")

        for c in CATEGORIAS:
            p1 = planilla_j1[c]
            p2 = planilla_j2[c]

            if p1 is None:
                p1 = 0
            if p2 is None:
                p2 = 0

            linea = c + "," + str(p1) + "," + str(p2) + "\n"
            archivo.write(linea)
def main():
    planilla_j1 = crear_planilla()
    planilla_j2 = crear_planilla()
    guardar_csv(planilla_j1, planilla_j2)
    while not (planilla_completa(planilla_j1) and planilla_completa(planilla_j2)):

        if not planilla_completa(planilla_j1):
            generala_real = turno_jugador(planilla_j1, "Jugador 1")
            guardar_csv(planilla_j1, planilla_j2)
            if generala_real:
                print("\n--- FIN DEL JUEGO ---")
                print("Ganó Jugador 1 por GENERALA REAL")
                return

        if not planilla_completa(planilla_j2):
            generala_real = turno_jugador(planilla_j2, "Jugador 2")
            guardar_csv(planilla_j1, planilla_j2)
            if generala_real:
                print("\n--- FIN DEL JUEGO ---")
                print("Ganó Jugador 2 por GENERALA REAL")
                return

    total_j1 = total_puntos(planilla_j1)
    total_j2 = total_puntos(planilla_j2)

    print("\n--- FIN DEL JUEGO ---")
    print("Puntaje total Jugador 1:", total_j1)
    print("Puntaje total Jugador 2:", total_j2)

    if total_j1 > total_j2:
        print("Ganó Jugador 1")
    elif total_j2 > total_j1:
        print("Ganó Jugador 2")
    else:
        print("Empate")
        
        
if __name__ == "__main__":
    main()