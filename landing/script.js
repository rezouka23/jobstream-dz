const STRINGS = {
  fr: {
    meta: {
      title: "JobStream DZ | Offres d'emploi fraîches en Algérie",
      description:
        "Consultez les offres d'emploi récentes en Algérie dans un flux multi-source filtré et sans doublons.",
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
    hero: {
      kicker: "Nouvelles offres dans un flux ouvert",
      title:
        "Offres fraîches en <span>Algérie.</span>",
      subtitle:
        "JobStream DZ surveille les plateformes qui recrutent, élimine les doublons et rassemble les nouvelles opportunités dans une interface ouverte.",
      join: "Explorer les offres",
      how: "Matching CV",
      monumentAlt: "Monument des Martyrs",
      mapAlt: "Carte des offres en Algérie",
      flagAlt: "Drapeau algérien",
      phoneAlt: "Aperçu du flux JobStream DZ",
      phoneLinkLabel: "Voir le digest des offres",
      cvTeaser: {
        title: "Importez votre CV",
        text: "Recevez les offres qui correspondent à votre profil.",
        action: "Tester le matching",
        ariaLabel: "Importez votre CV pour trouver les offres qui vous correspondent",
      },
    },
    proof: {
      eyebrow: "Pourquoi ça marche",
      title: "Un flux plus rapide, <span>moins bruyant.</span>",
      subtitle: "Les signaux qui comptent sont isolés avant d'arriver dans votre poche.",
      items: {
        speed: {
          title: "Mise à jour toutes les 3 min",
          description: "Le digest surveille les nouvelles opportunités sans vous obliger à rafraîchir plusieurs sites.",
        },
        clean: {
          title: "Aucun doublon",
          description: "Les annonces répétées sont filtrées pour garder un flux lisible.",
        },
        sources: {
          title: "4 sources vérifiées",
          description: "Les plateformes actives sont regroupées dans une seule lecture.",
        },
        openSource: {
          title: "100% open source",
          description: "Une base auto-hébergeable que vous pouvez adapter à votre propre flux d'emploi.",
        },
      },
    },
    feed: {
      title: "Dernier digest publié",
      subtitle: "Les dernières offres de la feuille configurée, avec un aperçu local si le backend n'est pas disponible.",
      loading: "Chargement du dernier digest...",
      empty: "Aucun digest n'est disponible pour le moment.",
      fallback: "Aperçu du digest",
      fallbackNote: "Aperçu local affiché pendant que le flux live se reconnecte.",
      updatedPrefix: "Publié",
      statusPrefix: "Digest publié",
      sourceLabel: "Source",
      apply: "Postuler",
      more: "Tester le matching CV",
      untitled: "Offre sans titre",
      unknownCompany: "Entreprise non précisée",
      unknownLocation: "Lieu non précisé",
      unavailableLink: "Lien indisponible",
      filters: {
        searchLabel: "Filtrer les offres",
        searchPlaceholder: "Rechercher un poste, une entreprise…",
        sourceLabel: "Filtrer par source",
        allSources: "Toutes",
        locationLabel: "Filtrer par lieu",
        allLocations: "Tous",
        recencyLabel: "Fraîcheur",
        recencyAny: "Toutes",
        recencyHour: "Dernière heure",
        recencyDay: "Dernières 24 h",
        recencyWeek: "7 derniers jours",
        clear: "Effacer les filtres",
        noMatches: "Aucune offre ne correspond à votre recherche.",
        resultsLabel: "Résultats",
      },
    },
    phonePreview: {
      eyebrow: "Flux d'offres en direct",
      fallbackEyebrow: "Aperçu du digest",
      badgeLive: "Live",
      badgePreview: "Aperçu",
      loading: "Chargement des dernières offres...",
      empty: "Aucun digest disponible pour le moment.",
      cta: "Voir les offres",
      tapHint: "Touchez pour ouvrir",
      showMore: "Afficher plus",
      showLess: "Réduire",
      close: "Fermer l’aperçu",
    },
    story: {
      eyebrow: "Comment ça marche",
      title: "Arrêtez de rafraîchir les sites d'emploi.",
      subtitle:
        "Collecter, nettoyer, livrer : chaque étape retire de la friction avant que l'offre ne vous atteigne.",
      steps: {
        collect: {
          title: "Collecte continue",
          description: "Les sources actives sont surveillées pendant que vous continuez votre journée.",
        },
        clean: {
          title: "Filtrage utile",
          description: "Les doublons, répétitions et signaux faibles sont réduits avant publication.",
        },
        deliver: {
          title: "Publication web",
          description: "Les offres prêtes à consulter arrivent dans un format mobile et partageable.",
        },
        feed: {
          title: "Flux en direct sur le site",
          description: "La même feuille alimente le flux du site et le moteur de matching CV.",
        },
      },
    },
    faq: {
      eyebrow: "Bon à savoir",
      title: "Questions fréquentes",
      subtitle: "L'essentiel avant de déployer votre propre instance.",
      items: {
        free: {
          question: "Est-ce vraiment gratuit ?",
          answer: "Oui. Le code est publié sous licence MIT et peut être auto-hébergé.",
        },
        frequency: {
          question: "À quelle fréquence les offres arrivent ?",
          answer: "Le flux est mis à jour toutes les 3 minutes lorsqu'il y a de nouvelles opportunités.",
        },
        quality: {
          question: "Comment évitez-vous les doublons ?",
          answer: "Chaque annonce reçoit une empreinte stable pour limiter les répétitions dans la feuille.",
        },
      },
    },
    banner: {
      title: "Trouvez les offres adaptées à votre profil.",
      subtitle: "Importez votre CV et comparez-le aux offres récentes de votre instance.",
      join: "Tester le matching CV",
      footnote: "Open source, auto-hébergeable et pensé pour les chercheurs d'emploi",
    },
    a11y: {
      nav: "Navigation principale",
      langSwitch: "Choix de la langue",
      workflow: "Étapes du produit",
      menu: "Ouvrir le menu",
    },
  },
  en: {
    meta: {
      title: "JobStream DZ | Fresh jobs in Algeria",
      description:
        "Browse recent Algeria job opportunities in an open, multi-source, duplicate-filtered feed.",
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
    hero: {
      kicker: "Fresh opportunities in an open feed",
      title:
        "Fresh jobs across <span>Algeria.</span>",
      subtitle:
        "JobStream DZ watches active hiring platforms, removes duplicate listings, and gathers new opportunities in an open interface.",
      join: "Explore jobs",
      how: "CV match",
      monumentAlt: "Martyrs Memorial",
      mapAlt: "Map of opportunities in Algeria",
      flagAlt: "Algerian flag",
      phoneAlt: "Preview of the JobStream DZ job feed",
      phoneLinkLabel: "See the jobs digest",
      cvTeaser: {
        title: "Upload your CV",
        text: "Get the job offers that match your profile.",
        action: "Try CV match",
        ariaLabel: "Upload your CV to find the jobs that match you",
      },
    },
    proof: {
      eyebrow: "Why it works",
      title: "A faster stream, <span>with less noise.</span>",
      subtitle: "The signals that matter are cleaned up before they reach your pocket.",
      items: {
        speed: {
          title: "Updated every 3 minutes",
          description: "The digest watches new opportunities without forcing you to refresh several job boards.",
        },
        clean: {
          title: "Duplicate-free",
          description: "Repeated listings are filtered so the stream stays readable.",
        },
        sources: {
          title: "4 verified sources",
          description: "Active platforms are combined into one focused reading flow.",
        },
        openSource: {
          title: "100% open source",
          description: "A self-hosted foundation you can adapt to your own job feed.",
        },
      },
    },
    feed: {
      title: "Latest published digest",
      subtitle: "The latest jobs from the configured sheet, with a local preview when the backend is unavailable.",
      loading: "Loading latest digest...",
      empty: "No digest is available yet.",
      fallback: "Digest preview",
      fallbackNote: "Local preview shown while the live feed reconnects.",
      updatedPrefix: "Published",
      statusPrefix: "Digest published",
      sourceLabel: "Source",
      apply: "Apply now",
      more: "Try CV match",
      untitled: "Untitled role",
      unknownCompany: "Unknown company",
      unknownLocation: "Unknown location",
      unavailableLink: "Link unavailable",
      filters: {
        searchLabel: "Filter jobs",
        searchPlaceholder: "Search a role, company…",
        sourceLabel: "Filter by source",
        allSources: "All",
        locationLabel: "Filter by location",
        allLocations: "All",
        recencyLabel: "Freshness",
        recencyAny: "Any",
        recencyHour: "Last hour",
        recencyDay: "Last 24 hours",
        recencyWeek: "Last 7 days",
        clear: "Clear filters",
        noMatches: "No jobs match your search.",
        resultsLabel: "Results",
      },
    },
    phonePreview: {
      eyebrow: "Live job feed",
      fallbackEyebrow: "Digest preview",
      badgeLive: "Live",
      badgePreview: "Preview",
      loading: "Loading fresh jobs...",
      empty: "No digest is available yet.",
      cta: "See jobs",
      tapHint: "Tap to preview",
      showMore: "Show more",
      showLess: "Show less",
      close: "Close preview",
    },
    story: {
      eyebrow: "How it works",
      title: "Stop refreshing job boards.",
      subtitle:
        "Collect, clean, deliver: every step removes friction before an opportunity reaches you.",
      steps: {
        collect: {
          title: "Continuous collection",
          description: "Active sources are watched while you get on with your day.",
        },
        clean: {
          title: "Useful filtering",
          description: "Duplicates, repeated posts, and weak signals are reduced before publishing.",
        },
        deliver: {
          title: "Web publishing",
          description: "Ready-to-review roles arrive in a mobile, shareable format.",
        },
        feed: {
          title: "Live on-site feed",
          description: "The same sheet powers the live site feed and CV matching engine.",
        },
      },
    },
    faq: {
      eyebrow: "Good to know",
      title: "Frequently asked questions",
      subtitle: "What you should know before deploying your own instance.",
      items: {
        free: {
          question: "Is it really free?",
          answer: "Yes. The code is available under the MIT License and can be self-hosted.",
        },
        frequency: {
          question: "How often is it updated?",
          answer: "The feed updates every 3 minutes when new opportunities are available.",
        },
        quality: {
          question: "How do you avoid duplicates?",
          answer: "Each listing goes through a dedicated filtering step to reduce repeated posts.",
        },
      },
    },
    banner: {
      title: "Find jobs that fit your profile.",
      subtitle: "Upload your CV and compare it with recent jobs from your instance.",
      join: "Try CV match",
      footnote: "Open source, self-hosted, and built for job seekers",
    },
    a11y: {
      nav: "Main navigation",
      langSwitch: "Language switcher",
      workflow: "Product workflow",
      menu: "Open menu",
    },
  },
  ar: {
    meta: {
      title: "JobStream DZ | أحدث وظائف الجزائر",
      description:
        "تصفح أحدث فرص العمل في الجزائر ضمن قائمة مفتوحة متعددة المصادر وبدون تكرار.",
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
    hero: {
      kicker: "فرص جديدة في قائمة مفتوحة",
      title:
        "أحدث فرص العمل في <span>الجزائر.</span>",
      subtitle:
        "يراقب JobStream DZ المنصات النشطة، يزيل التكرار، ويجمع الفرص الجديدة في واجهة مفتوحة.",
      join: "تصفح الوظائف",
      how: "مطابقة السيرة",
      monumentAlt: "مقام الشهيد",
      mapAlt: "خريطة فرص العمل في الجزائر",
      flagAlt: "العلم الجزائري",
      phoneAlt: "معاينة قائمة وظائف JobStream DZ",
      phoneLinkLabel: "شاهد ملخص الوظائف",
      cvTeaser: {
        title: "حمّل سيرتك الذاتية",
        text: "احصل على الوظائف التي تناسب ملفك.",
        action: "جرّب مطابقة السيرة",
        ariaLabel: "حمّل سيرتك الذاتية للعثور على الوظائف المناسبة لك",
      },
    },
    proof: {
      eyebrow: "لماذا تعمل المنظومة",
      title: "تدفق أسرع، <span>وضجيج أقل.</span>",
      subtitle: "نرتب الإشارات المهمة قبل أن تصل إلى هاتفك.",
      items: {
        speed: {
          title: "تحديث كل 3 دقائق",
          description: "يتابع الملخص الفرص الجديدة دون الحاجة إلى تحديث عدة مواقع.",
        },
        clean: {
          title: "بدون تكرار",
          description: "نقلل الإعلانات المتكررة حتى يبقى التدفق واضحا.",
        },
        sources: {
          title: "4 مصادر موثوقة",
          description: "تجتمع المنصات النشطة في قراءة واحدة مركزة.",
        },
        openSource: {
          title: "مفتوح المصدر 100%",
          description: "قاعدة ذاتية الاستضافة يمكنك تكييفها مع قائمة الوظائف الخاصة بك.",
        },
      },
    },
    feed: {
      title: "آخر ملخص منشور",
      subtitle: "آخر الوظائف من الجدول المهيأ، مع معاينة محلية عند غياب الواجهة الخلفية.",
      loading: "جار تحميل آخر ملخص...",
      empty: "لا يوجد ملخص منشور حاليا.",
      fallback: "معاينة الملخص",
      fallbackNote: "تظهر معاينة محلية أثناء إعادة الاتصال بالتدفق المباشر.",
      updatedPrefix: "نشر في",
      statusPrefix: "ملخص منشور",
      sourceLabel: "المصدر",
      apply: "قدّم الآن",
      more: "جرّب مطابقة السيرة",
      untitled: "وظيفة بدون عنوان",
      unknownCompany: "شركة غير محددة",
      unknownLocation: "مكان غير محدد",
      unavailableLink: "الرابط غير متاح",
      filters: {
        searchLabel: "تصفية الوظائف",
        searchPlaceholder: "ابحث عن وظيفة أو شركة…",
        sourceLabel: "تصفية حسب المصدر",
        allSources: "الكل",
        locationLabel: "تصفية حسب المكان",
        allLocations: "الكل",
        recencyLabel: "الحداثة",
        recencyAny: "الكل",
        recencyHour: "آخر ساعة",
        recencyDay: "آخر 24 ساعة",
        recencyWeek: "آخر 7 أيام",
        clear: "مسح عوامل التصفية",
        noMatches: "لا توجد وظيفة تطابق بحثك.",
        resultsLabel: "النتائج",
      },
    },
    phonePreview: {
      eyebrow: "قائمة وظائف مباشرة",
      fallbackEyebrow: "معاينة الملخص",
      badgeLive: "مباشر",
      badgePreview: "معاينة",
      loading: "جار تحميل أحدث الوظائف...",
      empty: "لا يوجد ملخص متاح حاليا.",
      cta: "شاهد الوظائف",
      tapHint: "اضغط للمعاينة",
      showMore: "عرض المزيد",
      showLess: "عرض أقل",
      close: "إغلاق المعاينة",
    },
    story: {
      eyebrow: "كيف تعمل المنظومة",
      title: "توقف عن تحديث مواقع التوظيف.",
      subtitle:
        "نجمع، ننظف، ونرسل: كل خطوة تقلل التعب قبل أن تصل الفرصة إليك.",
      steps: {
        collect: {
          title: "جمع مستمر",
          description: "نراقب المصادر النشطة بينما تتابع يومك بشكل طبيعي.",
        },
        clean: {
          title: "فلترة مفيدة",
          description: "نقلل التكرار والإشارات الضعيفة قبل النشر.",
        },
        deliver: {
          title: "نشر عبر الويب",
          description: "تصلك الوظائف الجاهزة للمراجعة بصيغة سهلة على الهاتف.",
        },
        feed: {
          title: "بث مباشر على الموقع",
          description: "يغذي نفس الجدول قائمة الموقع ومحرك مطابقة السيرة.",
        },
      },
    },
    faq: {
      eyebrow: "معلومات مفيدة",
      title: "أسئلة شائعة",
      subtitle: "أهم ما تحتاج معرفته قبل نشر نسختك الخاصة.",
      items: {
        free: {
          question: "هل الخدمة مجانية فعلا؟",
          answer: "نعم، الكود متاح برخصة MIT ويمكن استضافته ذاتيا.",
        },
        frequency: {
          question: "كم مرة تتحدث العروض؟",
          answer: "يمكن ضبط وقت تشغيل أداة الجمع حسب المصادر وحدود الاستخدام.",
        },
        quality: {
          question: "كيف تمنعون التكرار؟",
          answer: "كل عرض يمر عبر فلترة مخصصة لتقليل التكرار قدر الإمكان.",
        },
      },
    },
    banner: {
      title: "اعثر على الوظائف المناسبة لملفك.",
      subtitle: "حمّل سيرتك وقارنها بالوظائف الحديثة في نسختك.",
      join: "جرّب مطابقة السيرة",
      footnote: "مفتوح المصدر وذاتي الاستضافة ومصمم للباحثين عن عمل",
    },
    a11y: {
      nav: "التنقل الرئيسي",
      langSwitch: "تبديل اللغة",
      workflow: "خطوات سير العمل",
      menu: "فتح القائمة",
    },
  },
};

const STORAGE_KEY = "jobstream_lang";
const DEFAULT_LANG = "fr";
const LIVE_FEED_PATH = "/api/feed/latest";
const PHONE_PREVIEW_LIMIT = 3;
const PHONE_EXPANDED_LIMIT = 10;
const liveFeedState = {
  loading: false,
  data: null,
  error: "",
  fallback: false,
};
const feedFilterState = {
  query: "",
  sources: new Set(),
  locations: new Set(),
  recency: "",
};
const feedChipSignatures = { source: "", location: "", recency: "" };
const RECENCY_BUCKETS = [
  { key: "hour", minutes: 60 },
  { key: "day", minutes: 1440 },
  { key: "week", minutes: 10080 },
];
const RECENCY_LABEL_KEYS = { hour: "recencyHour", day: "recencyDay", week: "recencyWeek" };
let feedSearchDebounce = 0;
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

let motionReady = false;
let liveFeedMotionFrame = 0;
let liveFeedBatchTriggers = [];
let phonePreviewMotionFrame = 0;
let phoneModalTimeline = null;
const phoneModalState = {
  open: false,
  expanded: false,
  animating: false,
  originRect: null,
  placeholder: null,
  lastFocus: null,
};

function getValueByPath(obj, path) {
  return path.split(".").reduce((acc, part) => {
    if (!acc || typeof acc !== "object") {
      return undefined;
    }
    return acc[part];
  }, obj);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function getFeedEndpoint() {
  const apiBase = typeof window.JOBSTREAM_API_BASE === "string" ? window.JOBSTREAM_API_BASE.trim() : "";
  if (!apiBase) {
    return LIVE_FEED_PATH;
  }
  return new URL(LIVE_FEED_PATH, apiBase).toString();
}

function normalizeFeedPayload(payload) {
  const jobs = Array.isArray(payload?.jobs)
    ? payload.jobs
    : Array.isArray(payload?.items)
      ? payload.items
      : Array.isArray(payload?.data?.jobs)
        ? payload.data.jobs
        : Array.isArray(payload?.digest?.jobs)
          ? payload.digest.jobs
          : [];

  if (!jobs.length) {
    return null;
  }

  return {
    ...payload,
    published_at: payload.published_at || payload.updated_at || payload.created_at || payload.data?.published_at || "",
    jobs,
  };
}

function getFallbackFeed(lang) {
  const publishedAt = new Date(Date.now() - 8 * 60000).toISOString();
  const fallbackJobs = {
    fr: [
      {
        title: "Développeur Full Stack",
        company_name: "TechNova",
        location: "Alger",
        source: "Emploitic",
        published_date: "Aujourd'hui",
        published_time_utc: "09:40 UTC",
        apply_url: "",
      },
      {
        title: "Comptable confirmé",
        company_name: "Cabinet El Amel",
        location: "Oran",
        source: "JobDz",
        published_date: "Aujourd'hui",
        published_time_utc: "09:34 UTC",
        apply_url: "",
      },
      {
        title: "Assistant marketing",
        company_name: "Global Services",
        location: "Constantine",
        source: "LinkedIn",
        published_date: "Aujourd'hui",
        published_time_utc: "09:29 UTC",
        apply_url: "",
      },
    ],
    en: [
      {
        title: "Full Stack Developer",
        company_name: "TechNova",
        location: "Algiers",
        source: "Emploitic",
        published_date: "Today",
        published_time_utc: "09:40 UTC",
        apply_url: "",
      },
      {
        title: "Senior Accountant",
        company_name: "Cabinet El Amel",
        location: "Oran",
        source: "JobDz",
        published_date: "Today",
        published_time_utc: "09:34 UTC",
        apply_url: "",
      },
      {
        title: "Marketing Assistant",
        company_name: "Global Services",
        location: "Constantine",
        source: "LinkedIn",
        published_date: "Today",
        published_time_utc: "09:29 UTC",
        apply_url: "",
      },
    ],
    ar: [
      {
        title: "مطور Full Stack",
        company_name: "TechNova",
        location: "الجزائر",
        source: "Emploitic",
        published_date: "اليوم",
        published_time_utc: "09:40 UTC",
        apply_url: "",
      },
      {
        title: "محاسب مؤكد",
        company_name: "Cabinet El Amel",
        location: "وهران",
        source: "JobDz",
        published_date: "اليوم",
        published_time_utc: "09:34 UTC",
        apply_url: "",
      },
      {
        title: "مساعد تسويق",
        company_name: "Global Services",
        location: "قسنطينة",
        source: "LinkedIn",
        published_date: "اليوم",
        published_time_utc: "09:29 UTC",
        apply_url: "",
      },
    ],
  };

  const fallbackExtras = {
    fr: [
      ["Responsable RH", "People First DZ", "Alger", "LinkedIn"],
      ["Chargé support client", "Nexa Support", "Blida", "Emploitic"],
      ["Technicien réseau", "Connecta", "Sétif", "JobDz"],
      ["Commercial terrain", "MarketPro", "Tlemcen", "LinkedIn"],
      ["Designer UI/UX", "Studio Atlas", "Alger", "Emploitic"],
      ["Data analyst junior", "Insight Lab", "Oran", "LinkedIn"],
      ["Assistant administratif", "Bureau Nord", "Annaba", "JobDz"],
    ],
    en: [
      ["HR Manager", "People First DZ", "Algiers", "LinkedIn"],
      ["Customer Support Agent", "Nexa Support", "Blida", "Emploitic"],
      ["Network Technician", "Connecta", "Setif", "JobDz"],
      ["Field Sales Representative", "MarketPro", "Tlemcen", "LinkedIn"],
      ["UI/UX Designer", "Studio Atlas", "Algiers", "Emploitic"],
      ["Junior Data Analyst", "Insight Lab", "Oran", "LinkedIn"],
      ["Administrative Assistant", "Bureau Nord", "Annaba", "JobDz"],
    ],
    ar: [
      ["مسؤول موارد بشرية", "People First DZ", "الجزائر", "LinkedIn"],
      ["موظف دعم العملاء", "Nexa Support", "البليدة", "Emploitic"],
      ["تقني شبكات", "Connecta", "سطيف", "JobDz"],
      ["ممثل مبيعات ميداني", "MarketPro", "تلمسان", "LinkedIn"],
      ["مصمم UI/UX", "Studio Atlas", "الجزائر", "Emploitic"],
      ["محلل بيانات مبتدئ", "Insight Lab", "وهران", "LinkedIn"],
      ["مساعد إداري", "Bureau Nord", "عنابة", "JobDz"],
    ],
  };

  const extraJobs = (fallbackExtras[lang] || fallbackExtras[DEFAULT_LANG]).map(([title, company_name, location, source]) => ({
    title,
    company_name,
    location,
    source,
    published_date: lang === "ar" ? "اليوم" : lang === "en" ? "Today" : "Aujourd'hui",
    published_time_utc: "09:21 UTC",
    apply_url: "",
  }));

  return {
    published_at: publishedAt,
    jobs: [...(fallbackJobs[lang] || fallbackJobs[DEFAULT_LANG]), ...extraJobs].slice(0, PHONE_EXPANDED_LIMIT),
  };
}

function formatPublishedAt(value, lang) {
  if (!value) {
    return "";
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }

  const locale = lang === "ar" ? "ar-DZ" : lang === "en" ? "en-US" : "fr-FR";
  return new Intl.DateTimeFormat(locale, {
    dateStyle: "medium",
    timeStyle: "short",
    timeZone: "UTC",
  }).format(date);
}

function formatRelativeTime(value, lang) {
  if (!value) {
    return "";
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return "";
  }

  const diffMs = Date.now() - date.getTime();
  const minutes = Math.max(0, Math.round(diffMs / 60000));
  const locale = lang === "ar" ? "ar-DZ" : lang === "en" ? "en-US" : "fr-FR";
  const formatter = new Intl.RelativeTimeFormat(locale, { numeric: "auto" });
  const ranges = [
    [10080, 10080, "week"],
    [1440, 1440, "day"],
    [60, 60, "hour"],
  ];

  for (let i = 0; i < ranges.length; i += 1) {
    const [threshold, divisor, unit] = ranges[i];
    if (minutes >= threshold) {
      return formatter.format(-Math.round(minutes / divisor), unit);
    }
  }

  return formatter.format(-minutes, "minute");
}

function isPlaceholderValue(value) {
  const normalized = normalizeSearchText(value);
  return !normalized || ["not specified", "unknown", "inconnu", "non precise", "غير محدد"].includes(normalized);
}

function normalizePublishedDateTime(job) {
  const date = isPlaceholderValue(job?.published_date) ? "" : String(job.published_date).trim();
  const time = isPlaceholderValue(job?.published_time_utc) ? "" : String(job.published_time_utc).trim();
  return { date, time };
}

function getJobPublishedAt(job) {
  const candidates = [job?.published_at, job?.published_iso, job?.created_at];
  for (let i = 0; i < candidates.length; i += 1) {
    const raw = candidates[i];
    if (!raw || isPlaceholderValue(raw)) {
      continue;
    }
    const ts = new Date(raw).getTime();
    if (!Number.isNaN(ts)) {
      return new Date(ts).toISOString();
    }
  }

  const { date, time } = normalizePublishedDateTime(job);
  if (!date) {
    return "";
  }

  const rawTimePart = time ? time.replace(/\s*UTC$/i, "") : "00:00:00";
  const timeParts = rawTimePart.split(":");
  const timePart = timeParts.length >= 2
    ? [timeParts[0].padStart(2, "0"), timeParts[1].padStart(2, "0"), (timeParts[2] || "00").padStart(2, "0")]
        .join(":")
    : "00:00:00";
  const ts = new Date(`${date}T${timePart}Z`).getTime();
  return Number.isNaN(ts) ? "" : new Date(ts).toISOString();
}

function getJobPublishedLabel(job) {
  const { date, time } = normalizePublishedDateTime(job);
  return [date, time].filter(Boolean).join(" ").trim();
}

function normalizeSearchText(value) {
  return String(value || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f\u064b-\u065f\u0670]/g, "")
    .toLowerCase()
    .trim();
}

function getUniqueFeedSources(jobs) {
  const ordered = [];
  jobs.forEach((job) => {
    const source = String(job.source || "unknown");
    if (!ordered.includes(source)) {
      ordered.push(source);
    }
  });
  return ordered;
}

function getUniqueFeedLocations(jobs) {
  const ordered = [];
  jobs.forEach((job) => {
    const location = String(job.location || "").trim();
    if (!location || normalizeSearchText(location) === "not specified") {
      return;
    }
    if (!ordered.includes(location)) {
      ordered.push(location);
    }
  });
  return ordered;
}

function getJobAgeMinutes(job, digestPublishedAt) {
  const candidates = [getJobPublishedAt(job), digestPublishedAt];
  for (let i = 0; i < candidates.length; i += 1) {
    const raw = candidates[i];
    if (!raw) {
      continue;
    }
    const ts = new Date(raw).getTime();
    if (!Number.isNaN(ts)) {
      return Math.max(0, Math.round((Date.now() - ts) / 60000));
    }
  }
  return NaN;
}

function getRelevantRecencyBuckets(jobs, digestPublishedAt) {
  const ages = jobs
    .map((job) => getJobAgeMinutes(job, digestPublishedAt))
    .filter((minutes) => !Number.isNaN(minutes));
  if (ages.length < 2) {
    return [];
  }
  return RECENCY_BUCKETS.filter(({ minutes }) => {
    const inside = ages.filter((age) => age <= minutes).length;
    return inside > 0 && inside < ages.length;
  }).map(({ key }) => key);
}

function jobMatchesFilters(job, context) {
  const { query, sources, locations, recency } = feedFilterState;
  if (sources.size && !sources.has(String(job.source || "unknown"))) {
    return false;
  }
  if (locations.size && !locations.has(String(job.location || "").trim())) {
    return false;
  }
  if (recency) {
    const bucket = RECENCY_BUCKETS.find((entry) => entry.key === recency);
    const age = getJobAgeMinutes(job, context?.digestPublishedAt || "");
    if (!bucket || Number.isNaN(age) || age > bucket.minutes) {
      return false;
    }
  }
  if (query) {
    const haystack = normalizeSearchText(
      [job.title, job.company_name, job.location, job.source].filter(Boolean).join(" ")
    );
    if (!haystack.includes(query)) {
      return false;
    }
  }
  return true;
}

function sourceClassName(source) {
  const normalized = String(source || "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
  return normalized ? `source-${normalized}` : "source-unknown";
}

function safeLanguage(lang) {
  return Object.prototype.hasOwnProperty.call(STRINGS, lang) ? lang : DEFAULT_LANG;
}

function getCurrentLanguage() {
  return safeLanguage(document.documentElement.lang || DEFAULT_LANG);
}

function getDisplayFeedData(lang) {
  return liveFeedState.fallback ? getFallbackFeed(lang) : liveFeedState.data;
}

function renderPhoneSkeleton(count = 3) {
  return Array.from({ length: count }, () => '<div class="phone-job-skeleton" aria-hidden="true"></div>').join("");
}

function hasGsapRuntime() {
  return Boolean(window.gsap && window.ScrollTrigger);
}

function refreshMotion() {
  if (!motionReady || !hasGsapRuntime()) {
    return;
  }

  window.requestAnimationFrame(() => {
    window.ScrollTrigger.refresh();
  });
}

function setCurrentNavLink(sectionId) {
  const navLinks = document.querySelectorAll(".main-nav a");
  navLinks.forEach((link) => {
    const href = link.getAttribute("href") || "";
    const isHome = sectionId === "home" && href === "#";
    const isMatch = sectionId !== "home" && href === `#${sectionId}`;
    const active = isHome || isMatch;
    link.classList.toggle("is-current", active);
    if (active) {
      link.setAttribute("aria-current", "page");
    } else {
      link.removeAttribute("aria-current");
    }
  });
}

function initMotionSystem() {
  if (motionReady || !hasGsapRuntime()) {
    return;
  }

  const { gsap, ScrollTrigger } = window;
  gsap.registerPlugin(ScrollTrigger);

  // Keep content fully readable; only position and progress respond to scrolling.
  gsap.matchMedia().add("(prefers-reduced-motion: no-preference)", () => {
    const revealTargets = [
      ".proof-panel",
      ".live-feed-panel",
      ".story-panel",
      ".faq-panel",
      ".bottom-banner",
    ];

    revealTargets.forEach((selector) => {
      const section = document.querySelector(selector);
      if (!section) {
        return;
      }

      gsap.from(section, {
        y: 10,
        duration: 0.35,
        ease: "power3.out",
        scrollTrigger: {
          trigger: section,
          start: "top 82%",
          once: true,
        },
      });
    });

    gsap.utils
      .toArray(".story-pipeline, .proof-pipeline, .faq-pipeline")
      .forEach((pipeline) => {
        const progressFill = pipeline.querySelector(
          ".story-progress-fill, .proof-progress-fill, .faq-progress-fill"
        );
        if (progressFill) {
          gsap.fromTo(
            progressFill,
            { scaleY: 0 },
            {
              scaleY: 1,
              ease: "none",
              transformOrigin: "top",
              scrollTrigger: {
                trigger: pipeline,
                start: "top 70%",
                end: "bottom 60%",
                scrub: true,
              },
            }
          );
        }

        pipeline.querySelectorAll("li").forEach((step) => {
          ScrollTrigger.create({
            trigger: step,
            start: "top 62%",
            end: "bottom 38%",
            onToggle: ({ isActive }) =>
              step.classList.toggle("is-active", isActive),
          });
        });
      });
  });

  setCurrentNavLink("home");
  gsap.utils.toArray("main section[id]").forEach((section) => {
    const sectionId = section.getAttribute("id") || "";
    if (!sectionId) {
      return;
    }

    ScrollTrigger.create({
      trigger: section,
      start: "top 45%",
      end: "bottom 45%",
      onEnter: () => setCurrentNavLink(sectionId),
      onEnterBack: () => setCurrentNavLink(sectionId),
    });
  });

  ScrollTrigger.create({
    trigger: ".hero-panel",
    start: "top top",
    end: "bottom 35%",
    onEnter: () => setCurrentNavLink("home"),
    onEnterBack: () => setCurrentNavLink("home"),
  });

  motionReady = true;
  refreshMotion();
}

function queueLiveFeedMotion() {
  if (!motionReady || prefersReducedMotion.matches || !hasGsapRuntime()) {
    return;
  }

  if (liveFeedMotionFrame) {
    window.cancelAnimationFrame(liveFeedMotionFrame);
  }

  liveFeedMotionFrame = window.requestAnimationFrame(() => {
    liveFeedMotionFrame = 0;
    if (prefersReducedMotion.matches) {
      return;
    }
    const { gsap, ScrollTrigger } = window;

    liveFeedBatchTriggers.forEach((trigger) => trigger.kill());
    liveFeedBatchTriggers = [];

    const cards = gsap.utils.toArray(".live-feed-grid .live-job-card");
    if (!cards.length) {
      refreshMotion();
      return;
    }

    const isMobileRail = window.matchMedia("(max-width: 620px)").matches;

    if (isMobileRail) {
      gsap.fromTo(
        cards,
        { y: 6 },
        { y: 0, duration: 0.25, ease: "power3.out" }
      );
      refreshMotion();
      return;
    }

    gsap.set(cards, { y: 6 });
    liveFeedBatchTriggers = ScrollTrigger.batch(cards, {
      start: "top 88%",
      once: true,
      onEnter: (batch) =>
        gsap.to(batch, {
          y: 0,
          duration: 0.25,
          ease: "power3.out",
          overwrite: true,
        }),
    });

    refreshMotion();
  });
}

function queuePhonePreviewMotion() {
  if (!motionReady || prefersReducedMotion.matches || !hasGsapRuntime()) {
    return;
  }

  if (phonePreviewMotionFrame) {
    window.cancelAnimationFrame(phonePreviewMotionFrame);
  }

  phonePreviewMotionFrame = window.requestAnimationFrame(() => {
    phonePreviewMotionFrame = 0;
    if (prefersReducedMotion.matches) {
      return;
    }
    const cards = window.gsap.utils.toArray(".phone-preview-list .phone-job-card");
    if (!cards.length) {
      return;
    }

    window.gsap.fromTo(
      cards,
      { y: 6 },
      {
        y: 0,
        duration: 0.25,
        ease: "power3.out",
      }
    );
  });
}

function getPhoneModalNodes() {
  return {
    phoneNode: document.querySelector("[data-phone-preview]"),
    backdropNode: document.querySelector("[data-phone-modal-backdrop]"),
    openNode: document.querySelector("[data-phone-open]"),
    closeNode: document.querySelector("[data-phone-close]"),
    expandNode: document.querySelector("[data-phone-expand]"),
    listNode: document.querySelector("[data-phone-preview-list]"),
  };
}

function getPhoneModalWidth() {
  if (window.innerWidth <= 520) {
    return Math.min(window.innerWidth - 12, 360);
  }

  if (window.innerWidth <= 860) {
    return Math.min(window.innerWidth - 16, 390);
  }

  return Math.min(window.innerWidth - 24, 430);
}

function syncPhoneModalAttributes() {
  const { phoneNode, openNode, closeNode, expandNode } = getPhoneModalNodes();
  if (!phoneNode || !openNode) {
    return;
  }

  phoneNode.classList.toggle("is-modal-open", phoneModalState.open);
  phoneNode.classList.toggle("is-expanded", phoneModalState.open && phoneModalState.expanded);
  openNode.setAttribute("aria-expanded", String(phoneModalState.open));

  if (phoneModalState.open) {
    phoneNode.setAttribute("role", "dialog");
    phoneNode.setAttribute("aria-modal", "true");
    phoneNode.setAttribute("aria-labelledby", "phone-preview-title");
  } else {
    phoneNode.removeAttribute("role");
    phoneNode.removeAttribute("aria-modal");
    phoneNode.removeAttribute("aria-labelledby");
  }

  if (closeNode) {
    closeNode.hidden = !phoneModalState.open;
  }

  if (expandNode) {
    expandNode.removeAttribute("aria-expanded");
  }
}

function setDocumentModalLock(locked) {
  document.documentElement.classList.toggle("phone-modal-lock", locked);
  document.body.classList.toggle("phone-modal-lock", locked);
}

function focusPhoneCloseButton() {
  const { closeNode } = getPhoneModalNodes();
  if (closeNode && !closeNode.hidden) {
    closeNode.focus({ preventScroll: true });
  }
}

function openPhoneModal() {
  const { phoneNode, backdropNode } = getPhoneModalNodes();
  if (!phoneNode || !backdropNode || phoneModalState.open || phoneModalState.animating) {
    return;
  }

  const rect = phoneNode.getBoundingClientRect();
  const placeholder = document.createComment("phone-modal-placeholder");
  phoneNode.after(placeholder);
  document.body.append(backdropNode, phoneNode);
  phoneModalState.open = true;
  phoneModalState.expanded = false;
  phoneModalState.animating = true;
  phoneModalState.originRect = rect;
  phoneModalState.placeholder = placeholder;
  phoneModalState.lastFocus = document.activeElement instanceof HTMLElement ? document.activeElement : null;

  backdropNode.hidden = false;
  setDocumentModalLock(true);
  syncPhoneModalAttributes();
  renderPhonePreview(getCurrentLanguage());

  if (phoneModalTimeline) {
    phoneModalTimeline.kill();
  }

  if (prefersReducedMotion.matches || !window.gsap) {
    phoneModalState.animating = false;
    focusPhoneCloseButton();
    return;
  }

  const { gsap } = window;
  const targetWidth = getPhoneModalWidth();
  gsap.killTweensOf([phoneNode, backdropNode]);
  gsap.set(backdropNode, { autoAlpha: 0 });
  gsap.set(phoneNode, {
    position: "fixed",
    inset: "auto",
    left: rect.left,
    top: rect.top,
    right: "auto",
    bottom: "auto",
    width: rect.width,
    minWidth: 0,
    margin: 0,
    zIndex: 1002,
    x: 0,
    y: 0,
    xPercent: 0,
    yPercent: 0,
    transform: "none",
  });

  phoneModalTimeline = gsap.timeline({
    defaults: { ease: "power3.inOut" },
    onComplete: () => {
      phoneModalState.animating = false;
      focusPhoneCloseButton();
    },
  });

  phoneModalTimeline
    .to(backdropNode, { autoAlpha: 1, duration: 0.28 }, 0)
    .to(
      phoneNode,
      {
        left: "50%",
        top: "50%",
        xPercent: -50,
        yPercent: -50,
        width: targetWidth,
        duration: 0.68,
      },
      0
    );
}

function closePhoneModal() {
  const { phoneNode, backdropNode, openNode } = getPhoneModalNodes();
  if (!phoneNode || !backdropNode || !phoneModalState.open || phoneModalState.animating) {
    return;
  }

  const originRect = phoneModalState.originRect;
  phoneModalState.open = false;
  phoneModalState.expanded = false;
  phoneModalState.animating = true;
  renderPhonePreview(getCurrentLanguage());

  const finishClose = () => {
    phoneModalState.animating = false;
    phoneModalState.originRect = null;

    if (phoneModalState.placeholder?.parentNode) {
      phoneModalState.placeholder.replaceWith(phoneNode);
    }

    phoneModalState.placeholder = null;
    syncPhoneModalAttributes();

    if (window.gsap) {
      window.gsap.set(phoneNode, {
        clearProps: "position,inset,left,top,right,bottom,width,minWidth,margin,zIndex,x,y,xPercent,yPercent,transform",
      });
      window.gsap.set(backdropNode, { clearProps: "opacity,visibility" });
    }

    backdropNode.hidden = true;
    setDocumentModalLock(false);

    const focusTarget = phoneModalState.lastFocus || openNode;
    phoneModalState.lastFocus = null;
    if (focusTarget && typeof focusTarget.focus === "function") {
      focusTarget.focus({ preventScroll: true });
    }
  };

  if (phoneModalTimeline) {
    phoneModalTimeline.kill();
  }

  if (prefersReducedMotion.matches || !window.gsap || !originRect) {
    finishClose();
    return;
  }

  const { gsap } = window;
  gsap.killTweensOf([phoneNode, backdropNode]);
  phoneModalTimeline = gsap.timeline({ defaults: { ease: "power3.inOut" }, onComplete: finishClose });
  phoneModalTimeline
    .to(backdropNode, { autoAlpha: 0, duration: 0.22 }, 0)
    .to(
      phoneNode,
      {
        left: originRect.left,
        top: originRect.top,
        xPercent: 0,
        yPercent: 0,
        width: originRect.width,
        duration: 0.54,
      },
      0
    );
}

function setPhonePreviewExpanded(expanded) {
  const { phoneNode, listNode } = getPhoneModalNodes();
  if (!phoneNode || !listNode || !phoneModalState.open || phoneModalState.expanded === expanded) {
    return;
  }

  const previousHeight = listNode.offsetHeight;
  phoneModalState.expanded = expanded;
  syncPhoneModalAttributes();
  renderPhonePreview(getCurrentLanguage());
  listNode.scrollTop = 0;

  if (prefersReducedMotion.matches || !window.gsap) {
    return;
  }

  const nextHeight = listNode.offsetHeight;
  window.gsap.fromTo(
    listNode,
    { height: previousHeight, opacity: 0.78 },
    { height: nextHeight, opacity: 1, duration: 0.36, ease: "power3.out", clearProps: "height,opacity" }
  );
}

function setupPhoneModal() {
  const { backdropNode, openNode, closeNode, expandNode } = getPhoneModalNodes();
  if (!openNode || !backdropNode) {
    return;
  }

  openNode.addEventListener("click", openPhoneModal);
  backdropNode.addEventListener("click", closePhoneModal);

  if (closeNode) {
    closeNode.addEventListener("click", closePhoneModal);
  }

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && phoneModalState.open) {
      closePhoneModal();
    }
  });
}

function renderPhonePreview(lang) {
  const safeLang = safeLanguage(lang);
  const dict = STRINGS[safeLang];
  const phoneNode = document.querySelector("[data-phone-preview]");
  const modeNode = document.querySelector("[data-phone-preview-mode]");
  const badgeNode = document.querySelector("[data-phone-preview-badge]");
  const statusNode = document.querySelector("[data-phone-preview-status]");
  const listNode = document.querySelector("[data-phone-preview-list]");
  const ctaNode = document.querySelector("[data-phone-preview-cta]");
  const expandNode = document.querySelector("[data-phone-expand]");

  if (!phoneNode || !modeNode || !badgeNode || !statusNode || !listNode || !ctaNode || !expandNode) {
    return;
  }

  ctaNode.textContent = dict.phonePreview.cta;
  expandNode.textContent = dict.phonePreview.showMore;
  expandNode.href = "#live-feed";
  expandNode.hidden = true;
  expandNode.removeAttribute("aria-expanded");

  if (liveFeedState.loading) {
    phoneNode.setAttribute("data-phone-mode", "loading");
    modeNode.textContent = dict.phonePreview.eyebrow;
    badgeNode.textContent = dict.phonePreview.badgePreview;
    statusNode.textContent = dict.phonePreview.loading;
    listNode.innerHTML = renderPhoneSkeleton();
    return;
  }

  const displayData = getDisplayFeedData(safeLang);
  const allJobs = Array.isArray(displayData?.jobs) ? displayData.jobs : [];
  const jobLimit = PHONE_PREVIEW_LIMIT;
  const jobs = allJobs.slice(0, jobLimit);
  const isFallback = liveFeedState.fallback;
  phoneNode.setAttribute("data-phone-mode", isFallback ? "fallback" : "live");
  modeNode.textContent = isFallback ? dict.phonePreview.fallbackEyebrow : dict.phonePreview.eyebrow;
  badgeNode.textContent = isFallback ? dict.phonePreview.badgePreview : dict.phonePreview.badgeLive;

  if (!jobs.length) {
    statusNode.textContent = dict.phonePreview.empty;
    listNode.innerHTML = `<p class="phone-preview-empty">${escapeHtml(dict.phonePreview.empty)}</p>`;
    return;
  }

  const digestPublishedAt = displayData?.published_at || "";
  const relativeDigestAge = formatRelativeTime(digestPublishedAt, safeLang);
  statusNode.textContent = isFallback
    ? dict.feed.fallbackNote
    : `${dict.feed.statusPrefix}${relativeDigestAge ? ` ${relativeDigestAge}` : ""}`;
  expandNode.hidden = !phoneModalState.open;

  listNode.innerHTML = jobs
    .map((job) => {
      const title = escapeHtml(job.title || dict.feed.untitled);
      const companyName = escapeHtml(isPlaceholderValue(job.company_name) ? dict.feed.unknownCompany : job.company_name);
      const location = escapeHtml(isPlaceholderValue(job.location) ? dict.feed.unknownLocation : job.location);
      const source = escapeHtml(job.source || "unknown");
      const relativeJobAge = escapeHtml(formatRelativeTime(getJobPublishedAt(job) || digestPublishedAt, safeLang));

      return `
        <article class="phone-job-card">
          <h3 dir="auto">${title}</h3>
          <p class="phone-job-meta" dir="auto"><bdi>${companyName}</bdi> · <bdi>${location}</bdi></p>
          <div class="phone-job-row">
            <span class="phone-job-source"><bdi>${source}</bdi></span>
            <span class="phone-job-time">${relativeJobAge}</span>
          </div>
        </article>
      `;
    })
    .join("");

  queuePhonePreviewMotion();
}

function setLocationDropdownOpen(open) {
  const dropdown = document.querySelector('[data-feed-dropdown="location"]');
  if (!dropdown) {
    return;
  }
  const trigger = dropdown.querySelector('[data-feed-dropdown-trigger="location"]');
  const panel = dropdown.querySelector('[data-feed-chips="location"]');
  dropdown.classList.toggle("is-open", open);
  if (trigger) {
    trigger.setAttribute("aria-expanded", String(open));
  }
  if (panel) {
    panel.hidden = !open;
  }
}

function renderChipGroup(facet, items, isActive, lang) {
  const chipsNode = document.querySelector(`[data-feed-chips="${facet}"]`);
  if (!chipsNode) {
    return;
  }

  const signature = `${lang}|${items.map((item) => item.value).join("|")}`;
  if (signature !== feedChipSignatures[facet]) {
    feedChipSignatures[facet] = signature;
    chipsNode.innerHTML = items
      .map(
        (item) =>
          `<button type="button" class="live-feed-chip ${item.className || ""}" data-chip-facet="${facet}" data-chip-value="${escapeHtml(item.value)}">${escapeHtml(item.label)}</button>`
      )
      .join("");
  }

  chipsNode.querySelectorAll("[data-chip-value]").forEach((chip) => {
    const active = isActive(chip.getAttribute("data-chip-value"));
    chip.classList.toggle("is-active", active);
    chip.setAttribute("aria-pressed", String(active));
  });
}

function renderFeedFacets(jobs, dict, lang, digestPublishedAt) {
  const sources = getUniqueFeedSources(jobs);
  renderChipGroup(
    "source",
    [{ value: "", label: dict.feed.filters.allSources }].concat(
      sources.map((source) => ({ value: source, label: source, className: sourceClassName(source) }))
    ),
    (value) => (value === "" ? feedFilterState.sources.size === 0 : feedFilterState.sources.has(value)),
    lang
  );

  const locations = getUniqueFeedLocations(jobs);
  const locationGroup = document.querySelector('[data-feed-facet-group="location"]');
  const showLocations = locations.length >= 2;
  if (locationGroup) {
    locationGroup.hidden = !showLocations;
  }
  if (showLocations) {
    renderChipGroup(
      "location",
      [{ value: "", label: dict.feed.filters.allLocations }].concat(
        locations.map((location) => ({ value: location, label: location }))
      ),
      (value) => (value === "" ? feedFilterState.locations.size === 0 : feedFilterState.locations.has(value)),
      lang
    );
    const valueNode = document.querySelector('[data-feed-dropdown="location"] [data-feed-dropdown-value]');
    if (valueNode) {
      const selected = Array.from(feedFilterState.locations);
      valueNode.textContent = selected.length ? selected.join(", ") : dict.feed.filters.allLocations;
    }
  } else {
    if (feedFilterState.locations.size) {
      feedFilterState.locations.clear();
    }
    setLocationDropdownOpen(false);
  }

  const buckets = getRelevantRecencyBuckets(jobs, digestPublishedAt);
  const recencyGroup = document.querySelector('[data-feed-facet-group="recency"]');
  const showRecency = buckets.length > 0;
  if (recencyGroup) {
    recencyGroup.hidden = !showRecency;
  }
  if (showRecency) {
    renderChipGroup(
      "recency",
      [{ value: "", label: dict.feed.filters.recencyAny }].concat(
        buckets.map((key) => ({ value: key, label: dict.feed.filters[RECENCY_LABEL_KEYS[key]] }))
      ),
      (value) => feedFilterState.recency === value,
      lang
    );
  } else if (feedFilterState.recency) {
    feedFilterState.recency = "";
  }
}

function renderLiveFeed(lang) {
  const safeLang = safeLanguage(lang);
  const dict = STRINGS[safeLang];
  const statusNode = document.querySelector("[data-live-feed-status]");
  const listNode = document.querySelector("[data-live-feed-list]");
  const controlsNode = document.querySelector("[data-live-feed-controls]");
  const clearNode = document.querySelector("[data-feed-clear]");
  const countNode = document.querySelector("[data-feed-count]");

  if (!statusNode || !listNode) {
    return;
  }

  if (liveFeedState.loading) {
    listNode.setAttribute("aria-busy", "true");
    listNode.setAttribute("data-feed-mode", "empty");
    if (controlsNode) {
      controlsNode.hidden = true;
    }
    statusNode.innerHTML = `<span class="live-feed-status-main">${escapeHtml(dict.feed.loading)}</span>`;
    listNode.innerHTML = `<p class="live-feed-empty">${escapeHtml(dict.feed.loading)}</p>`;
    return;
  }

  listNode.setAttribute("aria-busy", "false");

  const displayData = liveFeedState.fallback ? getFallbackFeed(safeLang) : liveFeedState.data;
  const jobs = Array.isArray(displayData?.jobs) ? displayData.jobs : [];
  if (!jobs.length) {
    listNode.setAttribute("data-feed-mode", "empty");
    if (controlsNode) {
      controlsNode.hidden = true;
    }
    statusNode.innerHTML = `<span class="live-feed-status-main">${escapeHtml(dict.feed.empty)}</span>`;
    listNode.innerHTML = `<p class="live-feed-empty">${escapeHtml(dict.feed.empty)}</p>`;
    return;
  }

  listNode.setAttribute("data-feed-mode", "cards");

  const publishedAt = formatPublishedAt(displayData?.published_at || "", safeLang);
  const relativeDigestAge = formatRelativeTime(displayData?.published_at || "", safeLang);
  const statusLabel = liveFeedState.fallback ? dict.feed.fallback : dict.feed.statusPrefix;
  const statusDate = liveFeedState.fallback ? dict.feed.fallbackNote : publishedAt || dict.feed.updatedPrefix;
  statusNode.innerHTML = `
    <span class="live-feed-status-main">
      <span class="live-feed-status-dot" aria-hidden="true"></span>
      <span>${escapeHtml(statusLabel)}${relativeDigestAge ? ` ${escapeHtml(relativeDigestAge)}` : ""}</span>
    </span>
    <span class="live-feed-status-date">${escapeHtml(statusDate)}</span>
  `;

  const digestPublishedAt = displayData?.published_at || "";
  renderFeedFacets(jobs, dict, safeLang, digestPublishedAt);
  if (controlsNode) {
    controlsNode.hidden = false;
  }

  const hasActiveFilter =
    feedFilterState.query !== "" ||
    feedFilterState.sources.size > 0 ||
    feedFilterState.locations.size > 0 ||
    feedFilterState.recency !== "";
  if (clearNode) {
    clearNode.hidden = !hasActiveFilter;
  }

  const filteredJobs = jobs.filter((job) => jobMatchesFilters(job, { digestPublishedAt }));
  if (countNode) {
    countNode.textContent = `${dict.feed.filters.resultsLabel} : ${filteredJobs.length}`;
  }

  if (!filteredJobs.length) {
    listNode.setAttribute("data-feed-mode", "empty");
    listNode.innerHTML = `<p class="live-feed-empty">${escapeHtml(dict.feed.filters.noMatches)}</p>`;
    return;
  }

  listNode.innerHTML = filteredJobs
    .map((job) => {
      const title = escapeHtml(job.title || dict.feed.untitled);
      const companyName = escapeHtml(isPlaceholderValue(job.company_name) ? dict.feed.unknownCompany : job.company_name);
      const location = escapeHtml(isPlaceholderValue(job.location) ? dict.feed.unknownLocation : job.location);
      const source = escapeHtml(job.source || "unknown");
      const relativeJobAge = escapeHtml(formatRelativeTime(getJobPublishedAt(job) || digestPublishedAt, safeLang));
      const applyUrl = typeof job.apply_url === "string" ? job.apply_url.trim() : "";
      const publishedLabel = escapeHtml(getJobPublishedLabel(job));
      const sourceClass = sourceClassName(job.source || "unknown");

      const actionMarkup = applyUrl
        ? `<a class="live-job-link" href="${escapeHtml(applyUrl)}" target="_blank" rel="noreferrer">${escapeHtml(dict.feed.apply)}</a>`
        : `<span class="live-job-link is-disabled">${escapeHtml(dict.feed.unavailableLink)}</span>`;

      return `
        <article class="live-job-card">
          <div class="live-job-topline">
            <p class="live-job-source ${sourceClass}">${source}</p>
            <p class="live-job-age">${relativeJobAge}</p>
          </div>
          <div>
            <h3>${title}</h3>
          </div>
          <div class="live-job-meta">
            <p>${companyName}</p>
            <p>${location}</p>
          </div>
          <div class="live-job-footer">
            <p>${publishedLabel || ""}</p>
            ${actionMarkup}
          </div>
        </article>
      `;
    })
    .join("");

  queueLiveFeedMotion();
}

async function fetchLatestFeed() {
  liveFeedState.loading = true;
  liveFeedState.error = "";
  liveFeedState.fallback = false;
  const currentLang = getCurrentLanguage();
  renderLiveFeed(currentLang);
  renderPhonePreview(currentLang);

  try {
    const response = await fetch(getFeedEndpoint(), {
      headers: {
        Accept: "application/json",
      },
      cache: "no-store",
    });

    if (!response.ok) {
      throw new Error(`Feed request failed with status ${response.status}`);
    }

    const payload = normalizeFeedPayload(await response.json());
    if (!payload) {
      throw new Error("Feed payload is invalid");
    }

    liveFeedState.data = payload;
    liveFeedState.fallback = false;
  } catch (error) {
    liveFeedState.data = null;
    liveFeedState.error = error instanceof Error ? error.message : "Feed request failed";
    liveFeedState.fallback = true;
  } finally {
    liveFeedState.loading = false;
    const finalLang = getCurrentLanguage();
    renderLiveFeed(finalLang);
    renderPhonePreview(finalLang);
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
    const key = node.getAttribute("data-i18n");
    const value = getValueByPath(dict, key);
    if (typeof value === "string") {
      node.textContent = value;
    }
  });

  document.querySelectorAll("[data-i18n-html]").forEach((node) => {
    const key = node.getAttribute("data-i18n-html");
    const value = getValueByPath(dict, key);
    if (typeof value === "string") {
      node.innerHTML = value;
    }
  });

  document.querySelectorAll("[data-i18n-alt]").forEach((node) => {
    const key = node.getAttribute("data-i18n-alt");
    const value = getValueByPath(dict, key);
    if (typeof value === "string") {
      node.setAttribute("alt", value);
    }
  });

  document.querySelectorAll("[data-i18n-aria-label]").forEach((node) => {
    const key = node.getAttribute("data-i18n-aria-label");
    const value = getValueByPath(dict, key);
    if (typeof value === "string") {
      node.setAttribute("aria-label", value);
    }
  });

  document.querySelectorAll("[data-i18n-placeholder]").forEach((node) => {
    const key = node.getAttribute("data-i18n-placeholder");
    const value = getValueByPath(dict, key);
    if (typeof value === "string") {
      node.setAttribute("placeholder", value);
    }
  });

  document.querySelectorAll(".lang-btn").forEach((button) => {
    const isActive = button.getAttribute("data-lang") === safeLang;
    button.classList.toggle("is-active", isActive);
    button.setAttribute("aria-pressed", String(isActive));
  });

  window.localStorage.setItem(STORAGE_KEY, safeLang);
  renderLiveFeed(safeLang);
  renderPhonePreview(safeLang);
  refreshMotion();
}

function setupLanguageSwitcher() {
  document.querySelectorAll(".lang-btn").forEach((button) => {
    button.addEventListener("click", () => {
      const lang = button.getAttribute("data-lang");
      applyLanguage(lang);
    });
  });
}

const MOBILE_MENU_QUERY = window.matchMedia("(max-width: 860px)");

function setupMobileMenu() {
  const toggle = document.querySelector(".nav-toggle");
  const menu = document.getElementById("site-menu");
  if (!toggle || !menu) {
    return;
  }

  const setMenuOpen = (open) => {
    toggle.setAttribute("aria-expanded", String(open));
    menu.classList.toggle("is-open", open);
    document.body.classList.toggle("is-menu-open", open);
  };

  toggle.addEventListener("click", () => {
    const isOpen = toggle.getAttribute("aria-expanded") === "true";
    setMenuOpen(!isOpen);
  });

  menu.querySelectorAll(".main-nav a").forEach((link) => {
    link.addEventListener("click", () => setMenuOpen(false));
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
      setMenuOpen(false);
      toggle.focus();
    }
  });

  document.addEventListener("click", (event) => {
    if (toggle.getAttribute("aria-expanded") !== "true") {
      return;
    }
    const target = event.target;
    if (target instanceof Node && !menu.contains(target) && !toggle.contains(target)) {
      setMenuOpen(false);
    }
  });

  const handleQueryChange = () => {
    if (!MOBILE_MENU_QUERY.matches) {
      setMenuOpen(false);
    }
  };
  if (typeof MOBILE_MENU_QUERY.addEventListener === "function") {
    MOBILE_MENU_QUERY.addEventListener("change", handleQueryChange);
  }
}

function toggleSetValue(set, value) {
  if (value === "") {
    set.clear();
  } else if (set.has(value)) {
    set.delete(value);
  } else {
    set.add(value);
  }
}

function setupFeedFilters() {
  const controlsNode = document.querySelector("[data-live-feed-controls]");
  const searchNode = document.querySelector("[data-feed-search]");
  const clearNode = document.querySelector("[data-feed-clear]");

  if (searchNode) {
    searchNode.addEventListener("input", (event) => {
      const value = event.target.value;
      if (feedSearchDebounce) {
        window.clearTimeout(feedSearchDebounce);
      }
      feedSearchDebounce = window.setTimeout(() => {
        feedSearchDebounce = 0;
        feedFilterState.query = normalizeSearchText(value);
        renderLiveFeed(getCurrentLanguage());
      }, 150);
    });
  }

  if (controlsNode) {
    controlsNode.addEventListener("click", (event) => {
      const chip = event.target.closest("[data-chip-facet]");
      if (!chip) {
        return;
      }
      const facet = chip.getAttribute("data-chip-facet");
      const value = chip.getAttribute("data-chip-value");
      if (facet === "source") {
        toggleSetValue(feedFilterState.sources, value);
      } else if (facet === "location") {
        toggleSetValue(feedFilterState.locations, value);
      } else if (facet === "recency") {
        feedFilterState.recency = value;
      }
      renderLiveFeed(getCurrentLanguage());
    });

    const locationTrigger = controlsNode.querySelector('[data-feed-dropdown-trigger="location"]');
    if (locationTrigger) {
      locationTrigger.addEventListener("click", (event) => {
        event.stopPropagation();
        setLocationDropdownOpen(locationTrigger.getAttribute("aria-expanded") !== "true");
      });
    }

    document.addEventListener("click", (event) => {
      const dropdown = controlsNode.querySelector('[data-feed-dropdown="location"]');
      if (dropdown && !dropdown.contains(event.target)) {
        setLocationDropdownOpen(false);
      }
    });

    document.addEventListener("keydown", (event) => {
      if (event.key !== "Escape") {
        return;
      }
      const dropdown = controlsNode.querySelector('[data-feed-dropdown="location"]');
      if (dropdown && dropdown.classList.contains("is-open")) {
        setLocationDropdownOpen(false);
        const trigger = dropdown.querySelector('[data-feed-dropdown-trigger="location"]');
        if (trigger) {
          trigger.focus();
        }
      }
    });
  }

  if (clearNode) {
    clearNode.addEventListener("click", () => {
      feedFilterState.sources.clear();
      feedFilterState.locations.clear();
      feedFilterState.recency = "";
      feedFilterState.query = "";
      if (searchNode) {
        searchNode.value = "";
      }
      renderLiveFeed(getCurrentLanguage());
    });
  }
}

function init() {
  setupLanguageSwitcher();
  setupMobileMenu();
  setupFeedFilters();
  setupPhoneModal();
  const savedLang = window.localStorage.getItem(STORAGE_KEY) || DEFAULT_LANG;
  applyLanguage(savedLang);
  setCurrentNavLink("home");
  initMotionSystem();

  if (typeof prefersReducedMotion.addEventListener === "function") {
    prefersReducedMotion.addEventListener("change", () => {
      if (prefersReducedMotion.matches && hasGsapRuntime()) {
        liveFeedBatchTriggers.forEach((trigger) => trigger.kill());
        liveFeedBatchTriggers = [];
        const cards = ".live-job-card, .phone-job-card";
        window.gsap.killTweensOf(cards);
        window.gsap.set(cards, { clearProps: "transform" });
      }
    });
  }

  fetchLatestFeed();
}

init();
