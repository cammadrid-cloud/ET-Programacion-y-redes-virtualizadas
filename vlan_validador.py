# vlan_validador.py

def verificar_vlan():
    print("=== Validador de Rangos VLAN ===")
    try:
        vlan = int(input("Por favor, ingrese el número de VLAN a verificar: "))
        
        if vlan >= 1 and vlan <= 1005:
            print(f"La VLAN {vlan} corresponde al Rango Normal.")
        elif vlan >= 1006 and vlan <= 4094:
            print(f"La VLAN {vlan} corresponde al Rango Extendido.")
        elif vlan == 0 or vlan == 4095:
            print(f"La VLAN {vlan} está reservada por el sistema.")
        else:
            print("Número de VLAN inválido. El rango permitido en redes es de 1 a 4094.")
            
    except ValueError:
        print("Error: Por favor, introduzca solo números enteros.")

if __name__ == "__main__":
    verificar_vlan()
