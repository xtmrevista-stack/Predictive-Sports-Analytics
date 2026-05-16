import json
import os
from datetime import datetime

def calcular_ied(precision, ruido, progreso_evento):
    """
    Calcula el Índice de Entropía Dinámica (IED).
    Un IED bajo (cercano a 0.0) significa certeza y estabilidad matemática.
    """
    return round((1.0 - precision) + (ruido * 0.4) - (progreso_evento * 0.3), 4)

def procesar_mercado_caliente():
    # Estructura basada en los datos de telemetría de tus capturas
    eventos = [
        {
            "competidor": "MAVERICK MCNEALY", 
            "precision_tiro": 0.95, 
            "ruido_drift": 0.05, 
            "progreso": 1.0,
            "momio_apuesta": 1.12
        },
        {
            "competidor": "ALDRICH POTGIETER", 
            "precision_tiro": 0.72, 
            "ruido_drift": 0.35, 
            "progreso": 0.5, 
            "momio_apuesta": 2.20
        },
        {
            "competidor": "MIN WOO LEE", 
            "precision_tiro": 0.65, 
            "ruido_drift": 0.20, 
            "progreso": 0.4, 
            "momio_apuesta": 17.00
        }
    ]
    
    estado_procesado = []
    for ev in eventos:
        ied = calcular_ied(ev['precision_tiro'], ev['ruido_drift'], ev['progreso'])
        ppt = round((1.0 - ied) * 100, 2)
        if ppt < 1.0: ppt = 1.0
        
        valor_esperado = round((ppt * ev['momio_apuesta']) / 100, 2)
        
        estado_procesado.append({
            "competidor": ev['competidor'],
            "ied": ied,
            "probabilidad_teorica_pct": ppt,
            "momio": ev['momio_apuesta'],
            "valor_esperado": valor_esperado,
            "condicion": "Estable (Baja Entropía)" if ied < 0.25 else "Volátil",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
    return estado_procesado

if __name__ == "__main__":
    if not os.path.exists('data'):
        os.makedirs('data')
        
    datos = procesar_mercado_caliente()
    
    with open('data/state.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
        
    print("Estado predictivo actualizado con éxito en /data/state.json")
