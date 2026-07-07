# integrantes.py

def mostrar_integrantes():
    integrantes = [
        "camilo madrid",
        "jonathan carrasco",
        "angel villalobos"
    ]
    print("=== Integrantes del Examen Transversal - DRY7122 ===")
    for persona in integrantes:
        print(f"- {persona}")

if __name__ == "__main__":
    mostrar_integrantes()
