
if __name__=="__main__":
    import uvicorn
    from app.main import app
    uvicorn.run(app="app.main:app",host="localhost",reload=True)