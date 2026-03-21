#!/usr/bin/env python3
import base64
import urllib.parse
import re  # 必須！

## Input
while True:
    print("Input: ", end="")
    input_str = input()
    if not input_str:
        print("No input provided. Exiting.")
    else:
         break

## Flag format input with validation
pattern = r"^flag\{.+\}$"

while True:
    print("Flag format (ex: flag{...}) : ", end="")
    raw_format = input()
    
    # re.fullmatch で入力全体がパターンに一致するかチェック
    if re.fullmatch(pattern, raw_format) or raw_format == "":
        # 正しい形式なら、解析用に "flag{" などの接頭辞を取得
        flag_format = raw_format.split("{")[0] + "{"
        break
    else:
        # 形式が違う場合は突き返す
        print(f"[!] Error: '{raw_format}' is invalid. Please use 'flag{{...}}' format.")


## Decode
try:
    dec_hex = bytes.fromhex(input_str)
    try:
        display_hex = dec_hex.decode()
    except UnicodeDecodeError:
        display_hex = str(dec_hex)
except Exception:
    display_hex = "Invalid Hex"

try:
    dec_b64 = base64.b64decode(input_str)
    try:
        display_b64 = dec_b64.decode()
    except UnicodeDecodeError:
        display_b64 = str(dec_b64)
except Exception:
    display_b64 = "Invalid Base64"

try:
    dec_url = urllib.parse.unquote(input_str)
    display_url = dec_url
except Exception:
    display_url = "Invalid URL Encoding"


## Scoring
hex_score = (len(display_hex) - repr(display_hex).count('\'') ) / len(display_hex) * 100
b64_score = (len(display_b64) - repr(display_b64).count('\'') ) / len(display_b64) * 100
url_score = (len(display_url) - repr(display_url).count('\'') ) / len(display_url) * 100





if flag_format != "":
    if flag_format in display_hex:
        hex_score += 50
    if flag_format in display_b64:
        b64_score += 50
    if flag_format in display_url:
        url_score += 50

else:
    if "{" in display_hex:
            hex_score += 25
    if "{" in display_b64:
            b64_score += 25
    if "{" in display_url:
            url_score += 25

    if "}" in display_hex:
            hex_score += 25
    if "}" in display_b64:
            b64_score += 25
    if "}" in display_url:
            url_score += 25


def max_score(a, b, c):
    if a >= b and a >= c:
        return a
    elif b >= a and b >= c:
        return b
    else:
        return c
    
if max_score(hex_score, b64_score, url_score) == hex_score:
    recommendation = display_hex
elif max_score(hex_score, b64_score, url_score) == b64_score:
    recommendation = display_b64
else:    recommendation = display_url
## Output
print("")
print("Recommendation:" , recommendation , " (Score: ", max_score(hex_score, b64_score, url_score), "%)")
print("")
print("Hex: ", display_hex , " (Score: ", hex_score, "%)")
print("Base64: ", display_b64 , " (Score: ", b64_score, "%)")
print("URL Decoded: ", display_url , " (Score: ", url_score, "%)")
print("")
