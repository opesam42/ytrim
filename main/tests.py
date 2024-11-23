from django.test import TestCase
from .misc import Misc
import re

# Create your tests here.

misc = Misc()
dd = misc.sanitize_filename("My:Invalid|File*N ame?<>/With\\WeirdChars.mp4")
result = re.sub(r'\s+', '_', dd)
# print(result)

encodedString = "https://google.com".encode("utf-8")
print(encodedString)
