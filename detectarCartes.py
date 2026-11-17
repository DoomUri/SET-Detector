import cv2
import numpy as np
import os



OUTPUT_DIR = "cartas"

MIN_AREA = 5000
MIN_RATIO = 1.15
MAX_RATIO = 2.00

ROWS = 3
COLS = 4

def detectarCartes(s):

    return_cards = []
    # ==========================================
    # CARGAR
    # ==========================================
    img = cv2.imread(s)

    if img is None:
        print("No se ha podido cargar la imagen")
        exit()

    height, width = img.shape[:2]


    # ==========================================
    # DETECCIÓN NORMAL
    # ==========================================

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(blur, 50, 150)

    # small = cv2.resize(edges, (1200, 1200))
    # cv2.imshow(
    #     "Grid",
    #     small
    # )

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    print("Number of Contours Found = " + str(len(contours)))

    candidates = []

    for contour in contours:

        area = cv2.contourArea(contour)

        if area < MIN_AREA:
            continue

        x, y, w, h = cv2.boundingRect(contour)

        ratio = h / w

        if ratio < MIN_RATIO or ratio > MAX_RATIO:
            continue

        candidates.append({
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "cx": x + w / 2,
            "cy": y + h / 2,
            "area": area
        })


    print("Candidatos encontrados:", len(candidates))


    # ==========================================
    # CASO NORMAL
    # ==========================================

    if len(candidates) == 12:

        print("Se han detectado las 12 cartas.")

        # Ordenar por Y
        candidates.sort(key=lambda c: c["cy"])

        # Calcular altura típica
        median_height = np.median(
            [c["h"] for c in candidates]
        )

        tolerance = median_height * 0.5

        rows = []

        for card in candidates:

            added = False

            for row in rows:

                row_y = np.mean(
                    [c["cy"] for c in row]
                )

                if abs(card["cy"] - row_y) < tolerance:
                    row.append(card)
                    added = True
                    break

            if not added:
                rows.append([card])

        # Ordenar filas
        rows.sort(
            key=lambda row: np.mean(
                [c["cy"] for c in row]
            )
        )

        # Ordenar columnas
        for row in rows:
            row.sort(key=lambda c: c["cx"])


        # Aplanar
        ordered_cards = []

        for row in rows:
            ordered_cards.extend(row)


        # ======================================
        # GUARDAR
        # ======================================

        os.makedirs(OUTPUT_DIR, exist_ok=True)

        for i, card in enumerate(ordered_cards):

            x = int(card["x"])
            y = int(card["y"])
            w = int(card["w"])
            h = int(card["h"])

            return_cards.append((x, y, w, h))
            
            cropped = img[y:y+h, x:x+w]

            filename = os.path.join(
                OUTPUT_DIR,
                f"card_{i+1:02d}.jpg"
            )

            cv2.imwrite(filename, cropped)

            print("Guardada:", filename)


    # ==========================================
    # PLAN B: RECONSTRUIR CUADRÍCULA 3x4
    # ==========================================

    else:

        print("No se han detectado 12 cartas.")
        print("Activando reconstrucción por cuadrícula...")

        if len(candidates) < 6:
            print("Demasiadas pocas cartas detectadas.")
            exit()


        # ======================================
        # 1. TAMAÑO TÍPICO DE UNA CARTA
        # ======================================

        card_width = np.median(
            [c["w"] for c in candidates]
        )

        card_height = np.median(
            [c["h"] for c in candidates]
        )


        # ======================================
        # 2. AGRUPAR CENTROS X EN 4 COLUMNAS
        # ======================================

        x_values = sorted(
            [c["cx"] for c in candidates]
        )

        x_tolerance = card_width * 0.5

        x_groups = []

        for x in x_values:

            added = False

            for group in x_groups:

                group_center = np.mean(group)

                if abs(x - group_center) < x_tolerance:

                    group.append(x)
                    added = True
                    break

            if not added:
                x_groups.append([x])


        # ======================================
        # 3. SI HAY MÁS DE 4 GRUPOS,
        #    QUEDARNOS CON LOS 4 MÁS GRANDES
        # ======================================

        if len(x_groups) > COLS:

            x_groups.sort(
                key=lambda g: len(g),
                reverse=True
            )

            x_groups = x_groups[:COLS]


        # Ordenar izquierda -> derecha
        x_groups.sort(
            key=lambda g: np.mean(g)
        )


        if len(x_groups) != COLS:

            print(
                "No se han podido determinar las 4 columnas."
            )
            print(
                "Columnas encontradas:",
                len(x_groups)
            )
            exit()


        column_centers = [
            np.mean(group)
            for group in x_groups
        ]


        # ======================================
        # 4. AGRUPAR CENTROS Y EN 3 FILAS
        # ======================================

        y_values = sorted(
            [c["cy"] for c in candidates]
        )

        y_tolerance = card_height * 0.5

        y_groups = []

        for y in y_values:

            added = False

            for group in y_groups:

                group_center = np.mean(group)

                if abs(y - group_center) < y_tolerance:

                    group.append(y)
                    added = True
                    break

            if not added:
                y_groups.append([y])


        # ======================================
        # 5. QUEDARNOS CON LAS 3 FILAS
        # ======================================

        if len(y_groups) > ROWS:

            y_groups.sort(
                key=lambda g: len(g),
                reverse=True
            )

            y_groups = y_groups[:ROWS]


        # Ordenar arriba -> abajo
        y_groups.sort(
            key=lambda g: np.mean(g)
        )


        if len(y_groups) != ROWS:

            print(
                "No se han podido determinar las 3 filas."
            )
            print(
                "Filas encontradas:",
                len(y_groups)
            )
            exit()


        row_centers = [
            np.mean(group)
            for group in y_groups
        ]


        # ======================================
        # 6. CREAR LAS 12 POSICIONES
        # ======================================

        grid = [
            [None for _ in range(COLS)]
            for _ in range(ROWS)
        ]


        # Para cada candidato buscamos la posición
        # de la cuadrícula más cercana.

        for card in candidates:

            distances = []

            for r in range(ROWS):

                for c in range(COLS):

                    dx = card["cx"] - column_centers[c]
                    dy = card["cy"] - row_centers[r]

                    distance = np.sqrt(
                        dx * dx + dy * dy
                    )

                    distances.append(
                        (distance, r, c)
                    )


            # Posición más cercana
            distances.sort(
                key=lambda x: x[0]
            )

            distance, r, c = distances[0]


            # Si ya hay una carta en esa posición,
            # nos quedamos con la más cercana.

            if grid[r][c] is None:

                grid[r][c] = card

            else:

                old_card = grid[r][c]

                old_dx = old_card["cx"] - column_centers[c]
                old_dy = old_card["cy"] - row_centers[r]

                old_distance = np.sqrt(
                    old_dx * old_dx +
                    old_dy * old_dy
                )

                if distance < old_distance:

                    grid[r][c] = card


        # ======================================
        # 7. MOSTRAR LA CUADRÍCULA
        # ======================================

        print("\nCuadrícula detectada:")

        for r in range(ROWS):

            line = []

            for c in range(COLS):

                if grid[r][c] is None:
                    line.append("X")
                else:
                    line.append("O")

            print(" ".join(line))


        # ======================================
        # 8. GUARDAR LAS 12 CARTAS
        # ======================================

        os.makedirs(
            OUTPUT_DIR,
            exist_ok=True
        )


        result = img.copy()

        number = 1
        
        for r in range(ROWS):

            for c in range(COLS):

                card = grid[r][c]


                # ==================================
                # CARTA DETECTADA
                # ==================================

                if card is not None:

                    x = int(card["x"])
                    y = int(card["y"])
                    w = int(card["w"])
                    h = int(card["h"])

                    detected = True


                # ==================================
                # CARTA NO DETECTADA
                # ==================================

                else:

                    print(
                        f"Carta {number} "
                        f"no detectada → reconstruida"
                    )

                    cx = column_centers[c]
                    cy = row_centers[r]

                    x = int(
                        cx - card_width / 2
                    )

                    y = int(
                        cy - card_height / 2
                    )

                    w = int(card_width)
                    h = int(card_height)

                    detected = False


                # ==================================
                # LIMITAR AL TAMAÑO DE LA IMAGEN
                # ==================================

                x1 = max(0, x)
                y1 = max(0, y)

                x2 = min(
                    width,
                    x + w
                )

                y2 = min(
                    height,
                    y + h
                )


                # ==================================
                # RECORTAR
                # ==================================

                cropped = img[
                    y1:y2,
                    x1:x2
                ]

                return_cards.append((x, y, w, h))
                # ==================================
                # GUARDAR
                # ==================================

                filename = os.path.join(
                    OUTPUT_DIR,
                    f"card_{number:02d}.jpg"
                )

                cv2.imwrite(
                    filename,
                    cropped
                )


                # ==================================
                # DIBUJAR
                # ==================================

                if detected:

                    cv2.rectangle(
                        result,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        3
                    )

                else:

                    cv2.rectangle(
                        result,
                        (x1, y1),
                        (x2, y2),
                        (0, 0, 255),
                        3
                    )


                cv2.putText(
                    result,
                    str(number),
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )


                number += 1


        # ======================================
        # MOSTRAR
        # ======================================
        # small = cv2.resize(result, (1200, 1200))
        # cv2.imshow(
        #     "Grid",
        #     small
        # )
        
        

        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return return_cards