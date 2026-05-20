window.Transportify = window.Transportify || {};

window.Transportify.showAlert = function showAlert(element, message, type = "info") {
    if (!element) {
        return;
    }

    element.className = `alert app-alert alert-${type}`;
    element.textContent = message;
    element.classList.remove("d-none");
};

window.Transportify.hideAlert = function hideAlert(element) {
    if (!element) {
        return;
    }

    element.classList.add("d-none");
};

window.Transportify.formatPercent = function formatPercent(value) {
    const number = Number(value || 0);
    return `${Math.round(number * 100)}%`;
};

window.Transportify.cacheBust = function cacheBust(url) {
    if (!url) {
        return "";
    }
    const separator = url.includes("?") ? "&" : "?";
    return `${url}${separator}t=${Date.now()}`;
};
