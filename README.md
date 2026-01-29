# Wiley University Business & Finance Website

Official website for the Business & Finance division of Wiley University, providing information, forms, and resources for students, faculty, and staff.

## Live Website

**[https://runellking123.github.io/Business-Finance-Website/](https://runellking123.github.io/Business-Finance-Website/)**

## Departments

- **Auxiliary Services** - Bookstore, dining, mail services
- **Business Office** - Accounts payable, purchasing, budget management
- **Facilities Management** - Building maintenance, work orders, sustainability
- **Financial Aid** - Scholarships, grants, loans, work-study
- **Information Technology** - IT support, network services, cybersecurity
- **Risk Management** - Insurance, safety, compliance
- **Student Accounts** - Tuition, billing, payment plans
- **Transportation & Fleet Management** - Parking, shuttle services, fleet vehicles

## Features

### Fillable PDF Forms
38 professional PDF forms with Wiley University branding, including:
- Travel and expense reimbursement
- Purchase requisitions
- Budget transfers
- Payroll forms
- Fleet management forms
- And more...

### Online Form Submission
Select forms are available for online submission with data routed to Google Sheets:
- Driver Authorization Application
- Vehicle Inspection Checklist
- Trip Log & Mileage Report
- Vehicle Accident Report
- Annual Fleet Inventory Report

## Brand Colors

| Color | Hex Code | Usage |
|-------|----------|-------|
| Wildcat Purple | `#3D2C68` | Primary brand color |
| Wiley Purple | `#65538F` | Secondary/accent color |
| Gray | `#595959` | Body text |
| Carbon | `#414042` | Headers |
| Silver | `#B1B6C1` | Borders, dividers |
| Light Stone | `#E2E2E2` | Backgrounds |

## Project Structure

```
wiley-business-finance-website/
├── index.html                 # Homepage
├── contact.html               # Contact page
├── forms-resources.html       # Forms & resources directory
├── policies.html              # Policies page
├── css/
│   └── styles.css             # Main stylesheet
├── js/
│   └── main.js                # Main JavaScript
├── departments/               # Department pages
│   ├── auxiliary-services.html
│   ├── business-office.html
│   ├── facilities-management.html
│   ├── financial-aid.html
│   ├── information-technology.html
│   ├── risk-management.html
│   ├── student-accounts.html
│   └── transportation-fleet.html
├── forms/                     # Fillable PDF forms
│   └── [38 PDF forms]
├── online-forms/              # Online form submission system
│   ├── css/
│   │   └── form-styles.css
│   ├── js/
│   │   └── form-handler.js
│   ├── transportation-fleet/
│   │   └── [5 HTML forms]
│   └── GOOGLE_SHEETS_SETUP.md
└── generate_forms.py          # Python script for PDF generation
```

## Online Forms Setup

To enable online form submissions to Google Sheets:

1. Create a Google Sheet
2. Add the Apps Script from `online-forms/GOOGLE_SHEETS_SETUP.md`
3. Deploy as a Web App
4. Update the script URL in `online-forms/js/form-handler.js`

See [GOOGLE_SHEETS_SETUP.md](online-forms/GOOGLE_SHEETS_SETUP.md) for detailed instructions.

## Technologies Used

- HTML5 / CSS3
- JavaScript (Vanilla)
- Python (ReportLab) for PDF generation
- Google Apps Script for form processing
- GitHub Pages for hosting

## Contact

**Wiley University Business & Finance**  
711 Wiley Avenue  
Marshall, Texas 75670  
Phone: (903) 927-3300

---

*Founded in 1873, Wiley University is a premier liberal arts institution in Marshall, Texas.*
