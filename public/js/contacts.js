// Ajoutez ces traductions à l'objet translations
const enhancedTranslations = {
  fr: {
    bulk_edit: "Édition multiple",
    selected_contacts: "Contacts sélectionnés",
    edit_field: "Champ à modifier",
    apply_changes: "Appliquer les modifications",
    share_contact: "Partager le contact",
    download_qr: "Télécharger QR Code",
    duplicate_contacts: "Doublons détectés",
    merge_selected: "Fusionner les sélectionnés",
    ignore: "Ignorer",
    scan_to_add: "Scanner pour ajouter à vos contacts",
    bulk_update_success: "Mise à jour groupée réussie",
    qr_generated: "QR Code généré avec succès",
    duplicates_found: "{count} doublons potentiels trouvés",
    merge_success: "Fusion réussie",
    no_duplicates: "Aucun doublon trouvé",
    select_all: "Tout sélectionner",
    deselect_all: "Tout désélectionner"
  },
  en: {
    bulk_edit: "Bulk Edit",
    selected_contacts: "Selected Contacts",
    edit_field: "Field to edit",
    apply_changes: "Apply Changes",
    share_contact: "Share Contact",
    download_qr: "Download QR Code",
    duplicate_contacts: "Duplicate Contacts",
    merge_selected: "Merge Selected",
    ignore: "Ignore",
    scan_to_add: "Scan to add to your contacts",
    bulk_update_success: "Bulk update successful",
    qr_generated: "QR Code generated successfully",
    duplicates_found: "{count} potential duplicates found",
    merge_success: "Merge successful",
    no_duplicates: "No duplicates found",
    select_all: "Select all",
    deselect_all: "Deselect all"
  },
  ar: {
    bulk_edit: "تحرير جماعي",
    selected_contacts: "جهات اتصال محددة",
    edit_field: "الحقل لتعديل",
    apply_changes: "تطبيق التغييرات",
    share_contact: "مشاركة جهة الاتصال",
    download_qr: "تحميل رمز الاستجابة السريعة",
    duplicate_contacts: "جهات اتصال مكررة",
    merge_selected: "دمج المحدد",
    ignore: "تجاهل",
    scan_to_add: "امسح لإضافة إلى جهات الاتصال الخاصة بك",
    bulk_update_success: "نجاح التحديث الجماعي",
    qr_generated: "تم إنشاء رمز الاستجابة السريعة بنجاح",
    duplicates_found: "تم العثور على {count} من التكرارات المحتملة",
    merge_success: "نجاح الدمج",
    no_duplicates: "لم يتم العثور على تكرارات",
    select_all: "اختر الكل",
    deselect_all: "إلغاء تحديد الكل"
  }
};

// Fusionnez les traductions
Object.keys(enhancedTranslations).forEach(lang => {
  translations[lang] = {...translations[lang], ...enhancedTranslations[lang]};
});

// Variables globales
let selectedContacts = [];
let duplicateContacts = [];

// Fonctions avancées
function setupBulkEdit() {
  document.getElementById('bulkEditField').addEventListener('change', function() {
    const container = document.getElementById('bulkEditValueContainer');
    container.innerHTML = '';
    
    if (this.value === 'category') {
      container.innerHTML = `
        <label data-translate="category">Catégorie :</label>
        <select id="bulkEditValue" class="form-control">
          <option value="clients" data-translate="category_clients">Clients</option>
          <option value="prospects" data-translate="category_prospects">Prospects</option>
          <option value="fournisseurs" data-translate="category_suppliers">Fournisseurs</option>
          <option value="personnel" data-translate="category_staff">Personnel</option>
        </select>
      `;
    } else {
      container.innerHTML = `
        <label data-translate="column_company">Entreprise :</label>
        <input type="text" id="bulkEditValue" class="form-control">
      `;
    }
  });
}

function handleBulkEdit() {
  const selectedRows = state.dataTable.rows('.selected').data().toArray();
  if (selectedRows.length === 0) {
    showAlert('error', translate('no_contacts_selected'));
    return;
  }
  
  selectedContacts = selectedRows;
  document.getElementById('selectedContactsCount').textContent = selectedRows.length;
  document.getElementById('bulkEditModal').style.display = 'flex';
}

async function applyBulkEdit(e) {
  e.preventDefault();
  
  try {
    showLoading(translate('loading'));
    
    const field = document.getElementById('bulkEditField').value;
    const value = document.getElementById('bulkEditValue').value;
    const updates = {};
    
    selectedContacts.forEach(contact => {
      updates[`contacts/${contact.category}/${contact.id}/${field}`] = value;
      updates[`contacts/${contact.category}/${contact.id}/lastUpdated`] = 
        firebase.database.ServerValue.TIMESTAMP;
    });
    
    await database.ref().update(updates);
    
    // Mettre à jour le tableau local
    selectedContacts.forEach(contact => {
      contact[field] = value;
      const index = state.allContacts.findIndex(c => c.id === contact.id);
      if (index !== -1) {
        state.allContacts[index][field] = value;
      }
    });
    
    state.dataTable.rows().invalidate().draw();
    showAlert('success', translate('bulk_update_success'));
    closeModal('bulkEditModal');
  } catch (error) {
    showAlert('error', `Firebase error: ${error.message}`);
  } finally {
    hideLoading();
  }
}

function generateQRCode(contact) {
  const vcardData = [
    'BEGIN:VCARD',
    'VERSION:3.0',
    `FN:${contact.name}`,
    `EMAIL:${contact.email}`,
    `TEL:${contact.phone}`,
    `ORG:${contact.company}`,
    'END:VCARD'
  ].join('\n');
  
  const qrContainer = document.getElementById('qrCodeContainer');
  qrContainer.innerHTML = '';
  
  QRCode.toCanvas(qrContainer, vcardData, { width: 200 }, error => {
    if (error) {
      showAlert('error', `QR Code error: ${error.message}`);
      return;
    }
    
    document.getElementById('downloadQrCode').onclick = () => {
      const canvas = qrContainer.querySelector('canvas');
      const link = document.createElement('a');
      link.download = `contact_${contact.name}_qrcode.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
    };
    
    showAlert('success', translate('qr_generated'));
  });
}

function shareContact(contact) {
  document.getElementById('qrCodeModal').style.display = 'flex';
  generateQRCode(contact);
}

function findDuplicates() {
  const duplicates = [];
  const seen = new Map();
  
  state.allContacts.forEach(contact => {
    const key = `${contact.email?.toLowerCase()}|${contact.phone}`;
    if (seen.has(key)) {
      if (!seen.get(key).marked) {
        duplicates.push(seen.get(key));
        seen.get(key).marked = true;
      }
      duplicates.push(contact);
    } else {
      seen.set(key, contact);
    }
  });
  
  return duplicates;
}

function showDuplicates() {
  duplicateContacts = findDuplicates();
  
  if (duplicateContacts.length === 0) {
    showAlert('info', translate('no_duplicates'));
    return;
  }
  
  const tbody = document.getElementById('duplicatesTable').querySelector('tbody');
  tbody.innerHTML = duplicateContacts.map(contact => `
    <tr>
      <td><input type="checkbox" class="duplicate-check" data-id="${contact.id}" checked></td>
      <td>${contact.name || '-'}</td>
      <td>${contact.email || '-'}</td>
      <td>${contact.phone || '-'}</td>
      <td>${translate(`category_${contact.category}`)}</td>
    </tr>
  `).join('');
  
  document.getElementById('duplicatesModal').style.display = 'flex';
  showAlert('info', translate('duplicates_found', { count: duplicateContacts.length }));
}

async function mergeContacts() {
  const selectedIds = Array.from(document.querySelectorAll('.duplicate-check:checked'))
    .map(el => el.dataset.id);
  
  if (selectedIds.length < 2) {
    showAlert('error', translate('select_at_least_two'));
    return;
  }
  
  try {
    showLoading(translate('loading'));
    
    // Ici vous implémenteriez votre logique de fusion
    // Pour l'exemple, nous gardons le premier contact et supprimons les autres
    const contactsToMerge = duplicateContacts.filter(c => selectedIds.includes(c.id));
    const primaryContact = contactsToMerge[0];
    
    // Fusionner les données (exemple simplifié)
    const mergedContact = {
      ...primaryContact,
      notes: contactsToMerge.map(c => c.notes).filter(Boolean).join('\n---\n')
    };
    
    // Mettre à jour Firebase
    const updates = {};
    updates[`contacts/${primaryContact.category}/${primaryContact.id}`] = mergedContact;
    
    // Supprimer les doublons
    contactsToMerge.slice(1).forEach(contact => {
      updates[`contacts/${contact.category}/${contact.id}`] = null;
    });
    
    await database.ref().update(updates);
    
    // Mettre à jour le tableau local
    state.allContacts = state.allContacts.filter(c => !selectedIds.includes(c.id) || c.id === primaryContact.id);
    if (!state.allContacts.some(c => c.id === primaryContact.id)) {
      state.allContacts.push(mergedContact);
    }
    
    state.dataTable.clear().rows.add(state.allContacts).draw();
    showAlert('success', translate('merge_success'));
    closeModal('duplicatesModal');
  } catch (error) {
    showAlert('error', `Merge error: ${error.message}`);
  } finally {
    hideLoading();
  }
}

function closeModal(modalId) {
  document.getElementById(modalId).style.display = 'none';
}

function setupAdvancedFeatures() {
  // Édition groupée
  document.getElementById('bulkEditForm').addEventListener('submit', applyBulkEdit);
  document.getElementById('cancelBulkEdit').addEventListener('click', () => closeModal('bulkEditModal'));
  
  // QR Code
  document.getElementById('qrCodeModal').addEventListener('click', (e) => {
    if (e.target === e.currentTarget) closeModal('qrCodeModal');
  });
  
  // Doublons
  document.getElementById('mergeSelected').addEventListener('click', mergeContacts);
  document.getElementById('ignoreDuplicates').addEventListener('click', () => closeModal('duplicatesModal'));
  document.getElementById('selectAllDupes').addEventListener('change', function() {
    document.querySelectorAll('.duplicate-check').forEach(checkbox => {
      checkbox.checked = this.checked;
    });
  });
  
  // Ajouter un bouton d'édition groupée dans l'UI
  const bulkEditBtn = document.createElement('button');
  bulkEditBtn.className = 'btn btn-outline';
  bulkEditBtn.innerHTML = `<i class="fas fa-users-cog"></i> ${translate('bulk_edit')}`;
  bulkEditBtn.addEventListener('click', handleBulkEdit);
  document.querySelector('.table-section').prepend(bulkEditBtn);
  
  // Ajouter un bouton de détection de doublons
  const duplicatesBtn = document.createElement('button');
  duplicatesBtn.className = 'btn btn-outline';
  duplicatesBtn.innerHTML = `<i class="fas fa-clone"></i> ${translate('duplicate_contacts')}`;
  duplicatesBtn.addEventListener('click', showDuplicates);
  document.querySelector('.table-section').prepend(duplicatesBtn);
  
  // Modifier le rendu du tableau pour ajouter des cases à cocher
  state.dataTable.on('draw', function() {
    $('.contact-table tbody tr').each(function() {
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.className = 'row-checkbox';
      $(this).prepend($('<td>').append(checkbox));
    });
  });
  
  // Activer la sélection de ligne
  $('.contact-table').on('change', '.row-checkbox', function() {
    $(this).closest('tr').toggleClass('selected', this.checked);
  });
}

// Modifiez la fonction init() pour inclure :
function enhancedInit() {
  init(); // Appel de la fonction init originale
  
  // Après l'initialisation de DataTables
  setTimeout(() => {
    setupAdvancedFeatures();
    setupBulkEdit();
    
    // Ajouter l'option de partage dans le modal d'édition
    const shareBtn = document.createElement('button');
    shareBtn.className = 'btn btn-outline';
    shareBtn.innerHTML = `<i class="fas fa-share-alt"></i> ${translate('share_contact')}`;
    shareBtn.addEventListener('click', () => {
      const contactId = document.getElementById('editId').value;
      const contact = state.allContacts.find(c => c.id === contactId);
      if (contact) shareContact(contact);
    });
    document.getElementById('editForm').appendChild(shareBtn);
  }, 1000);
}

// Remplacez document.addEventListener('DOMContentLoaded', init); par :
document.addEventListener('DOMContentLoaded', enhancedInit);