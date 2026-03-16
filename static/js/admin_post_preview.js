document.addEventListener("DOMContentLoaded", function () {
  const titleInput = document.getElementById("id_title");
  const subtitleInput = document.getElementById("id_subtitle");
  const descriptionInput = document.getElementById("id_description");
  const categorySelect = document.getElementById("id_category");
  const previewImageInput = document.getElementById("id_preview_image");

  const previewTitle = document.getElementById("preview-title");
  const previewSubtitle = document.getElementById("preview-subtitle");
  const previewDescription = document.getElementById("preview-description");
  const previewCategory = document.getElementById("preview-category");
  const previewImageWrap = document.getElementById("preview-image-wrap");
  const previewImage = document.getElementById("preview-image");
  const previewBody = document.getElementById("preview-body");
  const previewShell = document.getElementById("preview-shell");

  const modeButtons = document.querySelectorAll(".preview-mode-btn");

  function updateTextPreview() {
    previewTitle.textContent = titleInput.value || "제목을 입력하세요";
    previewSubtitle.textContent = subtitleInput.value || "부제목을 입력하세요";
    previewDescription.textContent = descriptionInput.value || "미리보기 설명을 입력하세요";

    if (categorySelect && categorySelect.selectedOptions.length > 0) {
      previewCategory.textContent = categorySelect.selectedOptions[0].text || "카테고리";
    }
  }

  function updateImagePreview() {
    const file = previewImageInput.files[0];

    if (!file) {
      previewImageWrap.style.display = "none";
      previewImage.removeAttribute("src");
      return;
    }

    const objectUrl = URL.createObjectURL(file);
    previewImage.src = objectUrl;
    previewImageWrap.style.display = "block";
  }

  function bindEditorPreview() {
    if (window.CKEDITOR && CKEDITOR.instances.id_content) {
      const editor = CKEDITOR.instances.id_content;

      function syncEditorContent() {
        const html = editor.getData();
        previewBody.innerHTML = html || "<p>본문 미리보기</p>";
      }

      editor.on("change", syncEditorContent);
      editor.on("instanceReady", syncEditorContent);
      syncEditorContent();
    }
  }

  function setPreviewMode(mode) {
    previewShell.classList.remove("preview-desktop", "preview-mobile");
    previewShell.classList.add(mode === "mobile" ? "preview-mobile" : "preview-desktop");

    modeButtons.forEach((button) => {
      button.classList.toggle("active", button.dataset.mode === mode);
    });
  }

  titleInput?.addEventListener("input", updateTextPreview);
  subtitleInput?.addEventListener("input", updateTextPreview);
  descriptionInput?.addEventListener("input", updateTextPreview);
  categorySelect?.addEventListener("change", updateTextPreview);
  previewImageInput?.addEventListener("change", updateImagePreview);

  modeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      setPreviewMode(button.dataset.mode);
    });
  });

  updateTextPreview();
  updateImagePreview();
  setPreviewMode("desktop");

  if (window.CKEDITOR) {
    CKEDITOR.on("instanceReady", function () {
      bindEditorPreview();
    });
  }
});