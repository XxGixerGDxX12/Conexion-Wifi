import requests
import speedtest
import httpx
import json

# Funciones para verificar conexión y medir velocidad
def check_website(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def check_internet_connection(sites):
    results = {}
    for site in sites:
        results[site] = check_website(site)
    return results

def get_speed():
    try:
        st = speedtest.Speedtest()
        st.download()
        st.upload()
        return st.results
    except speedtest.ConfigRetrievalError:
        return None

def get_speed_alternative():
    try:
        response = httpx.get('https://api.fast.com/netflix/speedtest', timeout=10)
        data = response.json()
        speeds = [server['url'] for server in data['servers']]
        return speeds
    except Exception as e:
        return str(e)

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        ip = response.json().get('ip')
        return ip
    except requests.RequestException:
        return "No se pudo obtener la IP pública"

# Funciones para obtener información de la IP utilizando ipinfo.io
def build_url(ip, api_key):
    """Construye la URL para la solicitud de la API."""
    return f"https://ipinfo.io/{ip}/json?token={api_key}"

def make_request(url):
    """Realiza la solicitud a la API y devuelve los datos en formato JSON."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return None

def is_bogon(data):
    """Verifica si la respuesta contiene datos de una dirección reservada o bogon."""
    return 'bogon' in data

def print_ip_info(ip, data):
    """Imprime la información de la IP obtenida de la API."""
    print(f"\nInformación para la IP: {ip}")
    print(f"IP: {data.get('ip', 'No disponible')}")
    print(f"País: {data.get('country', 'No disponible')}")
    print(f"Región: {data.get('region', 'No disponible')}")
    print(f"Ciudad: {data.get('city', 'No disponible')}")
    print(f"Organización: {data.get('org', 'No disponible')}")
    print(f"Ubicación: {data.get('loc', 'No disponible')}")
    print(f"Zona horaria: {data.get('timezone', 'No disponible')}")
    print(f"Código postal: {data.get('postal', 'No disponible')}")

def get_ip_info(ip, api_key):
    """Función principal que coordina la obtención y presentación de la información de la IP."""
    url = build_url(ip, api_key)
    data = make_request(url)

    if data is None:
        return

    if is_bogon(data):
        print(f"La IP {ip} es una dirección reservada o bogon.")
    else:
        print_ip_info(ip, data)

if __name__ == "__main__":
    sites = ['http://cripto-price.surge.sh', 'http://www.google.com', 'http://www.xataka.com', 'http://www.bing.com']
    connection_results = check_internet_connection(sites)
    
    print("Resultados de la conexión:")
    for site, status in connection_results.items():
        print(f"{site}: {'Conectado' if status else 'No conectado'}")
    
    if any(connection_results.values()):
        print("\nCalculando velocidad de Internet...")
        speed_results = get_speed()
        if speed_results:
            print(f"Velocidad de descarga: {speed_results.download / 1_000_000:.2f} Mbps")
            print(f"Velocidad de subida: {speed_results.upload / 1_000_000:.2f} Mbps")
            print(f"Ping: {speed_results.ping:.2f} ms")
        else:
            print("Speedtest falló, usando método alternativo (fast.com)...")
            speed_alternative = get_speed_alternative()
            print(f"Velocidades alternativas obtenidas de fast.com: {speed_alternative}")

        public_ip = get_public_ip()
        print(f"\nIP pública: {public_ip}")

        # Obtén información adicional de la IP pública
        api_key = 'b00fe5e6124f1a'  # Reemplaza esto con tu clave de API real
        get_ip_info(public_ip, api_key)
    else:
        print("\nNo se puede medir la velocidad de Internet ni obtener la IP pública porque no hay conexión.")
