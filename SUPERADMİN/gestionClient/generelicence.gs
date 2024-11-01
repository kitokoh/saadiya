function generateLicense() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
  // Données pour la génération de la licence
  var validityDays = Math.floor(Math.random() * 30) + 1; // Validité de 1 à 30 jours
  var serialNumber = getSerialNumber(); // Récupérer le numéro de série
  var macAddress = "E4-42-A6-3A-AC"; // Adresse MAC fixe
  var licenseDate = new Date(); // Date actuelle

  // Format de la licence
  var licenseKey = generateLicenseKey(validityDays, serialNumber, macAddress, licenseDate);
  
  // Envoi de la licence par e-mail
  var recipientEmail = "destinataire@example.com"; // Remplacez par l'adresse e-mail du destinataire
  sendLicenseEmail(recipientEmail, licenseKey);
  
  // Stockage de la licence dans Google Sheets
  sheet.appendRow([new Date(), recipientEmail, licenseKey]);
}

function generateLicenseKey(validityDays, serialNumber, macAddress, licenseDate) {
  var formattedDate = formatDate(licenseDate);
  return `A1a9${validityDays.toString().padStart(3, '0')}${serialNumber}:${macAddress}${formattedDate}${generateRandomString(8)}`;
}

function generateRandomString(length) {
  var chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  var result = '';
  for (var i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

function formatDate(date) {
  var year = date.getFullYear().toString().slice(-4); // 4 derniers chiffres de l'année
  var month = (date.getMonth() + 1).toString().padStart(2, '0'); // Mois au format 2 chiffres
  var day = date.getDate().toString().padStart(2, '0'); // Jour au format 2 chiffres
  var hours = date.getHours().toString().padStart(2, '0'); // Heures au format 2 chiffres
  var minutes = date.getMinutes().toString().padStart(2, '0'); // Minutes au format 2 chiffres
  return `${hours}${minutes}${day}${month}${year}`;
}

function getSerialNumber() {
  // Exemple de récupération du numéro de série, ici on le simule
  return "ABC123456789"; // Remplacez par votre logique de récupération
}

function sendLicenseEmail(recipient, licenseKey) {
  var subject = "Votre Licence Générée";
  var body = "Bonjour,\n\nVotre demande de licence a été traitée. Voici votre clé de licence : " + licenseKey + "\n\nCordialement,\nVotre Équipe.";
  MailApp.sendEmail(recipient, subject, body); // Envoi de l'e-mail
}
