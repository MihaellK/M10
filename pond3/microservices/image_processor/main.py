from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image, ImageFilter
import io

app = FastAPI()

@app.post("/process_image/")
async def process_image(file: UploadFile = File(...)):
    if file is None:
        raise HTTPException(status_code = 400, detail='Image not Found')

    # Leia a imagem enviada
    image = Image.open(file.file)

    # Aplica um filtro na imagem (neste caso, um desfoque)
    processed_image = image.filter(ImageFilter.CONTOUR)

    # Salva a imagem processada em um buffer de bytes
    img_byte_arr = io.BytesIO()
    processed_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return StreamingResponse(img_byte_arr, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
