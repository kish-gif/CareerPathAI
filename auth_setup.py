from pydrive2.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LoadClientConfigFile("client_secrets.json")
gauth.LocalWebserverAuth()  # now allowed to redirect to localhost:8502
gauth.SaveCredentialsFile("credentials.json")