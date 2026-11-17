import subprocess
import detectarColor
import detectarNumForma
import detectarInterior
import detectarCartes
import generarSol

def solver(image):

    TABLERO = image

    cartes = detectarCartes.detectarCartes(TABLERO)
    print(cartes)

    color = []
    relleno = []
    forma = []
    cantidad = []

    for i in range(12):
        color.append(detectarColor.detectarColor(i+1))
        aux = detectarNumForma.detectarNumForma(i+1)
        cantidad.append(aux[0])
        forma.append(aux[1])
        relleno.append(detectarInterior.detectarInterior(i+1))

    with open("cartes.txt", "w") as f:

        for i in range(12):

            carta = f"{color},{relleno},{forma},{cantidad}"

            f.write(color[i])
            f.write(",")
            f.write(relleno[i])
            f.write(",")
            f.write(forma[i])
            f.write(",")
            f.write(str(cantidad[i]))

            f.write(" ")

        f.write("0")

    with open("cartes.txt", "r") as entrada:
        with open("result.txt", "w") as salida:

            subprocess.run(
                ["set.exe"],
                stdin=entrada,
                stdout=salida,
                text=True
            )

    generarSol.generarSol(TABLERO, cartes)