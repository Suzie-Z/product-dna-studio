/* Accessible stage content, independent from the career intelligence engine. */
window.CareerJourney = {
  render(container, result, showEvidence) {
    container._worldObserver?.disconnect();
    container.replaceChildren();
    const plans = CareerDesign.plan(result.stages, result.stage_insights);
    for (const [index, stage] of result.stages.entries()) {
      const insight = result.stage_insights.find(
          (x) => x.stage_id === stage.id,
        ),
        plan = plans[index];
      const card = document.createElement("article");
      card.className = "island-card";
      card.dataset.stageId = stage.id;
      card.dataset.family = plan.family;
      const el = (tag, cls, text) => {
        const n = document.createElement(tag);
        if (cls) n.className = cls;
        if (text !== undefined) n.textContent = text;
        return n;
      };
      const counter = el("div", "chapter-number");
      counter.append(
        el("span", "", `Chapter ${String(index + 1).padStart(2, "0")}`),
        el(
          "span",
          "",
          stage.kind === "career_break" ? "A pause in the journey" : "",
        ),
      );
      const artwork = el("div", "island-art");
      artwork.innerHTML = CareerIslands.render(plan); // Only our fixed, typed artwork plan enters SVG.
      const company = el(
        "p",
        "stage-company",
        stage.company || "Independent chapter",
      );
      const role = el("h2", "stage-role", stage.role);
      const period = el(
        "p",
        "stage-period",
        stage.period || "Period not provided",
      );
      const chips = el("div", "capability-chips");
      for (const cap of insight.capabilities)
        chips.append(el("span", "", cap.label));
      const details = el("details");
      details.append(
        el("summary", "", "What this chapter added"),
        el("p", "", insight.contribution.text),
      );
      const evidence = el("button", "evidence-button", "Explore the evidence");
      evidence.onclick = () => showEvidence(insight.contribution.fact_ids);
      details.append(evidence);
      card.append(counter, artwork, company, role, period, chips, details);
      container.append(card);
    }
    const ns = "http://www.w3.org/2000/svg",
      paths = document.createElementNS(ns, "svg");
    paths.classList.add("journey-connections");
    paths.setAttribute("aria-hidden", "true");
    container.prepend(paths);
    const connect = () => {
      const rect = container.getBoundingClientRect();
      if (!rect.width || !rect.height) return;
      paths.setAttribute("viewBox", `0 0 ${rect.width} ${rect.height}`);
      paths.replaceChildren();
      const cards = [...container.querySelectorAll(".island-card")];
      for (let i = 0; i < cards.length - 1; i++) {
        const a = cards[i].getBoundingClientRect(),
          b = cards[i + 1].getBoundingClientRect();
        const sameRow = Math.abs(a.top - b.top) < 10;
        let d;
        if (sameRow) {
          const y = a.top - rect.top + Math.min(a.height, b.height) * 0.5;
          d = `M${a.right - rect.left} ${y}H${b.left - rect.left}`;
        } else {
          const x1 = a.left + a.width / 2 - rect.left,
            x2 = b.left + b.width / 2 - rect.left,
            y1 = a.bottom - rect.top,
            y2 = b.top - rect.top,
            m = (y1 + y2) / 2;
          d = `M${x1} ${y1}V${m}H${x2}V${y2}`;
        }
        const path = document.createElementNS(ns, "path");
        path.setAttribute("d", d);
        path.setAttribute("fill", "none");
        path.setAttribute("stroke", "#b5a0ce");
        path.setAttribute("stroke-width", "2");
        path.setAttribute("stroke-dasharray", "3 4");
        path.setAttribute("stroke-linecap", "round");
        path.setAttribute("stroke-linejoin", "round");
        paths.append(path);
      }
    };
    container._worldObserver = new ResizeObserver(connect);
    container._worldObserver.observe(container);
    requestAnimationFrame(connect);
    return plans;
  },
};
