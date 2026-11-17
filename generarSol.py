import cv2
import os


# ==========================================
# CONFIGURACIÓN
# ==========================================

def generarSol(s, cartas):

    IMAGE_PATH = s
    RESULT_PATH = "result.txt"
    OUTPUT_DIR = "sets"

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for archivo in os.listdir(OUTPUT_DIR):
        ruta = os.path.join(OUTPUT_DIR, archivo)

        if os.path.isfile(ruta):
            os.remove(ruta)
    
    # ==========================================
    # CARGAR FOTO ORIGINAL
    # ==========================================

    imagen_original = cv2.imread(
        IMAGE_PATH
    )

    if imagen_original is None:

        print(
            "No se ha podido cargar la imagen."
        )

        exit()


    # ==========================================
    # LEER RESULT.TXT
    # ==========================================

    with open(
        RESULT_PATH,
        "r"
    ) as f:

        numeros = list(
            map(
                int,
                f.read().split()
            )
        )


    # ==========================================
    # SEPARAR LOS SETS
    # ==========================================

    sets = []

    for i in range(
        0,
        len(numeros),
        3
    ):

        set_actual = numeros[
            i:i + 3
        ]

        # Comprobar que realmente
        # tenemos 3 cartas

        if len(set_actual) == 3:

            sets.append(
                set_actual
            )


    # ==========================================
    # GENERAR UNA FOTO POR SET
    # ==========================================

    for numero_set, set_actual in enumerate(
        sets,
        start=1
    ):

        # Copia de la imagen original

        imagen = imagen_original.copy()


        # ======================================
        # PINTAR LAS 3 CARTAS
        # ======================================

        for numero_carta in set_actual:

            # set.exe utiliza 1..12
            # Python utiliza 0..11

            indice = numero_carta - 1


            if (
                indice < 0
                or
                indice >= len(cartas)
            ):

                print(
                    "Carta inválida:",
                    numero_carta
                )

                continue


            x, y, w, h = cartas[indice]


            # ==================================
            # RECTÁNGULO
            # ==================================
            color = (255, 0, 0)

            cv2.rectangle(
                imagen,
                (x, y),
                (x + w, y + h),
                color,
                5
            )


            # ==================================
            # NÚMERO DE CARTA
            # ==================================

            cv2.putText(
                imagen,
                str(numero_carta),
                (x + 10, y + 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                color,
                3
            )


        # ======================================
        # GUARDAR
        # ======================================

        output_path = os.path.join(
            OUTPUT_DIR,
            f"set_{numero_set}.jpg"
        )


        cv2.imwrite(
            output_path,
            imagen
        )


        print(
            f"Set {numero_set}: "
            f"{set_actual} -> {output_path}"
        )