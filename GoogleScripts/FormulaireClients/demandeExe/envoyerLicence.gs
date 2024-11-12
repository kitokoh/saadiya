function envoyerLicences() {
  const sheetLicences = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("LicenseData");
  const sheetFactures = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Factures");
  const data = sheetLicences.getDataRange().getValues();

  Logger.log("Début de la vérification des licences");

  for (let i = 1; i < data.length; i++) {
    const [novausername, username, email, typeLicence, serialNumber, instance, dossier, dateDemand, mac_address, lang, dategen, licenceKey, statupaiement, status] = data[i];
    
    Logger.log(`Traitement de la ligne ${i + 1} - Status: ${status}`);
    
    if (status !== "no send" && statupaiement === "send") continue;

    let message, instructions, videoLink;
    switch (lang) {
      case "fr":
        message = `Bonjour ${username},<br><br>Suite à votre demande de renouvellement de licence <strong>${typeLicence}</strong>, voici votre clé de licence :<br><br> <strong>${licenceKey}</strong>.<br>`;
        instructions = `
          <h3 style="color: #003366; font-size: 18px;">Instructions d'activation :</h3>
          <ol style="color: #555; font-size: 14px;">
            <li>Copiez la clé de licence ci-dessus.</li>
            <li>Ouvrez votre application et accédez aux paramètres de licence.</li>
            <li>Collez la clé dans le champ de licence et cliquez sur "Activer".</li>
          </ol>`;
        videoLink = "https://www.youtube.com/watch?v=video_id_fr"; // Lien vers la vidéo en français
        break;
      case "en":
        message = `Hello ${username},<br><br>Following your request to renew your <strong>${typeLicence}</strong> license, here is your license key: <strong>${licenceKey}</strong>.<br>`;
        instructions = `
          <h3 style="color: #003366; font-size: 18px;">Activation Instructions:</h3>
          <ol style="color: #555; font-size: 14px;">
            <li>Copy the license key above.</li>
            <li>Open your application and go to license settings.</li>
            <li>Paste the key in the license field and click "Activate".</li>
          </ol>`;
        videoLink = "https://www.youtube.com/watch?v=video_id_en"; // Lien vers la vidéo en anglais
        break;
      case "ar":
        message = `مرحبًا ${username}،<br><br>وفقًا لطلبك لتجديد رخصتك <strong>${typeLicence}</strong>، إليك مفتاح الرخصة الخاص بك: <strong>${licenceKey}</strong>.<br>`;
        instructions = `
          <h3 style="color: #003366; font-size: 18px;">تعليمات التفعيل:</h3>
          <ol style="color: #555; font-size: 14px;">
            <li>انسخ مفتاح الرخصة أعلاه.</li>
            <li>افتح التطبيق وانتقل إلى إعدادات الرخصة.</li>
            <li>قم بلصق المفتاح في حقل الرخصة واضغط على "تفعيل".</li>
          </ol>`;
        videoLink = "https://www.youtube.com/watch?v=video_id_ar"; // Lien vers la vidéo en arabe
        break;
      // Ajouter d'autres langues si nécessaire
      default:
        message = `Bonjour ${username},<br><br>Suite à votre demande de renouvellement de licence <strong>${typeLicence}</strong>, voici votre clé de licence :<br><br> <strong>${licenceKey}</strong>.`;
        videoLink = "https://www.youtube.com/watch?v=video_id_fr"; // Par défaut en français
    }

    const htmlBody = `
      <html>
        <body style="font-family: Arial, sans-serif; color: #333; background-color: #f9f9f9; padding: 20px;">
          <table style="width: 100%; max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 10px;">
            <tr>
              <td style="text-align: center;">
                <h2 style="color: #003366;">nova360.ai - Licence</h2>
                <p style="color: #777;">799 Market St Floor 8, San Francisco, CA 94103</p>
                <hr style="border: none; background-color: #ddd; margin: 20px 0;">
              </td>
            </tr>
            <tr>
              <td>${message}</td>
            </tr>
            <tr>
              <td style="padding-top: 20px;">${instructions}</td>
            </tr>
            <tr>
              <td style="text-align: center; padding-top: 20px;">
                <p style="font-size: 16px; color: #003366;">Voir la vidéo d'installation :</p>
                <a href="${videoLink}" target="_blank">Comment installer votre licence - YouTube</a>
              </td>
            </tr>
            <tr>
              <td style="text-align: center; color: #999; padding-top: 20px;">
                <hr style="background-color: #ddd; margin: 20px 0;">
                <p>Cordialement,</p>
                <p><strong>Équipe nova360.ai</strong></p>
              </td>
            </tr>
          </table>
        </body>
      </html>
    `;

    Logger.log(`Préparation de l'envoi de l'email pour ${username} à ${email}`);
    
    const options = {
      htmlBody: htmlBody,
      attachments: [
        DriveApp.getFileById("ID_document_piece1").getAs(MimeType.PDF) // ID du fichier PDF dans Google Drive
      ],
      from: "info@turknovatech.com"
    };
    
    sendEmailWithLocalizedSubject(email, typeLicence, message, htmlBody, options, lang);
    sheetLicences.getRange(i + 1, 14).setValue("send");
    Logger.log(`Statut mis à jour pour ${username} dans LicenseData`);

    updateOrAppendLicence(sheetFactures, email, username, typeLicence);
    Logger.log(`Facture mise à jour pour ${username}`);
  }
  
  Logger.log("Traitement terminé pour toutes les licences.");
}
