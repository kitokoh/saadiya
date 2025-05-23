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

// Initialisation Firebase
firebase.initializeApp(firebaseConfig);
const database = firebase.database();

// Configuration Toastr
toastr.options = {
  closeButton: true,
  progressBar: true,
  positionClass: "toast-bottom-right",
  preventDuplicates: true,
  showDuration: 300,
  hideDuration: 1000,
  timeOut: 5000,
  extendedTimeOut: 1000,
  showEasing: "swing",
  hideEasing: "linear",
  showMethod: "fadeIn",
  hideMethod: "fadeOut"
};

// Traductions améliorées avec plus de clés
const translations = {
  fr: {
    contact_management: "Gestion des Contacts",
    statistics: "Statistiques",
    total_contacts: "Total Contacts",
    import_contacts: "Importer des contacts",
    preview: "Prévisualiser",
    category: "Catégorie :",
    category_clients: "Clients",
    category_prospects: "Prospects",
    category_suppliers: "Fournisseurs",
    category_staff: "Personnel",
    data_preview: "Aperçu des données",
    select_columns: "Sélectionnez les colonnes à afficher :",
    import_contacts_button: "Importer les contacts",
    search_placeholder: "Rechercher...",
    column_name: "Nom",
    column_email: "Email",
    column_phone: "Téléphone",
    column_company: "Entreprise",
    column_category: "Catégorie",
    column_actions: "Actions",
    column_notes: "Notes",
    loading: "Chargement...",
    edit_contact: "Modifier le contact",
    add_contact: "Ajouter un contact",
    full_name: "Nom complet",
    email: "Email",
    phone: "Téléphone",
    company: "Entreprise",
    notes: "Notes",
    cancel: "Annuler",
    save: "Enregistrer",
    delete: "Supprimer",
    language_french: "Français",
    language_english: "English",
    language_arabic: "العربية",
    confirm_import_title: "Confirmer l'importation",
    confirm_import_message: "Vous êtes sur le point d'importer {count} contacts dans la catégorie \"{category}\".",
    confirm: "Confirmer",
    import_success: "{count} contacts importés avec succès !",
    import_error: "Erreur lors de l'importation : {error}",
    delete_confirm: "Voulez-vous vraiment supprimer ce contact ?",
    delete_success: "Contact supprimé avec succès",
    save_success: "Contact enregistré avec succès",
    file_error: "Erreur de fichier : {error}",
    no_file: "Aucun fichier sélectionné",
    no_contacts: "Aucun contact valide trouvé",
    all_contacts: "Tous les contacts",
    export_contacts: "Exporter les contacts",
    export_format: "Format d'export",
    export_columns: "Colonnes à exporter",
    export_category: "Catégorie",
    export: "Exporter",
    export_success: "Exportation réussie",
    export_error: "Erreur lors de l'export : {error}",
    add_success: "Contact ajouté avec succès",
    add_error: "Erreur lors de l'ajout : {error}",
    validation_name_required: "Le nom est requis",
    validation_email_invalid: "Email invalide",
    stats_total: "Total",
    stats_clients: "Clients",
    stats_prospects: "Prospects",
    stats_fournisseurs: "Fournisseurs",
    stats_personnel: "Personnel",
    no_data: "Aucune donnée disponible",
    last_updated: "Dernière mise à jour",
    created_at: "Créé le",
    import_date: "Date d'importation",
    select_all: "Tout sélectionner",
    deselect_all: "Tout désélectionner",
    file_type_csv: "Fichier CSV",
    file_type_excel: "Fichier Excel",
    file_type_vcf: "Fichier vCard",
    file_type_json: "Fichier JSON"
  },
  en: {
    contact_management: "Contact Management",
    statistics: "Statistics",
    total_contacts: "Total Contacts",
    import_contacts: "Import Contacts",
    preview: "Preview",
    category: "Category:",
    category_clients: "Clients",
    category_prospects: "Prospects",
    category_suppliers: "Suppliers",
    category_staff: "Staff",
    data_preview: "Data Preview",
    select_columns: "Select columns to display:",
    import_contacts_button: "Import Contacts",
    search_placeholder: "Search...",
    column_name: "Name",
    column_email: "Email",
    column_phone: "Phone",
    column_company: "Company",
    column_category: "Category",
    column_actions: "Actions",
    column_notes: "Notes",
    loading: "Loading...",
    edit_contact: "Edit Contact",
    add_contact: "Add Contact",
    full_name: "Full Name",
    email: "Email",
    phone: "Phone",
    company: "Company",
    notes: "Notes",
    cancel: "Cancel",
    save: "Save",
    delete: "Delete",
    language_french: "French",
    language_english: "English",
    language_arabic: "Arabic",
    confirm_import_title: "Confirm Import",
    confirm_import_message: "You are about to import {count} contacts into the \"{category}\" category.",
    confirm: "Confirm",
    import_success: "Successfully imported {count} contacts!",
    import_error: "Import error: {error}",
    delete_confirm: "Are you sure you want to delete this contact?",
    delete_success: "Contact deleted successfully",
    save_success: "Contact saved successfully",
    file_error: "File error: {error}",
    no_file: "No file selected",
    no_contacts: "No valid contacts found",
    all_contacts: "All Contacts",
    export_contacts: "Export Contacts",
    export_format: "Export Format",
    export_columns: "Columns to export",
    export_category: "Category",
    export: "Export",
    export_success: "Export successful",
    export_error: "Export error: {error}",
    add_success: "Contact added successfully",
    add_error: "Error adding contact: {error}",
    validation_name_required: "Name is required",
    validation_email_invalid: "Invalid email",
    stats_total: "Total",
    stats_clients: "Clients",
    stats_prospects: "Prospects",
    stats_fournisseurs: "Suppliers",
    stats_personnel: "Staff",
    no_data: "No data available",
    last_updated: "Last updated",
    created_at: "Created at",
    import_date: "Import date",
    select_all: "Select all",
    deselect_all: "Deselect all",
    file_type_csv: "CSV file",
    file_type_excel: "Excel file",
    file_type_vcf: "vCard file",
    file_type_json: "JSON file"
  },
  ar: {
    contact_management: "إدارة الاتصالات",
    statistics: "إحصائيات",
    total_contacts: "إجمالي جهات الاتصال",
    import_contacts: "استيراد جهات الاتصال",
    preview: "معاينة",
    category: "الفئة:",
    category_clients: "العملاء",
    category_prospects: "الزبائن المحتملين",
    category_suppliers: "الموردين",
    category_staff: "الموظفين",
    data_preview: "معاينة البيانات",
    select_columns: "حدد الأعمدة لعرضها:",
    import_contacts_button: "استيراد جهات الاتصال",
    search_placeholder: "بحث...",
    column_name: "الاسم",
    column_email: "البريد الإلكتروني",
    column_phone: "الهاتف",
    column_company: "الشركة",
    column_category: "الفئة",
    column_actions: "الإجراءات",
    column_notes: "ملاحظات",
    loading: "جار التحميل...",
    edit_contact: "تعديل جهة الاتصال",
    add_contact: "إضافة جهة اتصال",
    full_name: "الاسم الكامل",
    email: "البريد الإلكتروني",
    phone: "الهاتف",
    company: "الشركة",
    notes: "ملاحظات",
    cancel: "إلغاء",
    save: "حفظ",
    delete: "حذف",
    language_french: "الفرنسية",
    language_english: "الإنجليزية",
    language_arabic: "العربية",
    confirm_import_title: "تأكيد الاستيراد",
    confirm_import_message: "أنت على وشك استيراد {count} جهات اتصال إلى فئة \"{category}\".",
    confirm: "تأكيد",
    import_success: "تم استيراد {count} جهات اتصال بنجاح!",
    import_error: "خطأ في الاستيراد: {error}",
    delete_confirm: "هل أنت متأكد أنك تريد حذف جهة الاتصال هذه؟",
    delete_success: "تم حذف جهة الاتصال بنجاح",
    save_success: "تم حفظ جهة الاتصال بنجاح",
    file_error: "خطأ في الملف: {error}",
    no_file: "لم يتم اختيار ملف",
    no_contacts: "لم يتم العثور على جهات اتصال صالحة",
    all_contacts: "كل جهات الاتصال",
    export_contacts: "تصدير جهات الاتصال",
    export_format: "تنسيق التصدير",
    export_columns: "الأعمدة للتصدير",
    export_category: "الفئة",
    export: "تصدير",
    export_success: "تم التصدير بنجاح",
    export_error: "خطأ في التصدير: {error}",
    add_success: "تمت إضافة جهة الاتصال بنجاح",
    add_error: "خطأ في الإضافة: {error}",
    validation_name_required: "الاسم مطلوب",
    validation_email_invalid: "بريد إلكتروني غير صالح",
    stats_total: "الإجمالي",
    stats_clients: "العملاء",
    stats_prospects: "الزبائن المحتملين",
    stats_fournisseurs: "الموردين",
    stats_personnel: "الموظفين",
    no_data: "لا توجد بيانات متاحة",
    last_updated: "آخر تحديث",
    created_at: "تم الإنشاء في",
    import_date: "تاريخ الاستيراد",
    select_all: "تحديد الكل",
    deselect_all: "إلغاء تحديد الكل",
    file_type_csv: "ملف CSV",
    file_type_excel: "ملف Excel",
    file_type_vcf: "ملف vCard",
    file_type_json: "ملف JSON"
  }
};

// État de l'application amélioré avec plus de propriétés
const state = {
  currentLanguage: 'fr',
  contactsToImport: [],
  allContacts: [],
  filteredContacts: [],
  selectedColumns: ['name', 'email', 'phone', 'company', 'category'],
  currentCategory: 'all',
  currentPage: 1,
  contactsPerPage: 10,
  stats: {
    total: 0,
    clients: 0,
    prospects: 0,
    fournisseurs: 0,
    personnel: 0
  },
  sortConfig: {
    key: null,
    direction: 'ascending'
  }
};

// Initialisation améliorée avec gestion des erreurs
document.addEventListener('DOMContentLoaded', () => {
  try {
    initLanguage();
    setupEventListeners();
    loadContactsFromFirebase();
    
    // Vérifie la connexion Firebase
    const databaseRef = database.ref('.info/connected');
    databaseRef.on('value', (snapshot) => {
      if (snapshot.val() === false) {
        showAlert('error', translate('firebase_connection_error'));
      }
    });
  } catch (error) {
    console.error('Initialization error:', error);
    showAlert('error', translate('initialization_error', { error: error.message }));
  }
});

/* ==================== FONCTIONS UTILITAIRES AMÉLIORÉES ==================== */

function translate(key, params = {}) {
  let translation = translations[state.currentLanguage][key] || key;
  
  // Remplace les paramètres dans la traduction
  Object.keys(params).forEach(param => {
    translation = translation.replace(new RegExp(`\\{${param}\\}`, 'g'), params[param]);
  });
  
  return translation;
}

function showLoading(message = '') {
  const overlay = document.getElementById('loadingOverlay');
  document.getElementById('loadingText').textContent = message || translate('loading');
  overlay.style.display = 'flex';
}

function hideLoading() {
  document.getElementById('loadingOverlay').style.display = 'none';
}

function showAlert(type, message) {
  toastr[type](message);
}

function showConfirmationDialog(title, message) {
  return new Promise((resolve) => {
    document.getElementById('confirmTitle').innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${title}`;
    document.getElementById('confirmMessage').textContent = message;
    
    const modal = document.getElementById('confirmModal');
    modal.style.display = 'flex';
    
    const confirmAction = () => {
      modal.style.display = 'none';
      document.getElementById('confirmAction').removeEventListener('click', confirmAction);
      document.getElementById('cancelConfirm').removeEventListener('click', cancelAction);
      resolve(true);
    };
    
    const cancelAction = () => {
      modal.style.display = 'none';
      document.getElementById('confirmAction').removeEventListener('click', confirmAction);
      document.getElementById('cancelConfirm').removeEventListener('click', cancelAction);
      resolve(false);
    };
    
    document.getElementById('confirmAction').addEventListener('click', confirmAction);
    document.getElementById('cancelConfirm').addEventListener('click', cancelAction);
    document.getElementById('closeConfirmModal').addEventListener('click', cancelAction);
  });
}

function formatDate(dateString) {
  if (!dateString) return '-';
  
  const date = new Date(dateString);
  return date.toLocaleDateString(state.currentLanguage, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

function generateId() {
  return 'contact_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function validateEmail(email) {
  if (!email) return true; // Email est optionnel
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(String(email).toLowerCase());
}

function validateContact(contact) {
  if (!contact.name || contact.name.trim() === '') {
    throw new Error(translate('validation_name_required'));
  }
  
  if (!validateEmail(contact.email)) {
    throw new Error(translate('validation_email_invalid'));
  }
  
  return true;
}

/* ==================== GESTION DE L'INTERFACE AMÉLIORÉE ==================== */

function initLanguage() {
  try {
    // Récupère la langue sauvegardée ou détecte la langue du navigateur
    const savedLang = localStorage.getItem('leopardo_lang');
    const browserLang = navigator.language.split('-')[0];
    const defaultLang = ['fr', 'en', 'ar'].includes(browserLang) ? browserLang : 'fr';
    
    setLanguage(savedLang || defaultLang);
  } catch (error) {
    console.error('Language initialization error:', error);
    setLanguage('fr'); // Fallback to French
  }
}

function setLanguage(lang) {
  state.currentLanguage = lang;
  localStorage.setItem('leopardo_lang', lang);
  
  // Met à jour le sélecteur de langue
  document.getElementById('current-lang-flag').textContent = 
    lang === 'fr' ? '🇫🇷' : lang === 'en' ? '🇬🇧' : '🇸🇦';
  document.getElementById('current-lang-name').textContent = 
    translations[lang].language_french;
  
  // Traduit tous les éléments
  document.querySelectorAll('[data-translate]').forEach(el => {
    const key = el.getAttribute('data-translate');
    el.textContent = translate(key);
  });
  
  // Traduit les placeholders
  document.querySelectorAll('[data-translate-ph]').forEach(el => {
    const key = el.getAttribute('data-translate-ph');
    el.placeholder = translate(key);
  });
  
  // Recharge les données si nécessaire
  if (state.allContacts.length > 0) {
    renderContactTable(state.filteredContacts);
    renderStats();
  }
}

function setupEventListeners() {
  try {
    // Langue
    document.querySelectorAll('.lang-option').forEach(option => {
      option.addEventListener('click', () => {
        setLanguage(option.dataset.lang);
        document.getElementById('langDropdown').style.display = 'none';
      });
    });
    
    document.getElementById('lang-current').addEventListener('click', (e) => {
      e.stopPropagation();
      const dropdown = document.getElementById('langDropdown');
      dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
    });

    document.addEventListener('click', (e) => {
      if (!e.target.closest('.language-selector')) {
        document.getElementById('langDropdown').style.display = 'none';
      }
    });

    // Fichier
    document.getElementById('previewBtn').addEventListener('click', handlePreview);
    document.getElementById('importBtn').addEventListener('click', handleImport);
    document.getElementById('searchInput').addEventListener('input', handleSearch);
    
    // Modal
    document.getElementById('closeEditModal').addEventListener('click', closeEditModal);
    document.getElementById('cancelEdit').addEventListener('click', closeEditModal);
    document.getElementById('editForm').addEventListener('submit', handleEditSubmit);
    
    document.getElementById('closeAddModal').addEventListener('click', closeAddModal);
    document.getElementById('cancelAdd').addEventListener('click', closeAddModal);
    document.getElementById('addForm').addEventListener('submit', handleAddSubmit);
    
    document.getElementById('closeExportModal').addEventListener('click', closeExportModal);
    document.getElementById('cancelExport').addEventListener('click', closeExportModal);
    document.getElementById('exportForm').addEventListener('submit', handleExportSubmit);
    
    // Boutons
    document.getElementById('addContactBtn').addEventListener('click', openAddModal);
    document.getElementById('exportBtn').addEventListener('click', openExportModal);
    
    // Onglets
    document.querySelectorAll('.tab').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        state.currentCategory = tab.dataset.category;
        filterContacts();
      });
    });

    // Tri des colonnes
    document.querySelectorAll('#contactTable th').forEach(header => {
      if (header.getAttribute('data-sortable') !== 'false') {
        header.addEventListener('click', () => {
          const key = header.getAttribute('data-column');
          if (key) {
            requestSort(key);
          }
        });
      }
    });
  } catch (error) {
    console.error('Event listeners setup error:', error);
    showAlert('error', translate('ui_error', { error: error.message }));
  }
}

function requestSort(key) {
  let direction = 'ascending';
  if (state.sortConfig.key === key && state.sortConfig.direction === 'ascending') {
    direction = 'descending';
  }
  state.sortConfig = { key, direction };
  sortContacts();
}

function sortContacts() {
  if (!state.sortConfig.key) return;

  state.filteredContacts.sort((a, b) => {
    const aValue = a[state.sortConfig.key] || '';
    const bValue = b[state.sortConfig.key] || '';
    
    if (aValue < bValue) {
      return state.sortConfig.direction === 'ascending' ? -1 : 1;
    }
    if (aValue > bValue) {
      return state.sortConfig.direction === 'ascending' ? 1 : -1;
    }
    return 0;
  });

  renderContactTable(state.filteredContacts);
}

/* ==================== GESTION DES CONTACTS AMÉLIORÉE ==================== */

async function loadContactsFromFirebase() {
  showLoading();
  
  try {
    const snapshot = await database.ref('contacts').once('value');
    state.allContacts = [];
    state.stats = { total: 0, clients: 0, prospects: 0, fournisseurs: 0, personnel: 0 };
    
    snapshot.forEach((categorySnapshot) => {
      categorySnapshot.forEach((contactSnapshot) => {
        const contact = {
          id: contactSnapshot.key,
          category: categorySnapshot.key,
          ...contactSnapshot.val()
        };
        
        state.allContacts.push(contact);
        
        // Mise à jour des statistiques
        state.stats.total++;
        if (state.stats[categorySnapshot.key] !== undefined) {
          state.stats[categorySnapshot.key]++;
        }
      });
    });
    
    filterContacts();
    renderStats();
  } catch (error) {
    console.error('Firebase load error:', error);
    showAlert('error', `Firebase error: ${error.message}`);
  } finally {
    hideLoading();
  }
}

function filterContacts() {
  const searchTerm = document.getElementById('searchInput').value.toLowerCase();
  
  state.filteredContacts = state.allContacts.filter(contact => {
    // Filtre par catégorie
    if (state.currentCategory !== 'all' && contact.category !== state.currentCategory) {
      return false;
    }
    
    // Filtre par recherche
    if (!searchTerm) return true;
    
    return (
      (contact.name && contact.name.toLowerCase().includes(searchTerm)) ||
      (contact.email && contact.email.toLowerCase().includes(searchTerm)) ||
      (contact.phone && contact.phone.toLowerCase().includes(searchTerm)) ||
      (contact.company && contact.company.toLowerCase().includes(searchTerm)) ||
      (contact.notes && contact.notes.toLowerCase().includes(searchTerm))
    );
  });
  
  state.currentPage = 1; // Réinitialise la pagination
  sortContacts(); // Applique le tri actuel
  renderPagination();
}

function renderStats() {
  const statsContainer = document.getElementById('statsContainer');
  
  statsContainer.innerHTML = `
    <div class="stat-card stat-total">
      <div class="stat-icon"><i class="fas fa-users"></i></div>
      <div class="stat-title">${translate('stats_total')}</div>
      <div class="stat-value">${state.stats.total}</div>
    </div>
    <div class="stat-card stat-clients">
      <div class="stat-icon"><i class="fas fa-user-tie"></i></div>
      <div class="stat-title">${translate('category_clients')}</div>
      <div class="stat-value">${state.stats.clients}</div>
    </div>
    <div class="stat-card stat-prospects">
      <div class="stat-icon"><i class="fas fa-handshake"></i></div>
      <div class="stat-title">${translate('category_prospects')}</div>
      <div class="stat-value">${state.stats.prospects}</div>
    </div>
    <div class="stat-card stat-fournisseurs">
      <div class="stat-icon"><i class="fas fa-truck"></i></div>
      <div class="stat-title">${translate('category_suppliers')}</div>
      <div class="stat-value">${state.stats.fournisseurs}</div>
    </div>
    <div class="stat-card stat-personnel">
      <div class="stat-icon"><i class="fas fa-id-card"></i></div>
      <div class="stat-title">${translate('category_staff')}</div>
      <div class="stat-value">${state.stats.personnel}</div>
    </div>
  `;
}

function renderContactTable(contacts) {
  const tbody = document.getElementById('contactTable').querySelector('tbody');
  
  if (contacts.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="6" class="empty-state">
          <i class="fas fa-inbox"></i>
          <p>${translate('no_data')}</p>
        </td>
      </tr>
    `;
    document.getElementById('pagination').innerHTML = '';
    return;
  }
  
  // Pagination
  const startIndex = (state.currentPage - 1) * state.contactsPerPage;
  const paginatedContacts = contacts.slice(startIndex, startIndex + state.contactsPerPage);
  
  tbody.innerHTML = paginatedContacts.map(contact => `
    <tr>
      <td>${contact.name || '-'}</td>
      <td>${contact.email || '-'}</td>
      <td>${contact.phone || '-'}</td>
      <td>${contact.company || '-'}</td>
      <td><span class="category-tag tag-${contact.category}">${translate(`category_${contact.category}`)}</span></td>
      <td class="actions">
        <button class="btn btn-icon edit-btn" data-id="${contact.id}" data-category="${contact.category}">
          <i class="fas fa-edit"></i>
        </button>
        <button class="btn btn-icon delete-btn" data-id="${contact.id}" data-category="${contact.category}">
          <i class="fas fa-trash"></i>
        </button>
      </td>
    </tr>
  `).join('');

  // Ajout des écouteurs
  document.querySelectorAll('.edit-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const contact = state.allContacts.find(c => 
        c.id === btn.dataset.id && c.category === btn.dataset.category
      );
      if (contact) openEditModal(contact);
    });
  });

  document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      confirmDeleteContact(btn.dataset.id, btn.dataset.category);
    });
  });
  
  renderPagination();
}

function renderPagination() {
  const totalPages = Math.ceil(state.filteredContacts.length / state.contactsPerPage);
  const pagination = document.getElementById('pagination');
  
  if (totalPages <= 1) {
    pagination.innerHTML = '';
    return;
  }
  
  let html = '';
  const maxVisiblePages = 5;
  let startPage = Math.max(1, state.currentPage - Math.floor(maxVisiblePages / 2));
  let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
  
  if (endPage - startPage + 1 < maxVisiblePages) {
    startPage = Math.max(1, endPage - maxVisiblePages + 1);
  }
  
  // Bouton Précédent
  html += `
    <li class="page-item">
      <a class="page-link ${state.currentPage === 1 ? 'disabled' : ''}" 
         href="#" data-page="${state.currentPage - 1}">
        <i class="fas fa-chevron-left"></i>
      </a>
    </li>
  `;
  
  // Première page
  if (startPage > 1) {
    html += `
      <li class="page-item">
        <a class="page-link" href="#" data-page="1">1</a>
      </li>
      ${startPage > 2 ? '<li class="page-item disabled"><span class="page-link">...</span></li>' : ''}
    `;
  }
  
  // Pages visibles
  for (let i = startPage; i <= endPage; i++) {
    html += `
      <li class="page-item">
        <a class="page-link ${i === state.currentPage ? 'active' : ''}" 
           href="#" data-page="${i}">${i}</a>
      </li>
    `;
  }
  
  // Dernière page
  if (endPage < totalPages) {
    html += `
      ${endPage < totalPages - 1 ? '<li class="page-item disabled"><span class="page-link">...</span></li>' : ''}
      <li class="page-item">
        <a class="page-link" href="#" data-page="${totalPages}">${totalPages}</a>
      </li>
    `;
  }
  
  // Bouton Suivant
  html += `
    <li class="page-item">
      <a class="page-link ${state.currentPage === totalPages ? 'disabled' : ''}" 
         href="#" data-page="${state.currentPage + 1}">
        <i class="fas fa-chevron-right"></i>
      </a>
    </li>
  `;
  
  pagination.innerHTML = html;
  
  // Ajout des écouteurs
  document.querySelectorAll('.page-link:not(.disabled)').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      state.currentPage = parseInt(link.dataset.page);
      renderContactTable(state.filteredContacts);
    });
  });
}

/* ==================== IMPORT/EXPORT AMÉLIORÉ ==================== */

async function handlePreview() {
  try {
    showLoading(translate('loading'));
    
    const file = document.getElementById('contactFile').files[0];
    if (!file) throw new Error(translate('no_file'));
    
    state.contactsToImport = await parseContactFile(file);
    if (state.contactsToImport.length === 0) throw new Error(translate('no_contacts'));
    
    generateColumnCheckboxes(state.contactsToImport[0]);
    renderPreviewTable();
    document.getElementById('previewContainer').style.display = 'block';
  } catch (error) {
    console.error('Preview error:', error);
    showAlert('error', translate('file_error', { error: error.message }));
  } finally {
    hideLoading();
  }
}

async function handleImport() {
  try {
    if (state.contactsToImport.length === 0) {
      throw new Error(translate('no_contacts'));
    }
    
    // Validation des contacts
    const validContacts = [];
    const invalidContacts = [];
    
    state.contactsToImport.forEach(contact => {
      try {
        validateContact(contact);
        validContacts.push(contact);
      } catch (error) {
        invalidContacts.push({ contact, error: error.message });
      }
    });
    
    if (validContacts.length === 0) {
      throw new Error(translate('no_contacts'));
    }
    
    if (invalidContacts.length > 0) {
      console.warn('Invalid contacts:', invalidContacts);
    }
    
    const category = document.getElementById('categorySelect').value;
    const confirmed = await showConfirmationDialog(
      translate('confirm_import_title'),
      translate('confirm_import_message', {
        count: validContacts.length,
        category: translate(`category_${category}`)
      })
    );
    
    if (!confirmed) return;
    
    showLoading(translate('loading'));
    await importContactsToFirebase(validContacts, category);
    
    showAlert('success', translate('import_success', { count: validContacts.length }));
    resetImportForm();
    loadContactsFromFirebase();
  } catch (error) {
    console.error('Import error:', error);
    showAlert('error', translate('import_error', { error: error.message }));
  } finally {
    hideLoading();
  }
}

async function parseContactFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = async (e) => {
      try {
        const content = e.target.result;
        const extension = file.name.split('.').pop().toLowerCase();
        
        let contacts = [];
        if (extension === 'csv') {
          contacts = parseCSV(content);
        } else if (extension === 'vcf') {
          contacts = parseVCF(content);
        } else if (extension === 'xlsx' || extension === 'xls') {
          contacts = await parseExcel(content);
        } else if (extension === 'json') {
          contacts = parseJSON(content);
        } else {
          throw new Error(translate('file_error', { error: "Format de fichier non supporté" }));
        }
        
        if (contacts.length === 0) throw new Error(translate('no_contacts'));
        resolve(contacts);
      } catch (error) {
        reject(error);
      }
    };
    reader.onerror = () => reject(new Error(translate('file_error', { error: "Erreur de lecture du fichier" })));
    reader.readAsText(file);
  });
}

function parseCSV(csvData) {
  const lines = csvData.split('\n').filter(line => line.trim() !== '');
  if (lines.length < 2) return [];
  
  const headers = lines[0].split(',').map(h => safeParse(h).toLowerCase().trim());
  const contacts = [];
  
  for (let i = 1; i < lines.length; i++) {
    try {
      const values = splitCSVLine(lines[i]);
      const contact = {};
      
      headers.forEach((header, index) => {
        contact[header] = index < values.length ? safeParse(values[index]) : '';
      });
      
      const formattedContact = formatContact(contact);
      if (formattedContact.name || formattedContact.email) {
        contacts.push(formattedContact);
      }
    } catch (error) {
      console.warn(`Error parsing line ${i + 1}:`, error);
    }
  }
  
  return contacts;
}

async function parseExcel(content) {
  const workbook = XLSX.read(content, { type: 'binary' });
  const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
  const jsonData = XLSX.utils.sheet_to_json(firstSheet, { header: 1 });
  
  if (jsonData.length < 2) return [];
  
  const headers = jsonData[0].map(h => safeParse(h).toLowerCase().trim());
  const contacts = [];
  
  for (let i = 1; i < jsonData.length; i++) {
    try {
      const row = jsonData[i];
      const contact = {};
      
      headers.forEach((header, index) => {
        contact[header] = index < row.length ? safeParse(row[index]) : '';
      });
      
      const formattedContact = formatContact(contact);
      if (formattedContact.name || formattedContact.email) {
        contacts.push(formattedContact);
      }
    } catch (error) {
      console.warn(`Error parsing row ${i + 1}:`, error);
    }
  }
  
  return contacts;
}

function parseVCF(vcfData) {
  const contacts = [];
  const vcfEntries = vcfData.split('BEGIN:VCARD');
  
  for (const entry of vcfEntries) {
    if (!entry.trim()) continue;
    
    try {
      const contact = {};
      const lines = entry.split('\n');
      
      for (const line of lines) {
        if (line.startsWith('FN:')) {
          contact.name = line.substring(3).trim();
        } else if (line.startsWith('EMAIL;') || line.startsWith('EMAIL:')) {
          const email = line.split(':')[1];
          if (email) contact.email = email.trim().toLowerCase();
        } else if (line.startsWith('TEL;') || line.startsWith('TEL:')) {
          const phone = line.split(':')[1];
          if (phone) contact.phone = phone.replace(/[^\d+]/g, '').trim();
        } else if (line.startsWith('ORG:')) {
          const company = line.substring(4);
          if (company) contact.company = company.trim();
        } else if (line.startsWith('NOTE:')) {
          const notes = line.substring(5);
          if (notes) contact.notes = notes.trim();
        }
      }
      
      if (contact.name || contact.email) {
        contacts.push(formatContact(contact));
      }
    } catch (error) {
      console.warn('Error parsing vCard:', error);
    }
  }
  
  return contacts;
}

function parseJSON(jsonData) {
  try {
    const data = JSON.parse(jsonData);
    if (!Array.isArray(data)) return [];
    
    return data.map(contact => formatContact(contact))
               .filter(contact => contact.name || contact.email);
  } catch (error) {
    throw new Error(translate('file_error', { error: "JSON invalide" }));
  }
}

function splitCSVLine(line) {
  // Gère les virgules à l'intérieur des guillemets
  const result = [];
  let inQuotes = false;
  let currentField = '';
  
  for (let i = 0; i < line.length; i++) {
    const char = line[i];
    
    if (char === '"') {
      inQuotes = !inQuotes;
    } else if (char === ',' && !inQuotes) {
      result.push(currentField);
      currentField = '';
    } else {
      currentField += char;
    }
  }
  
  result.push(currentField);
  return result;
}

function safeParse(str) {
  if (typeof str !== 'string') return str || '';
  
  return str
    .trim()
    .replace(/^"|"$/g, '') // Enlève les guillemets d'encadrement
    .replace(/""/g, '"') // Convertit les guillemets doubles
    .replace(/[\\\n\r\t]/g, '') // Enlève les caractères d'échappement
    .trim();
}

function formatContact(rawContact) {
  return {
    id: generateId(),
    name: buildName(rawContact),
    email: buildEmail(rawContact),
    phone: buildPhone(rawContact),
    company: buildCompany(rawContact),
    notes: rawContact.notes || rawContact.remarques || rawContact.comment || '',
    category: document.getElementById('categorySelect').value,
    importedAt: new Date().toISOString()
  };
}

function buildName(contact) {
  const nameParts = [
    contact['first name'] || contact.prenom || contact['prénom'] || '',
    contact['middle name'] || contact['second name'] || '',
    contact['last name'] || contact.nom || contact.name || ''
  ].filter(part => part.trim() !== '');

  return nameParts.join(' ').trim() || contact.name || contact.nom || '';
}

function buildEmail(contact) {
  const email = contact.email || contact['e-mail'] || contact['e-mail 1 - value'] || contact.mail || '';
  return email.toLowerCase().trim();
}

function buildPhone(contact) {
  const phone = contact.phone || contact.tel || contact['phone 1 - value'] || contact.telephone || contact.mobile || '';
  return phone.replace(/[^\d+]/g, '').trim();
}

function buildCompany(contact) {
  return contact.company || contact['organization name'] || contact.organisation || contact.societe || contact.employer || '';
}

async function importContactsToFirebase(contacts, category) {
  const batchUpdate = {};
  const timestamp = firebase.database.ServerValue.TIMESTAMP;

  contacts.forEach(contact => {
    contact.category = category;
    contact.importedAt = timestamp;
    contact.lastUpdated = timestamp;
    batchUpdate[`contacts/${category}/${contact.id}`] = contact;
  });

  try {
    await database.ref().update(batchUpdate);
  } catch (error) {
    throw new Error(`Firebase error: ${error.message}`);
  }
}

function resetImportForm() {
  document.getElementById('contactFile').value = '';
  document.getElementById('previewContainer').style.display = 'none';
  state.contactsToImport = [];
}

function openExportModal() {
  // Génère les cases à cocher pour les colonnes
  const exportColumns = document.getElementById('exportColumns');
  exportColumns.innerHTML = '';
  
  const columns = [
    { id: 'export_name', value: 'name', label: translate('column_name') },
    { id: 'export_email', value: 'email', label: translate('column_email') },
    { id: 'export_phone', value: 'phone', label: translate('column_phone') },
    { id: 'export_company', value: 'company', label: translate('column_company') },
    { id: 'export_category', value: 'category', label: translate('column_category') },
    { id: 'export_notes', value: 'notes', label: translate('column_notes') }
  ];
  
  columns.forEach(col => {
    const div = document.createElement('div');
    div.className = 'checkbox-item';
    div.innerHTML = `
      <input type="checkbox" id="${col.id}" value="${col.value}" checked>
      <label for="${col.id}">${col.label}</label>
    `;
    exportColumns.appendChild(div);
  });
  
  document.getElementById('exportModal').style.display = 'flex';
}

function closeExportModal() {
  document.getElementById('exportModal').style.display = 'none';
}

async function handleExportSubmit(e) {
  e.preventDefault();
  
  try {
    showLoading(translate('loading'));
    
    // Récupère les options d'export
    const format = document.querySelector('input[name="exportFormat"]:checked').value;
    const category = document.getElementById('exportCategory').value;
    const selectedColumns = Array.from(document.querySelectorAll('#exportColumns input:checked')).map(el => el.value);
    
    // Filtre les contacts
    let contactsToExport = [...state.allContacts];
    if (category !== 'all') {
      contactsToExport = contactsToExport.filter(contact => contact.category === category);
    }
    
    if (contactsToExport.length === 0) {
      throw new Error(translate('no_contacts'));
    }
    
    // Prépare les données
    const data = contactsToExport.map(contact => {
      const exportedContact = { id: contact.id };
      selectedColumns.forEach(col => {
        exportedContact[col] = contact[col] || '';
      });
      return exportedContact;
    });
    
    // Génère le fichier
    let blob, filename;
    const now = new Date().toISOString().replace(/[:.]/g, '-');
    
    switch (format) {
      case 'csv':
        filename = `contacts-${now}.csv`;
        blob = generateCSV(data, selectedColumns);
        break;
      case 'json':
        filename = `contacts-${now}.json`;
        blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        break;
      case 'xlsx':
        filename = `contacts-${now}.xlsx`;
        blob = await generateExcel(data, selectedColumns);
        break;
      case 'vcf':
        filename = `contacts-${now}.vcf`;
        blob = generateVCF(data);
        break;
      default:
        throw new Error(translate('file_error', { error: "Format non supporté" }));
    }
    
    // Télécharge le fichier
    downloadFile(blob, filename);
    showAlert('success', translate('export_success'));
    closeExportModal();
  } catch (error) {
    console.error('Export error:', error);
    showAlert('error', translate('export_error', { error: error.message }));
  } finally {
    hideLoading();
  }
}

function generateCSV(data, columns) {
  // Crée l'en-tête CSV
  const headers = columns.map(col => `"${translate(`column_${col}`)}"`).join(',');
  const rows = data.map(contact => 
    columns.map(col => `"${(contact[col] || '').toString().replace(/"/g, '""')}"`).join(',')
  );
  
  // Combine tout
  const csvContent = [headers, ...rows].join('\n');
  return new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
}

async function generateExcel(data, columns) {
  // Prépare les données pour Excel
  const headers = columns.map(col => translate(`column_${col}`));
  const rows = data.map(contact => 
    columns.map(col => contact[col] || '')
  );
  
  // Crée un workbook
  const wb = XLSX.utils.book_new();
  const ws = XLSX.utils.aoa_to_sheet([headers, ...rows]);
  XLSX.utils.book_append_sheet(wb, ws, "Contacts");
  
  // Convertit en blob
  const excelBuffer = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });
  return new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
}

function generateVCF(data) {
  const vcfEntries = data.map(contact => {
    let vcard = 'BEGIN:VCARD\nVERSION:3.0\n';
    if (contact.name) vcard += `FN:${contact.name}\n`;
    if (contact.email) vcard += `EMAIL:${contact.email}\n`;
    if (contact.phone) vcard += `TEL:${contact.phone}\n`;
    if (contact.company) vcard += `ORG:${contact.company}\n`;
    if (contact.notes) vcard += `NOTE:${contact.notes}\n`;
    vcard += 'END:VCARD\n';
    return vcard;
  });
  
  return new Blob([vcfEntries.join('\n')], { type: 'text/vcard' });
}

function downloadFile(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  setTimeout(() => {
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }, 100);
}

/* ==================== MODAL EDIT/ADD AMÉLIORÉ ==================== */

function openEditModal(contact) {
  // Remplit le formulaire
  document.getElementById('editName').value = contact.name || '';
  document.getElementById('editEmail').value = contact.email || '';
  document.getElementById('editPhone').value = contact.phone || '';
  document.getElementById('editCompany').value = contact.company || '';
  document.getElementById('editNotes').value = contact.notes || '';
  document.getElementById('editCategory').value = contact.category;
  
  // Stocke l'ID du contact à éditer
  document.getElementById('editForm').dataset.contactId = contact.id;
  document.getElementById('editForm').dataset.originalCategory = contact.category;
  
  // Ouvre le modal
  document.getElementById('editModal').style.display = 'flex';
}

function closeEditModal() {
  document.getElementById('editModal').style.display = 'none';
}

async function handleEditSubmit(e) {
  e.preventDefault();
  
  try {
    showLoading(translate('loading'));
    
    // Récupère les données du formulaire
    const contact = {
      name: document.getElementById('editName').value.trim(),
      email: document.getElementById('editEmail').value.trim(),
      phone: document.getElementById('editPhone').value.trim(),
      company: document.getElementById('editCompany').value.trim(),
      notes: document.getElementById('editNotes').value.trim(),
      category: document.getElementById('editCategory').value,
      lastUpdated: firebase.database.ServerValue.TIMESTAMP
    };
    
    // Validation
    validateContact(contact);
    
    // Récupère l'ID et l'ancienne catégorie
    const contactId = document.getElementById('editForm').dataset.contactId;
    const originalCategory = document.getElementById('editForm').dataset.originalCategory;
    
    // Prépare les mises à jour
    const updates = {};
    updates[`contacts/${contact.category}/${contactId}`] = contact;
    
    // Si la catégorie a changé, supprime l'ancienne entrée
    if (contact.category !== originalCategory) {
      updates[`contacts/${originalCategory}/${contactId}`] = null;
    }
    
    // Met à jour Firebase
    await database.ref().update(updates);
    
    showAlert('success', translate('save_success'));
    closeEditModal();
    loadContactsFromFirebase();
  } catch (error) {
    console.error('Edit contact error:', error);
    showAlert('error', translate('import_error', { error: error.message }));
  } finally {
    hideLoading();
  }
}

function openAddModal() {
  // Réinitialise le formulaire
  document.getElementById('addForm').reset();
  document.getElementById('addModal').style.display = 'flex';
}

function closeAddModal() {
  document.getElementById('addModal').style.display = 'none';
}

async function handleAddSubmit(e) {
  e.preventDefault();
  
  try {
    showLoading(translate('loading'));
    
    // Récupère les données du formulaire
    const contact = {
      name: document.getElementById('addName').value.trim(),
      email: document.getElementById('addEmail').value.trim(),
      phone: document.getElementById('addPhone').value.trim(),
      company: document.getElementById('addCompany').value.trim(),
      notes: document.getElementById('addNotes').value.trim(),
      category: document.getElementById('addCategory').value,
      importedAt: firebase.database.ServerValue.TIMESTAMP,
      lastUpdated: firebase.database.ServerValue.TIMESTAMP
    };
    
    // Validation
    validateContact(contact);
    
    // Crée un nouvel ID
    const contactId = generateId();
    
    // Ajoute à Firebase
    await database.ref(`contacts/${contact.category}/${contactId}`).set(contact);
    
    showAlert('success', translate('add_success'));
    closeAddModal();
    loadContactsFromFirebase();
  } catch (error) {
    console.error('Add contact error:', error);
    showAlert('error', translate('add_error', { error: error.message }));
  } finally {
    hideLoading();
  }
}

async function confirmDeleteContact(contactId, category) {
  const confirmed = await showConfirmationDialog(
    translate('delete'),
    translate('delete_confirm')
  );
  
  if (!confirmed) return;
  
  try {
    showLoading(translate('loading'));
    await database.ref(`contacts/${category}/${contactId}`).remove();
    showAlert('success', translate('delete_success'));
    loadContactsFromFirebase();
  } catch (error) {
    console.error('Delete contact error:', error);
    showAlert('error', translate('import_error', { error: error.message }));
  } finally {
    hideLoading();
  }
}

/* ==================== GESTION DES COLONNES AMÉLIORÉE ==================== */

function generateColumnCheckboxes(contact) {
  const container = document.getElementById('columnCheckboxes');
  container.innerHTML = '';
  
  // Ajoute des boutons pour sélectionner/désélectionner tout
  const selectAllDiv = document.createElement('div');
  selectAllDiv.className = 'checkbox-group';
  selectAllDiv.innerHTML = `
    <button type="button" class="btn btn-sm btn-outline" id="selectAllColumns">
      <i class="fas fa-check-square"></i> ${translate('select_all')}
    </button>
    <button type="button" class="btn btn-sm btn-outline" id="deselectAllColumns">
      <i class="far fa-square"></i> ${translate('deselect_all')}
    </button>
  `;
  container.appendChild(selectAllDiv);
  
  // Ajoute les cases à cocher pour chaque colonne
  Object.keys(contact).forEach(key => {
    if (key === 'id' || key === 'category' || key === 'importedAt' || key === 'lastUpdated') return;
    
    const div = document.createElement('div');
    div.className = 'checkbox-item';
    div.innerHTML = `
      <input type="checkbox" id="col_${key}" value="${key}" checked>
      <label for="col_${key}">${translate(`column_${key}`)}</label>
    `;
    container.appendChild(div);
  });
  
  // Ajoute les écouteurs pour les boutons
  document.getElementById('selectAllColumns').addEventListener('click', () => {
    container.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
      checkbox.checked = true;
    });
  });
  
  document.getElementById('deselectAllColumns').addEventListener('click', () => {
    container.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
      checkbox.checked = false;
    });
  });
  
  // Met à jour les colonnes sélectionnées quand elles changent
  container.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener('change', () => {
      state.selectedColumns = Array.from(container.querySelectorAll('input[type="checkbox"]:checked'))
        .map(el => el.value);
      renderPreviewTable();
    });
  });
}

function renderPreviewTable() {
  const previewTable = document.getElementById('previewTable');
  const thead = previewTable.querySelector('thead');
  const tbody = previewTable.querySelector('tbody');
  
  // En-têtes
  thead.innerHTML = '';
  const headerRow = document.createElement('tr');
  
  state.selectedColumns.forEach(col => {
    const th = document.createElement('th');
    th.textContent = translate(`column_${col}`);
    headerRow.appendChild(th);
  });
  
  thead.appendChild(headerRow);
  
  // Corps
  tbody.innerHTML = '';
  state.contactsToImport.slice(0, 5).forEach(contact => {
    const row = document.createElement('tr');
    
    state.selectedColumns.forEach(col => {
      const td = document.createElement('td');
      td.textContent = contact[col] || '-';
      row.appendChild(td);
    });
    
    tbody.appendChild(row);
  });
}

// Ferme les modals quand on clique en dehors
window.addEventListener('click', (e) => {
  if (e.target.classList.contains('modal')) {
    e.target.style.display = 'none';
  }
});

// Gestion de la recherche avec debounce
let searchTimeout;
function handleSearch() {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    filterContacts();
  }, 300);
}