"""Question generation and evaluation"""
from whitesmith.cli import cli
import applicat
import gunicorn

if __name__ == "__main__":
    ##cli()
    gunicorn.run(applicat, host= "0.0.0.0", port="8000")
    
