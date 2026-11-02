# Proyecto de Ingeniería Económica · Grupo 13

Aplicación web de la Universidad Agraria del Ecuador, hecha con **FastAPI + HTML + CSS + JavaScript**. Incluye los **8 ejercicios originales** del archivo `U1 S3 Taller 3 EduardoGuzman6sc.xlsx`, sus resultados de referencia, campos editables, procedimientos y enlace para descargar el Excel.

## Cómo actualizar el proyecto que ya tienes

1. **Detén** el servidor en VS Code con `Ctrl + C`.
2. Descomprime este ZIP.
3. En `D:\desarrollo\Proyecto_Economia`, **reemplaza `main.py` y las carpetas `templates` y `static`** con los contenidos del ZIP. Conserva tu carpeta `.venv` actual (no está incluida en el ZIP).
4. Opcionalmente copia `requirements.txt`, `.gitignore` y `render.yaml` a la carpeta principal para desplegar después.
5. En la terminal de VS Code, desde `D:\desarrollo\Proyecto_Economia` con tu entorno `.venv` activado:

   ```powershell
   python -m pip install -r requirements.txt
   python -m uvicorn main:app --reload --port 8000
   ```

6. Abre **http://127.0.0.1:8000/** y presiona Ctrl + F5. La documentación de las APIs está en **http://127.0.0.1:8000/docs**.

Si la terminal no muestra `(.venv)`, activa el entorno virtual desde la carpeta del proyecto con `\.venv\Scripts\Activate.ps1`. Si PowerShell bloquea el script, para esa sesión puedes ejecutar `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`.

> No copies ningún archivo dentro de `.venv`. Toda la aplicación va en la carpeta principal del proyecto.

## Distribución de los ejercicios

| Tema | Ejercicios | Resultados originales del Excel |
|---|---|---|
| Interés simple | 1, 2 y 3 | 15 % anual; 2 años; $1.435,41 |
| Fecha focal | 4, 5 y 6 | $31.726,96; $16.125,90; $1.517,75 |
| Descuento simple | 7 | Descuento $7.000,00; líquido $23.000,00 |
| Tasa equivalente | 8 | 45,6522 % anual |

Los ejercicios 4 y 5 conservan los **días consignados en Excel** (base comercial de 360 días) en vez de recalcular automáticamente las diferencias entre fechas. Si se cambian los días, el enunciado y las fechas de referencia siguen siendo los del taller original.

El ejercicio 8 conserva cuatro entradas, incluida la tasa de descuento. Si se cambian los importes y esa tasa de manera que dejan de ser consistentes, la aplicación muestra un aviso y presenta ambos resultados para que se detecte la diferencia.

## API y organización

- `main.py`: FastAPI, ocho endpoints POST `/api/ejercicios/1` a `/api/ejercicios/8` y una prueba GET antigua del ejercicio 1.
- `templates/index.html`: página principal con menú, teoría y secciones de los temas.
- `static/style.css`: diseño verde institucional adaptado a celular.
- `static/script.js`: formularios y presentación de resultados sin recargar la página.
- `static/img/agraria-banner.png`: imagen institucional que compartiste.
- `static/archivos/Taller_3_Grupo13.xlsx`: copia original del taller para descarga desde la web.
- `tests/test_ejercicios.py`: pruebas de resultados contra el Excel.
- `render.yaml`: configuración opcional para desplegar en Render.

## Subir gratuitamente a Render desde GitHub

1. Crea un repositorio en GitHub y sube todos los archivos del proyecto **excepto `.venv` y `__pycache__`** (la `.gitignore` ya los excluye).
2. Ve a [Render](https://render.com/) y crea un nuevo **Web Service** conectado al repositorio.
3. Selecciona el plan **Free** cuando esté disponible, runtime **Python** y usa:
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Render generará una URL pública HTTPS.

**Advertencia**: el servicio web gratuito puede suspenderse tras 15 minutos sin visitas y tarda en reanudarse. El sistema es de **lectura y cálculo**: no incluye una cuenta de administración ni carga de archivos por los visitantes. El Excel está incluido directamente en el proyecto y seguirá publicado tras los reinicios.

## Pruebas

Con FastAPI y `httpx` instalados:

```powershell
python -m unittest discover -s tests -v
```

Se verifican los ocho resultados principales y las validaciones más importantes.
