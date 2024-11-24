from django.test import TestCase
from django.conf import settings
import os
from dotenv import load_dotenv

load_dotenv()
# Create your tests here.
cookies = os.path.join(settings.MEDIA_ROOT, "ytcookies.txt")
f = open(cookies, 'r')

print(f.read())
