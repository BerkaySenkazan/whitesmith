"""Question generation and evaluation"""
from whitesmith.cli import cli
from whitesmith.applicat import app
import uvicorn

if __name__ == "__main__":
    ##cli()
    uvicorn.run(app, host= "0.0.0.0", port=8000)
    
