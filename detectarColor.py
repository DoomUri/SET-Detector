import cv2
import numpy as np


def detectarColor(i):

    IMAGE_PATH = f"cartas/card_{i:02d}.jpg"

    # ==========================================
    # CARREGAR IMATGE
    # ==========================================

    img = cv2.imread(IMAGE_PATH)

    if img is None:
        print("No s'ha pogut carregar la carta.")
        return None


    # ==========================================
    # HSV
    # ==========================================

    hsv = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2HSV
    )

    H = hsv[:, :, 0]
    S = hsv[:, :, 1]
    V = hsv[:, :, 2]


    # ==========================================
    # DETECTAR CONTORNS
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


    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )


    # ==========================================
    # MÀSCARA DE LES FIGURES
    # ==========================================

    figures_mask = np.zeros(
        gray.shape,
        dtype=np.uint8
    )


    # ==========================================
    # CLASSIFICAR CONTORNS
    # ==========================================

    for contour in contours:

        area = cv2.contourArea(contour)

        if area < 300:
            continue


        x, y, w, h = cv2.boundingRect(
            contour
        )

        if w < 20 or h < 20:
            continue


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

        extent = area / (w * h)


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
        # SI ÉS UNA FIGURA VÀLIDA
        # ======================================

        if forma is not None:

            cv2.drawContours(
                figures_mask,
                [contour],
                -1,
                255,
                -1
            )


    # ==========================================
    # COMPTAR COLORS NOMÉS DINS LES FIGURES
    # ==========================================

    vermell = 0
    verd = 0
    lila = 0


    # Recorrem només els píxels que pertanyen
    # a alguna figura vàlida

    for y in range(img.shape[0]):

        for x in range(img.shape[1]):

            # Fora de les figures → ignorar

            if figures_mask[y, x] == 0:
                continue


            h = H[y, x]
            s = S[y, x]
            v = V[y, x]


            # ==================================
            # IGNORAR BLANC / GRIS / NEGRE
            # ==================================

            if s < 60:
                continue

            if v < 40:
                continue


            # ==================================
            # VERMELL
            # ==================================

            if (
                (h <= 10 or h >= 170)
                and s > 80
                and v > 50
            ):
                vermell += 1


            # ==================================
            # VERD
            # ==================================

            elif (
                35 <= h <= 90
                and s > 80
                and v > 50
            ):
                verd += 1


            # ==================================
            # LILA
            # ==================================

            elif (
                110 <= h <= 160
                and s > 80
                and v > 50
            ):
                lila += 1


    # print(vermell)
    # print(lila)
    #print(verd)
    # ==========================================
    # RESULTAT
    # ==========================================

    if vermell > verd and vermell > lila:

        color = "vermell"

    elif verd > vermell and verd > lila:

        color = "verd"

    else:

        color = "lila"


    return color