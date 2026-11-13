window.CareerDNA = {
  render(result, showEvidence) {
    document.getElementById("identity").textContent = result.identity.text;
    document.getElementById("evolution").textContent = result.evolution.text;
    document.getElementById("recognition").textContent =
      result.recognition.text;
    for (const key of ["identity", "evolution", "recognition"])
      document.getElementById(key + "-evidence").onclick = () =>
        showEvidence(result[key].fact_ids);
    const grid = document.getElementById("strengths");
    grid.replaceChildren();
    grid.dataset.count = result.core_dna.length;
    const paths = {
      domain: "M4 7h16v12H4zM8 3v8m8-8v8",
      transferable: "M3 12h17m-6-6 6 6-6 6",
      leadership: "M12 4v16M4 12h16M6 6l12 12M6 18 18 6",
      strategy: "M4 19 9 5l11 4-5 11zM9 5l6 15",
      technical: "M7 5 2 12l5 7m10-14 5 7-5 7m-4-16-2 18",
      commercial: "M4 19V9m8 10V4m8 15v-7",
      problem_solving: "M4 18 9 7l5 7 6-10",
      adaptability: "M4 8a8 8 0 0115-1m1 9a8 8 0 01-15 1M4 3v5h5m11 13v-5h-5",
    };
    result.core_dna.forEach((cap, i) => {
      const c = document.createElement("article");
      c.className = "strength-card";
      c.style.setProperty("--card-light", CareerDesign.palette[i % 6].light);
      c.style.setProperty("--card-accent", CareerDesign.palette[i % 6].top);
      const motif = document.createElement("div");
      motif.className = "strength-motif";
      motif.innerHTML = `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="${paths[cap.category] || paths.transferable}" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
      const h = document.createElement("h3");
      h.textContent = cap.title;
      const p = document.createElement("p");
      p.textContent = cap.explanation;
      const b = document.createElement("button");
      b.className = "evidence-button";
      b.textContent = "See the evidence";
      b.onclick = () => showEvidence(cap.fact_ids);
      c.append(motif, h, p, b);
      grid.append(c);
    });
  },
};
