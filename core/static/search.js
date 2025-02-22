// document.addEventListener("DOMContentLoaded", function() {
//     console.log("✅ JavaScript 로드 완료!");
//
//     // ✅ CSRF 토큰 가져오기
//     const csrftokenMeta = document.querySelector('meta[name="csrf-token"]');
//     const csrftoken = csrftokenMeta ? csrftokenMeta.getAttribute("content") : null;
//
//     if (!csrftoken) {
//         console.warn("🚨 CSRF 토큰이 없습니다. 로그인 후 다시 시도하세요.");
//     } else {
//         console.log("✅ CSRF 토큰이 설정되었습니다.");
//     }
//
//     // ✅ 검색 기능 구현
//     function filterWebLinks() {
//         console.log("🔍 검색 실행");
//
//         const searchInput = document.getElementById("searchInput").value.toLowerCase();
//         const weblinks = document.querySelectorAll("#weblink-list .list-group-item");
//
//         if (!weblinks.length) {
//             console.warn("🚨 검색할 링크 목록이 없습니다.");
//             return;
//         }
//
//         let found = false;
//
//         weblinks.forEach(link => {
//             const nameElement = link.querySelector("strong");
//             const urlElement = link.querySelector("a");
//             const categoryElement = link.querySelector("small");
//
//             const name = nameElement ? nameElement.textContent.toLowerCase() : "";
//             const url = urlElement ? urlElement.textContent.toLowerCase() : "";
//             const category = categoryElement ? categoryElement.textContent.toLowerCase() : "";
//
//             if (name.includes(searchInput) || url.includes(searchInput) || category.includes(searchInput)) {
//                 link.style.display = "block";
//                 found = true;
//             } else {
//                 link.style.display = "none";
//             }
//         });
//
//         // 검색 결과가 없으면 메시지 표시
//         const noResultsMessage = document.getElementById("no-results-message");
//         if (!found) {
//             if (!noResultsMessage) {
//                 const message = document.createElement("li");
//                 message.id = "no-results-message";
//                 message.className = "list-group-item text-center text-muted";
//                 message.textContent = "🔍 검색 결과가 없습니다.";
//                 document.getElementById("weblink-list").appendChild(message);
//             }
//         } else {
//             if (noResultsMessage) noResultsMessage.remove();
//         }
//     }
//
//     // ✅ 검색 입력 이벤트 리스너 추가
//     const searchInputElement = document.getElementById("searchInput");
//     if (searchInputElement) {
//         searchInputElement.addEventListener("keyup", filterWebLinks);
//     } else {
//         console.warn("🚨 검색 입력창 (`searchInput`)을 찾을 수 없습니다.");
//     }
// });
//
//
//
(function() {
    console.log("✅ JavaScript 로드 완료!");

    const csrftokenMeta = document.querySelector('meta[name="csrf-token"]');
    const csrftoken = csrftokenMeta ? csrftokenMeta.getAttribute("content") : null;

    if (!csrftoken) {
        console.warn("🚨 CSRF 토큰이 없습니다. 로그인 후 다시 시도하세요.");
    } else {
        console.log("✅ CSRF 토큰이 설정되었습니다.");
    }

    function filterWebLinks() {
        console.log("🔍 검색 실행");

        const searchInput = document.getElementById("searchInput").value.toLowerCase();
        const weblinks = document.querySelectorAll("#weblink-list .list-group-item");

        if (!weblinks.length) {
            console.warn("🚨 검색할 링크 목록이 없습니다.");
            return;
        }

        let found = false;

        weblinks.forEach(link => {
            const nameElement = link.querySelector("strong");
            const urlElement = link.querySelector("a");
            const categoryElement = link.querySelector("small");

            const name = nameElement ? nameElement.textContent.toLowerCase() : "";
            const url = urlElement ? urlElement.textContent.toLowerCase() : "";
            const category = categoryElement ? categoryElement.textContent.toLowerCase() : "";

            if (name.includes(searchInput) || url.includes(searchInput) || category.includes(searchInput)) {
                link.style.display = "block";
                found = true;
            } else {
                link.style.display = "none";
            }
        });

        const noResultsMessage = document.getElementById("no-results-message");
        if (!found) {
            if (!noResultsMessage) {
                const message = document.createElement("li");
                message.id = "no-results-message";
                message.className = "list-group-item text-center text-muted";
                message.textContent = "🔍 검색 결과가 없습니다.";
                document.getElementById("weblink-list").appendChild(message);
            }
        } else {
            if (noResultsMessage) noResultsMessage.remove();
        }
    }

    window.filterWebLinks = filterWebLinks;

    document.addEventListener("DOMContentLoaded", function() {
        const searchInputElement = document.getElementById("searchInput");
        if (searchInputElement) {
            searchInputElement.addEventListener("keyup", filterWebLinks);
        } else {
            console.warn("🚨 검색 입력창 (`searchInput`)을 찾을 수 없습니다.");
        }
    });
})();
