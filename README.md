# Guía Detallada: Despliegue desde GitHub a AWS App Runner

Esta guía te mostrará el método más directo para desplegar tu API: conectando tu repositorio de GitHub directamente a **AWS App Runner**. Con este enfoque, cada vez que hagas `git push`, tu API se actualizará automáticamente.

## ¿Por qué Desplegar desde GitHub?

Es el camino más rápido y sencillo. Te ahorras todos los pasos de construir y subir imágenes de Docker manualmente. AWS App Runner se encarga de leer tu código, instalar las dependencias (`requirements.txt`) y lanzar la aplicación basándose en la configuración que le proporcionemos en el archivo `apprunner.yaml`.

---

## Prerrequisitos

1.  **Una Cuenta de AWS:** Debes resolver el problema de activación o verificación de la cuenta para poder continuar.
2.  **Un Repositorio en GitHub:**
    -   Crea un nuevo repositorio en [GitHub](https://github.com/new).
    -   Sube todos los archivos de este proyecto (`main.py`, `requirements.txt`, `apprunner.yaml`, etc.) a ese repositorio.

---

## Paso 1: Subir tu Código a GitHub

Asegúrate de que la última versión de tu código, incluyendo el archivo `apprunner.yaml` restaurado, esté en tu repositorio de GitHub.

```bash
# Añade los cambios (el nuevo apprunner.yaml y la eliminación del Procfile)
git add .

# Haz un commit con los cambios para volver a la configuración de AWS
git commit -m "Reconfiguración para despliegue en AWS App Runner"

# Sube los cambios a GitHub
git push origin main
```

---

## Paso 2: Desplegar en AWS App Runner (Consola Web)

Una vez que tu cuenta de AWS esté completamente activa, sigue estos pasos.

1.  **Navega a App Runner:**
    -   Inicia sesión en la [Consola de AWS](https://aws.amazon.com/console/).
    -   En la barra de búsqueda superior, escribe `App Runner` y selecciona el servicio.

2.  **Crear un Servicio:**
    -   Haz clic en el botón naranja que dice **"Crear un servicio" (Create a service)**.

3.  **Sección 1: Fuente y Despliegue (Source and deployment)**
    -   Selecciona **"Source code repository"** (Repositorio de código fuente).
    -   **Conectar con GitHub:** Conecta tu cuenta de GitHub con AWS.
    -   Selecciona tu repositorio y la rama (`main`).
    -   **Configuración del Despliegue (Deployment settings):** Deja la opción **"Automatic"** (Automático).

4.  **Sección 2: Configuración de la Construcción (Configure build)**
    -   Selecciona **"Use a configuration file"** (Usar un archivo de configuración). App Runner detectará tu archivo `apprunner.yaml`.

5.  **Sección 3: Configuración del Servicio (Configure service)**
    -   **Nombre del servicio (Service name):** Escribe un nombre, por ejemplo: `api-unir-pdf-github`.

6.  **Sección 4: Revisar y Crear (Review and create)**
    -   Revisa la configuración y haz clic en **"Crear y desplegar" (Create & deploy)**.

---

## Paso 3: ¡Tu API está en línea!

-   Cuando el estado del servicio cambie a **`Running`**, tu API estará desplegada.
-   Busca el **"Dominio predeterminado" (Default domain)** en la página del servicio para obtener la URL pública de tu API.
