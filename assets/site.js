const SITE_DATA = window.SITE_DATA;

const ICONS = {
  beaker:
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M9 2h6v2l-1 1v4.4l4.8 7.7A3 3 0 0 1 16.25 22h-8.5a3 3 0 0 1-2.55-4.9L10 9.4V5L9 4V2Zm2 4.17v3.8l-4.1 6.58a1 1 0 0 0 .85 1.45h8.5a1 1 0 0 0 .85-1.45L13 9.97v-3.8l.59-.59h-3.18l.59.59Z"/></svg>',
  branch:
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M7 3a3 3 0 0 1 1 5.83V10a3 3 0 0 0 3 3h2.17a3 3 0 1 1 0 2H11a5 5 0 0 1-5-5V8.83A3 3 0 1 1 7 3Zm0 2a1 1 0 1 0 0 2 1 1 0 0 0 0-2Zm10 10a1 1 0 1 0 0 2 1 1 0 0 0 0-2Zm0-10a3 3 0 0 1 1 5.83V18a3 3 0 1 1-2 0v-7.17A3 3 0 0 1 17 5Zm0 2a1 1 0 1 0 0 2 1 1 0 0 0 0-2Zm0 12a1 1 0 1 0 0 2 1 1 0 0 0 0-2Z"/></svg>',
  browser:
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4 5a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V5Zm2 0v2h12V5H6Zm12 14V9H6v10h12Z"/></svg>',
  chart:
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M5 3h2v18H5V3Zm6 8h2v10h-2V11Zm6-5h2v15h-2V6Z"/></svg>',
  chip:
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M9 2h2v2h2V2h2v2.13A4 4 0 0 1 18.87 8H21v2h-2v2h2v2h-2v2h2v2h-2.13A4 4 0 0 1 15 19.87V22h-2v-2h-2v2H9v-2.13A4 4 0 0 1 5.13 18H3v-2h2v-2H3v-2h2v-2H3V8h2.13A4 4 0 0 1 9 4.13V2Zm0 4a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2H9Zm1 2h4v8h-4V8Z"/></svg>',
  cloud:
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M7 18a4 4 0 1 1 .7-7.94A5.5 5.5 0 0 1 18.5 11a3.5 3.5 0 1 1 0 7H7Z"/></svg>',
  code:
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="m8.7 16.6-4-4 4-4 1.4 1.4L7.5 12l2.6 2.6-1.4 1.4Zm6.6 0-1.4-1.4 2.6-2.6-2.6-2.6 1.4-1.4 4 4-4 4ZM13.6 4l-3.2 16h-2l3.2-16h2Z"/></svg>',
  droplet:
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2s6 6.2 6 11a6 6 0 1 1-12 0c0-4.8 6-11 6-11Zm0 15a4 4 0 0 0 4-4c0-2.2-2.3-5.6-4-7.5-1.7 1.9-4 5.3-4 7.5a4 4 0 0 0 4 4Z"/></svg>',
  folder:
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M3 6a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8.5A2.5 2.5 0 0 1 18.5 19h-13A2.5 2.5 0 0 1 3 16.5V6Zm2 2v8.5a.5.5 0 0 0 .5.5h13a.5.5 0 0 0 .5-.5V8H5Z"/></svg>',
  leaf:
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M19 3c-7.5 0-13 4.1-13 10a6 6 0 0 0 6 6c5.9 0 10-5.5 10-13V3h-3Zm-6.3 12.3-1.4-1.4 4.6-4.6c-5 .3-8.3 2.7-8.3 7.7a4 4 0 0 0 4 4c3.7 0 6.7-3.1 7.2-8.8l-6.1 6.1Z"/></svg>',
};

function setText(id, value) {
  document.getElementById(id).textContent = value;
}

function formatDate(isoDate) {
  return new Date(isoDate).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

function statCard(value, label) {
  const card = document.createElement("div");
  card.className = "stat-card";
  card.innerHTML = `<strong>${value}</strong><p>${label}</p>`;
  return card;
}

function createCard(item, options = {}) {
  const card = document.createElement("article");
  card.className = "card";
  card.dataset.search = [
    item.name,
    item.description,
    item.language || "",
    options.subtitle || "",
    options.headline || item.headline || "",
  ]
    .join(" ")
    .toLowerCase();

  const pills = [];
  if (options.showLanguage && item.language) {
    pills.push(`<span class="pill">${item.language}</span>`);
  }
  if (item.fork) {
    pills.push('<span class="pill pill--fork">Fork</span>');
  }
  if (options.extraPill) {
    pills.push(`<span class="pill">${options.extraPill}</span>`);
  }

  const homepageLink = item.homepage
    ? `<a href="${item.homepage}" target="_blank" rel="noreferrer">Live Link</a>`
    : "";

  const subtitle = options.subtitle
    ? `<p class="meta">${options.subtitle}</p>`
    : item.updated_at
      ? `<p class="meta">Updated ${formatDate(item.updated_at)}</p>`
      : "";

  const headlineText = options.headline || item.headline || "";
  const headline = headlineText ? `<p>${headlineText}</p>` : "";
  const image = item.image
    ? `<img class="card__image" src="${item.image}" alt="${item.name} preview" loading="lazy" onerror="this.style.display='none'" />`
    : "";

  card.innerHTML = `
    ${image}
    <div class="card__icon">${ICONS[item.icon] || ICONS.folder}</div>
    <div class="card__title-row">
      <a class="card__title" href="${item.url}" target="_blank" rel="noreferrer">
        <h3>${item.name}</h3>
      </a>
    </div>
    ${subtitle}
    <div class="pill-row">${pills.join("")}</div>
    ${headline}
    <p>${item.description}</p>
    <div class="card__actions">
      <a href="${item.url}" target="_blank" rel="noreferrer">View Repo</a>
      ${homepageLink}
    </div>
  `;

  return card;
}

function renderCards(targetId, items, options = {}) {
  const target = document.getElementById(targetId);
  items.forEach((item) => target.appendChild(createCard(item, options)));
}

function renderOrganizations(organizations) {
  const root = document.getElementById("org-sections");

  organizations.forEach((org) => {
    const section = document.createElement("section");
    section.className = "repo-group";

    const header = document.createElement("div");
    header.className = "org-block__header";
    header.innerHTML = `
      <h3>${org.name}</h3>
      <div class="org-block__actions">
        <a href="${org.github_url}" target="_blank" rel="noreferrer">GitHub Page</a>
        <a href="${org.website_url}" target="_blank" rel="noreferrer">Website</a>
      </div>
    `;
    section.appendChild(header);

    const grid = document.createElement("div");
    grid.className = "card-grid";
    org.repos.forEach((repo) => grid.appendChild(createCard(repo, { showLanguage: true })));
    section.appendChild(grid);

    root.appendChild(section);
  });
}

function renderStats(data) {
  const stats = document.getElementById("stats-row");
  const createdCount = data.personal.created.length;
  const forkedCount = data.personal.forked.length;
  const orgCount = data.organizations.reduce((total, org) => total + org.repos.length, 0);

  stats.appendChild(statCard(data.featured.length, "Featured tools"));
  stats.appendChild(statCard(createdCount, "Original repositories"));
  stats.appendChild(statCard(forkedCount, "Forked repositories"));
  stats.appendChild(statCard(orgCount, "Collaboration repos"));
}

function setupSearch() {
  const input = document.getElementById("project-search");
  const cards = Array.from(document.querySelectorAll("#projects .card, #organizations .card"));

  input.addEventListener("input", () => {
    const query = input.value.trim().toLowerCase();

    cards.forEach((card) => {
      const matches = !query || card.dataset.search.includes(query);
      card.classList.toggle("is-hidden", !matches);
    });
  });
}

function init() {
  setText("site-title", SITE_DATA.profile.title);
  setText("site-tagline", SITE_DATA.profile.tagline);
  setText("site-about", SITE_DATA.profile.about);
  setText("private-repos-note", SITE_DATA.notes.private_repos);
  setText(
    "automation-note",
    "The repo list on this page is generated automatically so the catalog stays current. If you want to build something similar, the Python generator and site source are available in this repository."
  );
  document.getElementById("automation-icon").innerHTML = ICONS.code;

  renderCards("featured-grid", SITE_DATA.featured, {
    showLanguage: true,
    subtitle: "Featured project",
  });
  renderCards("apps-grid", SITE_DATA.online_apps, {
    extraPill: "Live app",
    subtitle: "Interactive deployment",
  });
  renderCards("created-grid", SITE_DATA.personal.created, { showLanguage: true });
  renderCards("forked-grid", SITE_DATA.personal.forked, { showLanguage: true });
  renderOrganizations(SITE_DATA.organizations);
  renderStats(SITE_DATA);
  setupSearch();
}

init();
