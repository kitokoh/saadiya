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
try {
    if (!firebase.apps.length) {
        firebase.initializeApp(firebaseConfig);
    }
    const database = firebase.database();
    const analytics = firebase.analytics();
    const auth = firebase.auth();
} catch (error) {
    console.error("Firebase initialization error:", error);
}

// Configuration GitHub
const GITHUB_REPO = "kitokoh/leopardo";
const APP_DOWNLOAD_PAGE = "https://leopardo.ai/download";
const CHROME_EXTENSION_URL = "https://chrome.google.com/webstore/detail/leopardo-ai/your-extension-id";
const FIREFOX_EXTENSION_URL = "https://addons.mozilla.org/firefox/addon/leopardo-ai/";

// Variables d'état
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
let isDownloading = false;

// Cache DOM
const DOM = {
    platformTabs: document.querySelectorAll('.platform-tab'),
    platformContents: document.querySelectorAll('.platform-content'),
    windowsDownloadBtn: document.getElementById('windows-download'),
    macosDownloadBtn: document.getElementById('macos-download'),
    ubuntuDownloadBtn: document.getElementById('ubuntu-download'),
    downloadCountEl: document.getElementById('download-count'),
    activeUsersEl: document.getElementById('active-users'),
    countriesEl: document.getElementById('countries'),
    appVersionEls: {
        fr: document.getElementById('app-version'),
        en: document.getElementById('app-version-en'),
        ar: document.getElementById('app-version-ar'),
        pt: document.getElementById('app-version-pt'),
        tr: document.getElementById('app-version-tr')
    },
    latestVersionEls: {
        fr: document.getElementById('latest-version'),
        en: document.getElementById('latest-version-en'),
        ar: document.getElementById('latest-version-ar'),
        pt: document.getElementById('latest-version-pt'),
        tr: document.getElementById('latest-version-tr')
    },
    modalVersionEls: {
        fr: document.getElementById('modal-version'),
        en: document.getElementById('modal-version-en'),
        ar: document.getElementById('modal-version-ar'),
        pt: document.getElementById('modal-version-pt'),
        tr: document.getElementById('modal-version-tr')
    },
    updateInfoEl: document.getElementById('update-info'),
    langButtons: {
        fr: document.getElementById('lang-fr'),
        en: document.getElementById('lang-en'),
        ar: document.getElementById('lang-ar'),
        pt: document.getElementById('lang-pt'),
        tr: document.getElementById('lang-tr')
    },
    releaseNotesBtn: document.getElementById('release-notes-btn'),
    releaseNotesModal: document.getElementById('release-notes-modal'),
    helpButton: document.getElementById('help-button'),
    helpModal: document.getElementById('help-modal'),
    closeModalBtns: document.querySelectorAll('.close-modal'),
    releaseNotesContent: document.getElementById('release-notes'),
    qrCodeEl: document.getElementById('qr-code'),
    fileSizeEls: {
        windows: document.getElementById('windows-size'),
        macos: document.getElementById('macos-size'),
        ubuntu: document.getElementById('ubuntu-size')
    },
    conditionalForm: document.getElementById('conditional-form'),
    chromeExtensionBtn: document.getElementById('chrome-extension'),
    firefoxExtensionBtn: document.getElementById('firefox-extension'),
    progressContainers: {
        windows: document.getElementById('windows-progress'),
        macos: document.getElementById('macos-progress'),
        ubuntu: document.getElementById('ubuntu-progress')
    },
    progressBars: {
        windows: document.getElementById('windows-progress-bar'),
        macos: document.getElementById('macos-progress-bar'),
        ubuntu: document.getElementById('ubuntu-progress-bar')
    },
    speedEls: {
        windows: document.getElementById('windows-speed'),
        macos: document.getElementById('macos-speed'),
        ubuntu: document.getElementById('ubuntu-speed')
    },
    completeEls: {
        windows: document.getElementById('windows-complete'),
        macos: document.getElementById('macos-complete'),
        ubuntu: document.getElementById('ubuntu-complete')
    },
    testimonialSlider: document.getElementById('testimonial-slider'),
    sliderDots: document.querySelectorAll('.slider-dot'),
    contactForm: document.getElementById('contactForm'),
    nameError: document.getElementById('nameError'),
    emailError: document.getElementById('emailError'),
    phoneError: document.getElementById('phoneError'),
    formSuccess: document.getElementById('formSuccess')
};

// Expressions régulières pour validation
const REGEX = {
    name: /^[a-zA-ZÀ-ÿ\s'-]{2,}$/,
    email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    phone: /^(\+?\d{1,3}[- ]?)?\d{10}$/
};

// Messages multilingues
const MESSAGES = {
    fr: {
        downloadComplete: 'Téléchargement terminé !',
        nameError: 'Veuillez entrer un nom valide',
        emailError: 'Veuillez entrer un email valide',
        phoneError: 'Veuillez entrer un numéro valide',
        formError: 'Une erreur s\'est produite. Veuillez réessayer.',
        loginError: 'Email ou mot de passe incorrect',
        resetSuccess: 'Email de réinitialisation envoyé'
    },
    en: {
        downloadComplete: 'Download complete!',
        nameError: 'Please enter a valid name',
        emailError: 'Please enter a valid email',
        phoneError: 'Please enter a valid phone number',
        formError: 'An error occurred. Please try again.',
        loginError: 'Incorrect email or password',
        resetSuccess: 'Reset email sent'
    },
    ar: {
        downloadComplete: 'اكتمل التنزيل!',
        nameError: 'الرجاء إدخال اسم صالح',
        emailError: 'الرجاء إدخال بريد إلكتروني صالح',
        phoneError: 'الرجاء إدخال رقم هاتف صالح',
        formError: 'حدث خطأ. يرجى المحاولة مرة أخرى.',
        loginError: 'البريد الإلكتروني أو كلمة المرور غير صحيحة',
        resetSuccess: 'تم إرسال بريد إلكتروني لإعادة التعيين'
    },
    pt: {
        downloadComplete: 'Download completo!',
        nameError: 'Por favor, insira um nome válido',
        emailError: 'Por favor, insira um e-mail válido',
        phoneError: 'Por favor, insira um número de telefone válido',
        formError: 'Ocorreu um erro. Por favor, tente novamente.',
        loginError: 'E-mail ou senha incorretos',
        resetSuccess: 'E-mail de redefinição enviado'
    },
    tr: {
        downloadComplete: 'İndirme tamamlandı!',
        nameError: 'Lütfen geçerli bir isim giriniz',
        emailError: 'Lütfen geçerli bir e-posta giriniz',
        phoneError: 'Lütfen geçerli bir telefon numarası giriniz',
        formError: 'Bir hata oluştu. Lütfen tekrar deneyin.',
        loginError: 'E-posta veya şifre yanlış',
        resetSuccess: 'Sıfırlama e-postası gönderildi'
    }
};

// Gestion du multilinguisme
function setLanguage(lang) {
    // Vérifier si la langue est supportée
    if (!MESSAGES[lang]) lang = 'en';
    
    document.querySelectorAll(`[data-lang]`).forEach(el => {
        el.style.display = el.getAttribute('data-lang') === lang ? '' : 'none';
    });

    // Mettre à jour le dropdown
    const selectedLang = document.querySelector(`.dropdown-menu a[data-lang="${lang}"]`);
    if (selectedLang) {
        document.getElementById('current-lang-flag').textContent = selectedLang.getAttribute('data-flag');
        document.getElementById('current-lang-code').textContent = lang.toUpperCase();
    }

    // Stocker la préférence
    localStorage.setItem('leopardo_lang', lang);

    // Appliquer la direction RTL pour l'arabe
    document.body.style.direction = lang === 'ar' ? 'rtl' : 'ltr';

    // Envoyer l'événement d'analyse
    analytics.logEvent('language_change', { language: lang });
}

// Gestion des onglets de plateforme
function setActivePlatform(platform) {
    DOM.platformTabs.forEach(tab => tab.classList.remove('active'));
    DOM.platformContents.forEach(content => content.classList.remove('active'));

    document.querySelector(`.platform-tab[data-platform="${platform}"]`).classList.add('active');
    document.getElementById(`${platform}-content`).classList.add('active');

    // Envoyer l'événement d'analyse
    analytics.logEvent('platform_select', { platform });
}

// Formater la taille du fichier
function formatFileSize(bytes) {
    if (bytes === 0 || isNaN(bytes)) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1) + ' ' + sizes[i];
}

// Récupérer la dernière version depuis GitHub avec cache
async function fetchLatestRelease() {
    const CACHE_KEY = 'leopardo_latest_release';
    const CACHE_DURATION = 30 * 60 * 1000; // 30 minutes
    
    // Vérifier le cache
    const cachedData = localStorage.getItem(CACHE_KEY);
    if (cachedData) {
        const { data, timestamp } = JSON.parse(cachedData);
        if (Date.now() - timestamp < CACHE_DURATION) {
            return data;
        }
    }

    try {
        // Afficher le skeleton pendant le chargement
        Object.values(DOM.appVersionEls).forEach(el => {
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

        // Préparer les données de la release
        const releaseData = {
            version,
            downloadUrls: {
                windows: assets.windows?.browser_download_url || '',
                macos: assets.macos?.browser_download_url || '',
                ubuntu: assets.ubuntu?.browser_download_url || ''
            },
            fileSizes: {
                windows: assets.windows?.size ? formatFileSize(assets.windows.size) : '',
                macos: assets.macos?.size ? formatFileSize(assets.macos.size) : '',
                ubuntu: assets.ubuntu?.size ? formatFileSize(assets.ubuntu.size) : ''
            },
            notes: data.body
        };

        // Mettre en cache
        localStorage.setItem(CACHE_KEY, JSON.stringify({
            data: releaseData,
            timestamp: Date.now()
        }));

        return releaseData;
    } catch (error) {
        console.error("Error fetching GitHub release:", error);
        
        // Essayer de retourner les données en cache même si expirées
        if (cachedData) {
            return JSON.parse(cachedData).data;
        }
        
        return null;
    } finally {
        // Retirer le skeleton
        Object.values(DOM.appVersionEls).forEach(el => el.classList.remove('skeleton'));
    }
}

// Mettre à jour l'interface avec les données de la release
function updateUIWithRelease(release) {
    if (!release) return;

    currentVersion = release.version;
    downloadUrls = release.downloadUrls;
    fileSizes = release.fileSizes;
    releaseNotes = release.notes;

    // Mettre à jour les versions affichées
    Object.values(DOM.appVersionEls).forEach(el => el.textContent = currentVersion);
    Object.values(DOM.modalVersionEls).forEach(el => el.textContent = currentVersion);

    // Configurer les liens de téléchargement
    DOM.windowsDownloadBtn.href = downloadUrls.windows || '#';
    DOM.macosDownloadBtn.href = downloadUrls.macos || '#';
    DOM.ubuntuDownloadBtn.href = downloadUrls.ubuntu || '#';

    // Mettre à jour les tailles de fichiers
    DOM.fileSizeEls.windows.textContent = fileSizes.windows ? `(${fileSizes.windows})` : '';
    DOM.fileSizeEls.macos.textContent = fileSizes.macos ? `(${fileSizes.macos})` : '';
    DOM.fileSizeEls.ubuntu.textContent = fileSizes.ubuntu ? `(${fileSizes.ubuntu})` : '';

    // Désactiver les boutons si pas de lien disponible
    DOM.windowsDownloadBtn.classList.toggle('disabled', !downloadUrls.windows);
    DOM.macosDownloadBtn.classList.toggle('disabled', !downloadUrls.macos);
    DOM.ubuntuDownloadBtn.classList.toggle('disabled', !downloadUrls.ubuntu);

    // Générer le QR code
    generateQRCode();

    // Vérifier si une nouvelle version est disponible
    checkForNewVersion();
}

// Générer le QR code
function generateQRCode() {
    if (!window.QRCode) {
        console.warn("QRCode library not loaded");
        return;
    }

    try {
        const qr = new QRCode(DOM.qrCodeEl, {
            text: APP_DOWNLOAD_PAGE,
            width: 150,
            height: 150,
            colorDark: "#000000",
            colorLight: "#ffffff",
            correctLevel: QRCode.CorrectLevel.L
        });
    } catch (error) {
        console.error("Error generating QR code:", error);
    }
}

// Vérifier si une nouvelle version est disponible
async function checkForNewVersion() {
    const storedVersion = localStorage.getItem('leopardo_last_version');
    if (storedVersion && storedVersion !== currentVersion) {
        Object.values(DOM.latestVersionEls).forEach(el => el.textContent = storedVersion);
        DOM.updateInfoEl.style.display = 'flex';
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
        animateCounter(DOM.downloadCountEl, count);
    });

    // Utilisateurs actifs
    database.ref('stats/active_users').on('value', (snapshot) => {
        const count = snapshot.val() || 0;
        animateCounter(DOM.activeUsersEl, count);
    });

    // Pays
    database.ref('stats/countries').on('value', (snapshot) => {
        const count = snapshot.val() || 0;
        animateCounter(DOM.countriesEl, count);
    });
}

// Animation du compteur
function animateCounter(element, target) {
    if (!element) return;
    
    const current = parseInt(element.textContent.replace(/,/g, '')) || 0;
    if (current === target) return;

    const increment = target > current ? 1 : -1;
    let currentValue = current;

    const duration = 1000; // 1 seconde
    const startTime = performance.now();
    
    function updateCounter(timestamp) {
        const elapsed = timestamp - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        currentValue = Math.floor(current + (target - current) * progress);
        element.textContent = currentValue.toLocaleString();

        if (progress < 1) {
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target.toLocaleString();
        }
    }

    requestAnimationFrame(updateCounter);
}

// Simuler le téléchargement avec une barre de progression
function simulateDownload(platform) {
    if (isDownloading) return;
    isDownloading = true;

    const progressBar = DOM.progressBars[platform];
    const speedEl = DOM.speedEls[platform];
    const completeEl = DOM.completeEls[platform];
    const progressContainer = DOM.progressContainers[platform];

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
            completeEl.textContent = MESSAGES[lang]?.downloadComplete || 'Download complete!';

            // Réinitialiser après 5 secondes
            setTimeout(() => {
                progressContainer.style.display = 'none';
                completeEl.style.display = 'none';
                progressBar.style.width = '0%';
                isDownloading = false;
            }, 5000);
        }
    }, 200);
}

// Afficher le formulaire conditionnel pendant le téléchargement
function showConditionalForm() {
    DOM.conditionalForm.classList.add('active');
    
    // Masquer le formulaire après 30 secondes
    setTimeout(() => {
        DOM.conditionalForm.classList.remove('active');
    }, 30000);
}

// Enregistrer un téléchargement
function registerDownload(e) {
    if (e) e.preventDefault();
    
    const platform = document.querySelector('.platform-tab.active')?.getAttribute('data-platform');
    const language = localStorage.getItem('leopardo_lang') || 'fr';

    // Vérifier la plateforme
    if (!platform || !['windows', 'macos', 'ubuntu'].includes(platform)) return;
    
    // Empêcher le téléchargement si désactivé
    if (!downloadUrls[platform]) {
        return;
    }

    // Simuler le téléchargement
    simulateDownload(platform);
    
    // Afficher le formulaire conditionnel
    showConditionalForm();

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
    DOM.updateInfoEl.style.display = 'none';

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

// Gestion du slider de témoignages
let currentSlide = 0;
let slideInterval;

function goToSlide(index) {
    if (!DOM.testimonialSlider || index < 0 || index >= DOM.sliderDots.length) return;
    
    currentSlide = index;
    DOM.testimonialSlider.scrollTo({
        left: DOM.testimonialSlider.clientWidth * index,
        behavior: 'smooth'
    });

    // Mettre à jour les points de navigation
    DOM.sliderDots.forEach((dot, i) => {
        dot.classList.toggle('active', i === index);
    });
}

function startSlider() {
    if (!DOM.testimonialSlider || DOM.sliderDots.length === 0) return;
    
    stopSlider();
    
    slideInterval = setInterval(() => {
        currentSlide = (currentSlide + 1) % DOM.sliderDots.length;
        goToSlide(currentSlide);
    }, 5000);
}

function stopSlider() {
    if (slideInterval) {
        clearInterval(slideInterval);
    }
}

// Partager sur les réseaux sociaux
function setupSocialSharing() {
    const shareUrl = encodeURIComponent(window.location.href);
    const shareText = encodeURIComponent("Découvrez Leopardo AI - La plateforme révolutionnaire de marketing intelligent");

    document.getElementById('share-twitter')?.setAttribute('href', `https://twitter.com/intent/tweet?url=${shareUrl}&text=${shareText}`);
    document.getElementById('share-facebook')?.setAttribute('href', `https://www.facebook.com/sharer/sharer.php?u=${shareUrl}`);
    document.getElementById('share-linkedin')?.setAttribute('href', `https://www.linkedin.com/shareArticle?mini=true&url=${shareUrl}&title=${shareText}`);
    document.getElementById('share-whatsapp')?.setAttribute('href', `https://wa.me/?text=${shareText}%20${shareUrl}`);
}

// Installer les extensions navigateur
function setupExtensionButtons() {
    DOM.chromeExtensionBtn?.addEventListener('click', function(e) {
        e.preventDefault();
        analytics.logEvent('install_extension', { browser: 'chrome' });
        window.open(CHROME_EXTENSION_URL, '_blank');
    });

    DOM.firefoxExtensionBtn?.addEventListener('click', function(e) {
        e.preventDefault();
        analytics.logEvent('install_extension', { browser: 'firefox' });
        window.open(FIREFOX_EXTENSION_URL, '_blank');
    });
}

// Afficher les notes de version
function showReleaseNotes() {
    if (!DOM.releaseNotesContent || !DOM.releaseNotesModal) return;
    
    DOM.releaseNotesContent.textContent = releaseNotes;
    Object.values(DOM.modalVersionEls).forEach(el => {
        if (el) el.textContent = currentVersion;
    });
    DOM.releaseNotesModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';

    // Envoyer l'événement d'analyse
    analytics.logEvent('view_release_notes', { version: currentVersion });
}

// Afficher l'aide
function showHelp() {
    if (!DOM.helpModal) return;
    
    DOM.helpModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';

    // Envoyer l'événement d'analyse
    analytics.logEvent('view_help');
}

// Fermer la modal
function closeModal() {
    if (DOM.releaseNotesModal) DOM.releaseNotesModal.style.display = 'none';
    if (DOM.helpModal) DOM.helpModal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Validation du champ de formulaire
function validateField(field, regex, errorElement) {
    const lang = localStorage.getItem('leopardo_lang') || 'fr';
    const messageKey = `${field.id.replace('contact', '').toLowerCase()}Error`;

    if (!regex.test(field.value)) {
        errorElement.textContent = MESSAGES[lang]?.[messageKey] || 'Invalid field';
        errorElement.style.display = 'block';
        return false;
    } else {
        errorElement.style.display = 'none';
        return true;
    }
}

// Soumission du formulaire
DOM.contactForm?.addEventListener('submit', async function(e) {
    e.preventDefault();

    // Récupérer les valeurs
    const name = document.getElementById('contactName')?.value.trim();
    const email = document.getElementById('contactEmail')?.value.trim();
    const phone = document.getElementById('contactPhone')?.value.trim().replace(/\s/g, '');
    const lang = localStorage.getItem('leopardo_lang') || 'fr';

    // Validation finale
    const isNameValid = validateField(
        { id: 'contactName', value: name },
        REGEX.name,
        DOM.nameError
    );

    const isEmailValid = validateField(
        { id: 'contactEmail', value: email },
        REGEX.email,
        DOM.emailError
    );

    const isPhoneValid = validateField(
        { id: 'contactPhone', value: phone },
        REGEX.phone,
        DOM.phoneError
    );

    if (!isNameValid || !isEmailValid || !isPhoneValid) return;

    // Afficher le spinner
    const spinnerId = `submitSpinner${lang === 'fr' ? '' : lang.charAt(0).toUpperCase() + lang.slice(1)}`;
    const btnTextId = `submitBtnText${lang === 'fr' ? '' : lang.charAt(0).toUpperCase() + lang.slice(1)}`;

    const spinner = document.getElementById(spinnerId);
    const btnText = document.getElementById(btnTextId);
    
    if (spinner) spinner.style.display = 'inline-block';
    if (btnText) btnText.style.display = 'none';

    // Formatage du numéro de téléphone
    let formattedPhone = phone;
    if (phone.startsWith('0')) {
        formattedPhone = '+33' + phone.substring(1);
    } else if (!phone.startsWith('+')) {
        formattedPhone = '+' + phone;
    }

    // Créer un objet de données
    const contactData = {
        name,
        email,
        phone: formattedPhone,
        language: lang,
        timestamp: firebase.database.ServerValue.TIMESTAMP,
        userAgent: navigator.userAgent,
        page: window.location.href
    };

    try {
        // Envoyer les données à Firebase
        await database.ref('contacts').push(contactData);
        await sendToGoogleSheets(contactData);

        // Succès
        DOM.contactForm.reset();
        DOM.formSuccess.style.display = 'block';

        // Masquer le formulaire conditionnel
        DOM.conditionalForm.classList.remove('active');

        // Masquer le spinner
        if (spinner) spinner.style.display = 'none';
        if (btnText) btnText.style.display = 'inline';

        // Cacher le message après 5 secondes
        setTimeout(() => {
            DOM.formSuccess.style.display = 'none';
        }, 5000);

        // Envoyer l'événement d'analyse
        analytics.logEvent('contact_form_submit', {
            form_name: 'contact_form',
            language: lang
        });
    } catch (error) {
        console.error("Erreur d'enregistrement: ", error);

        // Masquer le spinner
        if (spinner) spinner.style.display = 'none';
        if (btnText) btnText.style.display = 'inline';

        // Afficher un message d'erreur
        alert(MESSAGES[lang]?.formError || 'An error occurred');
    }
});

async function sendToGoogleSheets(data) {
    const webhookUrl = 'https://script.google.com/macros/s/AKfycbzjBEtoeGcosEFv7yULAxa4RdPdTWUb7Tovtlr6Ym4EkDdttIYz2SU1s5HUHmqSaIDk1Q/exec';

    try {
        const response = await fetch(webhookUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error sending to Google Sheets:', error);
        throw error;
    }
}

// Gestion de la connexion admin
function setupAuth() {
    // Vérifier si l'utilisateur est déjà connecté
    auth.onAuthStateChanged(user => {
        if (user) {
            // Utilisateur connecté - rediriger vers le dashboard
            window.location.href = 'dashboard.html';
        }
    });

    // Gérer le clic sur le bouton de connexion admin
    document.getElementById('admin-login-btn')?.addEventListener('click', () => {
        document.getElementById('login-modal').style.display = 'flex';
        document.body.style.overflow = 'hidden';
    });

    // Gérer la fermeture du modal
    document.querySelector('#login-modal .close-modal')?.addEventListener('click', () => {
        document.getElementById('login-modal').style.display = 'none';
        document.body.style.overflow = 'auto';
    });

    // Toggle visibilité du mot de passe
    document.getElementById('togglePassword')?.addEventListener('click', function() {
        const passwordInput = document.getElementById('loginPassword');
        if (!passwordInput) return;
        
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        this.classList.toggle('fa-eye-slash');
    });

    // Gérer la soumission du formulaire de connexion
    document.getElementById('loginForm')?.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const email = document.getElementById('loginEmail')?.value;
        const password = document.getElementById('loginPassword')?.value;
        const submitBtn = document.getElementById('loginSubmitBtn');
        const spinner = document.getElementById('loginSpinner');
        const errorEl = document.getElementById('loginError');
        
        if (!email || !password || !submitBtn || !spinner || !errorEl) return;
        
        // Afficher le spinner
        submitBtn.disabled = true;
        spinner.style.display = 'inline-block';
        errorEl.style.display = 'none';
        
        try {
            // Connexion avec Firebase Auth
            await auth.signInWithEmailAndPassword(email, password);
            
            // Redirection vers le dashboard se fait automatiquement via onAuthStateChanged
        } catch (error) {
            // Gérer les erreurs
            submitBtn.disabled = false;
            spinner.style.display = 'none';
            errorEl.style.display = 'block';
            
            const lang = localStorage.getItem('leopardo_lang') || 'fr';
            errorEl.textContent = MESSAGES[lang]?.loginError || 'Login error';
            
            // Envoyer l'événement d'analyse
            analytics.logEvent('login_error', {
                error_code: error.code,
                email: email
            });
        }
    });

    // Gérer la réinitialisation du mot de passe
    document.getElementById('resetPasswordLink')?.addEventListener('click', async function(e) {
        e.preventDefault();
        
        const email = document.getElementById('loginEmail')?.value;
        const errorEl = document.getElementById('loginError');
        if (!email || !errorEl) return;
        
        const lang = localStorage.getItem('leopardo_lang') || 'fr';
        
        try {
            await auth.sendPasswordResetEmail(email);
            
            errorEl.style.display = 'block';
            errorEl.style.color = 'var(--success)';
            errorEl.textContent = MESSAGES[lang]?.resetSuccess || 'Reset email sent';
            
            // Envoyer l'événement d'analyse
            analytics.logEvent('password_reset_request', {
                email: email
            });
        } catch (error) {
            errorEl.style.display = 'block';
            errorEl.style.color = 'var(--error)';
            
            let errorMessage;
            switch (error.code) {
                case 'auth/user-not-found':
                    errorMessage = {
                        fr: "Aucun compte avec cet email",
                        en: "No account with this email",
                        ar: "لا يوجد حساب بهذا البريد الإلكتروني",
                        pt: "Nenhuma conta com este e-mail",
                        tr: "Bu e-postayla hesap bulunamadı"
                    };
                    break;
                default:
                    errorMessage = {
                        fr: "Erreur lors de l'envoi de l'email",
                        en: "Error sending email",
                        ar: "خطأ في إرسال البريد الإلكتروني",
                        pt: "Erro ao enviar e-mail",
                        tr: "E-posta gönderilirken hata"
                    };
            }
            
            errorEl.textContent = errorMessage[lang];
        }
    });
}

// Initialisation
async function init() {
    // Configurer les écouteurs d'événements
    DOM.platformTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            setActivePlatform(tab.getAttribute('data-platform'));
        });
    });

    Object.entries(DOM.langButtons).forEach(([lang, btn]) => {
        if (btn) btn.addEventListener('click', () => setLanguage(lang));
    });

    DOM.windowsDownloadBtn?.addEventListener('click', registerDownload);
    DOM.macosDownloadBtn?.addEventListener('click', registerDownload);
    DOM.ubuntuDownloadBtn?.addEventListener('click', registerDownload);

    // Gérer plusieurs boutons de notes de version (un par langue)
    document.querySelectorAll('#release-notes-btn').forEach(btn => {
        btn.addEventListener('click', showReleaseNotes);
    });

    DOM.closeModalBtns.forEach(btn => {
        if (btn) btn.addEventListener('click', closeModal);
    });

    window.addEventListener('click', (e) => {
        if (e.target === DOM.releaseNotesModal || e.target === DOM.helpModal) closeModal();
    });

    // Configurer le slider de témoignages
    if (DOM.testimonialSlider) {
        DOM.testimonialSlider.addEventListener('mouseenter', stopSlider);
        DOM.testimonialSlider.addEventListener('mouseleave', startSlider);
    }

    DOM.sliderDots.forEach((dot, index) => {
        if (dot) dot.addEventListener('click', () => {
            goToSlide(index);
        });
    });

    // Configurer le bouton d'aide
    DOM.helpButton?.addEventListener('click', showHelp);

    startSlider();

    // Configurer le partage social
    setupSocialSharing();
    
    // Configurer les boutons d'extension
    setupExtensionButtons();

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
        updateUIWithRelease({ version: currentVersion, downloadUrls, fileSizes, notes: releaseNotes });
    }

    // Envoyer l'événement d'analyse de page vue
    analytics.logEvent('page_view', {
        page_title: 'Download Page',
        page_location: window.location.href,
        user_language: localStorage.getItem('leopardo_lang') || navigator.language
    });

    setupAuth();
}

// Démarrer l'application
document.addEventListener('DOMContentLoaded', init);