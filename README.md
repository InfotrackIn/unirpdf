# Guía Detallada: Despliegue desde GitHub a AWS App Runner

Esta guía te mostrará el método más directo para desplegar tu API: conectando tu repositorio de GitHub directamente a **AWS App Runner**. Con este enfoque, cada vez que hagas `git push`, tu API se actualizará automáticamente.

## ¿Por qué Desplegar desde GitHub?

Es el camino más rápido y sencillo. Te ahorras todos los pasos de construir y subir imágenes de Docker manualmente. AWS App Runner se encarga de leer tu código, instalar las dependencias (`requirements.txt`) y lanzar la aplicación basándose en la configuración que le proporcionemos en el archivo `apprunner.yaml`.

---

## Prerrequisitos

1.  **Una Cuenta de AWS:** Si no tienes una, puedes crearla [aquí](https://aws.amazon.com/free/).
2.  **Un Repositorio en GitHub:**
    -   Crea un nuevo repositorio en [GitHub](https://github.com/new).
    -   Sube todos los archivos de este proyecto (`main.py`, `requirements.txt`, `apprunner.yaml`, etc.) a ese repositorio.

---

## Paso 1: Subir tu Código a GitHub

Asegúrate de que la última versión de tu código, incluyendo el archivo `apprunner.yaml` que hemos creado, esté en tu repositorio de GitHub. Los comandos básicos son:

```bash
# Inicia un repositorio de Git (si no lo has hecho)
git init

# Añade todos los archivos
git add .

# Haz tu primer commit
git commit -m "Versión inicial para despliegue en App Runner"

# Conecta tu repositorio local con el de GitHub
git remote add origin TU_URL_DE_GITHUB.git

# Sube el código a la rama principal (main)
git push -u origin main
```
*   Reemplaza `TU_URL_DE_GITHUB.git` por la URL de tu repositorio (ej: `https://github.com/tu-usuario/api-unir-pdf.git`).

---

## Paso 2: Desplegar en AWS App Runner (Consola Web)

Ahora viene la parte fácil. Vamos a conectar AWS con tu repositorio.

1.  **Navega a App Runner:**
    -   Inicia sesión en la [Consola de AWS](https://aws.amazon.com/console/).
    -   En la barra de búsqueda superior, escribe `App Runner` y selecciona el servicio.

2.  **Crear un Servicio:**
    -   Haz clic en el botón naranja que dice **"Crear un servicio" (Create a service)**.

3.  **Sección 1: Fuente y Despliegue (Source and deployment)**
    -   Selecciona **"Source code repository"** (Repositorio de código fuente).
    -   **Conectar con GitHub:** Si es la primera vez, haz clic en **"Add new"** (Añadir nuevo) en la sección de conexión. Se abrirá una ventana para que autorices a AWS a acceder a tus repositorios de GitHub. Puedes darle acceso a todos o solo al que acabas de crear.
    -   Una vez conectado, selecciona tu repositorio (ej. `tu-usuario/api-unir-pdf`) y la rama (`main`).
    -   **Configuración del Despliegue (Deployment settings):** Deja la opción **"Automatic"** (Automático). Esto hará que App Runner se redespliegue cada vez que hagas un `push` a la rama `main`.
    -   Haz clic en **"Siguiente" (Next)**.

4.  **Sección 2: Configuración de la Construcción (Configure build)**
    -   Selecciona **"Use a configuration file"** (Usar un archivo de configuración).
    -   App Runner detectará automáticamente tu archivo `apprunner.yaml`. No necesitas cambiar nada aquí. Este archivo le dice a AWS exactamente cómo instalar las dependencias y ejecutar tu API.
    -   Haz clic en **"Siguiente" (Next)**.

5.  **Sección 3: Configuración del Servicio (Configure service)**
    -   **Nombre del servicio (Service name):** Escribe un nombre, por ejemplo: `api-unir-pdf-github`.
    -   **Configuración de CPU y memoria:** Puedes dejar los valores por defecto (1 vCPU, 2 GB).
    -   **Puerto (Port):** App Runner leerá el puerto `8080` directamente desde nuestro archivo `apprunner.yaml`, por lo que no necesitas escribirlo aquí.
    -   Haz clic en **"Siguiente" (Next)**.

6.  **Sección 4: Revisar y Crear (Review and create)**
    -   Revisa que toda la configuración sea correcta.
    -   Haz clic en el botón naranja **"Crear y desplegar" (Create & deploy)**.

---

## Paso 3: ¡Tu API está en línea!

El proceso de despliegue tardará unos minutos. App Runner primero descargará tu código de GitHub, luego seguirá las instrucciones de `apprunner.yaml` para construir y finalmente lanzar tu servicio.

-   Cuando el estado del servicio cambie a **`Running` (En ejecución)**, ¡tu API estará desplegada!
-   En la página de tu servicio, encontrarás el **"Dominio predeterminado" (Default domain)**. Esa es la URL pública de tu API.

Ahora, cada vez que quieras actualizar tu API, solo tienes que hacer `git push` en tu repositorio, y AWS App Runner se encargará del resto. ¡Mucho más fácil!
