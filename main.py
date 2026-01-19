from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from pypdf import PdfWriter
from pypdf.errors import PdfReadError
import aiofiles

app = FastAPI(
    title="API para Unir PDFs",
    description="Sube archivos PDF en una sesión y únelos en un solo documento.",
    version="1.0.0"
)

# --- Configuración de CORS ---
# Esto permite que la documentación de Swagger UI y otras aplicaciones web
# que se ejecutan en diferentes dominios/IPs puedan llamar a tu API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)


UPLOAD_DIRECTORY = "/tmp/uploads"

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.get("/")
def read_root():
    return {"message": "API para unir PDFs está en funcionamiento."}

@app.post("/unir-pdfs/")
async def unir_pdfs(session_id: str = Form(...), is_last: bool = Form(...), file: UploadFile = File(...)):
    """
    Sube un archivo PDF. Si es el último archivo de una sesión, une todos los PDFs
    de esa sesión y devuelve el resultado.
    """
    session_dir = os.path.join(UPLOAD_DIRECTORY, session_id)
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)

    file_location = os.path.join(session_dir, file.filename)
    try:
        async with aiofiles.open(file_location, "wb") as f:
            while chunk := await file.read(1024 * 1024):  # Lee en chunks de 1MB
                await f.write(chunk)
    finally:
        await file.close()

    if not is_last:
        return {"message": f"Archivo '{file.filename}' subido a la sesión '{session_id}'. Esperando más archivos."}

    # --- Lógica de Unión ---
    merger = PdfWriter()
    
    # Obtener y ordenar archivos para mantener el orden de subida (asumiendo nombres de archivo que se puedan ordenar)
    try:
        pdf_files = sorted([f for f in os.listdir(session_dir) if f.lower().endswith(".pdf")])
        
        if not pdf_files:
            raise HTTPException(status_code=400, detail="No se encontraron archivos PDF en la sesión para unir.")

        for pdf_filename in pdf_files:
            file_path = os.path.join(session_dir, pdf_filename)
            try:
                merger.append(file_path)
            except PdfReadError as e:
                # Captura errores de pypdf para archivos corruptos o protegidos
                raise HTTPException(
                    status_code=400,
                    detail=f"No se pudo procesar el archivo '{pdf_filename}'. El archivo puede estar corrupto o tener una protección que impide la unión. Error original: {e}"
                )
            except Exception as e:
                # Captura cualquier otro error inesperado durante la unión
                raise HTTPException(
                    status_code=500,
                    detail=f"Ocurrió un error inesperado al procesar el archivo '{pdf_filename}': {e}"
                )

        output_filename = f"resultado_{session_id}.pdf"
        output_path = os.path.join(UPLOAD_DIRECTORY, output_filename)
        merger.write(output_path)
    finally:
        merger.close()

    # --- Limpieza ---
    try:
        shutil.rmtree(session_dir)
    except OSError as e:
        # Opcional: registrar el error si la limpieza falla
        print(f"Error limpiando el directorio {session_dir}: {e}")

    return FileResponse(
        path=output_path,
        media_type='application/pdf',
        filename=output_filename
    )
