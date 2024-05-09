import requests
import ssl
import json
import re
from simple_salesforce import Salesforce
import boto3
import csv
import os
import pandas as pd
from io import StringIO
from dotenv import load_dotenv

load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')