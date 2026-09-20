# FedOps Homepage · Blog · News

FedOps의 정적 홈페이지와 Git으로 작성하는 Blog/News를 관리합니다. Python 3.11 이상만 필요하며 DB나 관리자 CMS를 사용하지 않습니다.

- 홈페이지: https://gachon-cclab.github.io/fedops-homepage/
- Blog: https://gachon-cclab.github.io/fedops-homepage/blog/
- News: https://gachon-cclab.github.io/fedops-homepage/news/
- Docs: https://gachon-cclab.github.io/fedops-docs-1.3/ — 별도 저장소에서 관리합니다.
- Console: https://ccl.gachon.ac.kr/fedops — 별도 서비스로 운영합니다.

## 역할 분리

상단 메뉴는 Home / Docs / Blog / News입니다. Console은 `Open Console` 버튼으로 접근합니다. 이 저장소에는 Console, 로그인 서버, MongoDB, 학습 인프라 코드가 포함되지 않습니다.

홈페이지 / Blog / News는 디자인과 빌드가 같으므로 한 저장소에서 관리합니다. Docs는 매뉴얼 변경과 버전 관리 주기가 달라 기존 저장소를 유지합니다. Console은 별도 pod에서 운영할 수 있도록 URL로만 연결합니다.

## 로컬 미리보기

```sh
python build.py
python serve.py --port 4313
```

http://127.0.0.1:4313/ 에서 확인합니다. `/version-2/`는 같은 홈페이지를 보여주는 기존 미리보기 별칭입니다.

Windows에서 기존 `FedOps-Web/client`가 옆 폴더에 설치되어 있으면 `./start-preview.ps1`로 홈페이지와 로컬 Console을 함께 실행할 수 있습니다. 홈페이지 자체는 Console 없이 실행됩니다.

## 글 작성과 게시

1. `content/blog/` 또는 `content/news/`에 Markdown 파일을 추가합니다.
2. 아래 front matter와 본문을 작성합니다. `slug`는 섹션 안에서 고유해야 합니다.
3. `status: draft`로 준비합니다. 게시할 때 `status: published`로 바꿉니다. `sample: true`인 글은 게시되지 않습니다.
4. 로컬 빌드와 테스트를 확인하고 커밋/PR을 만듭니다.
5. `main`에 반영되면 GitHub Actions가 검사 후 Pages에 배포합니다. 실패한 빌드는 배포하지 않습니다.

```markdown
---
title: 글 제목
slug: article-slug
summary: 목록에 보일 소개
category: Development
status: draft
sample: false
---

## 소제목

본문, **강조**, `인라인 코드`, [문서](https://gachon-cclab.github.io/fedops-docs-1.3/).

1. 첫 단계
2. 다음 단계
```

코드블록, 번호/글머리 목록, 소제목, 문단, 강조, 링크, 인라인 코드, `/assets/` 이미지 경로를 지원합니다. 원시 HTML은 실행하지 않습니다. 전체 CommonMark/MDX 구현은 아닙니다. 이미지는 `dist/assets/`에 넣고 `![설명](/assets/image.png)`으로 참조합니다.

기존 개발 소개 News 한 편을 Markdown으로 옮겼습니다. Blog는 게시된 글이 없어 빈 목록으로 보입니다. 예시 초안은 `draft`/`sample`로 보존하며 배포 HTML에는 포함되지 않습니다.

## 빌드 설정

| 환경변수 | 로컬 기본 | 공개 빌드 |
|---|---|---|
| `FEDOPS_ENV` | `local` | `production` |
| `FEDOPS_BASE_PATH` | 빈 문자열 | `/fedops-homepage` |
| `FEDOPS_OUTPUT_DIR` | `dist` | `_site` |
| `FEDOPS_CONSOLE_URL` | `http://127.0.0.1:4314/fedops/task` | `https://ccl.gachon.ac.kr/fedops` |
| `FEDOPS_REGISTRY_URL` | `https://ccl.gachon.ac.kr/fedops/registry` | `https://ccl.gachon.ac.kr/fedops/registry` |

설정은 `site_config.py`에서 한 번에 관리합니다. 로컬 미리보기의 Home / Docs / Blog / News는 공개 주소를 사용하고 Open Console만 로컬 `4314/fedops/task`를 엽니다. 공개 빌드의 Open Console은 별도 서비스의 공개 주소를 사용합니다. 공개 빌드는 localhost 서비스 주소를 거부하고 저장소 경로를 HTML/이미지 링크에 적용합니다. CSS 이미지는 상대 경로를 사용합니다. GitHub repository variables로 `FEDOPS_CONSOLE_URL`, `FEDOPS_REGISTRY_URL`을 지정하면 Console pod의 공개 주소 변경에 대응할 수 있습니다.

Pages publishing source는 **GitHub Actions**입니다. `.github/workflows/pages.yml`이 테스트 → 공개 빌드 → 정적 검사 → 배포를 수행합니다. PR에서는 빌드/검사만 수행합니다. 기존 Docs 저장소나 Console 배포는 변경하지 않습니다.

## 소스 위치

- `build.py`: 홈페이지 섹션 및 문서 링크 매핑.
- `unified.py`: 공통 메뉴/푸터, Markdown 렌더러, Blog/News 목록/본문.
- `site_config.py`: 환경별 서비스 URL과 Pages 경로.
- `content/blog/*.md`, `content/news/*.md`: 실제 글 작성 위치.
- `dist/assets/`: 원본 PNG, 캡처, CSS, JavaScript. 생성 HTML과 달리 Git에 포함되는 소스입니다.
- `work/screens.json`, `work/flower-profile.json`: 화면 설명 및 GFedOps 수치/확인 날짜.
- `pages/`: 이전 시안의 보존 파일. 현재 Blog/News/Docs 작성 위치가 아닙니다. 빌드에서는 404 템플릿만 사용합니다.

GFedOps 앱 수/스타 수와 리더보드는 확인 날짜를 표시한 스냅샷입니다. 자동으로 갱신하지 않습니다. 새 아이콘은 제공된 원본 PNG를 변형 없이 사용합니다.

## 검증

```sh
python -m unittest discover -s tests -v
python build.py
python work/validate.py
python work/validate.py --url http://127.0.0.1:4313
node --check dist/assets/site.js
```

공개 빌드 후에는 `python work/validate.py --root _site --base-path /fedops-homepage --public`로 프로젝트 경로와 localhost 유출을 함께 검사합니다.

이 검사는 홈페이지/콘텐츠/이동 경로를 확인합니다. Console의 실제 계정 인증, Task/Registry 데이터, 학습 실행은 인증 백엔드가 연결된 환경에서 별도로 검증해야 합니다.
