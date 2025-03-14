"""
Project : 
Author : Ajeet
Date : March 14, 2025
"""
import re
import requests

response = requests.get(url='https://www.quikr.com/homes/3-bhk-apartment-of-2036sqft-for-sale-in-radiance-gardenia-bangalore/p/372255534/272495?source=qh',
                        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"}
                        )
result = {}
if response.status_code == 200:
    pattern = r'latitude":"(.+)","longitude":"(.+)"},"adlink"'
    matches = re.findall(pattern=pattern, string=response.text)

    result["latitude"] = matches[0][0]
    result["longitude"] = matches[0][1]

print(result)

"""
reference:
https://stackoverflow.com/a/79508250/11179336
"""