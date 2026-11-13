/* Pure semantic mapping. Future artwork providers may implement the same plan contract. */
window.CareerDesign = (() => {
  const families = {
    engineering: "workshop",
    technology: "laboratory",
    product: "bridges",
    creative: "garden",
    strategy: "observatory",
    leadership: "community",
    healthcare: "community",
    education: "garden",
    operations: "workshop",
    finance: "observatory",
    science: "laboratory",
    general: "bridges",
  };
  const palette = [
    { top: "#bde4e1", side: "#548e9f", accent: "#48b9ba", light: "#edfffa" },
    { top: "#cdb9ee", side: "#8d6db7", accent: "#a78adf", light: "#fbf6ff" },
    { top: "#bad9f8", side: "#6487bd", accent: "#79b7ed", light: "#f2f9ff" },
    { top: "#f3dbaa", side: "#b48b66", accent: "#e5b970", light: "#fff9eb" },
    { top: "#f1c6bf", side: "#b97d89", accent: "#e5a29a", light: "#fff7f2" },
    { top: "#cce6ba", side: "#7ca38c", accent: "#8fbd8c", light: "#f3fff1" },
  ];
  const hash = (s) =>
    [...s].reduce((a, c) => (Math.imul(a, 31) + c.charCodeAt(0)) >>> 0, 17);
  const affinity = {
    engineering: ["workshop", "bridges", "laboratory"],
    technology: ["laboratory", "bridges", "observatory"],
    product: ["bridges", "community", "observatory"],
    creative: ["garden", "observatory", "community"],
    education: ["garden", "community", "observatory"],
    healthcare: ["community", "garden", "workshop"],
    strategy: ["observatory", "bridges", "community"],
    leadership: ["community", "bridges", "observatory"],
    science: ["laboratory", "observatory", "garden"],
    finance: ["observatory", "workshop", "bridges"],
    operations: ["workshop", "bridges", "community"],
  };
  function plan(stages, insights) {
    const counts = {};
    return stages.map((stage, index) => {
      const insight = insights.find((s) => s.stage_id === stage.id);
      const domain = insight?.theme || stage.domain;
      const preferred = families[domain] || "bridges";
      const alternatives = [
        ...new Set([
          preferred,
          ...(affinity[domain] || []),
          ...Object.values(families),
        ]),
      ];
      const family = alternatives.reduce(
        (best, x) => ((counts[x] || 0) < (counts[best] || 0) ? x : best),
        alternatives[0],
      );
      const occurrence = counts[family] || 0;
      counts[family] = occurrence + 1;
      const seed = hash(stage.id + stage.role + (stage.company || ""));
      return {
        stageId: stage.id,
        family,
        domain,
        palette: palette[index % palette.length],
        seed,
        variant: ((hash(family) % 3) + occurrence) % 3,
        artworkProvider: "composed-svg-v1",
        camera: "isometric",
        light: "upper-left",
      };
    });
  }
  return { plan, families, palette };
})();
