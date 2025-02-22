# hyperlinker-hyunzy
수정# hyperlinker-hyunzy

## 🔐 로그인 후 기능 사용 (보안)

### 🔑 로그인 / 회원가입 - JWT 인증 방식
일반 로그인 / 회원가입을 제공합니다.

![JWT 로그인](images/EA2877D7-FB37-442D-8AD4-778963D599A8.jpeg)
![회원가입](images/CD2B2622-CC2F-44FC-85B9-62BC11DB3C69.jpeg)
![로그인 UI](images/2720FAF3-17A5-4944-B7B5-74D98FC074A7.jpeg)

### 🌐 로그인 / 회원가입 - 구글 간편 로그인
구글 계정을 활용한 간편 로그인을 지원합니다.

![구글 로그인](images/419F9E08-B83A-48CF-836E-268F2B43447D.jpeg)
![구글 인증](images/64DE6424-2E3F-407D-8AD9-AA2BF9083AF8.jpeg)

---

## 🔗 웹 링크 관리

### 📌 웹 링크 등록, 수정, 삭제
사용자는 자신만의 웹 링크를 추가하고 수정하거나 삭제할 수 있습니다.

![링크 관리](images/10AC8ED0-18FD-4FC7-87BF-5227628FFCF9.jpeg)

---

## 📤 공유 및 권한 관리

### 🗂 마이페이지 - 내가 공유한 링크 / 공유 받은 링크 확인
공유한 링크와 공유받은 링크를 한눈에 확인할 수 있습니다.

![마이페이지](images/0B48BB7E-D4A5-439E-8505-66D50E0A6BBE.jpeg)
![공유 받은 링크](images/42E8E5F8-1A7F-4603-87BC-C3420F59ABC1.jpeg)
![링크 권한 관리](images/83A9E03C-3E09-49FA-B22C-1FD49C4F3C72.jpeg)

---

## 🔍 검색 및 필터

### 🔎 검색 및 카테고리별 링크 정리
필요한 링크를 검색하고, 카테고리별로 정리할 수 있습니다.

![검색 기능](images/7B3DB010-BB17-4C79-ACC0-4B464AF8FC2B.jpeg)
![카테고리 필터](images/2B2BC068-05C3-4026-BDB3-E1D5B0E9CE94.jpeg)

---

## 📌 프로젝트 정보

- **기술 스택**: React, Django, PostgreSQL, JWT 인증
- **주요 기능**: 링크 관리, 검색, 공유 및 권한 관리, JWT 및 구글 로그인
- **개발 목표**: 보안이 강화된 웹 링크 저장 및 공유 플랫폼 제공

## 📌 설치 및 실행 방법

```bash
# 파일 설치 및 실행
pip install -r requirements.txt
python manage.py runserver
```
---

## 🚀 주요 트러블슈팅 사례

### 1️⃣ **Django 커스텀 User 모델 적용 시 AttributeError 발생**
#### **문제**
- `AUTH_USER_MODEL`을 변경한 후 `User.objects.all()` 호출 시 `AttributeError: Manager isn't available` 오류 발생

#### **원인**
- Django ORM이 기본 `auth.User` 모델을 참조하려고 시도하면서 충돌 발생
- `get_user_model()`을 사용하지 않고 기존 `from django.contrib.auth.models import User`를 사용한 문제
- 마이그레이션이 제대로 반영되지 않아 `auth.User`와 `accounts.User` 간 충돌

#### **해결 방법**
```python
from django.contrib.auth import get_user_model
User = get_user_model()  # ✅ 커스텀 User 모델을 올바르게 가져옴
```
```bash
# 마이그레이션 재적용
python manage.py makemigrations accounts
python manage.py migrate
```
```bash
# Django shell에서 ORM 확인
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> User.objects.all()
```

### 2️⃣ **Django JWT 인증 적용 후 자동 로그아웃 문제**
#### **문제**
- JWT 인증 적용 후 일정 시간이 지나면 자동 로그아웃됨
- 클라이언트에서 로그인 상태 유지가 되지 않음

#### **원인**
- `access_token` 만료 후 `refresh_token`을 사용하지 않음
- `httponly=True` 설정으로 인해 프론트엔드에서 `access_token`을 직접 갱신 불가능

#### **해결 방법**
✅ **1. Django에서 JWT를 쿠키에 저장**
```python
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

def login_view(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        response = JsonResponse({"access_token": str(refresh.access_token)})
        response.set_cookie("access_token", str(refresh.access_token), httponly=True)
        response.set_cookie("refresh_token", str(refresh), httponly=True)
        return response
    else:
        return JsonResponse({"error": "Invalid credentials"}, status=400)
```
✅ **2. 프론트엔드에서 자동으로 `refresh_token` 요청**
```javascript
async function fetchWithAuth(url, options = {}) {
    const response = await fetch(url, {
        ...options,
        credentials: "include",
        headers: {
            ...options.headers,
            "Content-Type": "application/json",
        },
    });

    if (response.status === 401) {
        const refreshResponse = await fetch("/accounts/token/refresh/", {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
        });
        if (refreshResponse.ok) {
            return fetchWithAuth(url, options);
        }
    }
    return response.json();
}
```
✅ **3. Django `settings.py`에서 JWT 만료 시간 설정**
```python
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}
```


