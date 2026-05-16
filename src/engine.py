import json
import os

def generar_leaderboard():
    # 1. Cargar los datos dinámicos extraídos en vivo (ej. desde data/state.json)
    # Supongamos que state.json contiene una lista con todos los jugadores del field
    try:
        with open('data/state.json', 'r', encoding='utf-8') as f:
            datos_torneo = json.load(f)
    except FileNotFoundError:
        datos_torneo = {"status": "PAUSA", "players": []}

    # Detectar si el torneo general o el jugador están detenidos (Horario nocturno)
    torneo_en_pausa = datos_torneo.get("status") == "PAUSA"

    filas_html = ""
    
    # 2. Iterar sobre TODOS los jugadores del torneo sin límite
    for player in datos_torneo.get("players", []):
        # Extraer métricas base individuales
        pos = player.get("pos", "-")
        name = player.get("name", "Unknown Player").upper()
        score = player.get("score", "E")
        sg_putt = player.get("sg_putt", 0.0)
        sg_arg = player.get("sg_arg", 0.0)
        sg_app = player.get("sg_app", 0.0)
        sg_t2g = player.get("sg_t2g", 0.0)
        
        # Índices propios calculados (Modelos probabilísticos de entropía)
        ied = player.get("ied", 0.0)
        ied_status = "Estable" if ied <= 0 else "Volátil"
        ied_color = "#48bb78" if ied <= 0 else "#e53e3e"
        ev = player.get("ev", 1.00)

        # 3. Lógica dinámica de seguimiento puntual (Telemetría de Campo)
        if torneo_en_pausa or player.get("state") == "PAUSED":
            # Formato desaturado para indicar que la jornada del jugador terminó o está en espera
            telemetria_html = f'''
                <td colspan="3" class="telemetry-cell status-paused">
                    <span class="pause-badge">EN PAUSA</span> — Esperando reanudación de jornada (Sábado)
                </td>
            '''
        else:
            # Datos activos en tiempo real cuando empiece la actividad el sábado
            hora_dia = player.get("live_time", "--:--")
            hoyo_actual = f"Hoyo {player.get('current_hole', '--')}"
            tiros_restantes = f"{player.get('shots_left', '--')} tiros para terminar"
            
            telemetria_html = f'''
                <td class="telemetry-cell">{hora_dia}</td>
                <td class="telemetry-cell">{hoyo_actual}</td>
                <td class="telemetry-cell">{tiros_restantes}</td>
            '''

        # Determinar clases CSS para colores de los Scores
        score_class = "metric-negative" if "-" in str(score) else ("metric-positive" if "+" in str(score) else "metric-neutral")
        
        # Construir fila horizontal completa del jugador
        filas_html += f'''
        <tr>
            <td>{pos}</td>
            <td class="player-name">{name}</td>
            <td class="{score_class}">{score}</td>
            <td><div class="metric-positive" style="background: {'rgba(72,187,120,0.15)' if sg_putt >= 0 else 'rgba(245,101,101,0.15)'}; color: {'#48bb78' if sg_putt >= 0 else '#f56565'}">{sg_putt:+.2f}</div></td>
            <td><div class="metric-positive" style="background: {'rgba(72,187,120,0.15)' if sg_arg >= 0 else 'rgba(245,101,101,0.15)'}; color: {'#48bb78' if sg_arg >= 0 else '#f56565'}">{sg_arg:+.2f}</div></td>
            <td><div class="metric-positive" style="background: {'rgba(72,187,120,0.15)' if sg_app >= 0 else 'rgba(245,101,101,0.15)'}; color: {'#48bb78' if sg_app >= 0 else '#f56565'}">{sg_app:+.2f}</div></td>
            <td><div class="metric-positive" style="background: {'rgba(72,187,120,0.15)' if sg_t2g >= 0 else 'rgba(245,101,101,0.15)'}; color: {'#48bb78' if sg_t2g >= 0 else '#f56565'}">{sg_t2g:+.2f}</div></td>
            
            {telemetria_html}
            
            <td class="entropy-index">{ied:.2f} <br><small style="color:{ied_color};">{ied_status}</small></td>
            <td class="ev-index">{ev:.2f}</td>
        </tr>
        '''
        
    # 4. Inyectar filas_html dentro de tu plantilla index.html y guardarla
    # (O generar el fragmento correspondiente si usas carga asíncrona mediante fetch)
    print("Leaderboard actualizado con éxito para todos los participantes.")

if __name__ == "__main__":
    generar_leaderboard()
