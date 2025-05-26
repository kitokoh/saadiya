// Configuration Firebase
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.0.0/firebase-app.js";
import { getFirestore, collection, addDoc } from "https://www.gstatic.com/firebasejs/9.0.0/firebase-firestore.js";

const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "your-project.firebaseapp.com",
    projectId: "your-project",
    storageBucket: "your-project.appspot.com",
    messagingSenderId: "123456789",
    appId: "1:123456789:web:abcdef123456"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// Gestion du formulaire
const form = document.getElementById('marketingForm');
const steps = document.querySelectorAll('.form-step');
const prevBtn = document.querySelector('.btn-prev');
const nextBtn = document.querySelector('.btn-next');
const submitBtn = document.querySelector('.btn-submit');
const progress = document.getElementById('progress');

let currentStep = 0;

// Navigation entre les étapes
nextBtn.addEventListener('click', () => {
    if (currentStep < steps.length - 1) {
        steps[currentStep].classList.remove('active');
        currentStep++;
        steps[currentStep].classList.add('active');
        updateProgress();
        updateButtons();
    }
});

prevBtn.addEventListener('click', () => {
    if (currentStep > 0) {
        steps[currentStep].classList.remove('active');
        currentStep--;
        steps[currentStep].classList.add('active');
        updateProgress();
        updateButtons();
    }
});

function updateProgress() {
    const progressPercent = (currentStep / (steps.length - 1)) * 100;
    progress.style.width = `${progressPercent}%`;
    
    document.querySelectorAll('.step').forEach((step, index) => {
        if (index <= currentStep) {
            step.classList.add('active');
        } else {
            step.classList.remove('active');
        }
    });
}

function updateButtons() {
    if (currentStep === 0) {
        prevBtn.disabled = true;
    } else {
        prevBtn.disabled = false;
    }
    
    if (currentStep === steps.length - 1) {
        nextBtn.style.display = 'none';
        submitBtn.style.display = 'block';
    } else {
        nextBtn.style.display = 'block';
        submitBtn.style.display = 'none';
    }
}

// Gestion de la soumission
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        company: {
            name: document.getElementById('companyName').value,
            // Récupérer tous les autres champs...
        },
        // Autres données...
        createdAt: new Date(),
        status: 'pending'
    };
    
    try {
        const docRef = await addDoc(collection(db, "marketing_orders"), formData);
        alert('Votre demande a été envoyée avec succès!');
        form.reset();
    } catch (error) {
        console.error("Erreur lors de l'envoi: ", error);
        alert('Une erreur est survenue. Veuillez réessayer.');
    }
});

// Internationalisation (i18n)
const translations = {
    fr: {
        step1_title: "Informations sur votre entreprise",
        company_name: "Nom de l'entreprise",
        prev: "Précédent",
        next: "Suivant",
        submit: "Envoyer ma demande"
    },
    en: {
        step1_title: "Company Information",
        company_name: "Company Name",
        prev: "Previous",
        next: "Next",
        submit: "Submit My Request"
    },
    es: {
        step1_title: "Información de la empresa",
        company_name: "Nombre de la empresa",
        prev: "Anterior",
        next: "Siguiente",
        submit: "Enviar mi solicitud"
    }
};

document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const lang = btn.dataset.lang;
        document.documentElement.lang = lang;
        
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            el.textContent = translations[lang][key];
        });
        
        document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    });
});

// Initialisation
updateButtons();