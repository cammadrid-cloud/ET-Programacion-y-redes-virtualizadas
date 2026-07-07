# web_usuarios.py
import sqlite3
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_NAME = "usuarios_examen.db"

def inicializar_bd():
    """Crea la tabla de usuarios e inserta a los integrantes con hash de contraseña"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Crear tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # Lista de integrantes y contraseñas a elección (Modifica con tus nombres reales si quieres)
    integrantes = [
        ("camilo", "passCamilo123"),
        ("juan", "passJuan456"),
        ("diego", "passDiego789")
    ]
    
    for nombre, clave in integrantes:
        # Generar hash SHA-256 de la contraseña
        hash_object = hashlib.sha256(clave.encode())
        password_hash = hash_object.hexdigest()
        
        try:
            cursor.execute("INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)", (nombre, password_hash))
        except sqlite3.IntegrityError:
            # Si el usuario ya existe en la BD, no lo duplica
            pass
            
    conn.commit()
    conn.close()

@app.route('/login', methods=['POST'])
def login():
    """Ruta para validar usuarios mediante JSON"""
    datos = request.get_json()
    if not datos or 'usuario' not in datos or 'password' not in datos:
        return jsonify({"status": "error", "message": "Faltan datos de ingreso"}), 400
        
    usuario = datos['usuario'].lower()
    password = datos['password']
    
    # Calcular hash de la password ingresada para comparar
    hash_ingresado = hashlib.sha256(password.encode()).hexdigest()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM usuarios WHERE nombre = ?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado and resultado[0] == hash_ingresado:
        return jsonify({"status": "success", "message": f"¡Bienvenido(a) {usuario}! Validación exitosa."}), 200
    else:
        return jsonify({"status": "error", "message": "Usuario o contraseña incorrectos."}), 401

if __name__ == "__main__":
    print("[INFO] Inicializando Base de Datos SQLite...")
    inicializar_bd()
    print("[INFO] Lanzando servidor web en el puerto 5800...")
    # Configurado obligatoriamente en el puerto 5800 como pide la pauta
    app.run(host="0.0.0.0", port=5800, debug=True)
