import asyncio
from urllib.parse import urlparse
import urllib.request as rq
import urllib
import re

async def save_video(url : str):
    save_name = re.sub("[/\:*?\"<>|]","",url.split('/')[-1])
    if len(save_name.split('.')) < 2 :
        save_name += '.mp4'
    print(f'{save_name} 다운로드 중..')
    try:
        rq.urlretrieve(url,save_name)
        print(f'{save_name} 저장 완료')
    except urllib.error.HTTPError as e:
        print(e)
    except urllib.error.URLerror as e:
        print(e)

urls = []
ans = ''
while True:
    ans = input('저장할 영상의 url입력 (end입력시 종료)>>>')
    if ans == 'end' : break
    url = urlparse(ans)
    url = url._replace(scheme='https')
    urls.append(ans)
    
for i in urls:
    asyncio.run(save_video(i))