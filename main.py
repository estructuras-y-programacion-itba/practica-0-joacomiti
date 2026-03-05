#EJERCICIO GENERALA 

def main():
    print("Hola, generala!")
if __name__ == "__main__":
    main()
    
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

    # si el jugador no quiere re-tirar, termina
    for nro_tirada in range(2, 4):  # 2 y 3
        indices = pedir_indices_a_retirar()
        if len(indices) == 0:
            break
        dados = reroll(dados, indices)
        print(f"Tirada {nro_tirada}:", dados)

    return dados
