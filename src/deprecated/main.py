from fastapi import FastAPI
from routers import user_router, broker_router, client_router, property_router, image_router

app = FastAPI()

# Mount the routers
app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(broker_router.router, prefix="/brokers", tags=["Brokers"])
app.include_router(client_router.router, prefix="/clients", tags=["Clients"])
app.include_router(property_router.router, prefix="/properties", tags=["Properties"])
app.include_router(image_router.router, prefix="/images", tags=["Images"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
