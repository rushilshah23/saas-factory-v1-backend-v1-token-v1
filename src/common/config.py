from dotenv import load_dotenv
import os
load_dotenv()

class CommonConfig:
    ENVIRONMENT:str = os.environ['ENVIRONMENT']
    LOG_LEVEL:str= os.environ['LOG_LEVEL'].upper()
