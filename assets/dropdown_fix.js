function fixDropdowns() {
    document.querySelectorAll('.dark-dropdown input').forEach(el => {
        el.style.backgroundColor = '#0D1B2E';
        el.style.color = '#cbd5e1';
    });
    document.querySelectorAll('.dark-dropdown .Select-control').forEach(el => {
        el.style.backgroundColor = '#0D1B2E';
        el.style.borderColor = '#1e3a5f';
    });
    document.querySelectorAll('.dark-dropdown .Select-value-label').forEach(el => {
        el.style.color = '#cbd5e1';
    });
    document.querySelectorAll('.dark-dropdown .Select-placeholder').forEach(el => {
        el.style.color = '#94a3b8';
    });
}

document.addEventListener('DOMContentLoaded', fixDropdowns);
const observer = new MutationObserver(fixDropdowns);
observer.observe(document.body, { childList: true, subtree: true });