import cv2
import numpy as np


# ==========================================
# ESCOLLIR CARTA
# ==========================================

def detectarNumForma(i):

    path = f"cartas/card_{i:02d}.jpg"


    # ==========================================
    # CARREGAR IMATGE
    # ==========================================

    img = cv2.imread(path)

    if img is None:
        print("No s'ha pogut carregar la imatge.")
        exit()


    # ==========================================
    # ESCALA DE GRISOS
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


    # ==========================================
    # THRESHOLD
    # ==========================================

    binary = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        31,
        7
    )


    # ==========================================
    # MORPH OPEN
    # ==========================================

    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (3, 3)
    )

    binary = cv2.morphologyEx(
        binary,
        cv2.MORPH_OPEN,
        kernel
    )


    # ==========================================
    # DETECTAR CONTORNS
    # ==========================================

    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    print("Number of Contours Found = " + str(len(contours)))


    figures = []


    # ==========================================
    # ANALITZAR CONTORNS
    # ==========================================

    for contour in contours:

        # --------------------------------------
        # ÀREA
        # --------------------------------------

        area = cv2.contourArea(contour)

        if area < 300:
            continue


        # --------------------------------------
        # BOUNDING BOX
        # --------------------------------------

        x, y, w, h = cv2.boundingRect(
            contour
        )

        if w < 20 or h < 20:
            continue

        if w > img.shape[1] * 0.8:
            continue

        if h > img.shape[0] * 0.8:
            continue


        # --------------------------------------
        # PERÍMETRE
        # --------------------------------------

        perimeter = cv2.arcLength(
            contour,
            True
        )

        if perimeter == 0:
            continue


        # ======================================
        # CIRCULARITAT
        # ======================================

        circularity = (
            4 * np.pi * area
            / (perimeter * perimeter)
        )


        # ======================================
        # EXTENT
        # ======================================

        extent = (
            area / (w * h)
        )


        # ======================================
        # CLASSIFICAR FORMA
        # ======================================

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


        # ======================================
        # GUARDAR NOMÉS FIGURES VÀLIDES
        # ======================================

        if forma is not None:

            figures.append({
                "contour": contour,
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "circularity": circularity,
                "extent": extent,
                "forma": forma
            })


    # ==========================================
    # ORDENAR
    # ==========================================

    figures.sort(
        key=lambda f: f["y"]
    )


    # ==========================================
    # RESULTAT
    # ==========================================

    # ==========================================
    # DIBUIXAR RESULTAT
    # ==========================================

    result = img.copy()


    for i, figure in enumerate(figures):

        contour = figure["contour"]

        x = figure["x"]
        y = figure["y"]
        w = figure["w"]
        h = figure["h"]

        forma = figure["forma"]


        # Contorn

        cv2.drawContours(
            result,
            [contour],
            -1,
            (0, 255, 0),
            2
        )


        # Text

        text = f"{i + 1}: {forma}"

        cv2.putText(
            result,
            text,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 0),
            2
        )


    # ==========================================
    # MOSTRAR
    # ==========================================

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return [len(figures), forma]