document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  if (!form) return;

  const submitBtn = form.querySelector("[type='submit']");
  const originalText = submitBtn?.innerHTML ?? "";
  const formUrl = form.getAttribute("action") || window.location.href;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    submitBtn.innerHTML =
      '<span class="inline-block animate-spin">⏳</span> Processing...';
    submitBtn.disabled = true;

    document.querySelectorAll(".field-error").forEach((el) => el.classList.remove("field-error"));
    document.querySelectorAll(".form-error").forEach((el) => el.remove());

    try {
      const response = await fetch(formUrl, {
        method: "POST",
        body: new FormData(form),
        redirect: "follow",
      });

      if (response.url !== formUrl) {
        window.location.href = response.url;
        return;
      }

      if (response.ok) {
        const doc = new DOMParser().parseFromString(
          await response.text(),
          "text/html"
        );
        const newForm = doc.querySelector("form");
        if (newForm) form.innerHTML = newForm.innerHTML;
        return;
      }

      submitBtn.innerHTML = originalText;
      submitBtn.disabled = false;
    } catch {
      submitBtn.innerHTML = originalText;
      submitBtn.disabled = false;
    }
  });
});
