# hyperlinker-hyunzy

## 🔐 로그인 후 기능 사용 (보안)

### 🔑 로그인 / 회원가입 - JWT 인증 방식
일반 로그인 / 회원가입을 제공합니다.

![JWT 로그인](core/static/images/EA2877D7-FB37-442D-8AD4-778963D599A8.jpeg)
![회원가입](core/static/images/CD2B2622-CC2F-44FC-85B9-62BC11DB3C69.jpeg)
![로그인 UI](core/static/images/2720FAF3-17A5-4944-B7B5-74D98FC074A7.jpeg)

### 🌐 로그인 / 회원가입 - 구글 간편 로그인
구글 계정을 활용한 간편 로그인을 지원합니다.

![구글 로그인](core/static/images/419F9E08-B83A-48CF-836E-268F2B43447D.jpeg)
![구글 인증](core/static/images/64DE6424-2E3F-407D-8AD9-AA2BF9083AF8.jpeg)

---

## 🔗 웹 링크 관리

### 📌 웹 링크 등록, 수정, 삭제
사용자는 자신만의 웹 링크를 추가하고 수정하거나 삭제할 수 있습니다.

![링크 관리](core/static/images/10AC8ED0-18FD-4FC7-87BF-5227628FFCF9.jpeg)
![링크 관리 추가](core/static/images/019E2312-DD9A-445B-9FCF-3A8B6EF6BCBB.jpeg)

### ✅ 공유 기능 사용법
1. 공유할 링크의 **🔗 공유 버튼**을 클릭합니다.
2. 공유할 대상 유저를 선택하고 **✅ 확인 버튼**을 누릅니다.
3. 마이페이지에서 공유된 링크를 확인할 수 있습니다.

### ✅ 권한 관리
- 공유한 링크는 마이페이지의 **📤 내가 공유한 링크**에서 관리할 수 있습니다.
- 다른 사용자에게 부여한 쓰기 권한(✍️)을 설정하거나 해제할 수 있습니다.
- **공유받은 링크**는 **📥 내가 공유받은 링크**에서 확인 가능합니다.

### ✅ 확인
- `hyunzy engel` 계정에서 `hyunzy` 계정으로 공유한 후, `hyunzy`로 로그인하면 공유받은 링크를 확인할 수 있습니다.


## 📤 공유 및 권한 관리

### 🗂 마이페이지 - 내가 공유한 링크 / 공유 받은 링크 확인
공유한 링크와 공유받은 링크를 한눈에 확인할 수 있습니다.

![마이페이지](core/static/images/0B48BB7E-D4A5-439E-8505-66D50E0A6BBE.jpeg)
![공유 받은 링크](core/static/images/42E8E5F8-1A7F-4603-87BC-C3420F59ABC1.jpeg)
![링크 권한 관리](core/static/images/83A9E03C-3E09-49FA-B22C-1FD49C4F3C72.jpeg)

---

## 🔍 검색 및 필터

### 🔎 검색 및 카테고리별 링크 정리
필요한 링크를 검색하고, 카테고리별로 정리할 수 있습니다.

![검색 기능](core/static/images/7B3DB010-BB17-4C79-ACC0-4B464AF8FC2B.jpeg)
![카테고리 필터](core/static/images/2B2BC068-05C3-4026-BDB3-E1D5B0E9CE94.jpeg)

---

## 📌 프로젝트 정보

- **기술 스택**: javaScript, python, Django, SQLite, JWT 인증
- **주요 기능**: 링크 관리, 검색, 공유 및 권한 관리, JWT 및 구글 로그인
- **개발 목표**: 보안이 강화된 웹 링크 저장 및 공유 플랫폼 제공

## 📌 설치 및 실행 방법

```bash
# 파일 설치 및 실행
pip install -r requirements.txt
python manage.py runserver
```
---

## 🔍 트러블슈팅 경험 및 느낀 점

개발 과정에서 Django를 활용하며 다음과 같은 주요 문제를 해결하는 경험을 하였습니다.

### 1️⃣ Django에서 커스텀 User 모델을 적용할 때 ORM 충돌 발생
- `AUTH_USER_MODEL` 변경 시 기존 `auth.User` 모델을 참조하여 오류 발생
- `get_user_model()`을 사용하여 유연성을 확보하는 것이 중요
- 마이그레이션과 데이터베이스 변경 시 충돌을 방지하기 위한 사전 점검 필요

### 2️⃣ **Django WebLink API 성능 최적화 및 데이터 정합성 강화**
Django REST Framework 기반으로 WebLink API를 구현하면서 성능 최적화 및 데이터 정합성 유지가 중요한 문제로 떠올랐습니다.

#### 🔹 문제점
- `get_queryset()`에서 `|` 연산자를 사용하여 **불필요한 중복 쿼리 실행**
- `partial_update()`에서 **ManyToMany 관계를 전체 조회 (`all()`)** 하여 **비효율적인 쿼리 발생**
- `web_link.shared_with.add(*users)` 실행 중 **일부 데이터만 저장되는 문제** 발생 가능  

#### ✅ **해결 방법**
1. **Q 객체 활용** → 중복 쿼리 제거 및 성능 최적화  
   ```python
   WebLink.objects.filter(Q(created_by=user) | Q(shared_with=user)).distinct()

### 🔹 느낀 점
이 과정에서 Django의 ORM과 인증 시스템을 보다 깊이 이해하게 되었으며,
백엔드와 프론트엔드 간의 인증 흐름을 설계하는 데 중요한 개념들을 익혔습니다.
또한, 실무에서 **보안성과 유지보수성을 고려한 인증 로직 설계**가 필수적임을 다시 한번 깨달았습니다.

---