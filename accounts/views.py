from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from accounts.forms import LoginForm, SignupForm
from accounts.models import User
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render
from django.shortcuts import resolve_url

# 구글
import requests
from django.contrib.auth import login
from django.shortcuts import redirect
from django.http import JsonResponse
from allauth.socialaccount.models import SocialAccount
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.contrib.auth import login as auth_login  # ✅ login 함수 import 명확히 지정
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
import requests
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from weblinks.models import WebLink
from django.contrib.auth import get_user_model


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = "crispy_form.html"
    extra_context = {
        "form_title": "회원가입",
    }

    success_url = reverse_lazy("accounts:login")

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect_to = self.success_url
            if redirect_to != self.request.path:
                messages.warning(self.request, "로그인 유저는 회원가입할 수 없습니다.")
                return HttpResponseRedirect(redirect_to)

        response = super().dispatch(request, *args, **kwargs)
        return response



    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password1"])
        user.save()
        self.object = user

        messages.success(self.request, "회원가입을 환영합니다. ;-)")

        user.backend = "django.contrib.auth.backends.ModelBackend"



        return HttpResponseRedirect(self.get_success_url())


signup = SignupView.as_view()


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)

            token_url = "http://127.0.0.1:8000/accounts/token/"
            token_response = requests.post(
                token_url, json={"username": username, "password": password}
            )

            if token_response.status_code == 200:
                token_data = token_response.json()

                next_url = (
                    request.GET.get("next")
                    or request.POST.get("next")
                    or "accounts:profile"
                )
                response = redirect(resolve_url(next_url))

                response.set_cookie(
                    "access_token", token_data["access"], httponly=True
                )
                response.set_cookie(
                    "refresh_token", token_data["refresh"], httponly=True
                )
                return response
            else:
                messages.error(request, "JWT 토큰 발급 실패")
                return redirect("accounts:login")
        else:
            messages.error(request, "아이디 또는 비밀번호가 잘못되었습니다.")

    return render(request, "accounts/login.html")


@method_decorator(never_cache, name="dispatch")
class LogoutView(DjangoLogoutView):
    next_page = "accounts:login"

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, "로그아웃했습니다. :-)")
        return response


logout_view = LogoutView.as_view()

def google_login(request):
    scope = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
    return redirect(
        f"https://accounts.google.com/o/oauth2/auth"
        f"?client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_CALLBACK_URI}"
        f"&response_type=code" 
        f"&scope={scope}"
        f"&access_type=offline" 
        f"&prompt=consent"
    )


def google_callback(request):

    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "Authorization code not provided"}, status=400)

    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.GOOGLE_CALLBACK_URI,
    }

    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()

    if "error" in token_json:
        return JsonResponse({"error": token_json["error"]}, status=400)

    access_token = token_json.get("access_token")

    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    user_info_response = requests.get(
        user_info_url, headers={"Authorization": f"Bearer {access_token}"}
    )
    user_info_json = user_info_response.json()

    if "email" not in user_info_json:
        return JsonResponse({"error": "Failed to retrieve user email"}, status=400)

    email = user_info_json["email"]
    name = user_info_json.get("name", "")
    google_id = user_info_json.get("id")

    user, created = User.objects.get_or_create(email=email, defaults={"username": name})

    if not user:
        return JsonResponse({"error": "User object not found"}, status=400)

    social_user = SocialAccount.objects.filter(user=user, provider="google").first()
    if not social_user:
        SocialAccount.objects.create(user=user, provider="google", uid=google_id)

    user.backend = "django.contrib.auth.backends.ModelBackend"

    auth_login(request, user)

    return redirect("accounts:profile")




@login_required
def logout(request):
    auth_logout(request)
    request.session.flush()

    messages.success(
        request, "로그아웃되었습니다. 다시 로그인하세요."
    )

    google_logout_url = "http://127.0.0.1:8000/"
    return redirect(google_logout_url)




User = get_user_model()


@login_required
def profile(request):
    user = request.user

    my_created_links = WebLink.objects.filter(created_by=user)
    my_shared_links = WebLink.objects.filter(
        created_by=user, shared_with__isnull=False
    )
    received_links = WebLink.objects.filter(
        shared_with=user
    ).distinct()

    context = {
        "user": user,
        "my_created_links": my_created_links,
        "my_shared_links": my_shared_links,
        "received_links": received_links,
    }

    return render(request, "accounts/profile.html", context)


@login_required
def user_list(request):
    users = User.objects.all().values("id", "username")
    return JsonResponse({"users": list(users)})


@csrf_exempt
@login_required
def share_weblink(request, weblink_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            permission = data.get("permission")

            if not user_id or not permission:
                return JsonResponse({"error": "잘못된 요청"}, status=400)

            weblink = get_object_or_404(WebLink, id=weblink_id, created_by=request.user)
            user = get_object_or_404(User, id=user_id)

            weblink.shared_with.add(user)
            if permission == "write":
                weblink.write_permissions.add(user)

            return JsonResponse({"message": "공유 성공!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "잘못된 요청"}, status=400)
