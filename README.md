# CV3 기술과제 - 라방바 데이터랩 방송 리스트

라방바 데이터랩(`http://live.ecomm-data.com/assignment`)의 라이브방송/홈쇼핑 랭킹을 토글로 전환해 보여주는 페이지입니다.

## 실행 방법

### 1. 백엔드 (FastAPI)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

`http://localhost:8000`에서 서버가 뜹니다. `http://localhost:8000/api/broadcasts?type=lb`로 정상 동작 확인 가능합니다.

### 2. 프론트엔드 (React + Vite)

새 터미널을 열고:

```bash
cd frontend
npm install
npm run dev
```

`http://localhost:5173`에서 화면을 확인할 수 있습니다. (백엔드가 8000번 포트에 떠 있어야 프론트의 `/api` 요청이 정상 동작합니다.)

## 데이터를 가져온 방법

별도의 공식 API가 제공되지 않아, `live.ecomm-data.com/assignment` 페이지가 자체적으로 사용하는 내부 API를 브라우저 개발자도구(Network 탭)로 확인해서 그대로 재현했습니다.

- 방송 목록: `POST https://live.ecomm-data.com/api/assignment/list`, body `{"type": "lb" | "hs"}`
- 라방(lb) 응답에는 분류명이 없고 `cid` 숫자만 내려와서, 같은 사이트의 카테고리 리포트 페이지(`/report/category/{cid}`)를 `cid` 0~300 범위로 순회하며 공식 분류표를 확보해 `backend/app/category_map.py`에 반영했습니다. (조사에 사용한 스크립트: `check_category.py`)
- 홈쇼핑(hs) 응답에는 분류명이 이미 포함되어 있어 그대로 사용했습니다.
- 방송사 표시명(`platform_name`)도 라방 쪽은 원본에 영문 id만 있어 화면에 보이는 실제 표기와 대조해 `backend/app/platform_names.py`에 직접 매핑했습니다.

두 API 모두 요청이 올 때마다(캐시 없이) 매번 새로 호출하므로, 항상 그 시점의 최신 랭킹을 보여줍니다.

## 알려진 제한사항

- 조회수/판매량/매출액은 로그인 없이는 원본 데이터 자체가 제공하지 않아 항상 `🔒 로그인`으로 표시됩니다.
- 라방(lb)의 분류명은 조사 시점(`cid` 0~300)에 확인된 값 기준이라, 그 범위 밖의 새로운 분류가 상위 랭킹에 진입하면 분류가 빈 값으로 표시될 수 있습니다.
