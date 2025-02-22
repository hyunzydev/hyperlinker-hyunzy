(function () {
    function getModalContainer() {
        let modalContainer = document.querySelector("#dynamic-modal-container");
        if (!modalContainer) {
            document.body.insertAdjacentHTML("beforeend", `<div id="dynamic-modal-container"></div>`);
            modalContainer = document.querySelector("#dynamic-modal-container");
        }
        return modalContainer;
    }

    function createModal({ title, bodyContent, confirmText = "확인", cancelText = "취소", onConfirm }) {
        const modalContainer = getModalContainer();
        modalContainer.innerHTML = "";

        const modalHTML = `
        <div class="modal fade" id="dynamicModal" tabindex="-1" inert>
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        ${bodyContent}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">${cancelText}</button>
                        <button type="button" class="btn btn-primary" id="modal-confirm-btn">${confirmText}</button>
                    </div>
                </div>
            </div>
        </div>`;

        modalContainer.insertAdjacentHTML("beforeend", modalHTML);
        const modalEl = document.getElementById("dynamicModal");
        const modal = new bootstrap.Modal(modalEl);

        modalEl.addEventListener("shown.bs.modal", function () {
            modalEl.removeAttribute("inert");
        });

        modalEl.addEventListener("hidden.bs.modal", function () {
            setTimeout(() => {
                modalEl.setAttribute("aria-hidden", "true");
                modalEl.setAttribute("inert", "true");
                document.body.focus();
            }, 300);
        });

        modal.show();

        document.getElementById("modal-confirm-btn").addEventListener("click", function () {
            if (typeof onConfirm === "function") {
                onConfirm();
            }
            modal.hide();
        });
    }

    document.body.addEventListener("show-modal", function (e) {
        createModal(e.detail);
    });

    window.showModal = createModal;

    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("edit-btn")) {
            const id = event.target.getAttribute("data-id");
            if (typeof window.editWebLink === "function") {
                window.editWebLink(id);
            } else {
                console.error("editWebLink is not defined!");
            }
        }
    });
})();
