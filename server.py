from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
import shutil
import os

from main import solver


app = FastAPI()


# Carpeta donde guardaremos las fotos recibidas
os.makedirs("uploads", exist_ok=True)

# Carpeta donde tu programa genera los sets
os.makedirs("sets", exist_ok=True)


# Permite acceder a las imágenes desde Flutter
app.mount(
    "/sets",
    StaticFiles(directory="sets"),
    name="sets"
)


@app.post("/resolver")
async def resolver_endpoint(
    foto: UploadFile = File(...)
):

    # ==========================================
    # GUARDAR FOTO RECIBIDA
    # ==========================================

    ruta_foto = os.path.join(
        "uploads",
        "input.jpg"
    )

    with open(ruta_foto, "wb") as f:

        shutil.copyfileobj(
            foto.file,
            f
        )


    # ==========================================
    # EJECUTAR TU PROGRAMA
    # ==========================================

    solver(ruta_foto)


    # ==========================================
    # BUSCAR LOS SETS GENERADOS
    # ==========================================

    archivos = []

    for archivo in os.listdir("sets"):

        if archivo.lower().endswith(
            (".jpg", ".jpeg", ".png")
        ):

            archivos.append(
                archivo
            )


    archivos.sort()


    # ==========================================
    # DEVOLVER RESULTADO
    # ==========================================

    return {
        "sets": [
            f"/sets/{archivo}"
            for archivo in archivos
        ]
    }