# SKN14-1st-2 Team

- SK 네트웍스 AI Camp 1차 프로젝트

---

## 👥 팀원 소개

| 캐릭터 | 이름  | 역할 | 담당 업무 |
|:-----:|:-----:|:-----:|-----|
| ![](./images/euiyoung.png) | 김의령 |추후 기입|추후 기입|
| ![](./images/junki.png)    | 김준기 |추후 기입|추후 기입|
| ![](./images/iseo.png)     | 윤이서 |추후 기입|추후 기입|
| ![](./images/sungryul.png) | 조성렬 |추후 기입|추후 기입|
| ![](./images/sungkyu.png)  | 한성규 |추후 기입|추후 기입|


---

# 1. 프로젝트 개요

## 1-1. 주제 및 프로젝트 소개

### 🚗 당신의 첫 차, 차근차근 함께 찾아요

✅ 이 웹 애플리케이션은 **사회초년생(첫 직장인/취업 준비생 등)** 을 위한 자동차 추천 서비스를 제공합니다.  
**경제성, 실용성, 유지비 등**을 기준으로 차량을 추천받을 수 있습니다.

## 1-2. 프로젝트 목적 (필요성 or 배경)

- 추후 기입 예정

---

# 2. 🖥️ 프로젝트

## 2-1. 📌 주요 기능

- ✅ 예산, 용도, 선호도, 기능 기반 자동차 추천  
- ✅ 다양한 필터 옵션 (가격, 브랜드, 크기, 연비 등)  
- ✅ 차량 상세 정보 제공 (외부 API 연동)  
- ✅ Streamlit 기반의 직관적인 웹 인터페이스 제공

> 📷 **Streamlit UI 화면은 추후 캡처 이미지로 추가될 예정**

## 2-2. 🛠️ 기술 스택


| 분류 | 기술/도구                                                                                                                                                                                                                                                                                                          |
|------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 언어 | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)                                                                                                                                                                                                          |
| 데이터크롤링 | ![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=green)                                                                                                                                                                                                    |
| 데이터베이스 | ![MySQL](https://img.shields.io/badge/MySQL-4B8BBE?style=for-the-badge&logo=mysql&logoColor=white)                                                                                                                                                                                                              |
| 웹 | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)                                                                                                                                                                                                 |
| 협업 툴 | ![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white),![Notion](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white),![Figma](https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white) |


## 2-3. 📝 요구사항 명세서

### 사용자 관련
- 사용자는 예산범위, 사용용도 등을 기반으로 자동차 추천을 받을 수 있다.
- 사용자의 정보는 `사용자 정보` 테이블에 저장된다.
- 사용자의 직업은 `직업 타입 정보` 테이블을 참조한다.

### 추천 시스템
- 추천 결과는 `차 추천 정보` 테이블에 저장된다.
- 추천은 `사용자`와 `자동차` 의 매칭으로 기록된다.

### 자동차 정보 관리
- 자동차 기본 정보는 `자동차 정보` 테이블에 저장된다.
- 자동차 정보에는 브랜드, 연료 종류, 차종 등의 세부 항목이 포함된다.
- 자동차 브랜드는 `브랜드 정보` 테이블을 참조한다.
- 연료 종류는 `연료 타입 정보` 테이블을 참조한다.
- 차종(바디 타입)은 `바디 타입 정보` 테이블을 참조한다.

### 자동차 리뷰 관리
- 각 자동차에 대한 리뷰는 `차 리뷰 정보` 테이블에 저장된다.
- 리뷰에는 `평균 점수`, `설문 참여자 수` 등이 포함된다.

### 댓글 기능
- 리뷰에 댓글을 남길 수 있다.
- 댓글 데이터는 `댓글 정보` 테이블에 저장되며, 닉네임과 점수, 작성 일자 등이 포함된다.

## 2-4. 🗃️ 테이블 정의서

- 추후 기입 예정

## 2-5. 📅 WBS

- 추후 기입 예정

## 2-6. 📊 플로우차트 (FlowChart)

![](./docs/FlowChart.jpg)

## 2-7. 🧩 ERD

- 추후 기입 예정

---

# 3. 💡사용 방법

- 추후 기입 예정 (시연영상 삽입)

---

# 4. 🕊️ 회고

- 프로젝트 진행 후 느낀 점 및 개선 사항 (추후 기입 예정)

---

# 5. ☑️ 피드백

- 개선 사항 (추후 기입 예정)

---