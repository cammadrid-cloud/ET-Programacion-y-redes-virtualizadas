
# viaje_api.py
import requests

API_KEY = "TU_API_KEY" # Reemplaza con tu clave de Graphhopper

def obtener_coordenadas(ciudad, pais):
    # Obtiene latitud y longitud de la ciudad
    url = f"https://graphhopper.com/api/1/geocode?q={ciudad},{pais}&locale=es&key={API_KEY}"
    response = requests.get(url).json()
    if response.get('hits'):
        lat = response['hits'][0]['point']['lat']
        lng = response['hits'][0]['point']['lng']
        return lat, lng
    return None

def calcular_ruta():
    while True:
        print("\n=============================================")
        print("    SISTEMA DE PLANIFICACIÓN DE VIAJES CHILE-ARG")
        print("=============================================")
        
        origen = input("Ciudad de Origen (Chile) [o escriba 's' para salir]: ").strip()
        if origen.lower() == 's':
            break
            
        destino = input("Ciudad de Destino (Argentina): ").strip()
        
        print("\nSeleccione su medio de transporte:")
        print("1. Auto (car)")
        print("2. Bicicleta (bike)")
        print("3. Caminando (foot)")
        opcion = input("Opción (1/2/3): ")
        
        transporte = "car"
        if opcion == "2": transporte = "bike"
        elif opcion == "3": transporte = "foot"

        print("\nBuscando localizaciones y calculando ruta...")
        coord_origen = obtener_coordenadas(origen, "Chile")
        coord_destino = obtener_coordenadas(destino, "Argentina")

        if not coord_origen or not coord_destino:
            print("Error: No se pudo encontrar una de las ciudades. Intente de nuevo.")
            continue

        # Consultar la ruta entre puntos
        url_route = f"https://graphhopper.com/api/1/route?point={coord_origen[0]},{coord_origen[1]}&point={coord_destino[0]},{coord_destino[1]}&vehicle={transporte}&locale=es&key={API_KEY}"
        res_route = requests.get(url_route).json()

        if 'paths' in res_route:
            distancia_m = res_route['paths'][0]['distance'] # en metros
            tiempo_ms = res_route['paths'][0]['time'] # en milisegundos
            
            # Conversiones
            km = distancia_m / 1000
            millas = km * 0.621371
            
            horas = int(tiempo_ms / 3600000)
            minutos = int((tiempo_ms % 3600000) / 60000)
            
            print("\n>>> RESULTADOS DEL VIAJE <<<")
            print(f"Desde: {origen} (Chile) -> Hasta: {destino} (Argentina)")
            print(f"Medio de transporte: {transporte}")
            print(f"Distancia en Kilómetros: {km:.2f} km")
            print(f"Distancia en Millas: {millas:.2f} mi")
            print(f"Duración estimada del viaje: {horas} horas con {minutos} minutos")
            
            print("\nNarrativa resumida del viaje:")
            print(f"Saliendo desde la hermosa ciudad de {origen} con dirección hacia {destino} mediante {transporte}, cruzando las fronteras entre Chile y Argentina.")
        else:
            print("No se pudo calcular una ruta terrestre válida para ese transporte entre ambas ciudades.")

if __name__ == "__main__":
    calcular_ruta()
def obtener_coordenadas(ciudad, pais):
    # Limpiamos el texto por si el usuario escribe el país por accidente
    ciudad_limpia = ciudad.lower().replace(f", {pais.lower()}", "").strip()
    ciudad_limpia = ciudad_limpia.replace(f",{pais.lower()}", "").strip()
    
    url = f"https://graphhopper.com/api/1/geocode?q={ciudad_limpia},{pais}&locale=es&key={API_KEY}"
    response = requests.get(url).json()
    if response.get('hits'):
        lat = response['hits'][0]['point']['lat']
        lng = response['hits'][0]['point']['lng']
        return lat, lng
    return None

