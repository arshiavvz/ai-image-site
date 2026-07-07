from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "سلام! سایت هوش مصنوعی من آماده است."}1
