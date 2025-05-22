// Fonction pour charger les fichiers partiels
async function loadPartial(url, elementId) {
    const response = await fetch(url);
    const html = await response.text();
    document.getElementById(elementId).innerHTML = html;
}

// Charger les fichiers partiels
document.addEventListener('DOMContentLoaded', async () => {
    await loadPartial('partials/hero.html', 'hero-container');
    await loadPartial('partials/download-section.html', 'download-section-container');
    await loadPartial('partials/benefits.html', 'benefits-container');
    await loadPartial('partials/testimonials.html', 'testimonials-container');
    await loadPartial('partials/features.html', 'features-container');
    await loadPartial('partials/modals.html', 'modals-container');

    // Initialiser votre application après le chargement des fichiers partiels
    init();
});





// Configuration Firebase
const firebaseConfig = {
    apiKey: "AIzaSyDMEs2f8IBooNo-rWVZ_fEZYPEpPvnyNC4",
    authDomain: "leopardo-ai.firebaseapp.com",
    databaseURL: "https://leopardo-ai-default-rtdb.europe-west1.firebasedatabase.app",
    projectId: "leopardo-ai",
    storageBucket: "leopardo-ai.firebasestorage.app",
    messagingSenderId: "838044402284",
    appId: "1:838044402284:web:3e8c53eb13fdac6b6e4e49",
    measurementId: "G-4NFRX042CB"
};

// Initialiser Firebase
firebase.initializeApp(firebaseConfig);
const database = firebase.database();
const analytics = firebase.analytics();

// Configuration GitHub
const GITHUB_REPO = "kitokoh/leopardo";
const APP_DOWNLOAD_PAGE = "https://leopardo.ai/download";
let currentVersion = "1.0.0";
let downloadUrls = {
    windows: "",
    macos: "",
    ubuntu: ""
};
let fileSizes = {
    windows: "",
    macos: "",
    ubuntu: ""
};
let releaseNotes = "";

// Éléments du DOM
const platformTabs = document.querySelectorAll('.platform-tab');
const platformContents = document.querySelectorAll('.platform-content');
const windowsDownloadBtn = document.getElementById('windows-download');
const macosDownloadBtn = document.getElementById('macos-download');
const ubuntuDownloadBtn = document.getElementById('ubuntu-download');
const downloadCountEl = document.getElementById('download-count');
const activeUsersEl = document.getElementById('active-users');
const countriesEl = document.getElementById('countries');
const appVersionEls = {
    fr: document.getElementById('app-version'),
    en: document.getElementById('app-version-en'),
    ar: document.getElementById('app-version-ar'),
    pt: document.getElementById('app-version-pt'),
    tr: document.getElementById('app-version-tr')
};
const latestVersionEls = {
    fr: document.getElementById('latest-version'),
    en: document.getElementById('latest-version-en'),
    ar: document.getElementById('latest-version-ar'),
    pt: document.getElementById('latest-version-pt'),
    tr: document.getElementById('latest-version-tr')
};
const modalVersionEls = {
    fr: document.getElementById('modal-version'),
    en: document.getElementById('modal-version-en'),
    ar: document.getElementById('modal-version-ar'),
    pt: document.getElementById('modal-version-pt'),
    tr: document.getElementById('modal-version-tr')
};
const updateInfoEl = document.getElementById('update-info');
const langButtons = {
    fr: document.getElementById('lang-fr'),
    en: document.getElementById('lang-en'),
    ar: document.getElementById('lang-ar'),
    pt: document.getElementById('lang-pt'),
    tr: document.getElementById('lang-tr')
};
const releaseNotesBtn = document.getElementById('release-notes-btn');
const releaseNotesModal = document.getElementById('release-notes-modal');
const helpButton = document.getElementById('help-button');
const helpModal = document.getElementById('help-modal');
const closeModalBtns = document.querySelectorAll('.close-modal');
const releaseNotesContent = document.getElementById('release-notes');
const qrCodeEl = document.getElementById('qr-code');
const fileSizeEls = {
    windows: document.getElementById('windows-size'),
    macos: document.getElementById('macos-size'),
    ubuntu: document.getElementById('ubuntu-size')
};

// Nouveaux éléments pour le téléchargement
const progressContainers = {
    windows: document.getElementById('windows-progress'),
    macos: document.getElementById('macos-progress'),
    ubuntu: document.getElementById('ubuntu-progress')
};

const progressBars = {
    windows: document.getElementById('windows-progress-bar'),
    macos: document.getElementById('macos-progress-bar'),
    ubuntu: document.getElementById('ubuntu-progress-bar')
};

const speedEls = {
    windows: document.getElementById('windows-speed'),
    macos: document.getElementById('macos-speed'),
    ubuntu: document.getElementById('ubuntu-speed')
};

const completeEls = {
    windows: document.getElementById('windows-complete'),
    macos: document.getElementById('macos-complete'),
    ubuntu: document.getElementById('ubuntu-complete')
};

// Éléments pour le slider de témoignages
const testimonialSlider = document.getElementById('testimonial-slider');
const sliderDots = document.querySelectorAll('.slider-dot');
let currentSlide = 0;
let slideInterval;

// Gestion du multilinguisme
function setLanguage(lang) {
    document.querySelectorAll(`[data-lang]`).forEach(el => {
        el.style.display = el.getAttribute('data-lang') === lang ? '' : 'none';
    });

    // Mettre à jour les boutons de langue
    Object.values(langButtons).forEach(btn => btn.classList.remove('active'));
    langButtons[lang].classList.add('active');

    // Stocker la préférence
    localStorage.setItem('leopardo_lang', lang);

    // Appliquer la direction RTL pour l'arabe
    document.body.style.direction = lang === 'ar' ? 'rtl' : 'ltr';

    // Envoyer l'événement d'analyse
    analytics.logEvent('language_change', { language: lang });
}

// Gestion des onglets de plateforme
function setActivePlatform(platform) {
    platformTabs.forEach(tab => tab.classList.remove('active'));
    platformContents.forEach(content => content.classList.remove('active'));

    document.querySelector(`.platform-tab[data-platform="${platform}"]`).classList.add('active');
    document.getElementById(`${platform}-content`).classList.add('active');

    // Envoyer l'événement d'analyse
    analytics.logEvent('platform_select', { platform });
}

// Formater la taille du fichier
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

// Récupérer la dernière version depuis GitHub
async function fetchLatestRelease() {
    try {
        // Afficher le skeleton pendant le chargement
        Object.values(appVersionEls).forEach(el => {
            el.textContent = '';
            el.classList.add('skeleton');
        });

        const response = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/releases/latest`);
        if (!response.ok) throw new Error("Failed to fetch release");

        const data = await response.json();
        const version = data.tag_name.replace(/^v/, '');

        // Trouver les assets pour chaque plateforme
        const assets = {
            windows: data.assets.find(asset =>
                asset.name.match(/(\.exe|windows|win)/i) &&
                !asset.name.match(/debug|symbols/i)
            ),
            macos: data.assets.find(asset =>
                asset.name.match(/(\.dmg|macos|mac|\.pkg)/i) &&
                !asset.name.match(/debug|symbols/i)
            ),
            ubuntu: data.assets.find(asset =>
                asset.name.match(/(\.deb|ubuntu|linux)/i) &&
                !asset.name.match(/debug|symbols/i)
            )
        };

        // Récupérer les tailles de fichiers
        const sizes = {
            windows: assets.windows?.size ? formatFileSize(assets.windows.size) : '',
            macos: assets.macos?.size ? formatFileSize(assets.macos.size) : '',
            ubuntu: assets.ubuntu?.size ? formatFileSize(assets.ubuntu.size) : ''
        };

        return {
            version,
            downloadUrls: {
                windows: assets.windows?.browser_download_url || '',
                macos: assets.macos?.browser_download_url || '',
                ubuntu: assets.ubuntu?.browser_download_url || ''
            },
            fileSizes: sizes,
            notes: data.body
        };
    } catch (error) {
        console.error("Error fetching GitHub release:", error);
        return null;
    } finally {
        // Retirer le skeleton
        Object.values(appVersionEls).forEach(el => el.classList.remove('skeleton'));
    }
}

// Mettre à jour l'interface avec les données de la release
function updateUIWithRelease(release) {
    currentVersion = release.version;
    downloadUrls = release.downloadUrls;
    fileSizes = release.fileSizes;
    releaseNotes = release.notes;

    // Mettre à jour les versions affichées
    Object.values(appVersionEls).forEach(el => el.textContent = currentVersion);
    Object.values(modalVersionEls).forEach(el => el.textContent = currentVersion);

    // Configurer les liens de téléchargement
    windowsDownloadBtn.href = downloadUrls.windows || '#';
    macosDownloadBtn.href = downloadUrls.macos || '#';
    ubuntuDownloadBtn.href = downloadUrls.ubuntu || '#';

    // Mettre à jour les tailles de fichiers
    fileSizeEls.windows.textContent = fileSizes.windows ? `(${fileSizes.windows})` : '';
    fileSizeEls.macos.textContent = fileSizes.macos ? `(${fileSizes.macos})` : '';
    fileSizeEls.ubuntu.textContent = fileSizes.ubuntu ? `(${fileSizes.ubuntu})` : '';

    // Désactiver les boutons si pas de lien disponible
    windowsDownloadBtn.classList.toggle('disabled', !downloadUrls.windows);
    macosDownloadBtn.classList.toggle('disabled', !downloadUrls.macos);
    ubuntuDownloadBtn.classList.toggle('disabled', !downloadUrls.ubuntu);

    // Générer le QR code
    generateQRCode();

    // Vérifier si une nouvelle version est disponible
    checkForNewVersion();
}

// Générer le QR code
function generateQRCode() {
    const qr = qrcode(0, 'L');
    qr.addData(APP_DOWNLOAD_PAGE);
    qr.make();
    qrCodeEl.innerHTML = qr.createImgTag(4);
    qrCodeEl.querySelector('img').style.width = '100%';
    qrCodeEl.querySelector('img').style.height = '100%';
}

// Vérifier si une nouvelle version est disponible
async function checkForNewVersion() {
    const storedVersion = localStorage.getItem('leopardo_last_version');
    if (storedVersion && storedVersion !== currentVersion) {
        Object.values(latestVersionEls).forEach(el => el.textContent = storedVersion);
        updateInfoEl.style.display = 'flex';
    }

    // Vérifier aussi sur GitHub pour les mises à jour futures
    try {
        const response = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/releases`);
        if (response.ok) {
            const releases = await response.json();
            if (releases.length > 0 && releases[0].tag_name.replace(/^v/, '') !== currentVersion) {
                database.ref('releases/latest').set({
                    version: releases[0].tag_name.replace(/^v/, ''),
                    timestamp: firebase.database.ServerValue.TIMESTAMP
                });
            }
        }
    } catch (error) {
        console.error("Error checking for updates:", error);
    }
}

// Mettre à jour les statistiques
function updateStats() {
    // Compteur de téléchargements
    database.ref('downloads/count').on('value', (snapshot) => {
        const count = snapshot.val() || 0;
        animateCounter(downloadCountEl, count);
    });

    // Utilisateurs actifs
    database.ref('stats/active_users').on('value', (snapshot) => {
        const count = snapshot.val() || 0;
        animateCounter(activeUsersEl, count);
    });

    // Pays
    database.ref('stats/countries').on('value', (snapshot) => {
        const count = snapshot.val() || 0;
        animateCounter(countriesEl, count);
    });
}

// Animation du compteur
function animateCounter(element, target) {
    const current = parseInt(element.textContent.replace(/,/g, '')) || 0;
    const increment = target > current ? 1 : -1;
    let currentValue = current;

    const timer = setInterval(() => {
        currentValue += increment;
        element.textContent = currentValue.toLocaleString();

        if ((increment === 1 && currentValue >= target) ||
            (increment === -1 && currentValue <= target)) {
            clearInterval(timer);
            element.textContent = target.toLocaleString();
        }
    }, 20);
}

// Simuler le téléchargement avec une barre de progression
function simulateDownload(platform) {
    const progressBar = progressBars[platform];
    const speedEl = speedEls[platform];
    const completeEl = completeEls[platform];
    const progressContainer = progressContainers[platform];

    let progress = 0;
    let speed = Math.random() * 2 + 1; // MB/s aléatoire entre 1 et 3

    progressContainer.style.display = 'block';
    speedEl.style.display = 'block';
    completeEl.style.display = 'none';

    const downloadInterval = setInterval(() => {
        progress += Math.random() * 10;
        if (progress > 100) progress = 100;

        progressBar.style.width = `${progress}%`;
        speedEl.textContent = `${speed.toFixed(1)} MB/s`;

        if (progress === 100) {
            clearInterval(downloadInterval);
            speedEl.style.display = 'none';
            completeEl.style.display = 'block';

            const lang = localStorage.getItem('leopardo_lang') || 'fr';

            const completeMessages = {
                fr: 'Téléchargement terminé !',
                en: 'Download complete!',
                ar: 'اكتمل التنزيل!',
                pt: 'Download completo!',
                tr: 'İndirme tamamlandı!'
            };

            completeEl.textContent = completeMessages[lang];

            // Réinitialiser après 5 secondes
            setTimeout(() => {
                progressContainer.style.display = 'none';
                completeEl.style.display = 'none';
                progressBar.style.width = '0%';
            }, 5000);
        }
    }, 200);
}

// Enregistrer un téléchargement
function registerDownload(e) {
    e.preventDefault();
    const platform = document.querySelector('.platform-tab.active').getAttribute('data-platform');
    const language = localStorage.getItem('leopardo_lang') || 'fr';

    // Empêcher le téléchargement si désactivé
    if ((platform === 'windows' && !downloadUrls.windows) ||
        (platform === 'macos' && !downloadUrls.macos) ||
        (platform === 'ubuntu' && !downloadUrls.ubuntu)) {
        return;
    }

    // Simuler le téléchargement
    simulateDownload(platform);

    // Détecter le pays
    const country = Intl.DateTimeFormat().resolvedOptions().timeZone.split('/')[0] || 'unknown';

    const downloadData = {
        version: currentVersion,
        platform,
        timestamp: firebase.database.ServerValue.TIMESTAMP,
        userAgent: navigator.userAgent,
        referrer: document.referrer || 'direct',
        language,
        country
    };

    // Envoyer les données
    database.ref('downloads').push(downloadData);

    // Incrémenter le compteur
    database.ref('downloads/count').transaction((count) => {
        return (count || 0) + 1;
    });

    // Mettre à jour les statistiques pays
    database.ref(`countries/${country}`).transaction((count) => {
        return (count || 0) + 1;
    });

    // Mettre à jour le nombre total de pays uniques
    database.ref('countries').once('value').then((snapshot) => {
        const countriesCount = snapshot.numChildren();
        database.ref('stats/countries').set(countriesCount);
    });

    // Stocker la version installée
    localStorage.setItem('leopardo_last_version', currentVersion);
    updateInfoEl.style.display = 'none';

    // Envoyer l'événement d'analyse
    analytics.logEvent('download', {
        platform,
        version: currentVersion,
        language,
        country
    });

    // Rediriger vers le téléchargement après un court délai
    setTimeout(() => {
        window.location.href = downloadUrls[platform];
    }, 1500);
}

// function registerDownload(e) {
//     e.preventDefault();
//     const platform = document.querySelector('.platform-tab.active').getAttribute('data-platform');
//     const language = localStorage.getItem('leopardo_lang') || 'fr';
//
//     // Empêcher le téléchargement si désactivé
//     if ((platform === 'windows' && !downloadUrls.windows) ||
//         (platform === 'macos' && !downloadUrls.macos) ||
//         (platform === 'ubuntu' && !downloadUrls.ubuntu)) {
//         return;
//     }
//
//     // Simuler le téléchargement
//     simulateDownload(platform);
//
//     // Détecter le pays
//     const country = Intl.DateTimeFormat().resolvedOptions().timeZone.split('/')[0] || 'unknown';
//
//     const downloadData = {
//         version: currentVersion,
//         platform,
//         timestamp: firebase.database.ServerValue.TIMESTAMP,
//         userAgent: navigator.userAgent,
//         referrer: document.referrer || 'direct',
//         language,
//         country
//     };
//
//     // Envoyer les données
//     database.ref('downloads').push(downloadData);
//
//     // Incrémenter le compteur
//     database.ref('downloads/count').transaction((count) => {
//         return (count || 0) + 1;
//     });
//
//     // Mettre à jour les statistiques pays
//     database.ref(`countries/${country}`).transaction((count) => {
//         return (count || 0) + 1;
//     });
//
//     // Mettre à jour le nombre total de pays uniques
//     database.ref('countries').once('value').then((snapshot) => {
//         const countriesCount = snapshot.numChildren();
//         database.ref('stats/countries').set(countriesCount);
//     });
//
//     // Stocker la version installée
//     localStorage.setItem('leopardo_last_version', currentVersion);
//     updateInfoEl.style.display = 'none';
//
//     // Envoyer l'événement d'analyse
//     analytics.logEvent('download', {
//         platform,
//         version: currentVersion,
//         language,
//         country
//     });
//
//     // Rediriger vers le téléchargement après un court délai
//     setTimeout(() => {
//         window.location.href = downloadUrls[platform];
//     }, 1500);
// }

// Gestion du slider de témoignages
function setupDownloadCounter() {
    // Écouter les changements sur le compteur
    database.ref('downloads/count').on('value', (snapshot) => {
        const count = snapshot.val() || 0;
        document.getElementById('download-count').textContent = count.toLocaleString();
    });

    // Initialiser avec la valeur actuelle
    database.ref('downloads/count').once('value').then((snapshot) => {
        const count = snapshot.val() || 0;
        document.getElementById('download-count').textContent = count.toLocaleString();
    });
}

function goToSlide(index) {
    currentSlide = index;
    testimonialSlider.scrollTo({
        left: testimonialSlider.clientWidth * index,
        behavior: 'smooth'
    });

    // Mettre à jour les points de navigation
    sliderDots.forEach((dot, i) => {
        dot.classList.toggle('active', i === index);
    });
}

function startSlider() {
    slideInterval = setInterval(() => {
        currentSlide = (currentSlide + 1) % sliderDots.length;
        goToSlide(currentSlide);
    }, 5000);
}

function stopSlider() {
    clearInterval(slideInterval);
}

// Partager sur les réseaux sociaux
function setupSocialSharing() {
    const shareUrl = encodeURIComponent(window.location.href);
    const shareText = encodeURIComponent("Découvrez Leopardo AI - La plateforme révolutionnaire de marketing intelligent");

    document.getElementById('share-twitter').href = `https://twitter.com/intent/tweet?url=${shareUrl}&text=${shareText}`;
    document.getElementById('share-facebook').href = `https://www.facebook.com/sharer/sharer.php?u=${shareUrl}`;
    document.getElementById('share-linkedin').href = `https://www.linkedin.com/shareArticle?mini=true&url=${shareUrl}&title=${shareText}`;
    document.getElementById('share-whatsapp').href = `https://wa.me/?text=${shareText}%20${shareUrl}`;
}

// Afficher les notes de version
function showReleaseNotes() {
    releaseNotesContent.textContent = releaseNotes;
    Object.values(modalVersionEls).forEach(el => el.textContent = currentVersion);
    releaseNotesModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';

    // Envoyer l'événement d'analyse
    analytics.logEvent('view_release_notes', { version: currentVersion });
}

// Afficher l'aide
function showHelp() {
    helpModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';

    // Envoyer l'événement d'analyse
    analytics.logEvent('view_help');
}

// Fermer la modal
function closeModal() {
    releaseNotesModal.style.display = 'none';
    helpModal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// // Initialisation
// async function init() {
//     // Configurer les écouteurs d'événements
//     platformTabs.forEach(tab => {
//         tab.addEventListener('click', () => {
//             setActivePlatform(tab.getAttribute('data-platform'));
//         });
//     });

//     Object.entries(langButtons).forEach(([lang, btn]) => {
//         btn.addEventListener('click', () => setLanguage(lang));
//     });

//     windowsDownloadBtn.addEventListener('click', registerDownload);
//     macosDownloadBtn.addEventListener('click', registerDownload);
//     ubuntuDownloadBtn.addEventListener('click', registerDownload);
//     setupDownloadCounter();

//     // Gérer plusieurs boutons de notes de version (un par langue)
//     document.querySelectorAll('#release-notes-btn').forEach(btn => {
//         btn.addEventListener('click', showReleaseNotes);
//     });

//     closeModalBtns.forEach(btn => {
//         btn.addEventListener('click', closeModal);
//     });

//     window.addEventListener('click', (e) => {
//         if (e.target === releaseNotesModal || e.target === helpModal) closeModal();
//     });

//     // Configurer le slider de témoignages
//     testimonialSlider.addEventListener('mouseenter', stopSlider);
//     testimonialSlider.addEventListener('mouseleave', startSlider);

//     sliderDots.forEach(dot => {
//         dot.addEventListener('click', () => {
//             goToSlide(parseInt(dot.getAttribute('data-index')));
//         });
//     });

//     // Configurer le bouton d'aide
//     helpButton.addEventListener('click', showHelp);

//     startSlider();

//     // Configurer le partage social
//     setupSocialSharing();

//     // Vérifier la langue préférée
//     const userLang = localStorage.getItem('leopardo_lang') ||
//                    (navigator.language.startsWith('fr') ? 'fr' :
//                    navigator.language.startsWith('ar') ? 'ar' :
//                    navigator.language.startsWith('pt') ? 'pt' :
//                    navigator.language.startsWith('tr') ? 'tr' : 'en');
//     setLanguage(userLang);

//     // Charger les données
//     updateStats();

//     // Simuler des utilisateurs actifs (à remplacer par des données réelles)
//     database.ref('stats/active_users').set(Math.floor(Math.random() * 5000) + 1000);

//     const release = await fetchLatestRelease();
//     if (release) {
//         updateUIWithRelease(release);

//         // Stocker la dernière version dans Firebase pour référence
//         database.ref('releases/latest').set({
//             version: release.version,
//             timestamp: firebase.database.ServerValue.TIMESTAMP,
//             windows: !!release.downloadUrls.windows,
//             macos: !!release.downloadUrls.macos,
//             ubuntu: !!release.downloadUrls.ubuntu,
//             notes: release.notes
//         });
//     } else {
//         // Fallback si GitHub échoue
//         currentVersion = "1.2.3";
//         downloadUrls = {
//             windows: "https://github.com/kitokoh/leopardo/releases/download/v1.2.3/Leopardo-ai.exe",
//             macos: "https://github.com/kitokoh/leopardo/releases/download/v1.2.3/Leopardo-ai.dmg",
//             ubuntu: "https://github.com/kitokoh/leopardo/releases/download/v1.2.3/Leopardo-ai.deb"
//         };
//         fileSizes = {
//             windows: "45.2 MB",
//             macos: "52.7 MB",
//             ubuntu: "48.5 MB"
//         };
//         releaseNotes = "Version initiale de Leopardo AI avec toutes les fonctionnalités de base.";
//         updateUIWithRelease({version: currentVersion, downloadUrls, fileSizes, notes: releaseNotes});
//     }

//     // Envoyer l'événement d'analyse de page vue
//     analytics.logEvent('page_view', {
//         page_title: 'Download Page',
//         page_location: window.location.href,
//         user_language: localStorage.getItem('leopardo_lang') || navigator.language
//     });
// }
async function init() {
    try {
        // Initialiser les éléments du DOM après le chargement des fichiers partiels
        platformTabs = document.querySelectorAll('.platform-tab');
        platformContents = document.querySelectorAll('.platform-content');
        windowsDownloadBtn = document.getElementById('windows-download');
        macosDownloadBtn = document.getElementById('macos-download');
        ubuntuDownloadBtn = document.getElementById('ubuntu-download');
        downloadCountEl = document.getElementById('download-count');
        activeUsersEl = document.getElementById('active-users');
        countriesEl = document.getElementById('countries');
        appVersionEls = {
            fr: document.getElementById('app-version'),
            en: document.getElementById('app-version-en'),
            ar: document.getElementById('app-version-ar'),
            pt: document.getElementById('app-version-pt'),
            tr: document.getElementById('app-version-tr')
        };
        latestVersionEls = {
            fr: document.getElementById('latest-version'),
            en: document.getElementById('latest-version-en'),
            ar: document.getElementById('latest-version-ar'),
            pt: document.getElementById('latest-version-pt'),
            tr: document.getElementById('latest-version-tr')
        };
        modalVersionEls = {
            fr: document.getElementById('modal-version'),
            en: document.getElementById('modal-version-en'),
            ar: document.getElementById('modal-version-ar'),
            pt: document.getElementById('modal-version-pt'),
            tr: document.getElementById('modal-version-tr')
        };
        updateInfoEl = document.getElementById('update-info');
        langButtons = {
            fr: document.getElementById('lang-fr'),
            en: document.getElementById('lang-en'),
            ar: document.getElementById('lang-ar'),
            pt: document.getElementById('lang-pt'),
            tr: document.getElementById('lang-tr')
        };
        releaseNotesBtn = document.getElementById('release-notes-btn');
        releaseNotesModal = document.getElementById('release-notes-modal');
        helpButton = document.getElementById('help-button');
        helpModal = document.getElementById('help-modal');
        closeModalBtns = document.querySelectorAll('.close-modal');
        releaseNotesContent = document.getElementById('release-notes');
        qrCodeEl = document.getElementById('qr-code');
        fileSizeEls = {
            windows: document.getElementById('windows-size'),
            macos: document.getElementById('macos-size'),
            ubuntu: document.getElementById('ubuntu-size')
        };
        progressContainers = {
            windows: document.getElementById('windows-progress'),
            macos: document.getElementById('macos-progress'),
            ubuntu: document.getElementById('ubuntu-progress')
        };
        progressBars = {
            windows: document.getElementById('windows-progress-bar'),
            macos: document.getElementById('macos-progress-bar'),
            ubuntu: document.getElementById('ubuntu-progress-bar')
        };
        speedEls = {
            windows: document.getElementById('windows-speed'),
            macos: document.getElementById('macos-speed'),
            ubuntu: document.getElementById('ubuntu-speed')
        };
        completeEls = {
            windows: document.getElementById('windows-complete'),
            macos: document.getElementById('macos-complete'),
            ubuntu: document.getElementById('ubuntu-complete')
        };
        testimonialSlider = document.getElementById('testimonial-slider');
        sliderDots = document.querySelectorAll('.slider-dot');

        // Configurer les écouteurs d'événements
        platformTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                setActivePlatform(tab.getAttribute('data-platform'));
            });
        });

        Object.entries(langButtons).forEach(([lang, btn]) => {
            btn.addEventListener('click', () => setLanguage(lang));
        });

        windowsDownloadBtn.addEventListener('click', registerDownload);
        macosDownloadBtn.addEventListener('click', registerDownload);
        ubuntuDownloadBtn.addEventListener('click', registerDownload);
        setupDownloadCounter();

        // Gérer plusieurs boutons de notes de version (un par langue)
        document.querySelectorAll('#release-notes-btn').forEach(btn => {
            btn.addEventListener('click', showReleaseNotes);
        });

        closeModalBtns.forEach(btn => {
            btn.addEventListener('click', closeModal);
        });

        window.addEventListener('click', (e) => {
            if (e.target === releaseNotesModal || e.target === helpModal) closeModal();
        });

        // Configurer le slider de témoignages
        testimonialSlider.addEventListener('mouseenter', stopSlider);
        testimonialSlider.addEventListener('mouseleave', startSlider);

        sliderDots.forEach(dot => {
            dot.addEventListener('click', () => {
                goToSlide(parseInt(dot.getAttribute('data-index')));
            });
        });

        // Configurer le bouton d'aide
        helpButton.addEventListener('click', showHelp);

        startSlider();

        // Configurer le partage social
        setupSocialSharing();

        // Vérifier la langue préférée
        const userLang = localStorage.getItem('leopardo_lang') ||
                       (navigator.language.startsWith('fr') ? 'fr' :
                       navigator.language.startsWith('ar') ? 'ar' :
                       navigator.language.startsWith('pt') ? 'pt' :
                       navigator.language.startsWith('tr') ? 'tr' : 'en');
        setLanguage(userLang);

        // Charger les données
        updateStats();

        // Simuler des utilisateurs actifs (à remplacer par des données réelles)
        database.ref('stats/active_users').set(Math.floor(Math.random() * 5000) + 1000);

        const release = await fetchLatestRelease();
        if (release) {
            updateUIWithRelease(release);

            // Stocker la dernière version dans Firebase pour référence
            database.ref('releases/latest').set({
                version: release.version,
                timestamp: firebase.database.ServerValue.TIMESTAMP,
                windows: !!release.downloadUrls.windows,
                macos: !!release.downloadUrls.macos,
                ubuntu: !!release.downloadUrls.ubuntu,
                notes: release.notes
            });
        } else {
            // Fallback si GitHub échoue
            currentVersion = "1.2.3";
            downloadUrls = {
                windows: "https://github.com/kitokoh/leopardo/releases/download/v1.2.3/Leopardo-ai.exe",
                macos: "https://github.com/kitokoh/leopardo/releases/download/v1.2.3/Leopardo-ai.dmg",
                ubuntu: "https://github.com/kitokoh/leopardo/releases/download/v1.2.3/Leopardo-ai.deb"
            };
            fileSizes = {
                windows: "45.2 MB",
                macos: "52.7 MB",
                ubuntu: "48.5 MB"
            };
            releaseNotes = "Version initiale de Leopardo AI avec toutes les fonctionnalités de base.";
            updateUIWithRelease({version: currentVersion, downloadUrls, fileSizes, notes: releaseNotes});
        }

        // Envoyer l'événement d'analyse de page vue
        analytics.logEvent('page_view', {
            page_title: 'Download Page',
            page_location: window.location.href,
            user_language: localStorage.getItem('leopardo_lang') || navigator.language
        });
    } catch (error) {
        console.error("An error occurred during initialization:", error);
    }
}

// Démarrer l'application
document.addEventListener('DOMContentLoaded', init);
