document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("feedbackModal");
  if (!modal) return;

  const closeBtn = document.getElementById("modalCloseBtn");
  const retryBtn = document.getElementById("retryBtn");

  function closeModal() {
    modal.style.animation = "fadeOut .2s ease-in forwards";
    setTimeout(() => modal.remove(), 200);
  }

  closeBtn?.addEventListener("click", closeModal);

  retryBtn?.addEventListener("click", () => {
    retryBtn.classList.add("btn-bounce");
    setTimeout(closeModal, 150);
  });
});
