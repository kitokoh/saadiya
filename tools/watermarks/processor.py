import os
import cv2
import numpy as np
from PyQt5.QtGui import QColor, QImage
#import face_recognition

class MediaProcessor:
    def __init__(self):
        pass
    
    def add_watermark_to_image(self, image_path, watermark_params, output_path=None, preview=False):
        # Charger l'image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Impossible de charger l'image")
        
        # Convertir en RGB pour le traitement
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Ajouter le watermark selon le type
        watermark_type = watermark_params.get('type', 'Texte')
        
        if watermark_type == 'Image':
            watermarked_img = self._add_image_watermark(img, watermark_params)
        elif watermark_type == 'Logo avec texte':
            watermarked_img = self._add_logo_with_text(img, watermark_params)
        else:  # Texte
            watermarked_img = self._add_text_watermark(img, watermark_params)
        
        if preview:
            return watermarked_img
        
        if output_path:
            output_img = self._prepare_output_image(watermarked_img, watermark_params)
            self._save_image(output_img, output_path, watermark_params)
        
        return watermarked_img
    
    def _add_text_watermark1(self, img, params):
        text = params.get('text', '')
        if not text:
            return img.copy()
        
        # Créer une copie de l'image
        watermarked = img.copy()
        
        # Calculer la position
        position = self._calculate_watermark_position(img, params)
        
        # Convertir QColor en BGR pour OpenCV
        color = params.get('color', QColor(255, 255, 255))
        color_bgr = (color.blue(), color.green(), color.red())
        
        # Opacité
        opacity = params.get('opacity', 0.8)
        
        # Rotation
        rotation = params.get('rotation', 0)
        
        # Effets
        effect = params.get('effect', 'Aucun')
        effect_color = params.get('effect_color', QColor(0, 0, 0))
        effect_color_bgr = (effect_color.blue(), effect_color.green(), effect_color.red())
        
        # Police
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = params.get('size', 30) / 30
        thickness = 2
        
        # Créer un overlay pour l'opacité
        overlay = watermarked.copy()
        
        # Ajouter les effets
        if effect == "Ombre":
            shadow_offset = 2
            cv2.putText(overlay, text, 
                       (position[0] + shadow_offset, position[1] + shadow_offset), 
                       font, font_scale, effect_color_bgr, thickness, cv2.LINE_AA)
        elif effect == "Contour":
            offsets = [(1,1), (1,-1), (-1,1), (-1,-1)]
            for offset in offsets:
                cv2.putText(overlay, text, 
                           (position[0] + offset[0], position[1] + offset[1]), 
                           font, font_scale, effect_color_bgr, thickness, cv2.LINE_AA)
        elif effect == "Dégradé":
            # Implémentation simplifiée d'un effet de dégradé
            for i, char in enumerate(text):
                ratio = i / len(text)
                grad_color = (
                    int(color.blue() * ratio + effect_color.blue() * (1 - ratio)),
                    int(color.green() * ratio + effect_color.green() * (1 - ratio)),
                    int(color.red() * ratio + effect_color.red() * (1 - ratio))
                )
                cv2.putText(overlay, char, 
                           (position[0] + i * int(20 * font_scale), position[1]), 
                           font, font_scale, grad_color, thickness, cv2.LINE_AA)
        
        # Ajouter le texte principal
        cv2.putText(overlay, text, position, font, font_scale, color_bgr, thickness, cv2.LINE_AA)
        
        # Appliquer la rotation si nécessaire
        if rotation != 0:
            overlay = self._rotate_image(overlay, rotation, position)
        
        # Appliquer l'opacité
        cv2.addWeighted(overlay, opacity, watermarked, 1 - opacity, 0, watermarked)
        
        return watermarked
    
    def _add_image_watermark1(self, img, params):
        # Implémentation similaire mais avec gestion des effets avancés
        pass
    
    def _add_logo_with_text(self, img, params):
        # Combinaison d'image et texte
        pass
    
    def _calculate_watermark_position(self, img, params):
        position = params.get('position', 'En bas à droite')
        
        if position == "Détection visage":
            return self._find_face_position(img)
        
        # Calcul des positions standard
        pass
    
    def _find_face_position(self, img):
        # Convertir l'image en RGB (face_recognition utilise RGB)
        rgb_img = img[:, :, ::-1]
        
        # Détecter les visages
        #face_locations = face_recognition.face_locations(rgb_img)
        face_locations= False
        if face_locations:
            # Prendre le premier visage détecté
            top, right, bottom, left = face_locations[0]
            return (left, top)
        
        # Si aucun visage n'est détecté, retourner la position par défaut
        return (img.shape[1] - 100, img.shape[0] - 50)
    
    def _prepare_output_image(self, img, params):
        # Conversion de format si nécessaire
        output_format = params.get('output_format', 'Original')
        
        if output_format == "JPEG":
            return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        elif output_format == "PNG":
            return cv2.cvtColor(img, cv2.COLOR_RGB2BGRA)
        else:
            return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    def _save_image(self, img, output_path, params):
        output_format = params.get('output_format', 'Original')
        ext = os.path.splitext(output_path)[1].lower()
        
        # Déterminer l'extension si 'Original'
        if output_format == "Original":
            if ext in ('.jpg', '.jpeg'):
                output_format = "JPEG"
            elif ext == '.png':
                output_format = "PNG"
            elif ext == '.webp':
                output_format = "WEBP"
            elif ext == '.bmp':
                output_format = "BMP"
            else:
                output_format = "JPEG"  # Par défaut
        
        # Paramètres d'enregistrement
        save_params = []
        
        if output_format == "JPEG":
            quality = params.get('quality', 90)
            save_params = [cv2.IMWRITE_JPEG_QUALITY, quality]
        elif output_format == "PNG":
            compression = params.get('compression', 3)
            save_params = [cv2.IMWRITE_PNG_COMPRESSION, compression]
        elif output_format == "WEBP":
            quality = params.get('quality', 90)
            save_params = [cv2.IMWRITE_WEBP_QUALITY, quality]
        
        cv2.imwrite(output_path, img, save_params)
    
    # ... autres méthodes pour le traitement vidéo et effets avancés




    

    def add_watermark_to_video(self, video_path, watermark_params, output_path=None, progress_callback=None):
        # Ouvrir la vidéo
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError("Impossible d'ouvrir la vidéo")
        
        # Obtenir les propriétés de la vidéo
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Préparer le writer de sortie
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
        
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convertir en RGB pour le traitement
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Ajouter le watermark
            if watermark_params.get('image_path'):
                # Watermark image
                watermarked_frame = self._add_image_watermark(
                    frame, 
                    watermark_params['image_path'],
                    watermark_params['position'],
                    watermark_params['opacity']
                )
            else:
                # Watermark texte
                watermarked_frame = self._add_text_watermark(
                    frame,
                    watermark_params['text'],
                    watermark_params['position'],
                    watermark_params['size'],
                    watermark_params['color'],
                    watermark_params['opacity']
                )
            
            if output_path:
                # Convertir de RGB à BGR pour l'enregistrement
                output_frame = cv2.cvtColor(watermarked_frame, cv2.COLOR_RGB2BGR)
                out.write(output_frame)
            
            frame_count += 1
            if progress_callback:
                progress_callback(frame_count / total_frames)
        
        cap.release()
        if output_path:
            out.release()
    
    def _add_text_watermark(self, img, text, position, size, color, opacity):
        if not text:
            return img.copy()
        
        # Convertir QColor en BGR pour OpenCV
        qcolor = QColor(color)
        color_bgr = (qcolor.blue(), qcolor.green(), qcolor.red())
        
        # Créer une copie de l'image
        watermarked = img.copy()
        
        # Calculer la position
        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, size/30, 2)
        
        if position == "En bas à droite":
            pos = (img.shape[1] - text_width - 20, img.shape[0] - 20)
        elif position == "En bas à gauche":
            pos = (20, img.shape[0] - 20)
        elif position == "En haut à droite":
            pos = (img.shape[1] - text_width - 20, text_height + 20)
        elif position == "En haut à gauche":
            pos = (20, text_height + 20)
        elif position == "Centré":
            pos = ((img.shape[1] - text_width) // 2, (img.shape[0] + text_height) // 2)
        else:  # Personnalisé (par défaut en bas à droite)
            pos = (img.shape[1] - text_width - 20, img.shape[0] - 20)
        
        # Ajouter le texte avec opacité
        overlay = watermarked.copy()
        cv2.putText(overlay, text, pos, cv2.FONT_HERSHEY_SIMPLEX, size/30, color_bgr, 2, cv2.LINE_AA)
        cv2.addWeighted(overlay, opacity, watermarked, 1 - opacity, 0, watermarked)
        
        return watermarked
    
    def _add_image_watermark(self, img, watermark_image_path, position, opacity):
        # Charger l'image de watermark
        watermark = cv2.imread(watermark_image_path, cv2.IMREAD_UNCHANGED)
        if watermark is None:
            raise ValueError("Impossible de charger l'image de watermark")
        
        # Convertir en RGBA si nécessaire
        if watermark.shape[2] == 3:
            watermark = cv2.cvtColor(watermark, cv2.COLOR_BGR2BGRA)
        
        # Redimensionner le watermark (20% de la largeur de l'image)
        watermark_height = int(img.shape[0] * 0.2)
        aspect_ratio = watermark.shape[1] / watermark.shape[0]
        watermark_width = int(watermark_height * aspect_ratio)
        watermark = cv2.resize(watermark, (watermark_width, watermark_height))
        
        # Créer une copie de l'image en RGBA
        if img.shape[2] == 3:
            watermarked = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
        else:
            watermarked = img.copy()
        
        # Calculer la position
        if position == "En bas à droite":
            x = watermarked.shape[1] - watermark.shape[1] - 20
            y = watermarked.shape[0] - watermark.shape[0] - 20
        elif position == "En bas à gauche":
            x = 20
            y = watermarked.shape[0] - watermark.shape[0] - 20
        elif position == "En haut à droite":
            x = watermarked.shape[1] - watermark.shape[1] - 20
            y = 20
        elif position == "En haut à gauche":
            x = 20
            y = 20
        elif position == "Centré":
            x = (watermarked.shape[1] - watermark.shape[1]) // 2
            y = (watermarked.shape[0] - watermark.shape[0]) // 2
        else:  # Personnalisé (par défaut en bas à droite)
            x = watermarked.shape[1] - watermark.shape[1] - 20
            y = watermarked.shape[0] - watermark.shape[0] - 20
        
        # Superposer le watermark avec opacité
        for c in range(0, 3):
            watermarked[y:y+watermark.shape[0], x:x+watermark.shape[1], c] = (
                watermark[:,:,c] * (watermark[:,:,3]/255.0) * opacity + 
                watermarked[y:y+watermark.shape[0], x:x+watermark.shape[1], c] * (1 - (watermark[:,:,3]/255.0) * opacity))
        
        # Convertir de nouveau en RGB si nécessaire
        if img.shape[2] == 3:
            watermarked = cv2.cvtColor(watermarked, cv2.COLOR_RGBA2RGB)
        
        return watermarked