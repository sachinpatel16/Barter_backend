import json
import os
import sys

import requests


# Read configuration from environment variables
access_token = "EAASsxVZATD08BPtmSo15rPR1qHLgMAXUZBBFD206QZAIMZBKy3DXdOhPh1gpZCYLw3Q4TT7un76qHOp3LrsM98ZBkBoeb1ugqlZA0ZA8KfkfVcP8E6EOrKaZBQil2wagiqAGQGnG93eKvbUoNWmS7KxlrMNGEEO9IwObhuerGQENVhOLztc24Heknh9KS4zJVxPMLgCMFhujXrkN77MJzkL9ZA8n7H5hZA6ibtVN2SQBLJZCXAvMXgZDZD"
phone_number_id = 741188952421435
# phone_number_id = 861045527085502
recipient = "+919824117496"
template_name = os.getenv("WHATSAPP_TEMPLATE_NAME", "hello_world")
language_code = os.getenv("WHATSAPP_LANGUAGE_CODE", "en_US")

missing = [
	name
	for name, value in [
		("WHATSAPP_TOKEN", access_token),
		("WHATSAPP_PHONE_NUMBER_ID", phone_number_id),
		("WHATSAPP_TO", recipient),
	]
	if not value
]
if missing:
	print(
		f"Missing required environment variable(s): {', '.join(missing)}",
		file=sys.stderr,
	)
	sys.exit(1)

url = f"https://graph.facebook.com/v22.0/{phone_number_id}/messages"
headers = {
	"Authorization": f"Bearer {access_token}",
	"Content-Type": "application/json",
}
payload = {
	"messaging_product": "whatsapp",
	"to": recipient,
	"type": "template",
	"template": {
		"name": template_name,
		"language": {"code": language_code},
	},
}

try:
	response = requests.post(url, headers=headers, json=payload, timeout=30)
	response.raise_for_status()
	print(json.dumps(response.json(), indent=2))
except requests.HTTPError as http_err:
	resp = getattr(http_err, "response", None)
	if resp is not None:
		try:
			print(json.dumps(resp.json(), indent=2), file=sys.stderr)
		except Exception:
			print(str(http_err), file=sys.stderr)
	else:
		print(str(http_err), file=sys.stderr)
	sys.exit(1)
except Exception as err:
	print(str(err), file=sys.stderr)
	sys.exit(1)

