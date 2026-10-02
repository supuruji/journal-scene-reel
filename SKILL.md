---
name: 논문-도해영상
description: 논문·학술지 원고(.docx/.hwpx)를 받아 중국어판·한국어판을 전환할 수 있는 시네마틱 16:9 애니메이션 "도해"(자동 재생 슬라이드 릴)를 만든다. 각 논문을 분야 태그·중/한/영 제목·저자·핵심 논지 한 줄로 한 장면씩 구성하고, 장면마다 음성 내레이션(브라우저 TTS 또는 네이버 클로바 보이스 mp3)을 넣는다. 산출은 HTML(화면녹화용) 또는 ffmpeg+헤드리스 Chrome으로 합성한 **완성 MP4(유튜브 바로 업로드 가능, 음성 포함)** 중 선택. "논문 도해 동영상 / 논문 소개 영상 / 중국어판 한글판 도해 / 학술지 소개 영상 / 유튜브용 논문 도해 / 권 전체 소개 영상 / 논문 인트로 영상 / 소리(내레이션)·클로바 음성 영상 / 논문 소개 MP4" 요청 시 사용.
---

# 논문 도해 영상 (Paper Illustrated Intro Reel)

논문 한 편 또는 학술지 한 권 전체를, **중국어(中文)·한국어 2개 버전을 토글로 전환**할 수 있는
**음성 내레이션 포함 자동 재생 16:9 애니메이션 도해**로 만든다. 산출은 둘 중 택:
- **(A) HTML 도해** — 브라우저 전체화면 재생/화면녹화용(즉시 확인·공유).
- **(B) 완성 MP4** — `ffmpeg` + 헤드리스 Chrome으로 각 장면을 1920×1080 정적 캡처하고 클로바/TTS
  음성과 합성해 **바로 유튜브 업로드 가능한 mp3 포함 MP4**를 만든다(화면 녹화 불필요·싱크 완벽).
  ffmpeg/ffprobe와 Chrome(또는 Edge)이 있어야 한다.

## 언제 쓰나
- "이 논문/학술지 소개 동영상 만들어줘", "중국어판·한글판 도해 영상"
- 학술지 한 권(여러 논문)을 각 논문 한 장면씩 소개하는 인트로 영상
- 논문 한 편을 심화 도해(핵심 논지·구조)로 소개하는 영상

## 먼저 확정할 것 (AskUserQuestion)
1. **대상**: 권 전체 소개(논문마다 한 장면) vs 특정 논문 1편 심화. 원고가 학술지 전체면 목차를 보여주고 고르게 한다.
2. **언어**: 기본은 **중국어+한국어 2개 버전(토글)**. 요청에 맞게 조정(영문 추가 등).
3. (산출 형태는 이 스킬의 기본값인 HTML 애니메이션 도해로 진행 — 이미 정해졌으면 건너뛴다.)

## 산출물
1. **HTML 도해** — `<원고폴더>/<약칭>_소개도해.html`(통합 토글) + `_한글.html`/`_中文.html`. Artifact publish+open.
2. **완성 MP4**(요청 시) — `<약칭>_소개_한글.mp4` / `_中文.mp4`(1080p·음성 포함). `render_video.py`로 생성.

---

## 절차

### 1) 원고에서 데이터 추출
`.docx`는 동봉 스크립트로 문단 텍스트를 UTF-8 파일로 뽑는다(콘솔 cp949 깨짐 방지 — **반드시 파일로**):
```bash
python "<스킬>/scripts/extract_docx.py" "<원고.docx>" "<scratchpad>/clean.txt"
```
`.hwpx`면 `hwpx-편집` 스킬 방식으로 텍스트를 얻는다.

clean.txt에서 아래 세 곳을 찾아 논문별로 매핑한다 (대순사상학술원 JEARC 등 중문 학술지 기준):
- **`CONTENTS` (영문 목차)** → 논문별 **영문 제목 + 저자(로마자)·소속**
- **`中文目錄`** → 논문별 **중문 제목**
- **`編者序`/`编者序` (편집자 서문)** → 논문별 **한 줄 핵심 논지**(저자 중문명 포함). ★도해의 핵심 소스★
  서문이 없으면 각 논문 **초록(Abstract)**에서 1~2문장으로 논지를 요약한다.

한국어는 중문 논지·제목을 **간결히 번역**해 넣는다(제목은 핵심 한자어 병기 권장: 예 "봉도(奉道)").
저자명 한국어는 한국인은 한글 실명, 외국인은 통용 음차(예: 베트남 성명, 중국 병음 한글표기).

### 2) 장면 구성
`title`(표지) → `overview`(이번 호 개관·논문 수) → 논문 N장면 → `closing`(편집자·발간처).
각 논문 장면 데이터:
```js
{n:1, tag:{ko:"불교 · 선종", zh:"佛教 · 禪宗"},     // 분야 태그(실제 주제 — 장식 아님)
 en:"English Title ...",
 who:{ko:"고문서", zh:"高文緒"}, lat:"GAO Wenxu", aff:"Beijing Language and Culture University",
 t:{ko:"《유마힐경》 문자설법론", zh:"《維摩詰經》文字說法論"},
 s:{ko:"한 줄 논지(1~2문장)…", zh:"一兩句核心論旨…"}}
```
`aff`(소속)가 원고에 없으면 `""`로 두고, **지어내지 말고** 사용자에게 보완 요청.

### 3) 템플릿에 데이터 주입
`templates/scene-reel.template.html`을 복사해 **DATA 블록만 교체**한다
(`/* DATA */` ~ `/* RENDER */` 사이: `PAPERS`, `EDITOR`, 그리고 `sceneHTML()`의
title/overview/closing 카피). **RENDER / PLAYER 엔진·CSS는 건드리지 않는다.**
- `<title>`은 학술지 약칭으로(예: "JEARC 3·2 소개 도해").
- `DUR`(장면 길이)·장면 수에 맞게 조정 가능(기본 논문당 9초).

### 4) 저장 + 게시
- HTML을 **원고 폴더**에 저장.
- Artifact로 **publish**(icon: `film`) 후 **open**. (게시 전 artifact-design의 1회 preview 점검 권장.)

---

## 음성 내레이션 (TTS)
- 템플릿에 **Web Speech API(`speechSynthesis`)** 내레이션이 내장돼 있다. **재생을 누르면**(사용자 제스처)
  장면마다 현재 언어로 제목+논지를 읽어주고, **음성 종료 시 다음 장면으로 자동 전환**(음소거면 타이머 전환).
- 소리 버튼(`🔊`/`M` 키)으로 켜고 끈다. 기본 켜짐.
- 음성 엔진은 OS 설치분을 쓴다. Windows에는 보통 한국어(Heami)·중국어(zh-CN) 음성이 있다.
  없으면 소리가 안 나므로, 필요 시 **설정 > 시간 및 언어 > 음성**에서 해당 언어 음성을 추가하도록 안내.
- **화면 녹화 시 "시스템 오디오(장치 소리)" 캡처를 켜야** 내레이션이 녹음된다(게임바: 마이크 아님/시스템 소리).
- 내레이션 문구는 `narrText()`에서 생성(책이름 괄호·한자 병기 자동 정리). 특수 멘트는 거기서 조정.

## 고품질 중국어 음성 = 네이버 클로바 (CLOVA Voice)
브라우저 중국어 TTS 대신 **클로바에서 만든 mp3**를 쓰려면(권장: 자연스러움·일관성):
1. **인증키 준비(사용자)**: 네이버 클라우드 플랫폼 → CLOVA Voice(Premium) 이용 신청 → Client ID/Secret.
   키는 **파일에만** 둔다(채팅/화면 출력 금지, 외부 전송 금지). 2줄 파일 `clova_key.txt`(1줄 ID, 2줄 Secret)
   또는 환경변수 `NCP_CLIENT_ID` / `NCP_CLIENT_SECRET`.
2. **생성** (언어별로 1회씩):
   ```bash
   # 중국어
   python "<스킬>/scripts/clova_voice.py" --html "<베이스.html>" --keyfile "<clova_key.txt>" \
     --lang zh --speaker meimei --out "<scratchpad>/zh_audio.js"
   # 한국어
   python "<스킬>/scripts/clova_voice.py" --html "<베이스.html>" --keyfile "<clova_key.txt>" \
     --lang ko --speaker nara  --out "<scratchpad>/ko_audio.js"
   ```
   - 성우(speaker): 중국어 `meimei`(여)·`liangliang`(남)·`chiahua`(대만) / 한국어 `nara`(여)·`jinho`(남)·`nminyoung` 등.
   - 속도: 빠르면 `--speed 1`(양수=느리게). HTML의 해당 언어 장면 텍스트를 추출해 장면별 mp3 생성.
   - 출력: `window.__ZH_AUDIO` / `window.__KO_AUDIO = {장면index:"data:audio/mp3;base64,..."}` 스니펫.
   - **베이스 HTML**: 음성이 아직 안 들어간 깨끗한 빌드본을 쓴다. 이미 음성이 주입된 파일을 다시 쓰려면
     먼저 `<script>…window.__ZH_AUDIO…</script>` / `__KO_AUDIO` / `__START_LANG` 주입 블록을 제거해 베이스를 복원.
3. **주입**: zh_audio.js·ko_audio.js 내용을 한 `<script> … </script>` 로 **메인 스크립트 앞에 인라인** 삽입
   (`window.__START_LANG` 주입과 같은 자리). 통합본·언어별 파일 모두에 넣으면, `clipFor()`가 현재 언어의
   `__ZH_AUDIO`/`__KO_AUDIO`에서 장면 오디오를 찾아 재생(없으면 자동 TTS 폴백).
4. 생성 후 **키 파일 삭제**.
- 비용: 글자당 과금(소액). 20장면×2언어 ≈ 수천 자 수준.

## MP4로 렌더링 (권장 — 화면 녹화 불필요)
`render_video.py`가 각 장면을 헤드리스 Chrome으로 **정적 1920×1080 캡처**(`#shot{n}`)하고,
클로바/TTS mp3와 ffmpeg로 합성해 장면 전환 페이드까지 넣어 이어붙인다. **베이스 HTML은 음성이
인라인 주입되지 않은 빌드본**(엔진+데이터)을 쓴다.
```bash
# 한국어
python "<스킬>/scripts/render_video.py" --base-html "<베이스.html>" --lang ko \
  --audio "<ko_audio.js>" --out "<폴더>/<약칭>_소개_한글.mp4" --workdir "<scratchpad>/vid"
# 중국어
python "<스킬>/scripts/render_video.py" --base-html "<베이스.html>" --lang zh \
  --audio "<zh_audio.js>" --out "<폴더>/<약칭>_소개_中文.mp4" --workdir "<scratchpad>/vid"
```
- `--audio` 생략 시 각 장면 `--seconds`(기본 7초) 무음 + `--scenes N`.
- Chrome 경로 자동탐색(미발견 시 `--chrome`). 결과: H.264 1080p + AAC stereo.
- 검증: `ffprobe`로 스트림 확인, `volumedetect`로 무음 아님 확인.

### (신규) render_mp4.mjs — 실시간 애니메이션 렌더 (음성 내장 HTML에서)
`render_video.py`가 장면별 **정적** 캡처라면, `scripts/render_mp4.mjs`는 **음성이 이미 인라인 주입된
완성 HTML**(`_한글.html`/`_中文.html`)을 헤드리스 Chrome에서 **실시간으로 재생·캡처**해 장면 안 애니메이션까지
담은 MP4를 만든다. 내레이션은 HTML에 박힌 클립(`__KO_AUDIO`/`__ZH_AUDIO`, film형은 `line.a`)에서 각 장면이
실제로 뜨는 시점에 맞춰 재합성한다. **film·reel 두 플레이어 자동 감지.** Node 18+/Chrome/ffmpeg만 필요(무설치).
```bash
node "<스킬>/scripts/render_mp4.mjs" "<폴더>/<약칭>_소개도해_한글.html" "<폴더>/<약칭>_소개_한글.mp4"
```
- 컨트롤바(`#controls`)·안내문(`.hint`)은 렌더 시 자동 숨김, 1920×1080 패딩 출력.
- 캡처는 **실시간**(영상 길이만큼 소요). 빠른 정적 결과가 필요하면 `render_video.py`를 쓴다.

### charset (한글/中文 깨짐 방지)
scene-reel 템플릿 맨 앞에 `<!DOCTYPE html>` + `<meta charset="utf-8">`가 있어야 한다 — 없으면 브라우저가
**EUC-KR**로 오판해 글자가 `` 로 깨진다. 템플릿에 반영됨. `render_mp4.mjs`도 UTF-8 헤더로 서빙해 이중 안전.

## (대안) 화면 녹화로 만들기
1. 언어별 HTML(`_한글.html` / `_中文.html`) 열기 → **전체화면(`F`)** → **재생(`Space`)**
2. 화면 녹화(Windows `Win+G`/OBS)에서 **"시스템 오디오" ON** → 내레이션 녹음
- 조작: `Space` 재생/정지 · `←``→` 이동 · `L` 언어 · `M` 음소거 · `F` 전체화면

## 디자인 원칙 (템플릿에 반영됨)
- **committed dark** 시네마틱 톤. 학술지 마스트헤드 색을 accent로(JEARC=틸 `#12b6c8`), 일련번호는 금박.
- 서체: 한국어 `Noto Serif KR` / 중국어 `Noto Serif SC` / 로마자 `Cormorant Garamond`(Google Fonts).
- `#stage`는 `container-type:size` + `cqw/cqh` 단위라 **녹화 해상도와 무관하게** 레이아웃이 비율로 스케일된다.
- 분야 태그·일련번호는 **실제 정보**(장식 아님). 장면마다 제목·논지·저자가 순차 페이드인, `prefers-reduced-motion` 존중.

## 전체 파이프라인 요약
`extract_docx.py`(원고→텍스트) → 데이터 매핑 → 템플릿에 주입(빌드본 HTML) → [선택] `clova_voice.py`(언어별 mp3)
→ HTML에 음성 인라인 주입(화면용) **또는** `render_video.py`(완성 MP4) → 저장/게시.

## 주의
- 소속·저자명 등 **불확실한 정보는 지어내지 않는다**(공란 후 확인).
- 긴 논지는 화면을 넘칠 수 있으니 2문장 이내로. preview로 오버플로 확인.
- 저작권: 원고 본문 전체가 아니라 **제목·저자·핵심 논지(서문 요약)** 수준만 노출한다.
