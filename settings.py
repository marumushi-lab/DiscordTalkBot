import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DSCT = os.environ.get("DISCORD_TOKEN")
OPJT = os.environ.get("OPEN_JTALK")
BID = os.environ.get("BID")
DEV = os.environ.get("DEV")