/* Original modular miniature worlds. Text stays in accessible HTML, never in artwork. */
window.CareerIslands = (() => {
  const polygon = (points, fill, extra = "") =>
    `<polygon points="${points}" fill="${fill}" ${extra}/>`;
  function box(x, y, w = 35, d = 22, h = 35, color = "#eee", roof = "#fff") {
    return (
      polygon(
        `${x},${y} ${x + w},${y - d} ${x + w},${y - d - h} ${x},${y - h}`,
        color,
      ) +
      polygon(
        `${x + w},${y - d} ${x + w + d},${y} ${x + w + d},${y - h} ${x + w},${y - d - h}`,
        "#a6a5c9",
      ) +
      polygon(
        `${x},${y - h} ${x + w},${y - d - h} ${x + w + d},${y - h} ${x + d},${y + d / 2 - h}`,
        roof,
        'stroke="#ffffff" stroke-opacity=".55" stroke-width="1.5"',
      ) +
      polygon(
        `${x + 7},${y - h + 10} ${x + w - 7},${y - d - h + 10} ${x + w - 7},${y - d - 9} ${x + 7},${y - 9}`,
        "#fff",
        'opacity=".3"',
      ) +
      `<path d="M${x + w / 2} ${y - d / 2 - h + 10}v${Math.max(8, h - 20)}" stroke="${roof}" stroke-width="2" opacity=".7"/>`
    );
  }
  function tree(x, y, c = "#88c5aa", s = 1) {
    return `<g transform="translate(${x} ${y}) scale(${s})"><path d="M0 0V-21" stroke="#8a8197" stroke-width="4"/><ellipse cy="-27" rx="13" ry="18" fill="${c}"/><ellipse cx="-5" cy="-32" rx="8" ry="11" fill="#dcf0c8"/></g>`;
  }
  function terrain(shape, p) {
    const vertices = shape
      .split(" ")
      .map((pair) => pair.split(",").map(Number));
    const sides = vertices
      .map(([x, y], i) => {
        const [nx, ny] = vertices[(i + 1) % vertices.length];
        return polygon(
          `${x},${y} ${nx},${ny} ${nx},${ny + 24} ${x},${y + 24}`,
          i % 2 ? p.side : "#9b9bb9",
        );
      })
      .join("");
    return `<g stroke-linejoin="round">${sides}${polygon(shape, `url(#TOP)`)}${polygon(shape, "none", 'stroke="#ffffff" stroke-opacity=".55" stroke-width="2"')}</g>`;
  }
  function art(plan) {
    const p = plan.palette,
      id = "world_" + plan.stageId,
      f = plan.family;
    let land = "",
      objects = "";
    const base = (shape, p) => {
      const points = shape
        .split(" ")
        .map((pair, i) => {
          let [x, y] = pair.split(",").map(Number);
          const shift =
            plan.variant === 1
              ? i % 2
                ? 10
                : -8
              : plan.variant === 2
                ? i % 3
                  ? 5
                  : -12
                : 0;
          return `${x + shift},${y + (plan.variant === 2 && i % 2 ? -7 : 0)}`;
        })
        .join(" ");
      return terrain(points, p);
    };
    if (f === "workshop") {
      land = base(
        "32,141 104,104 153,111 195,85 325,140 252,184 173,172 115,189",
        p,
      );
      objects =
        box(87, 140, 52, 24, 38, p.accent, "#e8f5ff") +
        box(178, 137, 63, 28, 59, "#ded9ed", "#fef9ff") +
        `<g stroke="#7589ac" stroke-width="7"><path d="M148 130l32-17M126 149l50 11"/></g><g transform="translate(219 89)"><circle r="20" fill="#c0afd9" stroke="#fff" stroke-width="6"/><circle r="7" fill="#6c658b"/><path d="M0-27v8M27 0h-8M0 27v-8M-27 0h8" stroke="#8979ad" stroke-width="8"/></g>` +
        tree(273, 151, "#a5c7bc", 0.7);
    } else if (f === "laboratory") {
      land = base(
        "55,126 130,89 188,106 237,92 307,143 257,173 214,174 177,196 84,166",
        p,
      );
      objects =
        `<path d="M99 150l58-24 57 25 47-25M157 126v-22M214 151v17" fill="none" stroke="#f3fffc" stroke-width="4"/>` +
        box(140, 133, 53, 27, 44, "#a2cbdc", "#effcff") +
        polygon("230,74 252,107 239,144 214,112", p.accent) +
        polygon("230,74 239,144 230,113", "#fff", 'opacity=".55"') +
        `<ellipse cx="176" cy="86" rx="34" ry="13" fill="none" stroke="#b2a3e4" stroke-width="5"/><path d="M176 65v42" stroke="#fff" stroke-width="4"/><circle cx="176" cy="86" r="9" fill="#78d6cf"/>`;
    } else if (f === "bridges") {
      land =
        base("26,141 82,110 135,136 107,169 62,166", p) +
        base("150,123 211,91 268,121 213,155", p) +
        base("210,171 269,140 326,170 268,201", p);
      objects =
        `<path d="M109 137l49-14M216 145l29 20" stroke="#9b83b6" stroke-width="17"/><path d="M109 131l49-14M216 139l29 20" stroke="#f9f3ff" stroke-width="12"/>` +
        box(62, 143, 29, 14, 25, "#c9b5ed", "#fff9fd") +
        box(195, 123, 31, 18, 32, p.accent, "#f1fcff") +
        box(253, 171, 27, 16, 22, "#f3d498", "#fff8df") +
        tree(290, 164, "#8fc5ad", 0.65);
    } else if (f === "garden") {
      land = base(
        "35,140 65,112 112,101 167,108 222,95 286,112 321,147 273,177 218,184 151,177 97,189",
        p,
      );
      objects =
        `<path d="M79 151q57-65 97-18t92 8" fill="none" stroke="#fff6dc" stroke-width="13"/>` +
        box(139, 138, 57, 26, 41, "#e4bcbd", "#fff4dd") +
        polygon("137,98 176,65 224,99 196,112", "#ae9acb") +
        tree(84, 143, "#b2cdaa", 1.15) +
        tree(262, 142, "#9dbed3", 1) +
        `<ellipse cx="236" cy="163" rx="19" ry="8" fill="#8ed3dc"/><path d="M116 157l10-15 10 15z" fill="#eebaa6"/>`;
    } else if (f === "observatory") {
      land = base(
        "67,159 90,122 150,106 171,81 239,108 294,149 247,182 188,196 129,184",
        p,
      );
      objects =
        box(129, 151, 65, 32, 32, "#c5bfda", "#f7eeff") +
        box(151, 118, 44, 22, 41, "#e1dced", "#f9f5ff") +
        `<path d="M148 78a34 27 0 0170 0z" fill="#b4a0d5"/><path d="M177 51v27" stroke="#e9e1f8" stroke-width="4"/><g transform="translate(212 70) rotate(-28)"><rect x="-13" y="-6" width="39" height="12" rx="4" fill="#8a9fbd"/><ellipse cx="26" rx="6" ry="10" fill="#d9eff4"/></g><path d="M99 158l20-10m-6 17l20-10m-6 17l20-10" stroke="#fff7e8" stroke-width="7"/>` +
        tree(256, 155, "#a9cab8", 0.7);
    } else {
      land = base(
        "34,136 92,102 144,113 193,93 269,106 326,143 274,183 199,174 138,194 79,173",
        p,
      );
      objects =
        `<ellipse cx="181" cy="150" rx="40" ry="19" fill="#fbf7ed"/><path d="M89 144l70 6m44-13l43-12" stroke="#e8d8b9" stroke-width="9"/>` +
        box(69, 142, 35, 19, 33, "#d2b8da", "#fff1e4") +
        box(151, 116, 42, 22, 43, p.accent, "#f4f6ff") +
        box(241, 146, 33, 19, 31, "#f1cf9e", "#fff8e9") +
        tree(276, 157, "#8fc4ab", 0.85) +
        tree(118, 164, "#afc4dc", 0.65);
    }
    // Variation changes physical environmental composition, not just color or icon.
    objects +=
      plan.variant === 0
        ? tree(52, 156, "#b0ccb5", 0.65)
        : plan.variant === 1
          ? `<g fill="#f5cf8f"><ellipse cx="304" cy="154" rx="11" ry="5"/><ellipse cx="296" cy="162" rx="8" ry="4"/></g>`
          : `<path d="M54 151v-25l18 6-18 6" fill="#f2d39c" stroke="#af95b0" stroke-width="3"/>`;
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 240" role="img" aria-label="${f} miniature island" data-family="${f}" data-camera="isometric" data-light="upper-left"><defs><linearGradient id="TOP" x2=".8" y2="1"><stop stop-color="${p.light}"/><stop offset="1" stop-color="${p.top}"/></linearGradient><filter id="SHADOW" x="-25%" y="-30%" width="150%" height="170%"><feDropShadow dx="0" dy="7" stdDeviation="5" flood-color="#514370" flood-opacity=".14"/></filter></defs><ellipse cx="181" cy="218" rx="119" ry="11" fill="#7e6b9c" opacity=".09"/><g filter="url(#SHADOW)">${land}${objects}</g></svg>`;
    return svg
      .replaceAll("TOP", id + "_top")
      .replaceAll("SHADOW", id + "_shadow");
  }
  return { render: art };
})();
