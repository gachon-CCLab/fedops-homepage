# FedOps 1.3 Homepage — local proposal

> **최신: 2026-09-20 역할 분리 반영** — 실행과 구성은 [UNIFIED_PREVIEW.md](UNIFIED_PREVIEW.md)를 확인하세요. `start-preview.ps1`로 홈페이지와 기존 Console을 함께 실행합니다. Docs는 공식 사이트로 연결하고 Blog/News는 Markdown에서 빌드합니다. 아래는 초기 시안의 기록이며 현재 동작은 최신 문서를 따릅니다.

로컬에서 수정·검토하기 위한 홈페이지 시안입니다. 기존 서비스와 Notion·GitHub 문서는 수정하지 않았습니다. 공개 배포하지 않았습니다.

## 실행

Python 3.11 이상이면 별도 라이브러리 설치 없이 실행할 수 있습니다.

```powershell
cd C:\Users\wjdwl\project\lab\fedops-homepage-1.3
python build.py
python serve.py --port 4313
```

브라우저에서 <http://127.0.0.1:4313/>을 엽니다. 종료는 해당 터미널에서 Ctrl+C입니다. 서버는 127.0.0.1에만 바인딩합니다. `dist/index.html` 더블클릭 대신 로컬 서버로 열어주세요.

## 페이지

Document 메뉴·푸터·문서 CTA는 공개된 [FedOps 1.3 Docs](https://gachon-cclab.github.io/fedops-docs-1.3/)로 연결합니다. Getting Started, Owner, Participant, Campaign 및 Resources 버튼은 해당 문서의 세부 페이지로 연결합니다. 주소 매핑은 `build.py`의 `DOCS`와 `DOC_LINKS`에서 관리합니다. 아래 `/document/` 로컬 페이지들은 이전 시안으로 보존하며 홈페이지의 문서 진입점에서는 사용하지 않습니다.

| 경로 | 내용 |
|---|---|
| `/` | FL 생명주기 소개, Why FedOps, Design Partner, 제품 화면, 구성요소, 생명주기, 시작 안내, News, Community |
| `/document/` | 역할별 가이드와 Resources, 기존 Docs 연결 |
| `/document/overview/` | 1.3 소개·구조·생명주기 |
| `/document/getting-started/` | 설치 원문과 역할별 시작 안내 |
| `/document/task-owner/` | Manual 01·02로 연결하는 Owner 요약 |
| `/document/participant/` | Manual 03 기반 참여 흐름 요약 |
| `/document/agent-builder/` | Manual 04와 Agent Build 개념 요약 |
| `/document/campaign/` | Manual 05 기반 운영 요약 |
| `/document/developer-guide/` | 1.3 개발 계약 핵심 요약 |
| `/news/` | 개발 현황 소개 목록 |
| `/news/fedops-1-3-preview/` | 제공된 1.3 자료에서 작성한 개발 소개 시안 |
| `/blog/` | 게시 글이 없는 상태와 문서·연구 진입점 |

## 어디를 수정하면 되나요?

| 수정 대상 | 파일 |
|---|---|
| 메인 본문·섹션 순서·메뉴·푸터 | `build.py` |
| 색상·폰트·간격·모바일 배치 | `dist/assets/site.css` |
| 모바일 메뉴·제품 화면 탭 | `dist/assets/site.js` |
| Document·News·Blog 본문 | `pages/*.html` |
| 각 내부 페이지의 제목·설명·경로 | `pages/*.json` |
| 제품 스크린샷 제목·설명 | `work/screens.json` |
| 제품 스크린샷 이미지 | `dist/assets/studio-01.png` ~ `studio-06.png` |

`build.py` 또는 `pages/` 수정 뒤에는 `python build.py`를 실행하고 브라우저를 새로고침합니다. CSS/JS는 직접 수정 후 새로고침하면 됩니다. `dist/*.html`은 생성 결과라 직접 수정하면 다음 빌드에서 덮어써집니다.

`work/seed_pages.py`는 최초 본문을 생성한 기록입니다. 이미 작성된 `pages/` 파일을 다시 초기화하므로 일반 수정 시 재실행하지 않습니다. `work/extract_assets.py`도 최초 이미지 추출 기록이며 이후 빌드에서는 필요하지 않습니다.

## 적용한 방향

- 교수님 `index.html`의 네이비·민트 색상, 타이포그래피, 기능 흐름과 원본 제품 화면을 기반으로 구성했습니다.
- 민혁 선배님 시안처럼 상단 메뉴는 Document / News / Blog, 우측은 GitHub와 FedOps Console로 구분했습니다.
- Get Started는 공개된 1.3 Docs의 Getting Started로, Console은 기존 `/fedops/task`로 연결합니다.
- 실제 Registry 진입은 구성요소 설명의 Open Registry 및 참여 가이드에서 기존 `/fedops/registry`로 연결합니다.
- 첫 소개 → Why FedOps·Design Partner → 제품 화면 → 구조 → 생명주기 → 시작 안내 → News → Community 순서로 구성했습니다.
- 첫 소개 문구, Why FedOps의 5개 설명, Design Partner, Community 문구와 Slack 초대 주소는 선배님 `homepage-v1.3.html`에서 가져왔습니다. Why FedOps는 제공된 기존 설명을 재사용한 것이며 각 기능의 1.3 호환성을 새로 검증한 내용은 아닙니다.
- Design Partner 로고 3개는 기존 운영 홈페이지가 사용하는 `/fedops/img/gachon.jpeg`, `/fedops/img/flower.png`, `/fedops/img/cambridge.png` 원본을 로컬 자산으로 보관했습니다.
- 로고 심볼과 파비콘은 처음 시안의 민트색 마름모 형태를 사용합니다.
- PC·태블릿·모바일의 반응형 배치와 모바일 메뉴, 키보드 탭 이동, Escape 메뉴 닫기, reduced motion을 포함했습니다.

## 문서·콘텐츠 범위

- 현재 Document 진입점은 별도로 공개된 1.3 Docs입니다. 로컬에 보존된 Document는 이전 **요약 안내와 원문 연결을 위한 홈페이지 시안**이며, Notion의 모든 본문·이미지를 기존 Jekyll Docs로 이관한 결과가 아닙니다.
- Manual 00·01·02·04는 이번 작업에서 전체 원문을 새로 검증한 문서가 아닙니다. 공개 원문으로 연결하고, 읽었던 메인 문서의 시나리오 범위에서 요약했습니다.
- Manual 02의 작성 중 상태, Manual 05의 확인 필요 순서가 남아 있음을 숨기지 않았습니다.
- 고급 기능 LLM/VLM/FedMAP/HPO/XAI가 1.3에서 모두 동작한다고 표시하지 않았습니다.
- News의 개발 소개는 시안용으로 편집한 글이며 실제 게시 이력·출시 날짜를 만들어 넣지 않았습니다. 최종 공개 전 문구 확인이 필요합니다.
- Blog는 실제 게시물이 없는 상태입니다. 글 작성·관리·검색용 CMS나 로그인 기능은 만들지 않았습니다.
- 모든 소개는 개발 프리뷰로 표시했습니다. 제품 기능의 실제 실행 또는 1.3 출시 여부를 검증한 결과는 아닙니다.

## 배포 판단

배포 주소는 이번에 확정하지 않았습니다. 우선 새 홈페이지를 서비스 루트에 두는 구조로 작성했습니다. 최종 `/fedops` 아래에서 제공할 경우 정적 자산·내부 링크의 base path 및 기존 앱 라우팅을 적용해야 합니다. 현재 기존 Task/Registry 경로와 로그인 동작은 변경하지 않았습니다.

`.openai/hosting.json`은 정적 출력 위치만 선언하며, 원격 사이트 등록이나 업로드는 하지 않았습니다.

## 점검

로컬 서버를 실행한 상태에서:

```powershell
python work/validate.py
node --check dist/assets/site.js
```

검사는 페이지별 HTTP 응답, 내부 링크·앵커·이미지 파일, 중복 ID와 대체 텍스트, JS 문법을 확인합니다. 외부 서비스 로그인·연합학습 실행은 검사하지 않습니다.
