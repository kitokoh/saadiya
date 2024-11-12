// Fonction de déploiement d'une application Web
function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
      .setTitle('Robot License Form')
      .setWidth(600)
      .setHeight(600);
}

// Fonction pour traiter la soumission des données
function submitFormData(formData) {
  // Ouvre le fichier Google Sheets par ID
  const spreadsheetId = '1NgyLuDmUz1N_gGNv_pEjEXSidGmkPdHnm_wXYvN2WEU'; // Remplace par l'ID de ta feuille
  const sheetName = 'entreeSaadiya'; // Nom de l'onglet dans le Google Sheets où tu veux enregistrer les données
  const sheet = SpreadsheetApp.openById(spreadsheetId).getSheetByName(sheetName);

  // Récupère les valeurs du formulaire
  const { name, email, phone, usageType, companyName, role, languageSelect, phoneCountry } = formData;

  // Crée une nouvelle ligne avec les données soumises
  const row = [
    name,
    email,
    phone,
    usageType,
    companyName || '',  // Si aucun nom de société n'est saisi, on insère une chaîne vide
    role || '',         // Si aucun rôle n'est saisi, on insère une chaîne vide
    languageSelect,
    phoneCountry,
    new Date()         // Ajoute la date et l'heure de la soumission
  ];

  // Ajoute la ligne à la feuille
  //sheet.appendRow(row);
  sheet.appendRow([formData.name, formData.email, formData.phone, formData.usageType, formData.companyName, formData.role, formData.languageSelect, formData.phoneCountry]);
  // Retourne un message de succès
  return "Form submitted successfully!";
}

