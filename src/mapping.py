import numpy as np
import cv2
import os
import datetime

class PointCloudGenerator:
    """
    Clase encargada de generar y exportar nubes de puntos 3D.
    """
    def __init__(self, output_dir="exports"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def export_fast(self, color_image, depth_frame, filename=None):
        """
        Exporta a formato PLY utilizando una implementación rápida basada en NumPy.
        """
        import pyrealsense2 as rs
        
        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.output_dir, f"nube_{timestamp}.ply")
            
        print(f"[Exportar] Guardando en {filename}...")
        
        try:
            # Usamos nuestra implementación manual NumPy por robustez
            self.save_ply_numpy(color_image, depth_frame, filename)
            
            print(f"[Exportar] Guardado con éxito.")
            return True
        except Exception as e:
            print(f"[Exportar] Fallo: {e}")
            return False

    def save_ply_numpy(self, color_image, depth_frame, filename):
        """
        Generación manual de PLY usando NumPy.
        Calcula las coordenadas 3D (x,y,z) desde el mapa de profundidad y
        asigna el color RGB correspondiente a cada punto.
        """
        import pyrealsense2 as rs
        
        # Obtener intrínsecos de la cámara (para proyectar 2D -> 3D)
        # profile = depth_frame.get_profile().as_video_stream_profile()
        # intrinsics = profile.get_intrinsics()
        
        # Nota: Usamos la función interna de pyrealsense2 'calculate' 
        # para generar la nube de puntos geométrica de forma eficiente en C++.
        pc = rs.pointcloud()
        points = pc.calculate(depth_frame)
        
        # Obtener vértices (geometría)
        # Devuelve una lista de tuplas estructurada (x,y,z)
        vtx = np.asanyarray(points.get_vertices())
        
        # Convertir a array estándar de float32 (N, 3)
        # Esto nos da una matriz donde cada fila es un punto (X, Y, Z)
        verts = vtx.view(np.float32).reshape(-1, 3)
        
        # Aplanar la imagen de color a (N, 3) para que coincida con los vértices
        colors = color_image.reshape(-1, 3)
        
        # Filtrar puntos válidos
        # Eliminamos puntos con Z <= 0 (errores o infinito)
        valid = verts[:, 2] > 0
        verts = verts[valid]
        colors = colors[valid]
        
        # Escribir Cabecera PLY (ASCII)
        # Define el formato para que programas como MeshLab lo entiendan
        header = f"""ply
format ascii 1.0
element vertex {len(verts)}
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
"""
        
        with open(filename, 'w') as f:
            f.write(header)
            # Escritura eficiente de datos
            # Combinamos geometría y color en una sola matriz (N, 6)
            data = np.hstack((verts, colors))
            # Guardamos como texto con formato: 3 flotantes + 3 enteros
            np.savetxt(f, data, fmt="%.4f %.4f %.4f %d %d %d")
