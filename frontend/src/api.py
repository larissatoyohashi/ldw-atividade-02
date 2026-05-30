import requests

BASE_URL = "http://localhost:5000"

def get_residencias():
    try:
        response = requests.get(f"{BASE_URL}/residencias", timeout=3)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Aviso: Backend offline ou erro de conexão - {e}")
        return []

def create_residencia(dados):
    try:
        response = requests.post(f"{BASE_URL}/residencias", json=dados, timeout=3)
        return response.status_code == 201 
    except Exception as e:
        print(f"Erro ao enviar dados: {e}")
        return False