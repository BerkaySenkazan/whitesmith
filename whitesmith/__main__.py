"""Question generation and evaluation"""
#from whitesmith.cli import cli
import applicat
import uvicorn

if __name__ == "__main__":
    ##cli()
    uvicorn.run(applicat, host= "0.0.0.0", port="8000")
    
