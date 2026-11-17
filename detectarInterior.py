import cv2
import numpy as np
import math


# ==========================================
# CARGAR CARTA
# ==========================================

def detectarInterior(i):
        
    img = cv2.imread(
        f"cartas/card_{i:02d}.jpg"
    )

    if img is None:
        print("No se ha podido cargar la imagen")
        exit()


    # ==========================================
    # PREPROCESADO
    # ==========================================

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    binary = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        31,
        7
    )


    # ==========================================
    # CONTORNOS
    # ==========================================

    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )


    figures = []


    # ==========================================
    # CLASIFICAR CONTORNOS
    # ==========================================

    for contour in contours:

        area = cv2.contourArea(contour)

        if area < 300:
            continue

        x, y, w, h = cv2.boundingRect(contour)

        if w < 20 or h < 20:
            continue

        perimeter = cv2.arcLength(
            contour,
            True
        )

        if perimeter == 0:
            continue

        circularity = (
            4 * np.pi * area
            / (perimeter * perimeter)
        )

        extent = area / (w * h)


        forma = None


        # ROMBE

        if (
            0.45 < circularity < 0.55
            and
            0.45 < extent < 0.55
        ):

            forma = "rombe"


        # SERP

        elif (
            0.5 < circularity < 0.6
            and
            0.65 < extent < 0.8
        ):

            forma = "serp"


        # OVAL

        elif (
            0.72 < circularity < 0.82
            and
            0.83 < extent < 0.93
        ):

            forma = "oval"


        if forma is not None:

            figures.append({
                "contour": contour,
                "forma": forma,
                "x": x,
                "y": y,
                "w": w,
                "h": h
            })


    # ==========================================
    # ORDENAR
    # ==========================================

    figures.sort(
        key=lambda f: (
            f["y"],
            f["x"]
        )
    )


    # ==========================================
    # ANALIZAR RELLENO
    # ==========================================

    for i, figure in enumerate(figures):

        contour = figure["contour"]

        x = figure["x"]
        y = figure["y"]
        w = figure["w"]
        h = figure["h"]


        # ======================================
        # MÁSCARA LOCAL
        # ======================================

        mask = np.zeros(
            (h, w),
            dtype=np.uint8
        )

        local_contour = contour.copy()

        local_contour[:, :, 0] -= x
        local_contour[:, :, 1] -= y

        cv2.drawContours(
            mask,
            [local_contour],
            -1,
            255,
            -1
        )


        # ======================================
        # ELIMINAR EL CONTORNO
        # ======================================
        #
        # Aquí está la corrección importante.
        #
        # No queremos que Hough vea el borde
        # exterior de la figura.
        #

        margin = max(
            5,
            int(min(w, h) * 0.20)
        )

        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE,
            (
                margin * 2 + 1,
                margin * 2 + 1
            )
        )

        interior_mask = cv2.erode(
            mask,
            kernel
        )


        # ======================================
        # CANNY SOLO INTERIOR
        # ======================================

        roi = gray[
            y:y+h,
            x:x+w
        ]

        edges = cv2.Canny(
            roi,
            40,
            120
        )

        edges = cv2.bitwise_and(
            edges,
            edges,
            mask=interior_mask
        )


        # ======================================
        # HOUGH
        # ======================================

        min_dimension = min(w, h)

        lines = cv2.HoughLinesP(
            edges,
            1,
            np.pi / 180,
            threshold=5,
            minLineLength=max(
                4,
                int(min_dimension * 0.06)
            ),
            maxLineGap=5
        )


        # ======================================
        # FILTRAR LÍNEAS
        # ======================================

        valid_lines = []


        if lines is not None:

            for line in lines:

                x1, y1, x2, y2 = line

                dx = x2 - x1
                dy = y2 - y1

                length = math.sqrt(
                    dx * dx +
                    dy * dy
                )

                if length < min_dimension * 0.10:
                    continue


                angle = math.degrees(
                    math.atan2(dy, dx)
                )

                if angle < 0:
                    angle += 180


                # ==================================
                # SOLO LÍNEAS DIAGONALES
                # ==================================

                if (
                    25 < angle < 65
                    or
                    115 < angle < 155
                ):

                    valid_lines.append(
                        (x1, y1, x2, y2, angle, length)
                    )


        # ======================================
        # COMPROBAR SI LAS LÍNEAS SON PARALELAS
        # ======================================

        ratlles = False


        if len(valid_lines) >= 2:

            angles = [
                line[4]
                for line in valid_lines
            ]


            for angle in angles:

                similares = 0

                for other in angles:

                    diferencia = abs(
                        angle - other
                    )

                    diferencia = min(
                        diferencia,
                        180 - diferencia
                    )

                    if diferencia < 10:
                        similares += 1


                if similares >= 3:

                    ratlles = True
                    break


        # ======================================
        # CLASIFICAR
        # ======================================

        if ratlles:

            relleno = "ratllat"

        else:

            # ==================================
            # BUIT / OPAC
            # ==================================

            pixels = roi[
                interior_mask > 0
            ]


            if len(pixels) == 0:

                relleno = "buit"

            else:

                media = np.mean(pixels)


                if media > 180:

                    relleno = "buit"

                else:

                    relleno = "opac"


        # ======================================
        # RESULTADO
        # ======================================

    return relleno