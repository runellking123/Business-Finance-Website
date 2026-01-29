# Google Sheets Setup Instructions

Follow these steps to connect your online forms to Google Sheets.

## Step 1: Create a Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new blank spreadsheet
3. Name it "Wiley Transportation & Fleet Forms"

## Step 2: Add the Apps Script

1. In your Google Sheet, go to **Extensions > Apps Script**
2. Delete any code in the editor
3. Copy and paste the entire code below:

```javascript
// Wiley University - Form Submission Handler
// This script receives form submissions and adds them to the appropriate sheet

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var sheet = getOrCreateSheet(data.formType);

    // Add headers if this is a new sheet
    if (sheet.getLastRow() === 0) {
      var headers = ['Timestamp', 'Submission ID'].concat(Object.keys(data.fields));
      sheet.appendRow(headers);

      // Format header row
      var headerRange = sheet.getRange(1, 1, 1, headers.length);
      headerRange.setFontWeight('bold');
      headerRange.setBackground('#3D2C68');
      headerRange.setFontColor('white');
    }

    // Create submission ID
    var submissionId = 'WU-' + data.formType.substring(0, 3).toUpperCase() + '-' + Date.now();

    // Build row data
    var rowData = [new Date(), submissionId];
    var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];

    for (var i = 2; i < headers.length; i++) {
      rowData.push(data.fields[headers[i]] || '');
    }

    sheet.appendRow(rowData);

    // Send email notification
    sendNotification(data.formType, submissionId, data.fields);

    return ContentService
      .createTextOutput(JSON.stringify({
        'status': 'success',
        'submissionId': submissionId
      }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({
        'status': 'error',
        'message': error.toString()
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function getOrCreateSheet(sheetName) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(sheetName);

  if (!sheet) {
    sheet = ss.insertSheet(sheetName);
  }

  return sheet;
}

function sendNotification(formType, submissionId, fields) {
  // CHANGE THIS to your notification email
  var notificationEmail = 'parking@wileyc.edu';

  var subject = 'New Form Submission: ' + formType + ' (' + submissionId + ')';

  var body = 'A new form has been submitted.\n\n';
  body += 'Form Type: ' + formType + '\n';
  body += 'Submission ID: ' + submissionId + '\n';
  body += 'Submitted: ' + new Date().toLocaleString() + '\n\n';
  body += '--- Form Data ---\n\n';

  for (var key in fields) {
    body += key + ': ' + fields[key] + '\n';
  }

  body += '\n---\n';
  body += 'Wiley University - Transportation & Fleet Management\n';
  body += 'View all submissions in Google Sheets.';

  try {
    MailApp.sendEmail(notificationEmail, subject, body);
  } catch (e) {
    // Email sending failed, but form was still saved
    console.log('Email notification failed: ' + e.toString());
  }
}

function doGet(e) {
  return ContentService
    .createTextOutput('Wiley University Form Handler is running.')
    .setMimeType(ContentService.MimeType.TEXT);
}
```

4. **IMPORTANT:** Change the email on line 67 (`notificationEmail`) to your actual email address

5. Click **Save** (Ctrl+S or Cmd+S)

## Step 3: Deploy as Web App

1. Click **Deploy > New deployment**
2. Click the gear icon next to "Select type" and choose **Web app**
3. Fill in:
   - Description: "Wiley Forms Handler"
   - Execute as: **Me**
   - Who has access: **Anyone**
4. Click **Deploy**
5. Click **Authorize access** and follow the prompts to authorize
6. **COPY THE WEB APP URL** - You'll need this!

The URL will look like:
```
https://script.google.com/macros/s/AKfycbx.../exec
```

## Step 4: Update Your Forms

1. Open the file `/online-forms/js/form-handler.js`
2. Replace `YOUR_GOOGLE_SCRIPT_URL_HERE` with your Web App URL
3. Save and push to GitHub

## Testing

1. Go to any online form on your website
2. Fill out the form and submit
3. Check your Google Sheet - a new row should appear
4. Check your email for the notification

## Troubleshooting

- **Form not submitting?** Check browser console for errors
- **No data in sheet?** Make sure the Web App URL is correct
- **No email?** Check spam folder, or verify the email address in the script

## Security Notes

- The Google Sheet is private to your Google account
- Only form submissions are accepted (no read access)
- Each submission gets a unique ID for tracking
