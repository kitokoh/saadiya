function checkEmailsAndGenerateLicense() {
  // Accéder à la boîte de réception
  var threads = GmailApp.search('subject:"Bonjour"'); // Recherche d'emails avec le sujet "Bonjour"
  
  threads.forEach(function(thread) {
    var messages = thread.getMessages();
    
    messages.forEach(function(message) {
      var body = message.getPlainBody(); // Contenu du message
      var sender = message.getFrom(); // Adresse e-mail de l'expéditeur
      
      // Vérifier si le contenu contient une demande de licence
      if (body.toLowerCase().includes('demande de licence')) {
        var licenseKey = generateLicenseKey(); // Générer une clé de licence
        sendLicenseEmail(sender, licenseKey); // Envoyer la clé de licence à l'expéditeur
        updateSheetWithLicense(sender, licenseKey); // Mettre à jour Google Sheets
      }
    });
  });
}

function generateLicenseKey() {
  // Générer une clé de licence fictive
  var chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  var licenseKey = '';
  for (var i = 0; i < 16; i++) {
    licenseKey += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return licenseKey;
}

function sendLicenseEmail(recipient, licenseKey) {
  var subject = "Votre Licence Générée";
  var body = "Bonjour,\n\nVotre demande de licence a été traitée. Voici votre clé de licence : " + licenseKey + "\n\nCordialement,\nVotre Équipe.";
  
  MailApp.sendEmail(recipient, subject, body); // Envoi de l'e-mail
}

function updateSheetWithLicense(email, licenseKey) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  sheet.appendRow([new Date(), email, licenseKey]); // Ajoute une nouvelle ligne avec la date, l'email et la clé de licence
}
