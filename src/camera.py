import pyrealsense2 as rs
import numpy as np
import time

class RealSenseCamera:
    """
    Clase envoltorio para manejar la cámara Intel RealSense D435i.
    Maneja la configuración del pipeline, filtros y captura de frames.
    """
    def __init__(self, width=640, height=480, fps=30):
        self.width = width
        self.height = height
        self.fps = fps
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.align = rs.align(rs.stream.color) # Alinear profundiad al color
        self.initialized = False
        self.scale = 0.001 # Escala por defecto

        # Filtros - Ajustados para Calidad
        # Decimación: Reduce la resolución para bajar ruido y coste computacional
        self.decimation = rs.decimation_filter()
        self.decimation.set_option(rs.option.filter_magnitude, 1) # 1 = Apagado (Resolución Completa)

        # Filtro Espacial: Suaviza la imagen preservando bordes
        self.spatial = rs.spatial_filter()
        self.spatial.set_option(rs.option.filter_magnitude, 2)
        self.spatial.set_option(rs.option.filter_smooth_alpha, 0.5)
        self.spatial.set_option(rs.option.filter_smooth_delta, 20)

        # Filtro Temporal: Promedia frames en el tiempo (reduce "nieve" o ruido dinámico)
        self.temporal = rs.temporal_filter() 
        self.temporal.set_option(rs.option.filter_smooth_alpha, 0.4)
        self.temporal.set_option(rs.option.filter_smooth_delta, 20)

        # Relleno de Huecos: Intenta rellenar píxeles negros interpolando vecindad
        self.hole_filling = rs.hole_filling_filter()
        self.hole_filling.set_option(rs.option.holes_fill, 1) # 1=Conservador
        
        self.filters_enabled = True

    def connect(self):
        """Inicializa la conexión con la cámara y configura los streams."""
        try:
            print(f"[RealSense] Conectando a cámara ({self.width}x{self.height} @ {self.fps}fps)...")
            self.config.enable_stream(rs.stream.depth, self.width, self.height, rs.format.z16, self.fps)
            self.config.enable_stream(rs.stream.color, self.width, self.height, rs.format.bgr8, self.fps)

            # Iniciar pipeline
            profile = self.pipeline.start(self.config)
            
            # Aplicar Preset "High Density" (Denso)
            # Esto mejora el relleno en objetos cercanos
            depth_sensor = profile.get_device().first_depth_sensor()
            if depth_sensor.supports(rs.option.visual_preset):
                depth_sensor.set_option(rs.option.visual_preset, 4) # 4 = High Density
            
            # Obtener escala de profundidad (metros por unidad)
            self.scale = depth_sensor.get_depth_scale()
            print(f"[RealSense] Escala de Profundidad: {self.scale}")

            # Dejar que el auto-exposición se estabilice
            for _ in range(30):
                self.pipeline.wait_for_frames()
                
            self.initialized = True
            print("[RealSense] Cámara inicializada con éxito.")
            return True

        except Exception as e:
            print(f"[RealSense] Error conectando: {e}")
            self.initialized = False
            return False

    def get_frames(self):
        """
        Captura y devuelve frames alineados de color y profundidad como arrays numpy.
        Retorno: (color_image, depth_image, depth_frame_obj)
        """
        if not self.initialized:
            return None, None, None

        try:
            # Timeout alto para soportar modos de bajos FPS (ej: 6fps = ~166ms)
            frames = self.pipeline.wait_for_frames(timeout_ms=2000)
            
            # 1. Aplicar filtros al frame de PROFUNDIDAD, ANTES de alinear
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            
            if not depth_frame or not color_frame:
                return None, None, None

            if self.filters_enabled:
                # Orden recomendado: Decimation -> Spatial -> Temporal -> Hole Filling
                depth_frame = self.spatial.process(depth_frame)
                depth_frame = self.temporal.process(depth_frame)
                depth_frame = self.hole_filling.process(depth_frame)

            # 2. Alinear la profundidad procesada al color
            aligned_frames = self.align.process(frames)
            depth_frame_aligned = aligned_frames.get_depth_frame()
            color_frame_aligned = aligned_frames.get_color_frame()
            
            # Nota: Al re-alinear después de filtrar, podríamos perder algo de coincidencia,
            # pero filtrar después de alinear suele generar artefactos extraños en bordes.
            # En esta implementación filtramos el original y luego alineamos los frames crudos.
            # (Corrección: 'frames' contiene los originales, así que lo de arriba filtra una COPIA
            # y luego alineamos los ORIGINALES sin filtrar).
            # Para hacerlo bien, deberíamos alinear el depth_frame FILTRADO con el color.
            # Pero 'align.process' requiere un objeto 'frameset'.
            
            # Solución pragmática: Aplicar filtros de nuevo al alineado O vivir con ello.
            # Aplicaremos filtros al alineado para asegurar visualización suave en pantalla.
            if self.filters_enabled:
                depth_frame_aligned = self.spatial.process(depth_frame_aligned)
                depth_frame_aligned = self.temporal.process(depth_frame_aligned)
                depth_frame_aligned = self.hole_filling.process(depth_frame_aligned)

            # Convertir a arrays numpy para OpenCV
            depth_image = np.asanyarray(depth_frame_aligned.get_data())
            color_image = np.asanyarray(color_frame_aligned.get_data())

            return color_image, depth_image, depth_frame_aligned 

        except Exception as e:
            print(f"[RealSense] Error capturando frames: {e}")
            return None, None, None

    def toggle_filters(self, state):
        self.filters_enabled = state
        print(f"[RealSense] Filtros {'Activados' if state else 'Desactivados'}")

    def stop(self):
        if self.initialized:
            self.pipeline.stop()
            self.initialized = False
            print("[RealSense] Cámara detenida.")
