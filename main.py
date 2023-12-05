import os
from src.routers.category import router as category_router
from src.routers.subcategory import router as subcategory_router
from src.routers.author import router as author_router
from fastapi import FastAPI
from fastapi.responses import UJSONResponse

app = FastAPI(debug=True)
# media settings
# Create a directory to store uploaded images
UPLOAD_DIRECTORY = "media/images"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
# add routers
app.include_router(category_router)
app.include_router(subcategory_router)
app.include_router(author_router)
#  edn touters


@app.get("/")
def getHello():
    return UJSONResponse(content={"Hello": "World"})
