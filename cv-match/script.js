const STORAGE_KEY = "jobstream_lang";
const DEFAULT_LANG = "fr";
const CV_MATCH_PATH = "/api/cv/match";
const MAX_FILE_MB = 5;

const STRINGS = {
  fr: {
    nav: {
      home: "Accueil",
      jobsToday: "Offres du jour",
      cvMatch: "Matching CV",
      feed: "Digest",
      faq: "FAQ",
      join: "Recevoir les offres",
    },
    cv: {
      kicker: "Matching intelligent",
      title: "Trouvez les offres qui <span>collent à votre CV.</span>",
      subtitle: "Importez votre CV. JobStream DZ analyse votre profil avec OpenAI, puis compare vos compétences aux offres ajoutées dans la feuille principale ces 7 derniers jours.",
      feedLink: "Voir le flux des offres",
      uploadTitle: "Déposez votre CV",
      uploadHint: "PDF, DOCX ou TXT, 5 MB maximum",
      noFile: "Aucun fichier sélectionné",
      submit: "Analyser mon CV",
      loading: "Analyse du CV et recherche des offres...",
      privacy: "Votre CV est utilisé uniquement pour cette recherche. Il n'est pas stocké par JobStream DZ.",
      unsupported: "Format non supporté. Utilisez PDF, DOCX ou TXT.",
      tooLarge: "Le fichier dépasse 5 MB.",
    },
    results: {
      kicker: "Résultats personnalisés",
      title: "Offres recommandées",
      reset: "Nouveau CV",
      empty: "Aucune correspondance claire trouvée dans les offres récentes.",
      matches: "offres trouvées",
      window: "Fenêtre",
      apply: "Postuler",
      score: "Score",
      summary: "Profil extrait",
      summarySub: "Basé sur votre CV et vos préférences",
      save: "Enregistrer l'offre",
      strong: "Très pertinent",
      good: "Bon match",
      possible: "Possible",
      skills: "Compétences",
      titles: "Postes ciblés",
      locations: "Lieux",
      languages: "Langues",
      experience: "Expérience",
      years: "ans",
    },
    errors: {
      generic: "Impossible de générer les correspondances. Réessayez plus tard.",
    },
    a11y: {
      nav: "Navigation principale",
      langSwitch: "Choix de la langue",
      menu: "Ouvrir le menu",
    },
  },
  en: {
    nav: {
      home: "Home",
      jobsToday: "Today's jobs",
      cvMatch: "CV match",
      feed: "Digest",
      faq: "FAQ",
      join: "Get job alerts",
    },
    cv: {
      kicker: "Smart matching",
      title: "Find jobs that <span>fit your CV.</span>",
      subtitle: "Upload your CV. JobStream DZ extracts your profile with OpenAI, then compares your skills against main-sheet jobs added in the last 7 days.",
      feedLink: "Browse the job feed",
      uploadTitle: "Drop your CV",
      uploadHint: "PDF, DOCX, or TXT, 5 MB max",
      noFile: "No file selected",
      submit: "Analyze my CV",
      loading: "Analyzing CV and searching jobs...",
      privacy: "Your CV is used only for this search. JobStream DZ does not store it.",
      unsupported: "Unsupported format. Use PDF, DOCX, or TXT.",
      tooLarge: "The file is larger than 5 MB.",
    },
    results: {
      kicker: "Personalized results",
      title: "Recommended jobs",
      reset: "New CV",
      empty: "No clear matches found in recent jobs.",
      matches: "jobs found",
      window: "Window",
      apply: "Apply now",
      score: "Match",
      summary: "Extracted profile",
      summarySub: "Based on your CV and preferences",
      save: "Save job",
      strong: "Strong match",
      good: "Good match",
      possible: "Possible",
      skills: "Skills",
      titles: "Target roles",
      locations: "Locations",
      languages: "Languages",
      experience: "Experience",
      years: "years",
    },
    errors: {
      generic: "Could not generate matches. Please try again later.",
    },
    a11y: {
      nav: "Main navigation",
      langSwitch: "Language switcher",
      menu: "Open menu",
    },
  },
  ar: {
    nav: {
      home: "الرئيسية",
      jobsToday: "وظائف اليوم",
      cvMatch: "مطابقة السيرة",
      feed: "الملخص",
      faq: "الأسئلة",
      join: "استقبل الوظائف",
    },
    cv: {
      kicker: "مطابقة ذكية",
      title: "اعثر على وظائف <span>تناسب سيرتك الذاتية.</span>",
      subtitle: "ارفع سيرتك الذاتية. يستخرج JobStream DZ ملفك المهني عبر OpenAI ثم يقارنه بوظائف الورقة الرئيسية المضافة خلال آخر 7 أيام.",
      feedLink: "تصفح قائمة الوظائف",
      uploadTitle: "ارفع سيرتك الذاتية",
      uploadHint: "PDF أو DOCX أو TXT، بحد أقصى 5 MB",
      noFile: "لم يتم اختيار ملف",
      submit: "حلل سيرتي الذاتية",
      loading: "جار تحليل السيرة والبحث عن الوظائف...",
      privacy: "تستخدم سيرتك الذاتية لهذه المطابقة فقط. لا يخزنها JobStream DZ.",
      unsupported: "صيغة غير مدعومة. استخدم PDF أو DOCX أو TXT.",
      tooLarge: "حجم الملف أكبر من 5 MB.",
    },
    results: {
      kicker: "نتائج مخصصة",
      title: "وظائف مقترحة",
      reset: "سيرة جديدة",
      empty: "لم يتم العثور على مطابقات واضحة في الوظائف الحديثة.",
      matches: "وظيفة موجودة",
      window: "الفترة",
      apply: "قدّم الآن",
      score: "تطابق",
      summary: "الملف المستخرج",
      summarySub: "استنادًا إلى سيرتك الذاتية وتفضيلاتك",
      save: "حفظ الوظيفة",
      strong: "مطابقة قوية",
      good: "مطابقة جيدة",
      possible: "محتمل",
      skills: "المهارات",
      titles: "الأدوار المستهدفة",
      locations: "الأماكن",
      languages: "اللغات",
      experience: "الخبرة",
      years: "سنوات",
    },
    errors: {
      generic: "تعذر إنشاء المطابقات. حاول مرة أخرى لاحقا.",
    },
    a11y: {
      nav: "التنقل الرئيسي",
      langSwitch: "تبديل اللغة",
      menu: "فتح القائمة",
    },
  },
};

const state = { response: null, loading: false };

function getValueByPath(obj, path) {
  return path.split(".").reduce((acc, part) => (acc && typeof acc === "object" ? acc[part] : undefined), obj);
}

function safeLanguage(lang) {
  return Object.prototype.hasOwnProperty.call(STRINGS, lang) ? lang : DEFAULT_LANG;
}

function currentLang() {
  return safeLanguage(document.documentElement.lang || localStorage.getItem(STORAGE_KEY) || DEFAULT_LANG);
}

function applyLanguage(lang) {
  const safe = safeLanguage(lang);
  const dict = STRINGS[safe];
  document.documentElement.lang = safe;
  document.documentElement.dir = safe === "ar" ? "rtl" : "ltr";
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    const value = getValueByPath(dict, node.dataset.i18n);
    if (typeof value === "string") node.textContent = value;
  });
  document.querySelectorAll("[data-i18n-html]").forEach((node) => {
    const value = getValueByPath(dict, node.dataset.i18nHtml);
    if (typeof value === "string") node.innerHTML = value;
  });
  document.querySelectorAll("[data-i18n-aria-label]").forEach((node) => {
    const value = getValueByPath(dict, node.dataset.i18nAriaLabel);
    if (typeof value === "string") node.setAttribute("aria-label", value);
  });
  document.querySelectorAll("[data-lang]").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.lang === safe);
    button.toggleAttribute("aria-pressed", button.dataset.lang === safe);
  });
  localStorage.setItem(STORAGE_KEY, safe);
  if (state.response) renderResults(state.response);
}

function escapeHtml(value) {
  return String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function setStatus(message, tone = "") {
  const node = document.querySelector("[data-cv-status]");
  if (!node) return;
  node.textContent = message;
  node.dataset.tone = tone;
}

function validateFile(file) {
  const dict = STRINGS[currentLang()];
  if (!file) return "";
  const extension = file.name.split(".").pop().toLowerCase();
  if (!["pdf", "docx", "txt"].includes(extension)) return dict.cv.unsupported;
  if (file.size > MAX_FILE_MB * 1024 * 1024) return dict.cv.tooLarge;
  return "";
}

async function submitCv(event) {
  event.preventDefault();
  const dict = STRINGS[currentLang()];
  const input = document.querySelector("[data-cv-file]");
  const file = input?.files?.[0];
  const validationError = validateFile(file);
  if (!file || validationError) {
    setStatus(validationError || dict.cv.noFile, "error");
    return;
  }

  state.loading = true;
  setFormLoading(true);
  setStatus(dict.cv.loading, "loading");
  renderLoadingState(dict);

  try {
    const formData = new FormData();
    formData.append("cv", file);
    const response = await fetch(CV_MATCH_PATH, { method: "POST", body: formData });
    const payload = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(payload.detail || dict.errors.generic);
    }
    state.response = payload;
    renderResults(payload);
    setStatus("");
  } catch (error) {
    state.response = null;
    setStatus(error.message || dict.errors.generic, "error");
    renderErrorState(error.message || dict.errors.generic, dict);
  } finally {
    state.loading = false;
    setFormLoading(false);
  }
}

function sourceClassName(source) {
  const slug = String(source || "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "");
  return slug ? `source-${slug}` : "";
}

function getResultNodes() {
  return {
    panel: document.querySelector("[data-results-panel]"),
    metaNode: document.querySelector("[data-results-meta]"),
    summaryNode: document.querySelector("[data-candidate-summary]"),
    matchesNode: document.querySelector("[data-matches]"),
  };
}

function renderLoadingState(dict) {
  const { panel, metaNode, summaryNode, matchesNode } = getResultNodes();
  if (!panel || !metaNode || !summaryNode || !matchesNode) return;
  panel.hidden = false;
  metaNode.textContent = dict.cv.loading;
  summaryNode.innerHTML = `
    <div class="cv-skeleton">
      <div class="cv-skel-line" style="width:38%"></div>
      <div class="cv-skel-line" style="width:72%"></div>
    </div>`;
  matchesNode.innerHTML = `
    <div class="cv-skeleton">
      ${Array.from({ length: 3 })
        .map(
          () => `
        <div class="cv-skel-card">
          <div class="cv-skel-block"></div>
          <div class="cv-skel-lines">
            <div class="cv-skel-line" style="width:44%"></div>
            <div class="cv-skel-line" style="width:70%"></div>
            <div class="cv-skel-line" style="width:88%"></div>
          </div>
        </div>`,
        )
        .join("")}
    </div>`;
  panel.scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderStateBlock({ tone, icon, title, message, dict }) {
  return `
    <div class="cv-state" data-tone="${escapeHtml(tone)}">
      <span class="cv-state-icon"><svg class="icon" aria-hidden="true"><use href="#${escapeHtml(icon)}"></use></svg></span>
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(message)}</p>
      <div class="cv-state-actions">
        <a class="cv-text-link" href="/landing/#live-feed">${escapeHtml(dict.cv.feedLink)}</a>
      </div>
    </div>`;
}

function renderErrorState(message, dict) {
  const { panel, metaNode, summaryNode, matchesNode } = getResultNodes();
  if (!panel || !metaNode || !summaryNode || !matchesNode) return;
  panel.hidden = false;
  metaNode.textContent = "";
  summaryNode.innerHTML = "";
  matchesNode.innerHTML = renderStateBlock({
    tone: "error",
    icon: "icon-spark",
    title: dict.errors.generic,
    message,
    dict,
  });
}

function setFormLoading(loading) {
  const submit = document.querySelector(".cv-submit");
  const input = document.querySelector("[data-cv-file]");
  if (submit) submit.disabled = loading;
  if (input) input.disabled = loading;
}

function renderResults(payload) {
  const dict = STRINGS[currentLang()];
  const panel = document.querySelector("[data-results-panel]");
  const metaNode = document.querySelector("[data-results-meta]");
  const summaryNode = document.querySelector("[data-candidate-summary]");
  const matchesNode = document.querySelector("[data-matches]");
  if (!panel || !metaNode || !summaryNode || !matchesNode) return;

  panel.hidden = false;
  const meta = payload.meta || {};
  const windowStart = meta.date_window_start || "--";
  const windowEnd = meta.date_window_end || "--";
  metaNode.innerHTML = `${payload.match_count || 0} ${escapeHtml(dict.results.matches)} · ${escapeHtml(dict.results.window)}: <bdi>${escapeHtml(windowStart)}</bdi> &ndash; <bdi>${escapeHtml(windowEnd)}</bdi>`;
  summaryNode.innerHTML = renderSummary(payload.candidate_summary || {}, dict);

  const matches = Array.isArray(payload.matches) ? payload.matches : [];
  matchesNode.innerHTML = matches.length
    ? matches.map((match, index) => renderMatchCard(match, dict, index)).join("")
    : renderStateBlock({
        tone: "empty",
        icon: "icon-briefcase",
        title: dict.results.empty,
        message: dict.cv.subtitle,
        dict,
      });
  panel.scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderSummary(summary, dict) {
  const groups = [
    [dict.results.titles, summary.target_titles],
    [dict.results.skills, summary.skills],
    [dict.results.locations, summary.locations],
    [dict.results.languages, summary.languages],
  ];
  const experience = summary.experience_years;
  return `
    <div class="cv-profile-card">
      <div class="cv-profile-head">
        <span class="cv-profile-icon"><svg class="icon" aria-hidden="true"><use href="#icon-user"></use></svg></span>
        <div>
          <h3>${escapeHtml(dict.results.summary)}</h3>
          <p>${escapeHtml(dict.results.summarySub)}</p>
        </div>
      </div>
      <div class="cv-summary-grid">
        ${groups.map(([label, items]) => renderSummaryGroup(label, items)).join("")}
        ${experience || experience === 0 ? renderSummaryGroup(dict.results.experience, [`${experience} ${dict.results.years}`]) : ""}
      </div>
    </div>
  `;
}

function renderSummaryGroup(label, items) {
  const safeItems = Array.isArray(items) ? items.filter(Boolean).slice(0, 8) : [];
  if (!safeItems.length) return "";
  return `
    <section class="cv-summary-group">
      <span class="cv-summary-label">${escapeHtml(label)}</span>
      <div class="cv-chip-list">${safeItems.map((item) => `<bdi class="cv-chip">${escapeHtml(item)}</bdi>`).join("")}</div>
    </section>
  `;
}

function clampScore(score) {
  const value = Number(score || 0);
  return Math.max(0, Math.min(100, Math.round(value)));
}

function getMatchTone(score) {
  if (score >= 88) return "strong";
  if (score >= 80) return "good";
  return "possible";
}

function getMatchColor(score) {
  if (score >= 88) return "#45E58A";
  if (score >= 80) return "#FACC15";
  return "#FDBA3B";
}

function renderMatchRing(score, dict) {
  const safeScore = clampScore(score);
  const radius = 42;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (safeScore / 100) * circumference;
  const color = getMatchColor(safeScore);
  return `
    <div class="cv-match-ring" aria-label="${escapeHtml(String(safeScore))}% ${escapeHtml(dict.results.score)}">
      <svg class="cv-match-ring-svg" viewBox="0 0 104 104" aria-hidden="true">
        <circle class="cv-match-ring-track" cx="52" cy="52" r="${radius}"></circle>
        <circle class="cv-match-ring-value" cx="52" cy="52" r="${radius}" style="--match-color:${color};--dash-array:${circumference};--dash-offset:${offset};"></circle>
      </svg>
      <div class="cv-match-ring-text">
        <strong>${safeScore}%</strong>
        <span>${escapeHtml(dict.results.score)}</span>
      </div>
    </div>
  `;
}

function renderMatchCard(match, dict, index = 0) {
  const score = clampScore(match.score);
  const tone = getMatchTone(score);
  const reasons = Array.isArray(match.reasons) ? match.reasons : [];
  const sourceClass = sourceClassName(match.source);
  return `
    <article class="cv-match-card" data-match-tone="${tone}" style="--i:${index}">
      <div class="cv-match-score">${renderMatchRing(score, dict)}</div>
      <div class="cv-match-body">
        ${score >= 88 ? `<p class="cv-match-badge">★ ${escapeHtml(dict.results.strong)}</p>` : ""}
        <p class="cv-source ${sourceClass}"><bdi>${escapeHtml(match.source || "unknown")}</bdi></p>
        <h3 dir="auto">${escapeHtml(match.title || "Not specified")}</h3>
        <p class="cv-meta" dir="auto"><bdi>${escapeHtml(match.company_name || "Not specified")}</bdi> <span aria-hidden="true">·</span> <bdi>${escapeHtml(match.location || "Not specified")}</bdi></p>
        <ul class="cv-reasons">${reasons.map((reason) => `<li>${escapeHtml(reason)}</li>`).join("")}</ul>
      </div>
      <div class="cv-match-actions">
        <button class="cv-bookmark" type="button" aria-label="${escapeHtml(dict.results.save)}" aria-pressed="false">
          <svg class="icon" aria-hidden="true"><use href="#icon-bookmark"></use></svg>
        </button>
        <a class="cv-apply" href="${escapeHtml(match.apply_url || "#")}" target="_blank" rel="noreferrer">
          <span>${escapeHtml(dict.results.apply)}</span>
          <svg class="icon" aria-hidden="true"><use href="#icon-chevron-right"></use></svg>
        </a>
      </div>
    </article>
  `;
}

function setupNav() {
  const toggle = document.querySelector(".nav-toggle");
  const menu = document.querySelector("#site-menu");
  if (!toggle || !menu) return;
  toggle.addEventListener("click", () => {
    const expanded = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!expanded));
    menu.classList.toggle("is-open", !expanded);
  });
}

function setupFileInput() {
  const input = document.querySelector("[data-cv-file]");
  const nameNode = document.querySelector("[data-cv-file-name]");
  if (!input || !nameNode) return;
  input.addEventListener("change", () => {
    const file = input.files?.[0];
    nameNode.textContent = file ? file.name : STRINGS[currentLang()].cv.noFile;
    const validationError = validateFile(file);
    setStatus(validationError, validationError ? "error" : "");
  });
}

function setupDropzone() {
  const dropzone = document.querySelector(".cv-dropzone");
  const input = document.querySelector("[data-cv-file]");
  if (!dropzone || !input) return;

  ["dragenter", "dragover"].forEach((type) => {
    dropzone.addEventListener(type, (event) => {
      event.preventDefault();
      dropzone.classList.add("is-dragging");
    });
  });

  ["dragleave", "dragend", "drop"].forEach((type) => {
    dropzone.addEventListener(type, () => dropzone.classList.remove("is-dragging"));
  });

  dropzone.addEventListener("drop", (event) => {
    event.preventDefault();
    const file = event.dataTransfer?.files?.[0];
    if (!file) return;
    const transfer = new DataTransfer();
    transfer.items.add(file);
    input.files = transfer.files;
    input.dispatchEvent(new Event("change", { bubbles: true }));
  });
}

document.addEventListener("DOMContentLoaded", () => {
  applyLanguage(localStorage.getItem(STORAGE_KEY) || DEFAULT_LANG);
  setupNav();
  setupFileInput();
  setupDropzone();
  document.querySelector("[data-cv-form]")?.addEventListener("submit", submitCv);
  document.querySelector("[data-cv-reset]")?.addEventListener("click", () => {
    state.response = null;
    document.querySelector("[data-results-panel]").hidden = true;
    document.querySelector("[data-cv-file]").value = "";
    document.querySelector("[data-cv-file-name]").textContent = STRINGS[currentLang()].cv.noFile;
    setStatus("");
  });
  document.querySelectorAll("[data-lang]").forEach((button) => {
    button.addEventListener("click", () => applyLanguage(button.dataset.lang));
  });
  document.addEventListener("click", (event) => {
    const bookmark = event.target.closest(".cv-bookmark");
    if (!bookmark) return;
    const pressed = bookmark.getAttribute("aria-pressed") === "true";
    bookmark.setAttribute("aria-pressed", String(!pressed));
    bookmark.classList.toggle("is-saved", !pressed);
  });
});
