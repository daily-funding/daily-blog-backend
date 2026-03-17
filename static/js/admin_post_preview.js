document.addEventListener("DOMContentLoaded", function () {
  const titleInput = document.getElementById("id_title");
  const subtitleInput = document.getElementById("id_subtitle");
  const categorySelect = document.getElementById("id_category");
  const previewImageInput = document.getElementById("id_preview_image");

  const previewTitle = document.getElementById("preview-title");
  const previewSubtitle = document.getElementById("preview-subtitle");
  const previewCategory = document.getElementById("preview-category");
  const previewBody = document.getElementById("preview-body");
  const previewShell = document.getElementById("preview-shell");
  const previewHero = document.getElementById("preview-hero");

  const modeButtons = document.querySelectorAll(".preview-mode-btn");

  function updateTextPreview() {
    previewTitle.textContent = titleInput.value || "제목을 입력하세요";
    previewSubtitle.textContent = subtitleInput.value || "부제목을 입력하세요";

    if (categorySelect && categorySelect.selectedOptions.length > 0) {
      const text = categorySelect.selectedOptions[0].text;
      previewCategory.textContent =
        text && text !== "---------" ? text : "카테고리";
    } else {
      previewCategory.textContent = "카테고리";
    }
  }

  function updateHeroImagePreview() {
    const file = previewImageInput.files[0];

    if (!file) {
      previewHero.style.backgroundImage = "none";
      previewHero.style.backgroundColor = "#d9d9d9";
      return;
    }

    const objectUrl = URL.createObjectURL(file);
    previewHero.style.backgroundImage = `url("${objectUrl}")`;
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
    previewShell.classList.remove("preview-desktop", "preview-mobile");
    previewShell.classList.add(mode === "mobile" ? "preview-mobile" : "preview-desktop");

    modeButtons.forEach((button) => {
      button.classList.toggle("active", button.dataset.mode === mode);
    });
  }

  titleInput?.addEventListener("input", updateTextPreview);
  subtitleInput?.addEventListener("input", updateTextPreview);
  categorySelect?.addEventListener("change", updateTextPreview);
  previewImageInput?.addEventListener("change", updateHeroImagePreview);

  modeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      setPreviewMode(button.dataset.mode);
    });
  });

  updateTextPreview();
  updateHeroImagePreview();
  setPreviewMode("desktop");

  if (window.CKEDITOR) {
    CKEDITOR.on("instanceReady", function () {
      bindEditorPreview();
    });
  }
});