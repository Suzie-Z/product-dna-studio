"use strict";
(() => {
  const $ = (id) => document.getElementById(id),
    screens = ["discover", "journey", "dna"];
  let analysedReview = null,
    upload = null,
    extraction = null,
    review = [],
    result = null,
    busy = false,
    epoch = 0,
    controller = null,
    pending = null;
  const rid = () => "req_" + crypto.randomUUID().replaceAll("-", "");
  function screen(name) {
    for (const s of screens) $(s).hidden = s !== name;
    for (const button of document.querySelectorAll("[data-screen]")) {
      button.disabled = button.dataset.screen !== "discover" && !result;
      button.setAttribute(
        "aria-current",
        button.dataset.screen === name ? "step" : "false",
      );
    }
    window.scrollTo({ top: 0, behavior: "instant" });
    if (name !== "discover") $(name + "-title").focus({ preventScroll: true });
  }
  function setBusy(value, operation) {
    busy = value;
    $("loading").hidden = !value;
    $("upload-panel").hidden = value || !!extraction;
    $("review-panel").hidden = value || !extraction;
    $("analyse").disabled = value;
    $("replace").disabled = value;
    $("cv-file").disabled = value;
    $("upload-label").setAttribute("aria-disabled", String(value));
    $("loading-title").textContent =
      operation === "analyse"
        ? "Seeing the strengths behind your story…"
        : "Finding the chapters in your story…";
    $("loading-copy").textContent =
      operation === "analyse"
        ? "Connecting your experiences with the evidence behind them."
        : "We’re reading your experience, not judging it.";
    for (const b of document.querySelectorAll("[data-screen]"))
      b.disabled = value || (b.dataset.screen !== "discover" && !result);
  }
  function error(message, retry = false) {
    $("error-message").textContent = message;
    $("error-panel").hidden = false;
    $("retry").hidden = !retry;
  }
  function clearError() {
    $("error-panel").hidden = true;
  }
  async function send(operation, body, mime, requestId, signal) {
    const timeout = setTimeout(() => controller?.abort("timeout"), 180000);
    try {
      const response = await fetch("/api/v2/" + operation, {
        method: "POST",
        headers: { "Content-Type": mime, "X-Request-ID": requestId },
        body,
        signal,
      });
      let data;
      try {
        data = await response.json();
      } catch {
        throw Error(
          "The connection was interrupted. Your file is still here—try again.",
        );
      }
      if (!response.ok)
        throw Error(
          data.error || "Something interrupted your journey. Please try again.",
        );
      return data;
    } finally {
      clearTimeout(timeout);
    }
  }
  async function run(operation) {
    if (
      busy ||
      (operation === "extract" && !upload) ||
      (operation === "analyse" && !extraction)
    )
      return;
    if (
      operation === "analyse" &&
      result &&
      analysedReview === JSON.stringify(review)
    ) {
      screen("journey");
      return;
    }
    const runEpoch = ++epoch;
    clearError();
    screen("discover");
    controller = new AbortController();
    setBusy(true, operation);
    const body =
      operation === "extract"
        ? upload.file
        : JSON.stringify({ session_id: extraction.session_id, review });
    const mime = operation === "extract" ? upload.mime : "application/json";
    if (!pending || pending.operation !== operation || pending.body !== body)
      pending = { operation, body, id: rid() };
    try {
      const data = await send(
        operation,
        body,
        mime,
        pending.id,
        controller.signal,
      );
      if (runEpoch !== epoch) return;
      if (operation === "extract") {
        if (data.status !== "ready") {
          pending = null;
          error(
            data.note ||
              "We could not find enough career experience. Try a more complete CV.",
          );
          return;
        }
        extraction = data;
        review = data.stages.map((s) => ({
          id: s.id,
          company: s.company,
          role: s.role,
          period: s.period,
        }));
        renderReview();
        $("review-note").textContent = data.note || "";
        pending = null;
      } else {
        if (
          data.schema_version !== "2.0" ||
          !Array.isArray(data.core_dna) ||
          !data.core_dna.length
        )
          throw Error("The reflection was incomplete. Please try again.");
        result = data;
        analysedReview = JSON.stringify(review);
        CareerJourney.render($("island-world"), result, showEvidence);
        CareerDNA.render(result, showEvidence);
        $("journey-order").textContent =
          "Chapters follow your reviewed order. Dates can overlap; not every journey is a straight line.";
        pending = null;
        screen("journey");
      }
    } catch (err) {
      if (runEpoch !== epoch) return;
      error(
        err.name === "AbortError"
          ? "This took longer than expected. Your file and review are safe—try again."
          : err instanceof TypeError
            ? "The connection was interrupted. Your file and review are safe—try again."
            : err.message,
        true,
      );
    } finally {
      if (runEpoch === epoch) {
        controller = null;
        setBusy(false);
        if (result && operation === "analyse" && !$("journey").hidden)
          screen("journey");
      }
    }
  }
  function renderReview() {
    $("review-list").replaceChildren();
    review.forEach((row, index) => {
      const el = document.createElement("div");
      el.className = "review-row";
      const number = document.createElement("span");
      number.className = "review-index";
      number.textContent = String(index + 1).padStart(2, "0");
      el.append(number);
      for (const [key, label, limit] of [
        ["company", "Company", 90],
        ["role", "Role", 90],
        ["period", "Period", 55],
      ]) {
        const l = document.createElement("label");
        l.textContent = label;
        const input = document.createElement("input");
        input.value = row[key] || "";
        input.maxLength = limit;
        input.autocomplete = "off";
        input.setAttribute("aria-label", `${label}, chapter ${index + 1}`);
        input.placeholder = key === "role" ? "Role" : "Not provided";
        input.required = key === "role";
        input.oninput = () => {
          row[key] = input.value.trim() || (key === "role" ? "" : null);
          pending = null;
          clearError();
        };
        l.append(input);
        el.append(l);
      }
      const controls = document.createElement("div");
      controls.className = "order-controls";
      for (const [delta, label, glyph] of [
        [-1, "Move up", "↑"],
        [1, "Move down", "↓"],
      ]) {
        const b = document.createElement("button");
        b.textContent = glyph;
        b.setAttribute("aria-label", `${label}, chapter ${index + 1}`);
        b.disabled = index + delta < 0 || index + delta >= review.length;
        b.onclick = () => {
          [review[index], review[index + delta]] = [
            review[index + delta],
            review[index],
          ];
          pending = null;
          renderReview();
          const target = $("review-list").children[index + delta].querySelector(
            ".order-controls button",
          );
          target?.focus();
        };
        controls.append(b);
      }
      el.append(controls);
      const original = extraction.stages.find((s) => s.id === row.id);
      if (original.uncertainty) {
        const note = document.createElement("p");
        note.className = "uncertainty";
        note.textContent = original.uncertainty;
        el.append(note);
      }
      $("review-list").append(el);
    });
  }
  function showEvidence(ids) {
    if (!result) return;
    const target = $("evidence-content");
    target.replaceChildren();
    for (const id of new Set(ids)) {
      const stage = result.stages.find((s) => s.facts.some((f) => f.id === id)),
        fact = stage?.facts.find((f) => f.id === id);
      if (!fact) continue;
      const item = document.createElement("article");
      item.className = "evidence-item";
      const h = document.createElement("h3");
      h.textContent = stage.role + (stage.company ? " · " + stage.company : "");
      const claim = document.createElement("p");
      claim.textContent = fact.claim;
      const quote = document.createElement("blockquote");
      quote.textContent = fact.quote;
      item.append(h, claim, quote);
      target.append(item);
    }
    $("evidence-dialog").showModal();
  }
  async function choose(files) {
    if (busy) return;
    clearError();
    let next;
    try {
      next = CareerUpload.validate(files);
    } catch (e) {
      error(e.message);
      return;
    }
    epoch++;
    upload = next;
    extraction = null;
    result = null;
    review = [];
    pending = null;
    $("file-label").textContent = next.file.name + " · selected";
    $("island-world").replaceChildren();
    $("strengths").replaceChildren();
    screen("discover");
    await run("extract");
  }
  function reset() {
    epoch++;
    controller?.abort();
    controller = null;
    upload = null;
    extraction = null;
    review = [];
    result = null;
    analysedReview = null;
    pending = null;
    busy = false;
    $("cv-file").value = "";
    $("file-label").textContent = "";
    $("evidence-dialog").close();
    $("evidence-content").replaceChildren();
    $("review-list").replaceChildren();
    $("island-world").replaceChildren();
    $("strengths").replaceChildren();
    for (const k of ["identity", "evolution", "recognition"])
      $(k).textContent = "";
    clearError();
    setBusy(false);
    screen("discover");
  }
  $("cv-file").onchange = (e) => {
    const files = [...e.target.files];
    e.target.value = "";
    if (files.length) choose(files);
  };
  $("upload-label").onkeydown = (e) => {
    if (["Enter", " "].includes(e.key)) {
      e.preventDefault();
      if (!busy) $("cv-file").click();
    }
  };
  const drop = $("drop-zone");
  for (const event of ["dragenter", "dragover"])
    drop.addEventListener(event, (e) => {
      e.preventDefault();
      if (!busy) drop.classList.add("dragging");
    });
  for (const event of ["dragleave", "drop"])
    drop.addEventListener(event, (e) => {
      e.preventDefault();
      drop.classList.remove("dragging");
    });
  drop.addEventListener("drop", (e) => choose([...e.dataTransfer.files]));
  $("analyse").onclick = () => {
    if (review.some((r) => !r.role || !r.role.trim())) {
      error("Each chapter needs a role.");
      return;
    }
    run("analyse");
  };
  $("retry").onclick = () =>
    run(pending?.operation || (extraction ? "analyse" : "extract"));
  $("cancel").onclick = () => {
    epoch++;
    controller?.abort();
    controller = null;
    setBusy(false);
    error("Paused here. Your file and review are safe.", true);
  };
  $("replace").onclick = () => {
    reset();
    $("cv-file").click();
  };
  $("reveal").onclick = () => screen("dna");
  $("back-review").onclick = () => {
    screen("discover");
    setBusy(false);
  };
  $("back-journey").onclick = () => screen("journey");
  $("start-over").onclick = reset;
  document.querySelector(".brand").onclick = (e) => {
    e.preventDefault();
    screen("discover");
  };
  for (const b of document.querySelectorAll("[data-screen]"))
    b.onclick = () => screen(b.dataset.screen);
  $("privacy-open").onclick = $("privacy-inline").onclick = () =>
    $("privacy-dialog").showModal();
  for (const b of document.querySelectorAll("[data-close]"))
    b.onclick = () => b.closest("dialog").close();
  for (const d of document.querySelectorAll("dialog"))
    d.onclick = (e) => {
      if (e.target === d) {
        const r = d.getBoundingClientRect();
        if (
          e.clientX < r.left ||
          e.clientX > r.right ||
          e.clientY < r.top ||
          e.clientY > r.bottom
        )
          d.close();
      }
    };
  window.addEventListener("pagehide", () => {
    reset();
  });
  screen("discover");
})();
