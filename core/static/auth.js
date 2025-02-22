function getAccessToken() {
    return localStorage.getItem("access_token");
}

function apiRequest(url, method = "GET", data = null) {
    const accessToken = getAccessToken();
    const headers = {
        "Content-Type": "application/json"
    };

    if (accessToken) {
        headers["Authorization"] = "Bearer " + accessToken;
    }

    return fetch(url, {
        method: method,
        headers: headers,
        body: data ? JSON.stringify(data) : null
    }).then(response => response.json());
}

async function getValidAccessToken() {
    let accessToken = localStorage.getItem("access_token");

    if (!accessToken) {
        const refreshToken = getCookie("refresh_token");
        if (refreshToken) {
            const response = await fetch("/accounts/token/refresh/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ "refresh": refreshToken })
            });

            if (response.ok) {
                const data = await response.json();
                accessToken = data.access;
                localStorage.setItem("access_token", accessToken);
            } else {
                console.error("토큰 갱신 실패");
            }
        }
    }

    return accessToken;
}


async function getProtectedData() {
    const token = await getValidAccessToken();
    if (!token) {
        console.error("로그인이 필요합니다.");
        return;
    }

    const response = await fetch("/protected/", {
        method: "GET",
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    const data = await response.json();
    console.log(data);
}


