#!/usr/bin/env python3
"""Planificador de rutas con la API de GraphHopper (version en espanol)."""

import urllib.parse
import requests

URL_GEOCODIFICACION = "https://graphhopper.com/api/1/geocode?"
URL_RUTA = "https://graphhopper.com/api/1/route?"
CLAVE = "PEGA_AQUI_TU_API_KEY"

SALIDAS = ("s", "salir")

TRANSPORTES = {
    "auto": "car",
    "bicicleta": "bike",
    "a pie": "foot",
}


def quiere_salir(texto):
    return texto.strip().lower() in SALIDAS


def geocodificar(lugar):
    url = URL_GEOCODIFICACION + urllib.parse.urlencode(
        {"q": lugar, "limit": "1", "locale": "es", "key": CLAVE}
    )
    respuesta = requests.get(url)
    if respuesta.status_code != 200:
        print(f"Error de geocodificacion (HTTP {respuesta.status_code}).")
        return None
    hits = respuesta.json().get("hits", [])
    if not hits:
        print(f"No se encontro la ubicacion: {lugar}")
        return None
    punto = hits[0]
    partes = [punto.get("name"), punto.get("state"), punto.get("country")]
    nombre = ", ".join(p for p in partes if p)
    return punto["point"]["lat"], punto["point"]["lng"], nombre


def formatear_tiempo(milisegundos):
    segundos = milisegundos / 1000
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    seg = int(segundos % 60)
    return f"{horas:02d}:{minutos:02d}:{seg:02d}"


def main():
    print("=" * 50)
    print("  Planificador de rutas - Biblioteca Nacional")
    print("  (escriba 's' o 'salir' en cualquier momento)")
    print("=" * 50)

    while True:
        print("\nMedios de transporte disponibles: auto, bicicleta, a pie")
        medio = input("Medio de transporte: ").strip().lower()
        if quiere_salir(medio):
            break
        if medio not in TRANSPORTES:
            print("Medio no valido, se usara 'auto'.")
            medio = "auto"
        vehiculo = TRANSPORTES[medio]

        origen = input("Ubicacion de origen: ")
        if quiere_salir(origen):
            break
        destino = input("Ubicacion de destino: ")
        if quiere_salir(destino):
            break

        punto_origen = geocodificar(origen)
        punto_destino = geocodificar(destino)
        if not punto_origen or not punto_destino:
            print("No fue posible calcular la ruta. Intente nuevamente.")
            continue

        parametros = urllib.parse.urlencode(
            {"key": CLAVE, "vehicle": vehiculo, "locale": "es"}
        )
        url = (
            f"{URL_RUTA}{parametros}"
            f"&point={punto_origen[0]},{punto_origen[1]}"
            f"&point={punto_destino[0]},{punto_destino[1]}"
        )
        respuesta = requests.get(url)
        datos = respuesta.json()

        if respuesta.status_code != 200:
            print(f"Error al calcular la ruta (HTTP {respuesta.status_code}): "
                  f"{datos.get('message', '')}")
            continue

        ruta = datos["paths"][0]
        km = ruta["distance"] / 1000
        millas = km / 1.61

        print("\n" + "=" * 50)
        print(f"Ruta desde {punto_origen[2]}")
        print(f"hasta {punto_destino[2]}")
        print(f"Medio de transporte: {medio}")
        print("=" * 50)
        print(f"Distancia recorrida: {km:.2f} km ({millas:.2f} millas)")
        print(f"Duracion del viaje: {formatear_tiempo(ruta['time'])}")
        print("=" * 50)
        print("Narrativa del viaje:")
        for paso in ruta["instructions"]:
            print(f"  - {paso['text']} ({paso['distance'] / 1000:.2f} km)")
        print("=" * 50)

    print("\nGracias por usar el planificador. Hasta luego.")


if __name__ == "__main__":
    main()