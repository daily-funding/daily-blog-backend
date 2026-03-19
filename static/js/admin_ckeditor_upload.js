function getCookie(name) {
  const cookies = document.cookie ? document.cookie.split(";") : [];

  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith(name + "=")) {
      return decodeURIComponent(cookie.substring(name.length + 1));
    }
  }

  return null;
}

document.addEventListener("DOMContentLoaded", function () {
  const csrfToken = getCookie("csrftoken");

  if (!window.CKEDITOR) {
    return;
  }

  CKEDITOR.on("instanceReady", function (event) {
    const editor = event.editor;

    editor.on("fileUploadRequest", function (evt) {
      const xhr = evt.data.fileLoader.xhr;
      if (csrfToken) {
        xhr.setRequestHeader("X-CSRFToken", csrfToken);
      }
    });
  });
});