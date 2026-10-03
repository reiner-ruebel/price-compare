import requests
import json
import time

BASE_URL = "https://urldefense.com/v3/__https://chat-api.lemonade.com/chat/public/scripts/gb-home-quote__;!!JTSHVUr6R1OOzg!LmEz0GefyD2Kb_X_qjiQkyCPPcCoWGKbqzMf0GBFMsuE9CA8jzN3vM-K0_63PgsgvxWFL2towRPLee4I_yweFzKkh_dXX_zG64rFMTaXgC77$ "

session = requests.Session()

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "origin": "https://urldefense.com/v3/__https://chat.lemonade.com__;!!JTSHVUr6R1OOzg!LmEz0GefyD2Kb_X_qjiQkyCPPcCoWGKbqzMf0GBFMsuE9CA8jzN3vM-K0_63PgsgvxWFL2towRPLee4I_yweFzKkh_dXX_zG64rFMTmfVuW5$ ",
    "referer": "https://urldefense.com/v3/__https://chat.lemonade.com/__;!!JTSHVUr6R1OOzg!LmEz0GefyD2Kb_X_qjiQkyCPPcCoWGKbqzMf0GBFMsuE9CA8jzN3vM-K0_63PgsgvxWFL2towRPLee4I_yweFzKkh_dXX_zG64rFMdSQfmq_$ ",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/150.0.0.0 Safari/537.36"
    )
}

response = session.post(
    f"{BASE_URL}/sessions",
    headers=headers,
    json={"forceRestart": False},
)

print("Status Code:", response.status_code)

data = response.json()

print("\nSession ID:")
print(data["sessionId"])

print("\nFirst Step:")
print(data["history"][0]["name"])

print("\nFirst Step ID:")
print(data["history"][0]["id"])

import json

step = data["history"][0]

print("\nStep Name:")
print(step["name"])

print("\nStep ID:")
print(step["id"])

print("\nAttributes:")
print(
    json.dumps(
        step["renderedStep"]["data"],
        indent=2
    )
)

# Extract session and first step

session_id = data["sessionId"]
step_id = data["history"][0]["id"]

print("\nSubmitting first step...")

payload = {
    "answers": {
        "insured": {
            "firstName": "Dheeraj",
            "lastName": "Yenamala"
        }
    },
    "skipHooks": False
}

response2 = session.post(
    f"{BASE_URL}/sessions/{session_id}/steps/{step_id}",
    headers=headers,
    json=payload
)

print("Status Code:", response2.status_code)

next_data = response2.json()

print("\nSession Status:")
print(next_data["sessionStatus"])

print("\nNext Step Name:")
print(next_data["history"][-1]["name"])

print("\nNext Step ID:")
print(next_data["history"][-1]["id"])

# -------------------------------------------------
# STEP 3: Submit postcode
# -------------------------------------------------

address_step = next_data["history"][-1]

step_id = address_step["id"]

print("\nSubmitting postcode...")

payload = {
    "answers": {
        "addressToInsure": {
            "postalCode": "WV39HY"
        }
    },
    "skipHooks": False
}

response3 = session.post(
    f"{BASE_URL}/sessions/{session_id}/steps/{step_id}",
    headers=headers,
    json=payload
)

print("Status Code:", response3.status_code)

postcode_data = response3.json()

print("\nNext Step Name:")
print(postcode_data["history"][-1]["name"])

print("\nNext Step ID:")
print(postcode_data["history"][-1]["id"])

# -------------------------------------------------
# STEP 4: Inspect available addresses
# -------------------------------------------------

confirm_step = postcode_data["history"][-1]

print("\nStep Name:")
print(confirm_step["name"])

items = (
    confirm_step["renderedStep"]
    ["presentation"]
    ["component"]
    ["content"][0]
    ["elements"][0]
    ["items"]
)

print("\nAvailable Addresses:")

for i, item in enumerate(items):
    print(f"{i+1}. {item['label']}")

# -------------------------------------------------
# STEP 5: Select Little Haven
# -------------------------------------------------

confirm_step = postcode_data["history"][-1]

items = (
    confirm_step["renderedStep"]
    ["presentation"]
    ["component"]
    ["content"][0]
    ["elements"][0]
    ["items"]
)

little_haven = None

for item in items:
    if "Little Haven" in item["label"]:
        little_haven = item
        break

if little_haven is None:
    raise Exception("Little Haven not found")

print("\nSelected Address:")
print(little_haven["label"])

print("\nAddress Provider ID:")
print(little_haven["value"])

payload = {
    "answers": {
        "addressProviderId": little_haven["value"]
    },
    "skipHooks": False
}

response4 = session.post(
    f"{BASE_URL}/sessions/{session_id}/steps/{confirm_step['id']}",
    headers=headers,
    json=payload
)

print("\nStatus Code:")
print(response4.status_code)

address_data = response4.json()

print("\nNext Step Name:")
print(address_data["history"][-1]["name"])

print("\nNext Step ID:")
print(address_data["history"][-1]["id"])

# -------------------------------------------------
# STEP 6: Inspect ownership question
# -------------------------------------------------

ownership_step = address_data["history"][-1]

print("\nStep Name:")
print(ownership_step["name"])

print("\nStep ID:")
print(ownership_step["id"])

print("\nStep Data:")
print(
    json.dumps(
        ownership_step["renderedStep"]["data"],
        indent=2
    )
)

print("\nStep Presentation:")
print(
    json.dumps(
        ownership_step["renderedStep"]["presentation"],
        indent=2
    )[:4000]  # keep output manageable
)

# -------------------------------------------------
# STEP 7: Submit ownership answer
# -------------------------------------------------

ownership_step = address_data["history"][-1]

payload = {
    "answers": {
        "property": {
            "relationToProperty": "owner"
        }
    },
    "skipHooks": False
}

response5 = session.post(
    f"{BASE_URL}/sessions/{session_id}/steps/{ownership_step['id']}",
    headers=headers,
    json=payload
)

print("\nStatus Code:")
print(response5.status_code)

owner_data = response5.json()

next_step = owner_data["history"][-1]

print("\nNext Step Name:")
print(next_step["name"])

print("\nNext Step ID:")
print(next_step["id"])

print("\nAttributes:")
print(
    json.dumps(
        next_step["renderedStep"]["data"],
        indent=2
    )
)

# -------------------------------------------------
# STEP 8: Submit property type
# -------------------------------------------------

dwelling_step = owner_data["history"][-1]

payload = {
    "answers": {
        "property": {
            "dwellingType": "detached_house"
        }
    },
    "skipHooks": False
}

response6 = session.post(
    f"{BASE_URL}/sessions/{session_id}/steps/{dwelling_step['id']}",
    headers=headers,
    json=payload
)

print("\nStatus Code:")
print(response6.status_code)

dwelling_data = response6.json()

next_step = dwelling_data["history"][-1]

print("\nNext Step Name:")
print(next_step["name"])

print("\nNext Step ID:")
print(next_step["id"])

print("\nAttributes:")
print(
    json.dumps(
        next_step["renderedStep"]["data"],
        indent=2
    )
)

# -------------------------------------------------
# STEP 9: Select Buildings and Contents cover
# -------------------------------------------------

coverage_step = dwelling_data["history"][-1]

payload = {
    "answers": {
        "property": {
            "coverageType": "buildings_and_contents"
        }
    },
    "skipHooks": False
}

response7 = session.post(
    f"{BASE_URL}/sessions/{session_id}/steps/{coverage_step['id']}",
    headers=headers,
    json=payload
)

print("\nSTEP 9 COMPLETE")
print("Status Code:", response7.status_code)

coverage_data = response7.json()

next_step = coverage_data["history"][-1]

print("\nNext Step Name:")
print(next_step["name"])

print("\nNext Step ID:")
print(next_step["id"])

print("\nAttributes:")
print(
    json.dumps(
        next_step["renderedStep"]["data"],
        indent=2
    )
)

# -------------------------------------------------
# STEP 10: Primary Residence = Yes
# -------------------------------------------------

primary_step = coverage_data["history"][-1]

payload = {
    "answers": {
        "property": {
            "declaredPrimaryResidence": True
        }
    },
    "skipHooks": False
}

response8 = session.post(
    f"{BASE_URL}/sessions/{session_id}/steps/{primary_step['id']}",
    headers=headers,
    json=payload
)

print("\nSTEP 10 COMPLETE")
print("Status Code:", response8.status_code)

primary_data = response8.json()

next_step = primary_data["history"][-1]

print("\nNext Step Name:")
print(next_step["name"])

print("\nNext Step ID:")
print(next_step["id"])

print("\nAttributes:")
print(
    json.dumps(
        next_step["renderedStep"]["data"],
        indent=2
    )
)

# -------------------------------------------------
# STEP 11: Daytime Occupation = Yes
# -------------------------------------------------

daytime_step = primary_data["history"][-1]

payload = {
    "answers": {
        "property": {
            "daytimeOccupation": True
        }
    },
    "skipHooks": False
}

response9 = session.post(
    f"{BASE_URL}/sessions/{session_id}/steps/{daytime_step['id']}",
    headers=headers,
    json=payload
)

print("\nSTEP 11 COMPLETE")
print("Status Code:", response9.status_code)

daytime_data = response9.json()

next_step = daytime_data["history"][-1]

print("\nNext Step Name:")
print(next_step["name"])

print("\nNext Step ID:")
print(next_step["id"])

print("\nAttributes:")
print(
    json.dumps(
        next_step["renderedStep"]["data"],
        indent=2
    )
)

# -------------------------------------------------
# STEP 12: Roof Material = Concrete
# -------------------------------------------------

roof_step = daytime_data["history"][-1]

payload = {
    "answers": {
        "property": {
            "roofMaterial": "concrete"
        }
    },
    "skipHooks": False
}

response10 = session.post(
    f"{BASE_URL}/sessions/{session_id}/steps/{roof_step['id']}",
    headers=headers,
    json=payload
)

print("\nSTEP 12 COMPLETE")
print("Status Code:", response10.status_code)

roof_data = response10.json()

next_step = roof_data["history"][-1]

print("\nNext Step Name:")
print(next_step["name"])

print("\nNext Step ID:")
print(next_step["id"])

print("\nAttributes:")
print(
    json.dumps(
        next_step["renderedStep"]["data"],
        indent=2
    )
)

# -------------------------------------------------
# STEP 13: House Condition = Yes
# -------------------------------------------------

house_step = roof_data["history"][-1]

payload = {
    "answers": {
        "property": {
            "declaredGoodHouseCondition": True
        }
    },
    "skipHooks": False
}

response11 = session.post(
    f"{BASE_URL}/sessions/{session_id}/steps/{house_step['id']}",
    headers=headers,
    json=payload
)

print("\nSTEP 13 COMPLETE")
print("Status Code:", response11.status_code)

house_data = response11.json()

next_step = house_data["history"][-1]

print("\nNext Step Name:")
print(next_step["name"])

print("\nNext Step ID:")
print(next_step["id"])

print("\nAttributes:")
print(
    json.dumps(
        next_step["renderedStep"]["data"],
        indent=2
    )
)

# -------------------------------------------------
# STEP 14 RETRY
# Smoke detector only
# -------------------------------------------------

security_step = house_data["history"][-1]

payload = {
    "answers": {
        "protectiveDevicesArray": [
            "smokeAlarm"
        ]
    },
    "skipHooks": False
}

response12 = session.post(
    f"{BASE_URL}/sessions/{session_id}/steps/{security_step['id']}",
    headers=headers,
    json=payload
)

print("\nSTEP 14 RETRY")
print("Status Code:", response12.status_code)

print("\nRaw Response:")
print(response12.text)

# -------------------------------------------------
# STEP 15: Other Residents = I live alone / no selection
# -------------------------------------------------

# response12 was returned by STEP 14 RETRY
# It contains the next pending step: other-residents

security_data = response12.json()

other_residents_step = security_data["history"][-1]

payload = {
    "answers": {
        "additionalResidentsArray": []
    },
    "skipHooks": False
}

response13 = session.post(
    f"{BASE_URL}/sessions/{session_id}/steps/{other_residents_step['id']}",
    headers=headers,
    json=payload
)

print("\nSTEP 15 COMPLETE")
print("Status Code:", response13.status_code)

print("\nRaw Response Status Check:")
print(response13.text[:1000])

other_residents_data = response13.json()

next_step = other_residents_data["history"][-1]

print("\nNext Step Name:")
print(next_step["name"])

print("\nNext Step ID:")
print(next_step["id"])

print("\nAttributes:")
print(
    json.dumps(
        next_step["renderedStep"]["data"],
        indent=2
    )
)

# -------------------------------------------------
# STEP 16: Expensive Items = No
# -------------------------------------------------

# STEP 15 returned the current "expensive-items" step
expensive_step = other_residents_data["history"][-1]

payload = {
    "answers": {
        "expensiveItems": False
    },
    "skipHooks": False
}

response14 = session.post(
    f"{BASE_URL}/sessions/{session_id}/steps/{expensive_step['id']}",
    headers=headers,
    json=payload
)

print("\nSTEP 16 COMPLETE")
print("Status Code:", response14.status_code)

expensive_data = response14.json()

next_step = expensive_data["history"][-1]

print("\nNext Step Name:")
print(next_step["name"])

print("\nNext Step ID:")
print(next_step["id"])

print("\nAttributes:")
print(json.dumps(next_step["renderedStep"]["data"], indent=2))

# -------------------------------------------------
# STEP 17: Past Home Claims = None
# -------------------------------------------------

claims_step = expensive_data["history"][-1]

payload = {
    "answers": {
        "userReportedClaims": "none"
    },
    "skipHooks": False
}

response15 = session.post(
    f"{BASE_URL}/sessions/{session_id}/steps/{claims_step['id']}",
    headers=headers,
    json=payload
)

print("\nSTEP 17 COMPLETE")
print("Status Code:", response15.status_code)

claims_data = response15.json()

next_step = claims_data["history"][-1]

print("\nNext Step Name:")
print(next_step["name"])

print("\nNext Step ID:")
print(next_step["id"])

print("\nAttributes:")
print(
    json.dumps(
        next_step["renderedStep"]["data"],
        indent=2
    )
)

# -------------------------------------------------
# STEP 18: Past Insurance Cancellation = No
# -------------------------------------------------

cancellation_step = claims_data["history"][-1]

payload = {
    "answers": {
        "pastInsuranceCancellations": False
    },
    "skipHooks": False
}

response16 = session.post(
    f"{BASE_URL}/sessions/{session_id}/steps/{cancellation_step['id']}",
    headers=headers,
    json=payload
)

print("\nSTEP 18 COMPLETE")
print("Status Code:", response16.status_code)

cancellation_data = response16.json()

next_step = cancellation_data["history"][-1]

print("\nNext Step Name:")
print(next_step["name"])

print("\nNext Step ID:")
print(next_step["id"])

print("\nAttributes:")
print(
    json.dumps(
        next_step["renderedStep"]["data"],
        indent=2
    )
)

# -------------------------------------------------
# STEP 19: Criminal History = No
# -------------------------------------------------

criminal_step = cancellation_data["history"][-1]

payload = {
    "answers": {
        "criminalHistory": False
    },
    "skipHooks": False
}

response17 = session.post(
    f"{BASE_URL}/sessions/{session_id}/steps/{criminal_step['id']}",
    headers=headers,
    json=payload
)

print("\nSTEP 19 COMPLETE")
print("Status Code:", response17.status_code)

print("\nRaw Response:")
print(response17.text)

if response17.status_code == 201:

    criminal_data = response17.json()

    next_step = criminal_data["history"][-1]

    print("\nNext Step Name:")
    print(next_step["name"])

    print("\nNext Step ID:")
    print(next_step["id"])

    print("\nAttributes:")
    print(
        json.dumps(
            next_step["renderedStep"]["data"],
            indent=2
        )
    )

# -------------------------------------------------
# STEP 20: Account Details
# -------------------------------------------------

import time

account_step = criminal_data["history"][-1]

payload = {
    "answers": {
        "accountDetails": {
            "email": f"lemonade_test_{int(time.time())}@example.com",
            "dateOfBirth": "1990-01-01",
            "compliance": {
                "marketingTermsApproved": False,
                "termsOfServiceApproved": True
            }
        }
    },
    "skipHooks": False
}

response18 = session.post(
    f"{BASE_URL}/sessions/{session_id}/steps/{account_step['id']}",
    headers=headers,
    json=payload
)

print("\nSTEP 20 COMPLETE")
print("Status Code:", response18.status_code)

if response18.status_code == 201:

    account_data = response18.json()

    next_step = account_data["history"][-1]

    print("\nNext Step Name:")
    print(next_step["name"])

    print("\nNext Step ID:")
    print(next_step["id"])

    print("\nAttributes:")
    print(
        json.dumps(
            next_step["renderedStep"]["data"],
            indent=2
        )
    )

else:

    print("\nResponse:")
    print(response18.text)

# -------------------------------------------------
# INSPECT CALCULATING PRICE STEP
# -------------------------------------------------

pricing_step = account_data["history"][-1]

print("\nStep Name:")
print(pricing_step["name"])

print("\nStep ID:")
print(pricing_step["id"])

print("\nFull Step:")
print(
    json.dumps(
        pricing_step,
        indent=2
    )
)

# -------------------------------------------------
# STEP 21: Continue From Calculating Price
# -------------------------------------------------

pricing_step = account_data["history"][-1]

payload = {
    "answers": {},
    "skipHooks": False
}

response19 = session.post(
    f"{BASE_URL}/sessions/{session_id}/steps/{pricing_step['id']}",
    headers=headers,
    json=payload
)

print("\nSTEP 21 COMPLETE")
print("Status Code:", response19.status_code)

print("\nResponse:")
print(response19.text[:10000])

if response19.status_code == 201:

    pricing_data = response19.json()

    next_step = pricing_data["history"][-1]

    print("\nQuote URL:")

if "payload" in next_step:
    print(next_step["payload"].get("redirectTo"))

    print("\nNext Step Name:")
print(next_step["name"])

print("\nNext Step ID:")
print(next_step["id"])

print("\nFull Next Step:")
print(
    json.dumps(
        next_step,
        indent=2
    )
)


# -------------------------------------------------
# STEP 22: FETCH QUOTE PAGE
# -------------------------------------------------

quote_url = next_step["payload"]["redirectTo"]

# clean Lemonade formatting
quote_url = quote_url.replace('"', '')

print("\nQUOTE URL:")
print(quote_url)

quote_response = session.get(
    quote_url,
    headers=headers,
    allow_redirects=True
)

print("\nQUOTE PAGE STATUS:")
print(quote_response.status_code)

print("\nFINAL URL:")
print(quote_response.url)

with open("quote_page.html", "w", encoding="utf-8") as f:
    f.write(quote_response.text)

print("\nSaved quote_page.html")

print("\nFirst 2000 characters:")
print(quote_response.text[:2000])

# -------------------------------------------------
# STEP 23: FIND API ENDPOINTS IN QUOTE PAGE
# -------------------------------------------------

import re

js_files = re.findall(
    r'src="([^"]+\.js[^"]*)"',
    quote_response.text
)

print("\nJS FILES FOUND:")
for js in js_files:
    print(js)

if js_files:

    js_url = js_files[0]

    print("\nDOWNLOADING:")
    print(js_url)

    js_response = session.get(js_url)

    print("\nJS STATUS:")
    print(js_response.status_code)

    with open("quote_bundle.js", "w", encoding="utf-8") as f:
        f.write(js_response.text)

    print("\nSaved quote_bundle.js")

    patterns = [
        "quotePublicId",
        "premium",
        "price",
        "pricing",
        "quote",
        "offer",
        "/api/",
        "graphql"
    ]

    print("\nMATCH COUNTS:")

    for pattern in patterns:
        count = js_response.text.lower().count(pattern.lower())
        print(pattern, count)


# -------------------------------------------------
# STEP 23: DOWNLOAD THE REAL LEMONADE APP BUNDLE
# -------------------------------------------------

bundle_url = "https://urldefense.com/v3/__https://uniclient-edge.lemonade.com/index-nFR41rkh.js__;!!JTSHVUr6R1OOzg!LmEz0GefyD2Kb_X_qjiQkyCPPcCoWGKbqzMf0GBFMsuE9CA8jzN3vM-K0_63PgsgvxWFL2towRPLee4I_yweFzKkh_dXX_zG64rFMVcO2fKm$ "

bundle_response = session.get(bundle_url)

print("\nBUNDLE STATUS:")
print(bundle_response.status_code)

with open("lemonade_app.js", "w", encoding="utf-8") as f:
    f.write(bundle_response.text)

print("\nBUNDLE SIZE:")
print(len(bundle_response.text))

patterns = [
    "quotePublicId",
    "premium",
    "pricing",
    "quote",
    "/quote/",
    "/quotes/",
    "/api/",
    "graphql",
]

print("\nPATTERN COUNTS:")

for pattern in patterns:
    print(pattern, bundle_response.text.count(pattern))


# -------------------------------------------------
# STEP 24: PRINT API CONTEXTS FROM LEMONADE BUNDLE
# -------------------------------------------------

search_terms = [
    "quotePublicId",
    "/quotes/",
    "/quote/",
    "premium",
    "pricing",
    "graphql",
    "/api/"
]

bundle_text = bundle_response.text

for term in search_terms:
    print("\n" + "=" * 80)
    print("SEARCH TERM:", term)
    print("=" * 80)

    start = 0
    hit_count = 0

    while True:
        idx = bundle_text.find(term, start)

        if idx == -1:
            break

        hit_count += 1

        left = max(idx - 500, 0)
        right = min(idx + 500, len(bundle_text))

        print("\n--- HIT", hit_count, "---")
        print(bundle_text[left:right])

        start = idx + len(term)

        if hit_count >= 5:
            break

    if hit_count == 0:
        print("No hits found")

# -------------------------------------------------
# STEP 25: FIND UK HOME QUOTE VIEW SCRIPT NAME
# -------------------------------------------------

bundle_text = bundle_response.text

search_terms = [
    "gb/home/quote/view",
    "home/quote/view",
    "homeowners-gb",
    "gb-home-quote-view",
    "home-gb-quote-view",
    "homeowners-gb-quote-view",
    "quotePublicId:\"initData.quotePublicId\""
]

for term in search_terms:
    print("\n" + "=" * 80)
    print("SEARCH TERM:", term)
    print("=" * 80)

    idx = bundle_text.find(term)

    if idx == -1:
        print("Not found")
    else:
        left = max(idx - 1500, 0)
        right = min(idx + 1500, len(bundle_text))
        print(bundle_text[left:right])


# -------------------------------------------------
# STEP 26: FIND ALL HOME QUOTE ROUTES IN BUNDLE
# -------------------------------------------------

import re

bundle_text = bundle_response.text

route_matches = re.findall(
    r'"([^"]*home[^"]*quote[^"]*)"\s*:\s*\{.{0,800}?scriptName:"([^"]+)"',
    bundle_text,
    flags=re.IGNORECASE
)

print("\nHOME QUOTE ROUTES FOUND:")

if not route_matches:
    print("No home quote route matches found")
else:
    for route, script_name in route_matches:
        print("ROUTE:", route)
        print("SCRIPT:", script_name)
        print("-" * 60)


# -------------------------------------------------
# STEP 27: EXTRACT URL-LIKE STRINGS FROM BUNDLE
# -------------------------------------------------

import re

matches = set()

patterns = [
    r"/api/[A-Za-z0-9_/\-]+",
    r"/quotes/[A-Za-z0-9_/\-]+",
    r"/quote/[A-Za-z0-9_/\-]+",
    r"[A-Za-z0-9_/\-]*quote[A-Za-z0-9_/\-]*",
    r"[A-Za-z0-9_/\-]*pricing[A-Za-z0-9_/\-]*",
    r"[A-Za-z0-9_/\-]*offer[A-Za-z0-9_/\-]*",
    r"[A-Za-z0-9_/\-]*graphql[A-Za-z0-9_/\-]*"
]

for pattern in patterns:
    for match in re.findall(pattern, bundle_response.text):
        matches.add(match)

print("\nEXTRACTED STRINGS:")

for item in sorted(matches):
    print(item)


# -------------------------------------------------
# STEP 28: SAVE SESSION DETAILS FOR DEBUGGING
# -------------------------------------------------

print("\nSESSION COOKIES:")
for c in session.cookies:
    print(c.name, c.value)

print("\nHEADERS:")
for k, v in headers.items():
    print(k, v)

with open("quote_page_full.html", "w", encoding="utf-8") as f:
    f.write(quote_response.text)

print("\nSaved quote_page_full.html")

import re

m = re.search(
    r'serverBaseUrl:([^,]+)',
    quote_response.text
)

print("SERVER BASE URL MATCH:")
print(m.group(0) if m else "NOT FOUND")

for term in [
    "window.lemonade",
    "serverBaseUrl",
    "paymentsUrl",
    "consumerUrl",
    "checkoutUrl"
]:
    idx = quote_response.text.find(term)

    print("\nTERM:", term)

    if idx == -1:
        print("NOT FOUND")
    else:
        print(
            quote_response.text[
                max(idx - 500, 0):
                min(idx + 1500, len(quote_response.text))
            ]
        )