import os

from openai import OpenAI, APITimeoutError

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url='https://api.openai-proxy.com/v1'
)

try:
    client.files.list()
    print('OpenAI proxy 工作正常')
except APITimeoutError as e:
    print('OpenAI proxy:', e)
