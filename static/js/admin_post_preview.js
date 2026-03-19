document.addEventListener("DOMContentLoaded", function () {
  const titleInput = document.getElementById("id_title");
  const subtitleInput = document.getElementById("id_subtitle");
  const descriptionInput = document.getElementById("id_description");
  const categorySelect = document.getElementById("id_category");
  const previewImageInput = document.getElementById("id_preview_image");
  const descriptionCounter = document.getElementById("description-counter");

  const previewTitle = document.getElementById("preview-title");
  const previewSubtitle = document.getElementById("preview-subtitle");
  const previewCategory = document.getElementById("preview-category");
  const previewBody = document.getElementById("preview-body");
  const previewShell = document.getElementById("preview-shell");
  const previewHero = document.getElementById("preview-hero");

  const modeButtons = document.querySelectorAll(".preview-mode-btn");
  let currentPreviewImageUrl = null;

  function updateDescriptionCounter() {
    if (!descriptionInput || !descriptionCounter) {
      return;
    }

    descriptionCounter.textContent = `${descriptionInput.value.length}/150`;
  }

  function updateTextPreview() {
    previewTitle.textContent = titleInput.value || "제목을 입력하세요";
    previewSubtitle.textContent = subtitleInput.value || "부제목을 입력하세요";

    if (categorySelect && categorySelect.selectedOptions.length > 0) {
      const selectedText = categorySelect.selectedOptions[0].text;
      previewCategory.textContent =
        selectedText && selectedText !== "---------" ? selectedText : "카테고리";
    } else {
      previewCategory.textContent = "카테고리";
    }
  }

  function updateHeroImagePreview() {
    const file = previewImageInput.files[0];

    if (currentPreviewImageUrl) {
      URL.revokeObjectURL(currentPreviewImageUrl);
      currentPreviewImageUrl = null;
    }

    if (!file) {
      previewHero.style.backgroundImage = "none";
      previewHero.style.backgroundColor = "#8f8f8f";
      return;
    }

    currentPreviewImageUrl = URL.createObjectURL(file);
    previewHero.style.backgroundImage = `url("${currentPreviewImageUrl}")`;
    previewHero.style.backgroundColor = "transparent";
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
    if (!previewShell) {
      return;
    }
    previewShell.classList.remove("preview-desktop", "preview-mobile");
    previewShell.classList.add(mode === "mobile" ? "preview-mobile" : "preview-desktop");

    modeButtons.forEach((button) => {
      button.classList.toggle("active", button.dataset.mode === mode);
    });
  }

  titleInput?.addEventListener("input", updateTextPreview);
  subtitleInput?.addEventListener("input", updateTextPreview);
  descriptionInput?.addEventListener("input", updateDescriptionCounter);
  categorySelect?.addEventListener("change", updateTextPreview);
  previewImageInput?.addEventListener("change", updateHeroImagePreview);

  modeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      setPreviewMode(button.dataset.mode);
    });
  });

  updateTextPreview();
  updateDescriptionCounter();
  updateHeroImagePreview();
  setPreviewMode("desktop");

  if (window.CKEDITOR) {
    CKEDITOR.on("instanceReady", function () {
      bindEditorPreview();
    });
  }

  window.addEventListener("beforeunload", function () {
    if (currentPreviewImageUrl) {
      URL.revokeObjectURL(currentPreviewImageUrl);
    }
  });
});
