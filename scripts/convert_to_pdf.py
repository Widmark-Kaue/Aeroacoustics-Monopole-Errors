#%%
import img2pdf
from src.path import PATH_IMAGES

for ext in ['png', 'jgp', 'jpeg']:
    for image in PATH_IMAGES.joinpath('overleaf').glob(f"*.{ext}"):
        OUTPUT = PATH_IMAGES.joinpath('overleaf', 'pdf', image.with_suffix('.pdf').name)
        if not OUTPUT.exists():
            print(image.name)
            # Abra a imagem
            with open(image, "rb") as file:
                img_bytes = file.read()

            # Converta a imagem para PDF
            pdf_bytes = img2pdf.convert(img_bytes)

            # Salve o PDF
            with open(OUTPUT, "wb") as file:
                file.write(pdf_bytes)
# %%
