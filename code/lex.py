import boto3

client = boto3.client('lexv2-runtime')
response = client.recognize_text(
botId='UKYYFAVJIB',
botAliasId='TSTALIASID',
localeId='en_US',
sessionId='test_session',
text='test_session')

print(response)