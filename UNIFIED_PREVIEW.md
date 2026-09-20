# FedOps 로컬 미리보기 · 2026-09-20

## 확정한 역할 분리

- 홈페이지: `http://127.0.0.1:4313/version-2/`. 상단 메뉴는 Home / Docs / Blog / News.
- Docs: `https://gachon-cclab.github.io/fedops-docs-1.3/`로 직접 연결. 홈페이지에서 별도 문서 본문을 만들지 않는다. 과거 로컬 `/document/` 주소는 공식 문서로 이동한다.
- Blog / News: `content/blog/*.md`, `content/news/*.md`를 수정하고 Git으로 관리한다. DB나 관리자 CMS를 사용하지 않는다.
- Console: 별도 `Open Console` 버튼으로 `http://127.0.0.1:4314/fedops/task`에 접근한다. 별도 pod 배포를 전제로 홈페이지와 실행 환경을 분리한다.
- Console 내부는 기존 My Federated Tasks / Registry / 상세 / 로그인 구조를 유지한다. 기존 Header에 홈페이지로 돌아오는 링크만 추가했다.

## 실행

```powershell
cd C:\Users\wjdwl\project\lab\fedops-homepage-1.3
.\start-preview.ps1
```

이미 해당 포트에서 실행 중인 서버는 중복 생성하지 않는다. 수정한 홈페이지는 `python build.py`로 생성한 뒤 새로고침한다. Console 환경변수를 바꾸면 개발 서버를 재시작한다.

## Markdown 글 관리

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

본문과 **강조**, [공식 문서](https://gachon-cclab.github.io/fedops-docs-1.3/)를 작성한다.
```

`status: published`이면서 `sample: true`가 아닌 글만 빌드한다. Markdown 편집 → 로컬 빌드·확인 → Git diff 검토 → 커밋/리뷰가 기본 작업 순서다. 원격 저장소 및 자동 배포 연결은 아직 설정하지 않았다.

기존 홈페이지의 개발 프리뷰 News 글을 Markdown으로 옮겨 유지했다. 임의로 추가했던 네 개의 예시 초안은 파일에만 남기고 목록·본문 출력에서 제외했다. Blog는 게시할 글이 없을 때 빈 목록을 표시한다.

렌더러는 소제목, 문단, 글머리 목록, 굵게, 인라인 코드, 링크와 `/assets/`의 이미지를 지원한다. 원시 HTML은 이스케이프한다. 별도 DB나 Python 패키지가 필요 없다.

## 수정 위치

- `build.py`: 홈페이지 섹션, Console 주소, Docs 링크 매핑.
- `unified.py`: 홈페이지 / Blog / News 공통 메뉴와 Markdown 빌드. Console URL도 여기에서 설정한다.
- `dist/assets/site.css`, `unified.css`: 스타일. `dist/assets/`에는 원본 이미지와 스크립트가 있으므로 보존한다.
- `content/blog/`, `content/news/`: Markdown 글.
- `work/flower-profile.json`: GFedOps 앱 수·스타 수와 확인 날짜. 2026-09-20 공식 프로필에서 7 / 103을 확인했다. 자동 갱신 수치가 아니다.
- `../FedOps-Web/client/src/components/common/Header.js`: 기존 Console 메뉴. 홈페이지 주소는 `REACT_APP_FEDOPS_HOME_URL`로 분리되어 있다. CRA 빌드 시 주입되므로 배포 주소 변경 후 재빌드한다.

기존 Agent Studio / Flower 캡처와 Design Partner 로고는 유지한다. `/`와 `/version-2/`는 같은 홈페이지다. 새로 디자인했던 `ConsolePreview`는 실행 경로에서 제외되어 있다.

## 백업

이번 수정 직전 실제 소스 백업은 `../fedops-integration-backups/before-scope-correction-20260920-230245/source-snapshot.zip`이다. 원격 서비스나 운영 DB는 변경하지 않았다.
