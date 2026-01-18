import cv2
import numpy as np
import time
import argparse
import signal
import sys
import select
import tty
import termios
from camera import RealSenseCamera
from mapping import PointCloudGenerator

# Bandera global para salida limpia
running = True

def signal_handler(sig, frame):
    """Manejador de señales para cerrar el programa con Ctrl+C."""
    global running
    print("\n[Sistema] Interrupción recibida, apagando...")
    running = False

def main():
    global running
    signal.signal(signal.SIGINT, signal_handler)

    # Argumentos de línea de comandos
    parser = argparse.ArgumentParser(description="KRIA 3D Mapping (Python)")
    parser.add_argument("--width", type=int, default=640, help="Ancho del stream")
    parser.add_argument("--height", type=int, default=480, help="Alto del stream")
    parser.add_argument("--fps", type=int, default=30, help="Fotogramas por segundo (FPS)")
    parser.add_argument("--headless", action="store_true", help="Ejecutar sin interfaz gráfica (GUI)")
    args = parser.parse_args()

    # Inicializar módulos
    cam = RealSenseCamera(width=args.width, height=args.height, fps=args.fps)
    mapper = PointCloudGenerator(output_dir="exports")
    
    # Conectar a la cámara
    if not cam.connect():
        print(f"[Sistema] Fallo al iniciar la cámara a {args.width}x{args.height} @ {args.fps} fps.")
        print("[Consejo] Si usas USB 2.0, prueba baja resolución (640x480) o bajos FPS (--fps 15 o --fps 6).")
        sys.exit(1)

    print("\n=== Controles ===")
    print(" [Q] Salir")
    print(" [S] Guardar Nube de Puntos (PLY)")
    print(" [F] Alternar Filtros")
    print(" [C] Cambiar Colores (Jet, Autumn, Bone...)")
    print(" [+] Aumentar Rango Vis (Ver más lejos)")
    print(" [-] Reducir Rango Vis (Ver más cerca)")
    print("================")

    paused = False

    # Configuración de Visualización
    vis_alpha = 0.03 # 0.03 -> ~8.5m rango. Menor alpha = Más lejos.
    vis_colormaps = [cv2.COLORMAP_JET, cv2.COLORMAP_AUTUMN, cv2.COLORMAP_BONE, cv2.COLORMAP_OCEAN, cv2.COLORMAP_DEEPGREEN]
    vis_cmap_names = ["Jet (Arcoiris)", "Autumn (Rojo/Amarillo)", "Bone (B/N)", "Ocean (Azul)", "DeepGreen (Verde)"]
    vis_cmap_idx = 0

    # Configurar terminal para entrada de una sola tecla (Habilitar siempre para control Serial)
    old_settings = None
    try:
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        print("[Sistema] Entrada de teclado habilitada (Terminal + GUI).")
    except Exception as e:
        print(f"[Aviso] No se pudo configurar el modo terminal: {e}")

    try:
        while running:
            # 1. Manejo de Entrada (Verifica AMBOS: Terminal y GUI)
            key = -1
            
            # Verificar Terminal (stdin)
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                try:
                    c = sys.stdin.read(1)
                    key = ord(c)
                except:
                    pass
            
            # Verificar Ventana GUI (si está activa)
            if not args.headless:
                key_gui = cv2.waitKey(1)
                if key_gui != -1:
                    key = key_gui # La tecla GUI tiene preferencia si se pulsa
            
            if key != -1:
                # Feedback para el usuario
                try:
                    char_key = chr(key & 0xFF).upper()
                    if 'key_gui' in locals() and key_gui != -1:
                         char_key = chr(key & 0xFF).upper()
                         
                    print(f"\r[Usuario] Tecla detectada: {char_key}   ", end='', flush=True)
                    if char_key == 'F':
                         print("\n[Acción] Alternando Filtros")
                    elif char_key == 'S':
                         print("\n[Acción] Guardando...")
                    elif char_key == 'Q':
                         print("\n[Acción] Saliendo...")
                    elif char_key == 'C':
                        vis_cmap_idx = (vis_cmap_idx + 1) % len(vis_colormaps)
                        print(f"\n[Visualización] Mapa de color: {vis_cmap_names[vis_cmap_idx]}")
                    elif char_key == '+' or key == 43 or key == 61:
                        vis_alpha = max(0.005, vis_alpha - 0.005)
                        range_m = 255 / (vis_alpha * 1000) if vis_alpha > 0 else 999
                        print(f"\n[Visualización] Rango aumentado a aprox {range_m:.1f}m")
                    elif char_key == '-' or key == 45 or key == 95:
                        vis_alpha = min(0.2, vis_alpha + 0.005)
                        range_m = 255 / (vis_alpha * 1000) if vis_alpha > 0 else 0
                        print(f"\n[Visualización] Rango reducido a aprox {range_m:.1f}m")

                except:
                    pass

            if key & 0xFF == ord('q') or key == 27: # 27 es ESC
                running = False
                break # Salir inmediatamente
                
            elif key & 0xFF == ord('s'):
                print("[Usuario] Guardando PLY...")
                if 'color' in locals() and color is not None:
                    mapper.export_fast(color, depth_frame_obj)
                else:
                    print("[Aviso] Aún no se han capturado cuadros para guardar.")
                
            elif key & 0xFF == ord('f'):
                cam.toggle_filters(not cam.filters_enabled)
                
            elif key & 0xFF == ord('p'):
                paused = not paused
                print(f"[Usuario] {'Pausado' if paused else 'Reanudado'}")
                
            elif key & 0xFF == ord('c'):
                 vis_cmap_idx = (vis_cmap_idx + 1) % len(vis_colormaps)

            # 2. Captura
            if not paused and running:
                frames_result = cam.get_frames()
                if frames_result[0] is not None:
                    color, depth, depth_frame_obj = frames_result
                else:
                    # Tiempo de espera o error, simplemente continuar el bucle
                    continue
                    
                # Visualización
                if not args.headless:
                    # Colorear profundidad para visualización
                    depth_colormap = cv2.applyColorMap(
                        cv2.convertScaleAbs(depth, alpha=vis_alpha), 
                        vis_colormaps[vis_cmap_idx]
                    )
                    
                    # Combinar (Apilar Horizontalmente)
                    images = np.hstack((color, depth_colormap))
                    
                    # Superponer Información Texto
                    cv2.putText(images, "KRIA 3D Mapping", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    
                    cv2.imshow('RealSense', images)

    finally:
        # Limpieza
        if old_settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

        cam.stop()
        if not args.headless:
            cv2.destroyAllWindows()
        
        # Auto-guardado al salir (Esencial para modo Headless)
        if 'color' in locals() and 'depth_frame_obj' in locals() and color is not None:
            print("\n[Sistema] Auto-guardando última captura antes de salir...")
            mapper.export_fast(color, depth_frame_obj)
        
        print("[Sistema] Adiós.")

if __name__ == "__main__":
    main()
