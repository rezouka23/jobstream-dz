const STORAGE_KEY = "jobstream_lang";
const DEFAULT_LANG = "fr";
const TODAY_JOBS_PATH = "/api/jobs/today";

const STRINGS = {
  fr: {
    meta: {
      title: "JobStream DZ | Offres du jour",
      description: "Consultez les offres ajoutées aujourd'hui sur JobStream DZ.",
    },
    nav: {
      home: "Accueil",
      jobsToday: "Offres du jour",
      cvMatch: "Matching CV",
      proof: "Preuves",
      feed: "Digest",
      story: "Méthode",
      faq: "FAQ",
      join: "Recevoir les offres",
    },
    today: {
      kicker: "Flux principal Google Sheets",
      title: "Offres ajoutées <span>aujourd'hui.</span>",
      subtitle: "Une page dédiée aux offres arrivées dans le flux principal aujourd'hui, avec un retour sur la date de publication quand l'horodatage d'arrivée manque.",
      note: "Cette page lit la feuille principale en direct via l'API JobStream DZ. Les liens restent privés côté serveur et les résultats sont mis en cache quelques minutes.",
      listTitle: "Toutes les offres du jour",
      listSubtitle: "Recherchez, filtrez et ouvrez les annonces directement depuis le flux collecté aujourd'hui.",
      telegram: "Recevoir les prochains lots sur Telegram",
      loading: "Chargement des offres du jour...",
      empty: "Aucune offre exploitable pour aujourd'hui.",
      error: "Impossible de charger les offres. Réessayez.",
      retry: "Réessayer",
      updated: "Mis à jour",
      apply: "Postuler",
      unavailableLink: "Lien indisponible",
      untitled: "Offre sans titre",
      unknownCompany: "Entreprise non précisée",
      unknownLocation: "Lieu non précisé",
      addedBasis: "Arrivée",
      fallbackBasis: "Date source",
      stats: {
        total: "offres aujourd'hui",
        windowTotal: "offres dans la période",
        date: "jour local Algérie",
        refreshed: "dernière lecture",
      },
      filters: {
        searchLabel: "Filtrer les offres",
        searchPlaceholder: "Rechercher un poste, une entreprise...",
        sourceLabel: "Source",
        allSources: "Toutes",
        locationLabel: "Lieu",
        allLocations: "Tous",
        showMoreLocations: "Afficher les {count} lieux",
        showLessLocations: "Réduire les lieux",
        clear: "Effacer les filtres",
        noMatches: "Aucune offre ne correspond à votre recherche.",
        resultsLabel: "Résultats",
      },
      pagination: {
        nav: "Pagination des offres",
        previous: "Précédent",
        next: "Suivant",
        status: "Offres {start}-{end} sur {total}",
        page: "Page {page}",
      },
      dash: {
        liveFeed: "Flux en direct",
        heroTagline: "Mises à jour en temps réel depuis des sources vérifiées partout en Algérie.",
        statTotalSub: "Postes collectés aujourd'hui",
        statWindowSub: "Fenêtre choisie par le filtre",
        statDateSub: "Algérie (GMT+1)",
        statSources: "Sources actives",
        statSourcesSub: "LinkedIn, sites carrière et plus",
        filterTitle: "Filtrer les offres",
        clearAll: "Tout effacer",
        sourcesLabel: "Sources",
        recencyLabel: "Récence",
        recencyAll: "Aujourd'hui",
        recency24: "Dernières 24h",
        recency3: "3 derniers jours",
        recency7: "7 derniers jours",
        allAlgeria: "Toute l'Algérie",
        sortBy: "Trier par",
        sortNewest: "Plus récentes",
        sortOldest: "Plus anciennes",
        viewLabel: "Affichage",
        gridView: "Vue grille",
        listView: "Vue liste",
        jobsFound: "offres trouvées",
        jobFound: "offre trouvée",
        endOfFeed: "Vous avez atteint la fin du flux du jour",
        badgeNew: "Nouveau",
        badgeCompany: "Site entreprise",
        bookmark: "Enregistrer l'offre",
      },
    },
    a11y: {
      nav: "Navigation principale",
      langSwitch: "Choix de la langue",
      menu: "Ouvrir le menu",
    },
  },
  en: {
    meta: {
      title: "JobStream DZ | Today's jobs",
      description: "Browse jobs added today on JobStream DZ.",
    },
    nav: {
      home: "Home",
      jobsToday: "Today's jobs",
      cvMatch: "CV match",
      proof: "Proof",
      feed: "Digest",
      story: "Method",
      faq: "FAQ",
      join: "Get job alerts",
    },
    today: {
      kicker: "Main Google Sheets feed",
      title: "Jobs added <span>today.</span>",
      subtitle: "A focused page for jobs that arrived in the main feed today, with a published-date fallback when arrival timestamps are missing.",
      note: "This page reads the main sheet through the JobStream DZ API. Credentials stay server-side and results are cached briefly.",
      listTitle: "All jobs added today",
      listSubtitle: "Search, filter, and open roles directly from today's collected feed.",
      telegram: "Get the next batches on Telegram",
      loading: "Loading today's jobs...",
      empty: "No usable jobs for today yet.",
      error: "Unable to load jobs. Please retry.",
      retry: "Retry",
      updated: "Updated",
      apply: "Apply now",
      unavailableLink: "Link unavailable",
      untitled: "Untitled role",
      unknownCompany: "Unknown company",
      unknownLocation: "Unknown location",
      addedBasis: "Arrived",
      fallbackBasis: "Source date",
      stats: {
        total: "jobs today",
        windowTotal: "jobs in window",
        date: "Algeria local day",
        refreshed: "last read",
      },
      filters: {
        searchLabel: "Filter jobs",
        searchPlaceholder: "Search a role, company...",
        sourceLabel: "Source",
        allSources: "All",
        locationLabel: "Location",
        allLocations: "All",
        showMoreLocations: "Show all {count} locations",
        showLessLocations: "Show fewer locations",
        clear: "Clear filters",
        noMatches: "No jobs match your search.",
        resultsLabel: "Results",
      },
      pagination: {
        nav: "Jobs pagination",
        previous: "Previous",
        next: "Next",
        status: "Jobs {start}-{end} of {total}",
        page: "Page {page}",
      },
      dash: {
        liveFeed: "Live feed",
        heroTagline: "Real-time updates from verified sources across Algeria.",
        statTotalSub: "Roles collected today",
        statWindowSub: "Selected recency window",
        statDateSub: "Algeria (GMT+1)",
        statSources: "Sources active",
        statSourcesSub: "LinkedIn, company sites & more",
        filterTitle: "Filter jobs",
        clearAll: "Clear all",
        sourcesLabel: "Sources",
        recencyLabel: "Recency",
        recencyAll: "Today",
        recency24: "Last 24h",
        recency3: "Last 3 days",
        recency7: "Last 7 days",
        allAlgeria: "All Algeria",
        sortBy: "Sort by",
        sortNewest: "Newest",
        sortOldest: "Oldest",
        viewLabel: "View",
        gridView: "Grid view",
        listView: "List view",
        jobsFound: "jobs found",
        jobFound: "job found",
        endOfFeed: "You've reached the end of today's feed",
        badgeNew: "New",
        badgeCompany: "Company site",
        bookmark: "Save job",
      },
    },
    a11y: {
      nav: "Main navigation",
      langSwitch: "Language switcher",
      menu: "Open menu",
    },
  },
  ar: {
    meta: {
      title: "JobStream DZ | وظائف اليوم",
      description: "تصفح الوظائف التي أضيفت اليوم على JobStream DZ.",
    },
    nav: {
      home: "الرئيسية",
      jobsToday: "وظائف اليوم",
      cvMatch: "مطابقة السيرة",
      proof: "الدليل",
      feed: "الملخص",
      story: "الطريقة",
      faq: "الأسئلة",
      join: "استقبل الوظائف",
    },
    today: {
      kicker: "التدفق الرئيسي من Google Sheets",
      title: "وظائف أضيفت <span>اليوم.</span>",
      subtitle: "صفحة مخصصة للوظائف التي وصلت إلى التدفق الرئيسي اليوم، مع استخدام تاريخ النشر عندما لا يتوفر وقت الإضافة.",
      note: "تقرأ هذه الصفحة الورقة الرئيسية عبر واجهة JobStream DZ. تبقى بيانات الوصول في الخادم وتخزن النتائج مؤقتا لفترة قصيرة.",
      listTitle: "كل وظائف اليوم",
      listSubtitle: "ابحث وصفّ وافتح العروض مباشرة من التدفق الذي جمع اليوم.",
      telegram: "استقبل الدفعات القادمة على تيليجرام",
      loading: "جار تحميل وظائف اليوم...",
      empty: "لا توجد وظائف قابلة للاستخدام لهذا اليوم.",
      error: "تعذر تحميل الوظائف. يرجى المحاولة مجددا.",
      retry: "إعادة المحاولة",
      updated: "آخر تحديث",
      apply: "قدّم الآن",
      unavailableLink: "الرابط غير متاح",
      untitled: "وظيفة بدون عنوان",
      unknownCompany: "شركة غير محددة",
      unknownLocation: "مكان غير محدد",
      addedBasis: "وصلت",
      fallbackBasis: "تاريخ المصدر",
      stats: {
        total: "وظائف اليوم",
        windowTotal: "وظائف في الفترة",
        date: "اليوم المحلي للجزائر",
        refreshed: "آخر قراءة",
      },
      filters: {
        searchLabel: "تصفية الوظائف",
        searchPlaceholder: "ابحث عن وظيفة أو شركة...",
        sourceLabel: "المصدر",
        allSources: "الكل",
        locationLabel: "المكان",
        allLocations: "الكل",
        showMoreLocations: "عرض كل الأماكن ({count})",
        showLessLocations: "إظهار أماكن أقل",
        clear: "مسح عوامل التصفية",
        noMatches: "لا توجد وظيفة تطابق بحثك.",
        resultsLabel: "النتائج",
      },
      pagination: {
        nav: "ترقيم صفحات الوظائف",
        previous: "السابق",
        next: "التالي",
        status: "الوظائف {start}-{end} من {total}",
        page: "الصفحة {page}",
      },
      dash: {
        liveFeed: "بث مباشر",
        heroTagline: "تحديثات لحظية من مصادر موثوقة عبر الجزائر.",
        statTotalSub: "وظائف جُمعت اليوم",
        statWindowSub: "الفترة المختارة من الفلتر",
        statDateSub: "الجزائر (توقيت +1)",
        statSources: "المصادر النشطة",
        statSourcesSub: "لينكدإن ومواقع الشركات والمزيد",
        filterTitle: "تصفية الوظائف",
        clearAll: "مسح الكل",
        sourcesLabel: "المصادر",
        recencyLabel: "الحداثة",
        recencyAll: "اليوم",
        recency24: "آخر 24 ساعة",
        recency3: "آخر 3 أيام",
        recency7: "آخر 7 أيام",
        allAlgeria: "كل الجزائر",
        sortBy: "ترتيب حسب",
        sortNewest: "الأحدث",
        sortOldest: "الأقدم",
        viewLabel: "العرض",
        gridView: "عرض شبكي",
        listView: "عرض قائمة",
        jobsFound: "وظيفة",
        jobFound: "وظيفة",
        endOfFeed: "لقد وصلت إلى نهاية تدفق اليوم",
        badgeNew: "جديد",
        badgeCompany: "موقع الشركة",
        bookmark: "حفظ الوظيفة",
      },
    },
    a11y: {
      nav: "التنقل الرئيسي",
      langSwitch: "تبديل اللغة",
      menu: "فتح القائمة",
    },
  },
};

const BOOKMARK_KEY = "jobstream_today_bookmarks";
const PAGE_SIZE = 24;
const LOCATION_CHIP_LIMIT = 8;

function loadBookmarks() {
  try {
    const raw = window.localStorage.getItem(BOOKMARK_KEY);
    const list = raw ? JSON.parse(raw) : [];
    return new Set(Array.isArray(list) ? list : []);
  } catch (error) {
    return new Set();
  }
}

const state = {
  loading: false,
  payload: null,
  error: "",
  query: "",
  source: "",
  location: "",
  recency: "",
  sort: "newest",
  view: "grid",
  page: 1,
  locationsExpanded: false,
  bookmarks: loadBookmarks(),
};

let searchDebounce = 0;
let fetchSequence = 0;

function getValueByPath(obj, path) {
  return path.split(".").reduce((acc, part) => (acc && typeof acc === "object" ? acc[part] : undefined), obj);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function safeLanguage(lang) {
  return Object.prototype.hasOwnProperty.call(STRINGS, lang) ? lang : DEFAULT_LANG;
}

function getCurrentLanguage() {
  return safeLanguage(document.documentElement.lang || DEFAULT_LANG);
}

function getEndpoint() {
  const days = Number(state.recency);
  const safeDays = Number.isFinite(days) ? Math.max(1, Math.min(7, Math.round(days))) : 1;
  const path = safeDays > 1 ? `${TODAY_JOBS_PATH}?days=${safeDays}` : TODAY_JOBS_PATH;
  const apiBase = typeof window.JOBSTREAM_API_BASE === "string" ? window.JOBSTREAM_API_BASE.trim() : "";
  return apiBase ? new URL(path, apiBase).toString() : path;
}

function normalizeSearchText(value) {
  return String(value || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f\u064b-\u065f\u0670]/g, "")
    .toLowerCase()
    .trim();
}

function isPlaceholderValue(value) {
  const normalized = normalizeSearchText(value);
  return !normalized || ["not specified", "unknown", "inconnu", "non precise", "غير محدد"].includes(normalized);
}

function formatDate(value, lang) {
  const date = new Date(`${value}T00:00:00+01:00`);
  if (Number.isNaN(date.getTime())) {
    return value || "--";
  }
  const locale = lang === "ar" ? "ar-DZ" : lang === "en" ? "en-US" : "fr-FR";
  return new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeZone: "Africa/Algiers" }).format(date);
}

function formatTimestamp(value, lang) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value || "--";
  }
  const locale = lang === "ar" ? "ar-DZ" : lang === "en" ? "en-US" : "fr-FR";
  return new Intl.DateTimeFormat(locale, {
    dateStyle: "medium",
    timeStyle: "short",
    timeZone: "Africa/Algiers",
  }).format(date);
}

function formatRelativeTime(value, lang) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return "";
  }
  const minutes = Math.max(0, Math.round((Date.now() - date.getTime()) / 60000));
  const locale = lang === "ar" ? "ar-DZ" : lang === "en" ? "en-US" : "fr-FR";
  const formatter = new Intl.RelativeTimeFormat(locale, { numeric: "auto" });
  if (minutes >= 1440) {
    return formatter.format(-Math.round(minutes / 1440), "day");
  }
  if (minutes >= 60) {
    return formatter.format(-Math.round(minutes / 60), "hour");
  }
  return formatter.format(-minutes, "minute");
}

function sourceClassName(source) {
  const normalized = String(source || "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
  return normalized ? `source-${normalized}` : "source-unknown";
}

function uniqueValues(jobs, key) {
  const values = [];
  jobs.forEach((job) => {
    const value = String(job[key] || "").trim();
    if (!value || isPlaceholderValue(value) || values.includes(value)) {
      return;
    }
    values.push(value);
  });
  return values;
}

function sourceIconId(value) {
  const v = normalizeSearchText(value);
  if (v.includes("linkedin")) return "icon-broadcast";
  if (v.includes("company") || v.includes("site") || v.includes("globe")) return "icon-globe";
  return "";
}

function renderChips(node, values, activeValue, allLabel, facet) {
  if (!node) {
    return;
  }
  const items = [{ value: "", label: allLabel }].concat(values.map((value) => ({ value, label: value })));
  node.innerHTML = items
    .map((item) => {
      const active = item.value === activeValue;
      const iconId = facet === "source" && item.value ? sourceIconId(item.value) : "";
      const iconMarkup = iconId ? `<svg class="icon" aria-hidden="true"><use href="#${iconId}"></use></svg>` : "";
      return `<button type="button" class="jt-chip ${active ? "is-active" : ""}" data-facet="${facet}" data-value="${escapeHtml(item.value)}" aria-pressed="${active}">${iconMarkup}${escapeHtml(item.label)}</button>`;
    })
    .join("");
}

function visibleLocationValues(locations) {
  if (state.locationsExpanded || locations.length <= LOCATION_CHIP_LIMIT) {
    return locations;
  }
  const visible = locations.slice(0, LOCATION_CHIP_LIMIT);
  if (state.location && locations.includes(state.location) && !visible.includes(state.location)) {
    visible.push(state.location);
  }
  return visible;
}

function getJobTime(job) {
  const raw = job.added_at || job.arrival_date || job.published_date || "";
  if (!raw) {
    return NaN;
  }
  const date = new Date(job.added_at ? raw : `${raw}T00:00:00+01:00`);
  return date.getTime();
}

function jobMatches(job) {
  if (state.source && String(job.source || "") !== state.source) {
    return false;
  }
  if (state.location && String(job.location || "") !== state.location) {
    return false;
  }
  if (state.recency) {
    const days = Number(state.recency);
    const time = getJobTime(job);
    if (!Number.isNaN(time) && (Date.now() - time) / 86400000 > days) {
      return false;
    }
  }
  if (state.query) {
    const haystack = normalizeSearchText([job.title, job.company_name, job.location, job.source].filter(Boolean).join(" "));
    if (!haystack.includes(state.query)) {
      return false;
    }
  }
  return true;
}

function sortJobs(jobs) {
  const dir = state.sort === "oldest" ? 1 : -1;
  return [...jobs].sort((a, b) => {
    const ta = getJobTime(a);
    const tb = getJobTime(b);
    return ((Number.isNaN(ta) ? 0 : ta) - (Number.isNaN(tb) ? 0 : tb)) * dir;
  });
}

function totalPagesFor(total) {
  return Math.max(1, Math.ceil(total / PAGE_SIZE));
}

function clampPage(total) {
  const totalPages = totalPagesFor(total);
  state.page = Math.min(Math.max(1, state.page), totalPages);
  return totalPages;
}

function paginatedJobs(jobs) {
  const start = (state.page - 1) * PAGE_SIZE;
  return jobs.slice(start, start + PAGE_SIZE);
}

function paginationPages(totalPages) {
  const pages = new Set([1, totalPages, state.page, state.page - 1, state.page + 1]);
  return [...pages]
    .filter((page) => page >= 1 && page <= totalPages)
    .sort((a, b) => a - b);
}

function formatClock(value, lang) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value || "--";
  }
  const locale = lang === "ar" ? "ar-DZ" : lang === "en" ? "en-US" : "fr-FR";
  return new Intl.DateTimeFormat(locale, { timeStyle: "short", timeZone: "Africa/Algiers" }).format(date);
}

function setText(selector, value) {
  const node = document.querySelector(selector);
  if (node) node.textContent = value;
}

function renderStats(jobs, lang, dict) {
  const isExpandedWindow = Number(state.recency || 1) > 1;
  setText("[data-jobs-total]", String(state.payload?.job_count || jobs.length || 0));
  setText("[data-jobs-total-label]", isExpandedWindow ? dict.today.stats.windowTotal : dict.today.stats.total);
  setText("[data-stat-total-sub]", isExpandedWindow ? dict.today.dash.statWindowSub : dict.today.dash.statTotalSub);
  setText("[data-jobs-date]", formatDate(state.payload?.date || "", lang));
  setText("[data-jobs-refreshed]", formatClock(state.payload?.generated_at || "", lang));
  setText("[data-jobs-sources]", String(uniqueValues(jobs, "source").length || 0));
  const sub = formatRelativeTime(state.payload?.generated_at || "", lang);
  if (sub) setText("[data-stat-refreshed-sub]", sub);
}

function renderFilters(jobs, dict) {
  const sources = uniqueValues(jobs, "source");
  const locations = uniqueValues(jobs, "location");
  renderChips(document.querySelector("[data-today-source-chips]"), sources, state.source, dict.today.filters.allSources, "source");
  renderChips(
    document.querySelector("[data-today-location-chips]"),
    visibleLocationValues(locations),
    state.location,
    dict.today.filters.allLocations,
    "location",
  );

  const select = document.querySelector("[data-today-location-select]");
  if (select) {
    const opts = [{ value: "", label: dict.today.dash.allAlgeria }].concat(locations.map((v) => ({ value: v, label: v })));
    select.innerHTML = opts
      .map((o) => `<option value="${escapeHtml(o.value)}"${o.value === state.location ? " selected" : ""}>${escapeHtml(o.label)}</option>`)
      .join("");
  }

  const locationGroup = document.querySelector("[data-today-location-group]");
  if (locationGroup) locationGroup.hidden = locations.length < 2;

  const locationToggle = document.querySelector("[data-today-location-toggle]");
  if (locationToggle) {
    const canToggle = locations.length > LOCATION_CHIP_LIMIT;
    locationToggle.hidden = !canToggle;
    locationToggle.setAttribute("aria-expanded", String(state.locationsExpanded));
    locationToggle.textContent = state.locationsExpanded
      ? dict.today.filters.showLessLocations
      : dict.today.filters.showMoreLocations.replace("{count}", String(locations.length));
  }

  document.querySelectorAll("[data-today-recency-chips] .jt-chip").forEach((chip) => {
    const active = (chip.getAttribute("data-value") || "") === state.recency;
    chip.classList.toggle("is-active", active);
    chip.setAttribute("aria-pressed", String(active));
  });

  const hasActiveFilter = Boolean(state.query || state.source || state.location || state.recency);
  const clearTop = document.querySelector("[data-today-clear]");
  if (clearTop) clearTop.hidden = !hasActiveFilter;
}

function jobCardMarkup(job, dict, lang) {
  const id = job.apply_url || job.title || "";
  const saved = state.bookmarks.has(id);
  const title = escapeHtml(job.title || dict.today.untitled);
  const companyName = escapeHtml(isPlaceholderValue(job.company_name) ? dict.today.unknownCompany : job.company_name);
  const location = escapeHtml(isPlaceholderValue(job.location) ? dict.today.unknownLocation : job.location);
  const isLinkedin = normalizeSearchText(job.source).includes("linkedin");
  const sourceLabel = isLinkedin
    ? "LinkedIn"
    : job.source && !isPlaceholderValue(job.source)
      ? job.source
      : dict.today.dash.badgeCompany;
  const applyUrl = typeof job.apply_url === "string" ? job.apply_url.trim() : "";
  const dateLabel = escapeHtml(
    job.added_at ? formatTimestamp(job.added_at, lang) : job.published_date || formatDate(job.arrival_date || state.payload?.date || "", lang),
  );
  const action = applyUrl
    ? `<a class="jt-apply" href="${escapeHtml(applyUrl)}" target="_blank" rel="noreferrer">${escapeHtml(dict.today.apply)}<svg class="icon jt-apply-arrow" aria-hidden="true"><use href="#icon-arrow-right"></use></svg></a>`
    : `<span class="jt-apply is-disabled">${escapeHtml(dict.today.unavailableLink)}</span>`;

  return `
    <article class="jt-card">
      <div class="jt-card-top">
        <span class="jt-badge jt-badge-source">${escapeHtml(sourceLabel)}</span>
        <span class="jt-badge jt-badge-new">${escapeHtml(dict.today.dash.badgeNew)}</span>
        <button type="button" class="jt-bookmark ${saved ? "is-saved" : ""}" data-bookmark="${escapeHtml(id)}" aria-pressed="${saved}" aria-label="${escapeHtml(dict.today.dash.bookmark)}">
          <svg class="icon" aria-hidden="true"><use href="#icon-bookmark"></use></svg>
        </button>
      </div>
      <h3 class="jt-card-title" dir="auto">${title}</h3>
      <div class="jt-card-meta">
        <p dir="auto"><svg class="icon" aria-hidden="true"><use href="#icon-building"></use></svg><span>${companyName}</span></p>
        <p dir="auto"><svg class="icon" aria-hidden="true"><use href="#icon-map-pin"></use></svg><span>${location}</span></p>
        <p><svg class="icon" aria-hidden="true"><use href="#icon-clock"></use></svg><span>${dateLabel}</span></p>
      </div>
      ${action}
    </article>
  `;
}

function revealCards() {
  const cards = document.querySelectorAll("[data-today-list] .jt-card");
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || typeof IntersectionObserver === "undefined") {
    cards.forEach((card) => card.classList.add("is-in"));
    return;
  }
  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          obs.unobserve(entry.target);
        }
      });
    },
    { rootMargin: "0px 0px -8% 0px" },
  );
  cards.forEach((card) => observer.observe(card));
}

function renderJobs(jobs, dict, lang) {
  const listNode = document.querySelector("[data-today-list]");
  const endNode = document.querySelector("[data-today-end]");
  if (!listNode) return;
  listNode.setAttribute("data-view", state.view);
  listNode.setAttribute("aria-busy", "false");
  if (!jobs.length) {
    listNode.innerHTML = `<p class="jt-empty">${escapeHtml(dict.today.filters.noMatches)}</p>`;
    if (endNode) endNode.hidden = true;
    return;
  }
  listNode.innerHTML = jobs.map((job) => jobCardMarkup(job, dict, lang)).join("");
  if (endNode) endNode.hidden = false;
  revealCards();
}

function renderPagination(total, dict) {
  const node = document.querySelector("[data-today-pagination]");
  if (!node) return;

  const totalPages = totalPagesFor(total);
  if (total <= PAGE_SIZE) {
    node.hidden = true;
    node.innerHTML = "";
    return;
  }

  const start = (state.page - 1) * PAGE_SIZE + 1;
  const end = Math.min(total, state.page * PAGE_SIZE);
  const status = dict.today.pagination.status
    .replace("{start}", String(start))
    .replace("{end}", String(end))
    .replace("{total}", String(total));
  const pages = paginationPages(totalPages);
  let previousPage = 0;
  const pageButtons = pages
    .map((page) => {
      const gap = previousPage && page - previousPage > 1 ? '<span class="jt-page-ellipsis" aria-hidden="true">...</span>' : "";
      previousPage = page;
      const active = page === state.page;
      const label = dict.today.pagination.page.replace("{page}", String(page));
      return `${gap}<button type="button" class="jt-page-btn ${active ? "is-active" : ""}" data-page="${page}" aria-label="${escapeHtml(label)}" ${active ? 'aria-current="page"' : ""}>${page}</button>`;
    })
    .join("");

  node.hidden = false;
  node.innerHTML = `
    <p class="jt-pagination-status">${escapeHtml(status)}</p>
    <div class="jt-pagination-actions">
      <button type="button" class="jt-page-btn" data-page="${state.page - 1}" ${state.page <= 1 ? "disabled" : ""}>${escapeHtml(dict.today.pagination.previous)}</button>
      ${pageButtons}
      <button type="button" class="jt-page-btn" data-page="${state.page + 1}" ${state.page >= totalPages ? "disabled" : ""}>${escapeHtml(dict.today.pagination.next)}</button>
    </div>
  `;
}

function render(lang = getCurrentLanguage()) {
  const safeLang = safeLanguage(lang);
  const dict = STRINGS[safeLang];
  const listNode = document.querySelector("[data-today-list]");
  const statusNode = document.querySelector("[data-today-status]");
  const countNode = document.querySelector("[data-today-count]");
  const endNode = document.querySelector("[data-today-end]");
  if (!listNode) return;

  if (state.loading) {
    listNode.setAttribute("aria-busy", "true");
    listNode.setAttribute("data-view", state.view);
    listNode.innerHTML = `<p class="jt-empty">${escapeHtml(dict.today.loading)}</p>`;
    if (statusNode) statusNode.textContent = dict.today.loading;
    if (countNode) countNode.textContent = "";
    if (endNode) endNode.hidden = true;
    renderPagination(0, dict);
    return;
  }

  const jobs = Array.isArray(state.payload?.jobs) ? state.payload.jobs : [];
  renderStats(jobs, safeLang, dict);

  if (!jobs.length) {
    listNode.setAttribute("aria-busy", "false");
    listNode.innerHTML = `<p class="jt-empty">${escapeHtml(state.error ? dict.today.error : dict.today.empty)}${state.error ? `<br><button type="button" class="jt-page-btn" data-today-retry>${escapeHtml(dict.today.retry)}</button>` : ""}</p>`;
    if (statusNode) statusNode.textContent = state.error ? dict.today.error : dict.today.empty;
    if (countNode) countNode.textContent = "";
    if (endNode) endNode.hidden = true;
    renderPagination(0, dict);
    return;
  }

  renderFilters(jobs, dict);

  const filtered = sortJobs(jobs.filter(jobMatches));
  const totalPages = clampPage(filtered.length);
  const visibleJobs = paginatedJobs(filtered);
  if (countNode) {
    const label = filtered.length === 1 ? dict.today.dash.jobFound : dict.today.dash.jobsFound;
    countNode.textContent = `${filtered.length} ${label}`;
  }
  if (statusNode) {
    statusNode.textContent = `${dict.today.updated} ${formatRelativeTime(state.payload?.generated_at || "", safeLang)}`.trim();
  }

  renderJobs(visibleJobs, dict, safeLang);
  renderPagination(filtered.length, dict);
  if (endNode) endNode.hidden = state.page < totalPages || !visibleJobs.length;
}

async function fetchTodayJobs() {
  const sequence = ++fetchSequence;
  state.loading = true;
  state.error = "";
  render();

  try {
    const response = await fetch(getEndpoint(), { headers: { Accept: "application/json" }, cache: "no-store" });
    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }
    const payload = await response.json();
    if (sequence !== fetchSequence) return;
    const jobs = Array.isArray(payload.jobs) ? payload.jobs : [];
    state.payload = { ...payload, jobs };
    state.error = "";
  } catch (error) {
    if (sequence !== fetchSequence) return;
    state.payload = null;
    state.error = "load_failed";
  } finally {
    if (sequence !== fetchSequence) return;
    state.loading = false;
    render();
  }
}

function applyLanguage(lang) {
  const safeLang = safeLanguage(lang);
  const dict = STRINGS[safeLang];
  document.documentElement.lang = safeLang;
  document.documentElement.dir = safeLang === "ar" ? "rtl" : "ltr";
  document.documentElement.setAttribute("data-lang", safeLang);
  document.title = dict.meta.title;

  const metaDescription = document.querySelector('meta[name="description"]');
  if (metaDescription) {
    metaDescription.setAttribute("content", dict.meta.description);
  }

  document.querySelectorAll("[data-i18n]").forEach((node) => {
    const value = getValueByPath(dict, node.getAttribute("data-i18n") || "");
    if (typeof value === "string") node.textContent = value;
  });
  document.querySelectorAll("[data-i18n-html]").forEach((node) => {
    const value = getValueByPath(dict, node.getAttribute("data-i18n-html") || "");
    if (typeof value === "string") node.innerHTML = value;
  });
  document.querySelectorAll("[data-i18n-aria-label]").forEach((node) => {
    const value = getValueByPath(dict, node.getAttribute("data-i18n-aria-label") || "");
    if (typeof value === "string") node.setAttribute("aria-label", value);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((node) => {
    const value = getValueByPath(dict, node.getAttribute("data-i18n-placeholder") || "");
    if (typeof value === "string") node.setAttribute("placeholder", value);
  });

  document.querySelectorAll(".lang-btn").forEach((button) => {
    const active = button.getAttribute("data-lang") === safeLang;
    button.classList.toggle("is-active", active);
    button.setAttribute("aria-pressed", String(active));
  });
  window.localStorage.setItem(STORAGE_KEY, safeLang);
  render(safeLang);
}

function setupEvents() {
  document.querySelectorAll(".lang-btn").forEach((button) => {
    button.addEventListener("click", () => applyLanguage(button.getAttribute("data-lang") || DEFAULT_LANG));
  });

  const navToggle = document.querySelector(".nav-toggle");
  const siteMenu = document.querySelector("#site-menu");
  if (navToggle && siteMenu) {
    navToggle.addEventListener("click", () => {
      const expanded = navToggle.getAttribute("aria-expanded") === "true";
      navToggle.setAttribute("aria-expanded", String(!expanded));
      siteMenu.classList.toggle("is-open", !expanded);
    });
  }

  const search = document.querySelector("[data-today-search]");
  if (search) {
    search.addEventListener("input", () => {
      window.clearTimeout(searchDebounce);
      searchDebounce = window.setTimeout(() => {
        state.query = normalizeSearchText(search.value);
        state.page = 1;
        render();
      }, 120);
    });
  }

  const locationSelect = document.querySelector("[data-today-location-select]");
  if (locationSelect) {
    locationSelect.addEventListener("change", () => {
      state.location = locationSelect.value;
      state.page = 1;
      render();
    });
  }

  const sortSelect = document.querySelector("[data-today-sort]");
  if (sortSelect) {
    sortSelect.addEventListener("change", () => {
      state.sort = sortSelect.value;
      state.page = 1;
      render();
    });
  }

  document.querySelectorAll(".jt-view-btn").forEach((button) => {
    button.addEventListener("click", () => {
      state.view = button.getAttribute("data-view") || "grid";
      document.querySelectorAll(".jt-view-btn").forEach((btn) => {
        const active = btn === button;
        btn.classList.toggle("is-active", active);
        btn.setAttribute("aria-pressed", String(active));
      });
      const listNode = document.querySelector("[data-today-list]");
      if (listNode) listNode.setAttribute("data-view", state.view);
    });
  });

  document.addEventListener("click", (event) => {
    if (event.target.closest("[data-today-retry]")) {
      fetchTodayJobs();
      return;
    }
    const chip = event.target.closest("[data-facet]");
    if (chip) {
      const facet = chip.getAttribute("data-facet");
      const value = chip.getAttribute("data-value") || "";
      if (facet === "source") state.source = value;
      if (facet === "location") state.location = value;
      if (facet === "recency") {
        if (state.recency === value) return;
        state.recency = value;
        state.page = 1;
        fetchTodayJobs();
        return;
      }
      state.page = 1;
      render();
      return;
    }
    const pageButton = event.target.closest("[data-page]");
    if (pageButton && !pageButton.disabled) {
      state.page = Number(pageButton.getAttribute("data-page") || 1);
      render();
      document.querySelector(".jt-results")?.scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }
    const locationToggle = event.target.closest("[data-today-location-toggle]");
    if (locationToggle) {
      state.locationsExpanded = !state.locationsExpanded;
      render();
      return;
    }
    const bookmark = event.target.closest("[data-bookmark]");
    if (bookmark) {
      toggleBookmark(bookmark.getAttribute("data-bookmark") || "", bookmark);
    }
  });

  document.querySelectorAll("[data-today-clear], [data-today-clear-btn]").forEach((button) => {
    button.addEventListener("click", resetFilters);
  });
}

function resetFilters() {
  const recencyChanged = Boolean(state.recency);
  state.query = "";
  state.source = "";
  state.location = "";
  state.recency = "";
  state.page = 1;
  state.locationsExpanded = false;
  const searchNode = document.querySelector("[data-today-search]");
  if (searchNode) searchNode.value = "";
  if (recencyChanged) {
    fetchTodayJobs();
  } else {
    render();
  }
}

function toggleBookmark(id, button) {
  if (!id) return;
  if (state.bookmarks.has(id)) {
    state.bookmarks.delete(id);
  } else {
    state.bookmarks.add(id);
  }
  const saved = state.bookmarks.has(id);
  if (button) {
    button.classList.toggle("is-saved", saved);
    button.setAttribute("aria-pressed", String(saved));
  }
  try {
    window.localStorage.setItem(BOOKMARK_KEY, JSON.stringify([...state.bookmarks]));
  } catch (error) {
    /* storage unavailable */
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const storedLang = safeLanguage(window.localStorage.getItem(STORAGE_KEY) || DEFAULT_LANG);
  setupEvents();
  applyLanguage(storedLang);
  fetchTodayJobs();
});
