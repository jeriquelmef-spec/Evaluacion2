# Evaluacion2 - Geolocalización con GraphHopper

## Descripción
Script en Python que usa la API de GraphHopper Directions para calcular rutas entre dos ubicaciones. Muestra la distancia y la duración del viaje (máximo 2 decimales) y la narrativa paso a paso, todo en español. Desarrollado para la Evaluación 2 de CUY6142.

## Requisitos
- Python 3
- Librería requests (`pip3 install requests`)
- Una API key de GraphHopper (https://www.graphhopper.com/)

## Cómo ejecutar
1. Abrir `graphhopper_es.py` y reemplazar `PEGA_AQUI_TU_API_KEY` por su API key.
2. Ejecutar en la terminal: `python3 graphhopper_es.py`
3. Ingresar el medio de transporte (auto, bicicleta o a pie), el origen y el destino.
4. Para salir del programa escribir `s` o `salir`.
