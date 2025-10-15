# videoDownloaderFor_mp4

비동기 처리 기반의 간단한 동영상 다운로더입니다.

## 개요

videoDownloaderFor_mp4는 Python의 urllib를 활용하여 웹 상의 동영상 파일을 다운로드하는 CLI 도구입니다. 여러 URL을 입력받아 순차적으로 다운로드하며, 파일명을 자동으로 정제하고 .mp4 확장자를 추가합니다.

## 주요 기능

- **비동기 다운로드**: asyncio를 이용한 효율적인 파일 다운로드
- **다중 URL 지원**: 여러 동영상 URL을 한 번에 입력하여 순차 다운로드
- **자동 파일명 정제**: URL에서 특수문자를 제거하여 안전한 파일명 생성
- **확장자 자동 추가**: .mp4 확장자가 없는 경우 자동으로 추가
- **에러 핸들링**: HTTP 오류 및 URL 오류 처리

## 기술 스택

- **Python 3.x**
- **asyncio** - 비동기 처리
- **urllib** - HTTP 요청 및 파일 다운로드

## 설치 및 실행

### 사전 요구사항

- Python 3.7 이상

### 1. 저장소 클론

```bash
git clone https://github.com/herbpot/videoDownloaderFor_mp4.git
cd videoDownloaderFor_mp4
```

### 2. 실행

```bash
python app.py
```

## 사용 방법

### 기본 사용

1. 프로그램 실행
2. 다운로드할 동영상 URL 입력
3. 계속해서 다른 URL 추가 가능
4. `end` 입력 시 다운로드 시작

```
저장할 영상의 url입력 (end입력시 종료)>>> https://example.com/video.mp4
저장할 영상의 url입력 (end입력시 종료)>>> https://example.com/another_video
저장할 영상의 url입력 (end입력시 종료)>>> end
video.mp4 다운로드 중..
video.mp4 저장 완료
another_video.mp4 다운로드 중..
another_video.mp4 저장 완료
```

## 핵심 코드

### 비동기 다운로드 함수

```python
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
```

### 파일명 정제

Windows 파일 시스템에서 사용할 수 없는 문자를 제거:
- `/` - 슬래시
- `:` - 콜론
- `*` - 별표
- `?` - 물음표
- `"` - 큰따옴표
- `<>` - 부등호
- `|` - 파이프

### HTTPS 자동 전환

```python
url = urlparse(ans)
url = url._replace(scheme='https')
```

## 프로그램 흐름

```
1. URL 입력 루프 시작
   └─> URL 수집
   └─> "end" 입력 시 종료

2. 다운로드 단계
   └─> 각 URL에 대해 save_video() 호출
   └─> 파일명 정제
   └─> urllib.request.urlretrieve()로 다운로드
   └─> 완료 메시지 출력
```

## 에러 처리

### HTTPError

```
urllib.error.HTTPError: HTTP Error 404: Not Found
```
- URL이 존재하지 않거나 접근 불가능한 경우

### URLError

```
urllib.error.URLError: <urlopen error [Errno -2] Name or service not known>
```
- 네트워크 연결 문제 또는 잘못된 URL 형식

## 제한사항

- **동기식 다운로드**: asyncio를 사용하지만 실제로는 순차적으로 다운로드
- **진행률 표시 없음**: 대용량 파일 다운로드 시 진행 상황 확인 불가
- **재시도 기능 없음**: 다운로드 실패 시 자동 재시도 없음
- **인증 미지원**: 로그인이 필요한 사이트는 다운로드 불가

## 향후 개선 방향

- [ ] 실제 비동기 병렬 다운로드 구현
- [ ] 진행률 표시 바 추가 (tqdm)
- [ ] 재시도 로직 추가
- [ ] 대용량 파일 지원 (청크 단위 다운로드)
- [ ] GUI 인터페이스 추가
- [ ] 다운로드 이력 관리
- [ ] YouTube-DL 통합 (YouTube 등 지원)

## 성능 최적화 아이디어

### 실제 비동기 다운로드

현재는 `asyncio.run()`을 반복문에서 호출하므로 순차 실행됩니다. 진정한 비동기 다운로드를 위해:

```python
# 개선안
async def download_all(urls):
    tasks = [save_video(url) for url in urls]
    await asyncio.gather(*tasks)

asyncio.run(download_all(urls))
```

### 진행률 표시

```python
from tqdm import tqdm

def progress_hook(block_num, block_size, total_size):
    downloaded = block_num * block_size
    percent = downloaded / total_size * 100
    print(f'\r진행률: {percent:.1f}%', end='')

rq.urlretrieve(url, save_name, reporthook=progress_hook)
```

## 사용 예시

### 단일 파일 다운로드

```bash
python app.py
저장할 영상의 url입력 (end입력시 종료)>>> https://example.com/sample.mp4
저장할 영상의 url입력 (end입력시 종료)>>> end
sample.mp4 다운로드 중..
sample.mp4 저장 완료
```

### 여러 파일 다운로드

```bash
python app.py
저장할 영상의 url입력 (end입력시 종료)>>> https://example.com/video1.mp4
저장할 영상의 url입력 (end입력시 종료)>>> https://example.com/video2.mp4
저장할 영상의 url입력 (end입력시 종료)>>> https://example.com/video3.mp4
저장할 영상의 url입력 (end입력시 종료)>>> end
video1.mp4 다운로드 중..
video1.mp4 저장 완료
video2.mp4 다운로드 중..
video2.mp4 저장 완료
video3.mp4 다운로드 중..
video3.mp4 저장 완료
```

## 주의사항

### 저작권

⚠️ **중요**: 이 도구는 개인적인 용도로만 사용하세요.

- 저작권이 있는 콘텐츠 무단 다운로드 금지
- 다운로드 전 저작권 확인 필요
- 상업적 이용 금지

### 합법적 사용

- 본인이 업로드한 파일
- 저작권자의 허락을 받은 경우
- 퍼블릭 도메인 자료
- Creative Commons 라이선스 준수

## 트러블슈팅

### SSL 인증서 오류

```python
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

### 대용량 파일 타임아웃

```python
import socket
socket.setdefaulttimeout(300)  # 5분
```

## 대안 도구

더 강력한 기능이 필요한 경우:

- **youtube-dl**: YouTube 등 다양한 사이트 지원
- **yt-dlp**: youtube-dl의 개선 버전
- **requests + tqdm**: 더 세밀한 제어 가능
- **wget**: 커맨드라인 다운로드 도구

## 참고 자료

- [urllib.request 문서](https://docs.python.org/3/library/urllib.request.html)
- [asyncio 문서](https://docs.python.org/3/library/asyncio.html)
- [정규표현식 re 모듈](https://docs.python.org/3/library/re.html)

## 라이선스

교육 목적으로 작성된 프로젝트입니다.
