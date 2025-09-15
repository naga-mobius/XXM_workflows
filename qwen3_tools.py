import requests
import json
import uuid

def get_access_token():
  """
  Generates an authentication token by making a POST request to the login endpoint.

  Returns:
    str: The authentication token.
  """
  url = "https://igs.gov-cloud.ai/mobius-iam-service/v1.0/login"

  payload = json.dumps({
    "userName": "aidtaas@gaiansolutions.com",
    "password": "Gaian@123",
    "productId": "c2255be4-ddf6-449e-a1e0-b4f7f9a2b636",
    "requestType": "TENANT"
  })

  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  response_json = response.json()

  # Assuming the token is in the 'token' key of the response
  return response_json['accessToken']

# Hardcoded auth token for convenience
AUTH_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3Ny1NUVdFRTNHZE5adGlsWU5IYmpsa2dVSkpaWUJWVmN1UmFZdHl5ejFjIn0.eyJleHAiOjE3NTMzOTM3MzksImlhdCI6MTc1MzM1NzczOSwianRpIjoiYjEwMWFjYWMtOWY4Ni00MTQ0LTkyMTItYTE1YmJmYWFiMDIyIiwiaXNzIjoiaHR0cDovL2tleWNsb2FrLXNlcnZpY2Uua2V5Y2xvYWsuc3ZjLmNsdXN0ZXIubG9jYWw6ODA4MC9yZWFsbXMvbWFzdGVyIiwiYXVkIjpbIkJPTFRaTUFOTl9CT1RfbW9iaXVzIiwiUEFTQ0FMX0lOVEVMTElHRU5DRV9tb2JpdXMiLCJNT05FVF9tb2JpdXMiLCJWSU5DSV9tb2JpdXMiLCJhY2NvdW50Il0sInN1YiI6IjJjZjc2ZTVmLTI2YWQtNGYyYy1iY2NjLWY0YmMxZTdiZmI2NCIsInR5cCI6IkJlYXJlciIsImF6cCI6IkhPTEFDUkFDWV9tb2JpdXMiLCJzaWQiOiJiNDI0NmFiNy0zNGIzLTRlZjctYmY1OS03NTYzODA0MDFkMTAiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIi8qIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfc3JlX2FkbWluIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX2JyX2FkbWluIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX3NlY3VyaXR5X2FkbWluIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX2RjZHJfYWRtaW4iLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfQWxlcnRzX1JlYWQiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfY2RfZXhlY3V0ZSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9pYWNfZXhlY3V0ZSIsIjllNzYxYjc4LTY4YjgtNDE2Ny04MjNhLWlwMV90ZXN0X2N1c3RvbV9wcm9kdWN0X3JvbGUxMjM0NTYiLCJ1bWFfYXV0aG9yaXphdGlvbiIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9kY2RyX2V4ZWN1dGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfYnJfcmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9rOHNfcmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9DdXN0b21lcl9Xcml0ZSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9jaV93cml0ZSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9zcmVfd3JpdGUiLCIwYmM0OWZhZC05MTIzLTRjYWItYWI5YS0wNTU2Nzk2MDBkMjhfYzFhNzU2NjctYjM1ZC00NmNhLWJkNGEtZDk1NGY1YmIyY2Y5X3Rlc3Ricl9yZWFkIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX2RjZHJfcmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9BcHByb3ZhbHNfV3JpdGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfUm9sZXNfUmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9BbGVydHNfV3JpdGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfazhzX3dyaXRlIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX2lhY19hZG1pbiIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9Qb2xpY2llc19SZWFkIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX2NkX2FkbWluIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX2NpX3JlYWQiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfSW5mcmFfV3JpdGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfUm9sZXNfV3JpdGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfc3JlX2V4ZWN1dGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfSW5mcmFfUmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9kY2RyX3dyaXRlIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX0xvZ3NfUmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9pYWNfcmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9rOHNfZXhlY3V0ZSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9UZWFtX1dyaXRlIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX3NlY3VyaXR5X2V4ZWN1dGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfY2RfcmVhZCIsIm9mZmxpbmVfYWNjZXNzIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX1BvbGljaWVzX1dyaXRlIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX3NlY3VyaXR5X3dyaXRlIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX1Byb2plY3RfV3JpdGUiLCJtb2JpdXNfZDBmNTJiMGUtMzZkNy00ODUzLTg4NjAtNmQyMWE5YTkyMGE1X0FCQ0QiLCJkZWZhdWx0LXJvbGVzLW1hc3RlciIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9DdXN0b21lcl9SZWFkIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX1RlYW1fUmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9icl9leGVjdXRlIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX2s4c19hZG1pbiIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9Qcm9qZWN0X1JlYWQiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfTG9nc19Xcml0ZSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9jZF93cml0ZSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9icl93cml0ZSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9zcmVfcmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9Vc2VyX1dyaXRlIiwiOWU3NjFiNzgtNjhiOC00MTY3LTgyM2EtaXAxX2YwYzFiODkzLWRjYTYtNGRkMS05MjI5LWlwMV90ZXN0X2N1c3RvbV9wcm9kdWN0X3JvbGUxMjM0NSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9pYWNfd3JpdGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfY2lfYWRtaW4iLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfc2VjdXJpdHlfcmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9jaV9leGVjdXRlIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX0FwcHJvdmFsc19SZWFkIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX1VzZXJfUmVhZCJdfSwicmVzb3VyY2VfYWNjZXNzIjp7IkJPTFRaTUFOTl9CT1RfbW9iaXVzIjp7InJvbGVzIjpbIkJPTFRaTUFOTl9CT1RfVVNFUiIsIkJPTFRaTUFOTl9CT1RfQURNSU4iXX0sIkhPTEFDUkFDWV9tb2JpdXMiOnsicm9sZXMiOlsiSE9MQUNSQUNZX1VTRVIiXX0sIlBBU0NBTF9JTlRFTExJR0VOQ0VfbW9iaXVzIjp7InJvbGVzIjpbIlBBU0NBTF9JTlRFTExJR0VOQ0VfQ09OU1VNRVIiLCJQQVNDQUxfSU5URUxMSUdFTkNFX1VTRVIiLCJQQVNDQUxfSU5URUxMSUdFTkNFX0FETUlOIiwiU0NIRU1BX1JFQUQiXX0sIk1PTkVUX21vYml1cyI6eyJyb2xlcyI6WyJNT05FVF9BUFBST1ZFIiwiTU9ORVRfVVNFUiJdfSwiVklOQ0lfbW9iaXVzIjp7InJvbGVzIjpbIlZJTkNJX1VTRVIiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoicHJvZmlsZSBlbWFpbCIsInJlcXVlc3RlclR5cGUiOiJURU5BTlQiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IkFpZHRhYXMgQWlkdGFhcyIsInRlbmFudElkIjoiMmNmNzZlNWYtMjZhZC00ZjJjLWJjY2MtZjRiYzFlN2JmYjY0IiwicGxhdGZvcm1JZCI6Im1vYml1cyIsInByZWZlcnJlZF91c2VybmFtZSI6InBhc3N3b3JkX3RlbmFudF9haWR0YWFzQGdhaWFuc29sdXRpb25zLmNvbSIsImdpdmVuX25hbWUiOiJBaWR0YWFzIiwiZmFtaWx5X25hbWUiOiJBaWR0YWFzIiwiZW1haWwiOiJwYXNzd29yZF90ZW5hbnRfYWlkdGFhc0BnYWlhbnNvbHV0aW9ucy5jb20iLCJwbGF0Zm9ybXMiOnsicm9sZXMiOlsiU0NIRU1BX1JFQUQiXX19.aU1Qq-zNiasF7cMvDKjxye4AJDauKYj-2bKNjTtSkIgTGlE4Tqxl69wNBrZBZix-6l8d9nnuvD85WMJIH9MyK6U5g_Q8HxCz2l8z3InWO-k6i_8Gp8U1AEVTxMlTYNjp_vL3WooNpLulLaE71Bp58GgO4IZzalCh7zmkTtaNzZGanQsAXObMrxisRp3VlSak5MX2KfRFNSLlFAEXLt_7NdNKjSZAZ5c-i5X2WJm0rijSz0_0pKJ9NR_mJ0vCPnRgOxZnfNsdXRz988FS_QC6ZzWthkE59WTC1W56PmDPACMV2HzrAK6Iq8lVWRp2UL1V_fFH6FJ2xFacTKDClkOXfw"

def upload_csv_file(file_path):
    url = "https://igs.gov-cloud.ai/mobius-content-service/v1.0/content/upload?filePathAccess=private&filePath=%2Fbottle%2Flimka%2Fsoda%2F"

    payload = {}
    files=[
    ('file',('sample.csv',open(file_path,'rb'),'text/csv'))
    ]
    headers = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3Ny1NUVdFRTNHZE5adGlsWU5IYmpsa2dVSkpaWUJWVmN1UmFZdHl5ejFjIn0.eyJleHAiOjE3NTMzOTM3MzksImlhdCI6MTc1MzM1NzczOSwianRpIjoiYjEwMWFjYWMtOWY4Ni00MTQ0LTkyMTItYTE1YmJmYWFiMDIyIiwiaXNzIjoiaHR0cDovL2tleWNsb2FrLXNlcnZpY2Uua2V5Y2xvYWsuc3ZjLmNsdXN0ZXIubG9jYWw6ODA4MC9yZWFsbXMvbWFzdGVyIiwiYXVkIjpbIkJPTFRaTUFOTl9CT1RfbW9iaXVzIiwiUEFTQ0FMX0lOVEVMTElHRU5DRV9tb2JpdXMiLCJNT05FVF9tb2JpdXMiLCJWSU5DSV9tb2JpdXMiLCJhY2NvdW50Il0sInN1YiI6IjJjZjc2ZTVmLTI2YWQtNGYyYy1iY2NjLWY0YmMxZTdiZmI2NCIsInR5cCI6IkJlYXJlciIsImF6cCI6IkhPTEFDUkFDWV9tb2JpdXMiLCJzaWQiOiJiNDI0NmFiNy0zNGIzLTRlZjctYmY1OS03NTYzODA0MDFkMTAiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIi8qIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfc3JlX2FkbWluIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX2JyX2FkbWluIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX3NlY3VyaXR5X2FkbWluIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX2RjZHJfYWRtaW4iLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfQWxlcnRzX1JlYWQiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfY2RfZXhlY3V0ZSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9pYWNfZXhlY3V0ZSIsIjllNzYxYjc4LTY4YjgtNDE2Ny04MjNhLWlwMV90ZXN0X2N1c3RvbV9wcm9kdWN0X3JvbGUxMjM0NTYiLCJ1bWFfYXV0aG9yaXphdGlvbiIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9kY2RyX2V4ZWN1dGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfYnJfcmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9rOHNfcmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9DdXN0b21lcl9Xcml0ZSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9jaV93cml0ZSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9zcmVfd3JpdGUiLCIwYmM0OWZhZC05MTIzLTRjYWItYWI5YS0wNTU2Nzk2MDBkMjhfYzFhNzU2NjctYjM1ZC00NmNhLWJkNGEtZDk1NGY1YmIyY2Y5X3Rlc3Ricl9yZWFkIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX2RjZHJfcmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9BcHByb3ZhbHNfV3JpdGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfUm9sZXNfUmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9BbGVydHNfV3JpdGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfazhzX3dyaXRlIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX2lhY19hZG1pbiIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9Qb2xpY2llc19SZWFkIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX2NkX2FkbWluIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX2NpX3JlYWQiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfSW5mcmFfV3JpdGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfUm9sZXNfV3JpdGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfc3JlX2V4ZWN1dGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfSW5mcmFfUmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9kY2RyX3dyaXRlIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX0xvZ3NfUmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9pYWNfcmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9rOHNfZXhlY3V0ZSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9UZWFtX1dyaXRlIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX3NlY3VyaXR5X2V4ZWN1dGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfY2RfcmVhZCIsIm9mZmxpbmVfYWNjZXNzIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX1BvbGljaWVzX1dyaXRlIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX3NlY3VyaXR5X3dyaXRlIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX1Byb2plY3RfV3JpdGUiLCJtb2JpdXNfZDBmNTJiMGUtMzZkNy00ODUzLTg4NjAtNmQyMWE5YTkyMGE1X0FCQ0QiLCJkZWZhdWx0LXJvbGVzLW1hc3RlciIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9DdXN0b21lcl9SZWFkIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX1RlYW1fUmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9icl9leGVjdXRlIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX2s4c19hZG1pbiIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9Qcm9qZWN0X1JlYWQiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfTG9nc19Xcml0ZSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9jZF93cml0ZSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9icl93cml0ZSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9zcmVfcmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9Vc2VyX1dyaXRlIiwiOWU3NjFiNzgtNjhiOC00MTY3LTgyM2EtaXAxX2YwYzFiODkzLWRjYTYtNGRkMS05MjI5LWlwMV90ZXN0X2N1c3RvbV9wcm9kdWN0X3JvbGUxMjM0NSIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9pYWNfd3JpdGUiLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfY2lfYWRtaW4iLCI2N2UxNDcxNTA2ZGE3NTJiNzg3MTZkMjFfc2VjdXJpdHlfcmVhZCIsIjY3ZTE0NzE1MDZkYTc1MmI3ODcxNmQyMV9jaV9leGVjdXRlIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX0FwcHJvdmFsc19SZWFkIiwiNjdlMTQ3MTUwNmRhNzUyYjc4NzE2ZDIxX1VzZXJfUmVhZCJdfSwicmVzb3VyY2VfYWNjZXNzIjp7IkJPTFRaTUFOTl9CT1RfbW9iaXVzIjp7InJvbGVzIjpbIkJPTFRaTUFOTl9CT1RfVVNFUiIsIkJPTFRaTUFOTl9CT1RfQURNSU4iXX0sIkhPTEFDUkFDWV9tb2JpdXMiOnsicm9sZXMiOlsiSE9MQUNSQUNZX1VTRVIiXX0sIlBBU0NBTF9JTlRFTExJR0VOQ0VfbW9iaXVzIjp7InJvbGVzIjpbIlBBU0NBTF9JTlRFTExJR0VOQ0VfQ09OU1VNRVIiLCJQQVNDQUxfSU5URUxMSUdFTkNFX1VTRVIiLCJQQVNDQUxfSU5URUxMSUdFTkNFX0FETUlOIiwiU0NIRU1BX1JFQUQiXX0sIk1PTkVUX21vYml1cyI6eyJyb2xlcyI6WyJNT05FVF9BUFBST1ZFIiwiTU9ORVRfVVNFUiJdfSwiVklOQ0lfbW9iaXVzIjp7InJvbGVzIjpbIlZJTkNJX1VTRVIiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoicHJvZmlsZSBlbWFpbCIsInJlcXVlc3RlclR5cGUiOiJURU5BTlQiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IkFpZHRhYXMgQWlkdGFhcyIsInRlbmFudElkIjoiMmNmNzZlNWYtMjZhZC00ZjJjLWJjY2MtZjRiYzFlN2JmYjY0IiwicGxhdGZvcm1JZCI6Im1vYml1cyIsInByZWZlcnJlZF91c2VybmFtZSI6InBhc3N3b3JkX3RlbmFudF9haWR0YWFzQGdhaWFuc29sdXRpb25zLmNvbSIsImdpdmVuX25hbWUiOiJBaWR0YWFzIiwiZmFtaWx5X25hbWUiOiJBaWR0YWFzIiwiZW1haWwiOiJwYXNzd29yZF90ZW5hbnRfYWlkdGFhc0BnYWlhbnNvbHV0aW9ucy5jb20iLCJwbGF0Zm9ybXMiOnsicm9sZXMiOlsiU0NIRU1BX1JFQUQiXX19.aU1Qq-zNiasF7cMvDKjxye4AJDauKYj-2bKNjTtSkIgTGlE4Tqxl69wNBrZBZix-6l8d9nnuvD85WMJIH9MyK6U5g_Q8HxCz2l8z3InWO-k6i_8Gp8U1AEVTxMlTYNjp_vL3WooNpLulLaE71Bp58GgO4IZzalCh7zmkTtaNzZGanQsAXObMrxisRp3VlSak5MX2KfRFNSLlFAEXLt_7NdNKjSZAZ5c-i5X2WJm0rijSz0_0pKJ9NR_mJ0vCPnRgOxZnfNsdXRz988FS_QC6ZzWthkE59WTC1W56PmDPACMV2HzrAK6Iq8lVWRp2UL1V_fFH6FJ2xFacTKDClkOXfw'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    response = response.json()
    cdn_url = response.get('cdnUrl')
    cdn_url = "https://cdn.gov-cloud.ai"+cdn_url
    return cdn_url

def create_ingestion_job(file_url: str, destination_schema: str, file_type: str, job_name: str = None):
    """
    Creates a data ingestion job.

    Args:
        file_url (str): The URL of the file to ingest.
        destination_schema (str): The destination schema ID.
        file_type (str): The type of the file (e.g., "CSV").
        job_name (str, optional): The name of the ingestion job. If None, a random UUID will be generated.

    Returns:
        dict: The JSON response from the job creation request.
    """
    url = "https://igs.gov-cloud.ai/pi-ingestion-service-dbaas/v2.0/jobs"

    if job_name is None:
        job_name = f"ingestion_job_{uuid.uuid4()}"

    payload = json.dumps({
      "universes": [
        "68c41b49bd3683669a241ea6" # This might need to be dynamic based on the user's context
      ],
      "name": job_name,
      "description": "Ingestion job created via API",
      "jobType": "ONE_TIME",
      "fileType": file_type,
      "sinks": [
        "TIDB" # This might need to be dynamic based on the user's context
      ],
      "jarVersion": "13.1.1", # This might need to be dynamic
      "mappingConfig": {
        "autoMap": True,
        "fileUrl": file_url,
        "destinationSchema": destination_schema
      },
      "source": {
        "sourceType": "FILE"
      },
      "tags": {
        "BLUE": [
          "api_ingestion"
        ]
      }
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {AUTH_TOKEN}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response.raise_for_status() # Raise an exception for bad status codes
    return response.json()

# Tool Descriptions for LLM Integration
TOOL_DESCRIPTIONS = {
    "upload_csv_file": {
        "name": "upload_csv_file",
        "description": "Uploads a CSV file to a specified URL and returns the CDN URL for the uploaded file. This tool is essential for preparing files before creating data ingestion jobs.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The local file system path to the CSV file that needs to be uploaded. Must be a valid path to an existing CSV file."
                }
                # "upload_url": {
                #     "type": "string",
                #     "description": "The target URL endpoint where the file should be uploaded. Default is 'https://igs.gov-cloud.ai/pi-file-service/v1.0/upload'.",
                #     "default": "https://igs.gov-cloud.ai/pi-file-service/v1.0/upload"
                # }
            },
            "required": ["file_path", "upload_url"]
        },
        "returns": {
            "type": "string",
            "description": "The full CDN URL where the uploaded file can be accessed, prefixed with 'https://cdn.gov-cloud.ai'."
        },
        "example": {
            "input": {
                "file_path": "/Users/user/data/sample.csv"
            },
            "output": "https://cdn.gov-cloud.ai/_ENC(4+j2JOgE1QQdq6yO427Uztql2TlqlMwKUOg5QJcVQ5XUgB/GP4/J5WLrrqWMDU3q)/bottle/limka/soda/8ecfade9-96ca-4dfd-8c35-2651a0b6b37c_$$_V1_sample.csv"
        }
    },
    "create_ingestion_job": {
        "name": "create_ingestion_job",
        "description": "Creates a data ingestion job to process files (CSV, JSON, etc.) and ingest them into a specified destination schema. This is typically used after uploading a file to create an automated data processing pipeline.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_url": {
                    "type": "string",
                    "description": "The complete URL of the file to be ingested. This is typically the CDN URL returned from upload_csv_file function."
                },
                "destination_schema": {
                    "type": "string",
                    "description": "The unique identifier of the destination schema where the data should be ingested. This should be a valid schema ID in the system."
                },
                "file_type": {
                    "type": "string",
                    "description": "The type of file being ingested. Supported types include 'CSV', 'JSON', etc.",
                    "enum": ["CSV", "JSON", "XML", "PARQUET"]
                },
                "job_name": {
                    "type": "string",
                    "description": "Optional custom name for the ingestion job. If not provided, a random UUID-based name will be generated.",
                    "default": "auto-generated"
                }
            },
            "required": ["file_url", "destination_schema", "file_type"]
        },
        "returns": {
            "type": "object",
            "description": "JSON response containing job details including job ID, status, and configuration information."
        },
        "example": {
            "input": {
                "file_url": "https://cdn.gov-cloud.ai/_ENC(4+j2JOgE1QQdq6yO427Uztql2TlqlMwKUOg5QJcVQ5XUgB/GP4/J5WLrrqWMDU3q)/bottle/limka/soda/8ecfade9-96ca-4dfd-8c35-2651a0b6b37c_$$_V1_sample.csv",
                "destination_schema": "68c41b50f34309622134ee3b",
                "file_type": "CSV",
                "job_name": "my_data_ingestion_job"
            },
            "output": {
                "jobId": "12345678-1234-1234-1234-123456789012",
                "status": "CREATED",
                "name": "my_data_ingestion_job"
            }
        }
    }
}

# Tool Registry for organizing and managing tools
class ToolRegistry:
    """
    A registry class to manage and organize tool descriptions for LLM integration.
    Provides methods to retrieve tool information, validate tools, and manage the tool catalog.
    """
    
    def __init__(self):
        self.tools = TOOL_DESCRIPTIONS.copy()
    
    def get_tool(self, tool_name: str) -> dict:
        """
        Retrieve a specific tool description by name.
        
        Args:
            tool_name (str): Name of the tool to retrieve
            
        Returns:
            dict: Tool description dictionary or None if not found
        """
        return self.tools.get(tool_name)
    
    def get_all_tools(self) -> dict:
        """
        Get all available tools in the registry.
        
        Returns:
            dict: Dictionary of all tool descriptions
        """
        return self.tools.copy()
    
    def get_tool_names(self) -> list:
        """
        Get a list of all available tool names.
        
        Returns:
            list: List of tool names
        """
        return list(self.tools.keys())
    
    def add_tool(self, tool_name: str, tool_description: dict):
        """
        Add a new tool to the registry.
        
        Args:
            tool_name (str): Name of the tool
            tool_description (dict): Tool description following the standard format
        """
        self.tools[tool_name] = tool_description
    
    def remove_tool(self, tool_name: str) -> bool:
        """
        Remove a tool from the registry.
        
        Args:
            tool_name (str): Name of the tool to remove
            
        Returns:
            bool: True if tool was removed, False if not found
        """
        if tool_name in self.tools:
            del self.tools[tool_name]
            return True
        return False
    
    def validate_tool_call(self, tool_name: str, parameters: dict) -> tuple:
        """
        Validate if a tool call has all required parameters.
        
        Args:
            tool_name (str): Name of the tool to validate
            parameters (dict): Parameters provided for the tool call
            
        Returns:
            tuple: (is_valid: bool, missing_params: list, error_message: str)
        """
        if tool_name not in self.tools:
            return False, [], f"Tool '{tool_name}' not found in registry"
        
        tool_desc = self.tools[tool_name]
        required_params = tool_desc.get("parameters", {}).get("required", [])
        missing_params = []
        
        for param in required_params:
            if param not in parameters:
                missing_params.append(param)
        
        if missing_params:
            return False, missing_params, f"Missing required parameters: {', '.join(missing_params)}"
        
        return True, [], "Valid tool call"
    
    def get_tool_for_llm(self, tool_name: str) -> dict:
        """
        Get tool description formatted for LLM function calling.
        
        Args:
            tool_name (str): Name of the tool
            
        Returns:
            dict: Tool description in LLM-compatible format
        """
        tool = self.get_tool(tool_name)
        if not tool:
            return {}
        
        return {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"]
            }
        }
    
    def get_all_tools_for_llm(self) -> list:
        """
        Get all tools formatted for LLM function calling.
        
        Returns:
            list: List of tools in LLM-compatible format
        """
        return [self.get_tool_for_llm(tool_name) for tool_name in self.get_tool_names()]

# Initialize the global tool registry
tool_registry = ToolRegistry()

# Example usage and tool registry demonstration
if __name__ == "__main__":
    print("=== Tool Registry Demo ===")
    
    # Display available tools
    print(f"Available tools: {tool_registry.get_tool_names()}")
    
    # Get tool descriptions for LLM
    llm_tools = tool_registry.get_all_tools_for_llm()
    print(f"\nNumber of tools for LLM: {len(llm_tools)}")
    
    # Validate a tool call
    test_params = {"file_path": "/test/file.csv", "upload_url": "https://example.com"}
    is_valid, missing, error = tool_registry.validate_tool_call("upload_csv_file", test_params)
    print(f"\nTool validation test: Valid={is_valid}, Error={error}")
    
    print("\n=== Function Usage Examples ===")
    
    # Example file upload
    upload_url = "https://igs.gov-cloud.ai/pi-file-service/v1.0/upload"  # Default upload URL
    
    # Uncomment and modify the following lines to test file upload:
    # file_path = "/path/to/your/file.csv"
    # cdn_url = upload_csv_file(file_path, upload_url)
    # print(f"File uploaded to: {cdn_url}")
    
    # Example ingestion job creation
file_url = "https://cdn.gov-cloud.ai/_ENC(4+j2JOgE1QQdq6yO427Uztql2TlqlMwKUOg5QJcVQ5XUgB/GP4/J5WLrrqWMDU3q)/bottle/limka/soda/7e728886-e9a0-4cbb-8fc8-e6ded08430ff_$$_V1_sample.csv"
destination_schema = "68c41b50f34309622134ee3b"
    file_type = "CSV"
    
    # Uncomment to test ingestion job creation:
    # ingestion_job_response = create_ingestion_job(file_url, destination_schema, file_type)
    # print(ingestion_job_response)
    
    print("\nTool registry setup complete! Use tool_registry to access tool descriptions and validation.")