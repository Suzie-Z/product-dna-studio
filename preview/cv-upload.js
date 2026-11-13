/* One input path. No text/URL/voice onboarding or external parser dependencies. */
window.CareerUpload = {
  validate(files) {
    if (!files || files.length !== 1) throw Error("Choose one CV at a time.");
    const file = files[0],
      extension = file.name.split(".").pop().toLowerCase();
    if (!["pdf", "docx"].includes(extension))
      throw Error("Choose a PDF or DOCX file.");
    if (!file.size || file.size > 5 * 1024 * 1024)
      throw Error("Choose a CV smaller than 5 MB.");
    return {
      file,
      mime:
        extension === "pdf"
          ? "application/pdf"
          : "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    };
  },
};
