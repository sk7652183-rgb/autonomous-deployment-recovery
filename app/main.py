from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Autonomous Deployment Recovery Platform"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/failure")
def failure():
    raise Exception("Intentional deployment failure")
