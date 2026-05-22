import cv2
import numpy as np
import tempfile
import subprocess
import os

def reconstruir_imagem(caminho_imagem: str, modo_posicao: int, pct_largura: float = 15.0, pct_altura: float = 8.0) -> np.ndarray:
    try:
        img = cv2.imread(caminho_imagem)
        if img is None:
            raise Exception("Falha ao abrir a imagem com OpenCV.")

        altura, largura = img.shape[:2]
        mask = np.zeros((altura, largura), dtype=np.uint8)

        h_roi = int(altura * (pct_altura / 100.0))
        w_roi = int(largura * (pct_largura / 100.0))

        # 1 — Canto inferior direito, 2 — Canto inferior esquerdo
        # 3 — Canto superior direito, 4 — Canto superior esquerdo, 5 — Custom
        if modo_posicao == 1 or modo_posicao == 5:
            # Inferior direito
            y_start = altura - h_roi
            x_start = largura - w_roi
            mask[y_start:altura, x_start:largura] = 255
        elif modo_posicao == 2:
            # Inferior esquerdo
            y_start = altura - h_roi
            x_start = 0
            mask[y_start:altura, x_start:w_roi] = 255
        elif modo_posicao == 3:
            # Superior direito
            y_start = 0
            x_start = largura - w_roi
            mask[y_start:h_roi, x_start:largura] = 255
        elif modo_posicao == 4:
            # Superior esquerdo
            y_start = 0
            x_start = 0
            mask[y_start:h_roi, x_start:w_roi] = 255
        else:
            raise Exception("Posição da máscara inválida.")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_img_dir = os.path.join(temp_dir, "image")
            temp_mask_dir = os.path.join(temp_dir, "mask")
            temp_out_dir = os.path.join(temp_dir, "output")
            
            os.makedirs(temp_img_dir)
            os.makedirs(temp_mask_dir)
            os.makedirs(temp_out_dir)

            base_name = os.path.basename(caminho_imagem)
            path_temp_img = os.path.join(temp_img_dir, base_name)
            path_temp_mask = os.path.join(temp_mask_dir, base_name)

            cv2.imwrite(path_temp_img, img)
            cv2.imwrite(path_temp_mask, mask)

            cmd = [
                "iopaint", "run",
                "--model", "lama",
                "--device", "cpu",
                "--image", path_temp_img,
                "--mask", path_temp_mask,
                "--output", temp_out_dir
            ]
            
            try:
                creationflags = subprocess.CREATE_NO_WINDOW
            except AttributeError:
                creationflags = 0

            result = subprocess.run(cmd, capture_output=True, text=True, creationflags=creationflags)
            if result.returncode != 0:
                raise Exception(f"Erro no IOPaint: {result.stderr.strip()}")

            arquivos_gerados = os.listdir(temp_out_dir)
            if not arquivos_gerados:
                raise Exception("Nenhum arquivo de saída foi gerado pelo IOPaint.")
            
            path_out_real = os.path.join(temp_out_dir, arquivos_gerados[0])
            img_resultante = cv2.imread(path_out_real)
            if img_resultante is None:
                raise Exception("Não foi possível carregar a imagem tratada.")
                
            return img_resultante

    except Exception as e:
        raise Exception(f"Pipeline error: {str(e)}")
