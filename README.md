# Wiley University Business & Finance Website

Official website for the Business & Finance division of Wiley University, providing information, forms, resources, and AI-powered assistance for students, faculty, and staff.

## Live Website

**[https://wiley-business-finance.netlify.app](https://wiley-business-finance.netlify.app)**

---

## Features

### AI Chatbot Assistant
An intelligent chatbot powered by Claude AI that helps users:
- Navigate the website and find information
- Answer questions about Business & Finance services
- Provide links to relevant forms and resources
- Direct users to the appropriate department contacts

**Chatbot Features:**
- Available on all pages (floating button, bottom-right)
- Session persistence across page navigation
- Quick prompt buttons for common questions
- Mobile-responsive design
- Fully accessible (ARIA labels, keyboard navigation, screen reader support)

### Department Pages
8 fully-designed department pages with:
- Service descriptions and contact information
- Staff directories with photos
- Quick links to relevant forms
- Office hours and location details

### Online Form Submission
50+ online forms with Netlify Forms integration:
- IT Support Requests
- Work Orders
- Financial Aid Applications
- Travel Reimbursements
- And many more...

### Fillable PDF Forms
38 professional PDF forms with Wiley University branding for download.

---

## Departments

| Department | Description |
|------------|-------------|
| **Auxiliary Services** | Bookstore, dining, ID cards, mail services |
| **Business Office** | Accounts payable, payroll, purchasing, travel |
| **Facilities Management** | Building maintenance, work orders, key requests |
| **Financial Aid** | Scholarships, grants, loans, work-study |
| **Information Technology** | Help desk, email, WiFi, technical support |
| **Risk Management** | Insurance, liability, safety compliance |
| **Student Accounts** | Tuition billing, payment plans, refunds |
| **Transportation & Fleet** | Parking permits, shuttle services, fleet vehicles |

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| HTML5 / CSS3 | Frontend structure and styling |
| JavaScript (Vanilla) | Client-side interactivity |
| Netlify | Hosting, forms, and serverless functions |
| Netlify Functions | Backend API for chatbot |
| Anthropic Claude API | AI chatbot responses |
| Google Apps Script | Legacy form processing (optional) |

---

## Project Structure

```
Business-Finance-Website/
├── index.html                      # Homepage
├── contact.html                    # Contact page
├── forms-resources.html            # Forms & resources directory
├── policies.html                   # Policies listing page
├── success.html                    # Form submission success page
│
├── css/
│   ├── styles.css                  # Main stylesheet
│   └── chatbot.css                 # AI chatbot styles
│
├── js/
│   ├── main.js                     # Main JavaScript (navigation, accordions)
│   └── chatbot.js                  # AI chatbot client-side logic
│
├── departments/                    # Department pages (8 pages)
│   ├── auxiliary-services.html
│   ├── business-office.html
│   ├── facilities-management.html
│   ├── financial-aid.html
│   ├── information-technology.html
│   ├── risk-management.html
│   ├── student-accounts.html
│   └── transportation-fleet.html
│
├── policies/                       # Policy pages (18 pages)
│   ├── travel-policy.html
│   ├── purchasing-policy.html
│   └── ... (16 more)
│
├── online-forms/                   # Online form submission pages
│   ├── css/
│   │   └── form-styles.css
│   ├── js/
│   │   └── form-handler.js
│   ├── business-office/            # 6 forms
│   ├── facilities-management/      # 5 forms
│   ├── financial-aid/              # 6 forms
│   ├── information-technology/     # 4 forms
│   ├── risk-management/            # 6 forms
│   ├── student-accounts/           # 6 forms
│   ├── transportation-fleet/       # 9 forms
│   └── auxiliary-services/         # 3 forms
│
├── forms/                          # Downloadable PDF forms
│   └── [38 PDF files]
│
├── images/                         # Staff photos and images
│   └── [image files]
│
├── netlify/                        # Netlify serverless functions
│   └── functions/
│       ├── chat.js                 # Claude AI chat endpoint
│       └── package.json            # Function dependencies
│
├── netlify.toml                    # Netlify configuration
└── README.md                       # This file
```

---

## Setup & Deployment Guide

### Prerequisites
- [Node.js](https://nodejs.org/) (v18 or higher)
- [Netlify CLI](https://docs.netlify.com/cli/get-started/) (`npm install -g netlify-cli`)
- [Anthropic API Key](https://console.anthropic.com/) (for chatbot)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/runellking123/Business-Finance-Website.git
cd Business-Finance-Website
```

### Step 2: Install Function Dependencies

```bash
cd netlify/functions
npm install
cd ../..
```

### Step 3: Set Up Netlify

```bash
# Login to Netlify
netlify login

# Initialize the site (or link to existing)
netlify init
```

### Step 4: Configure Environment Variables

Add your Anthropic API key in Netlify:

1. Go to: [Netlify Dashboard](https://app.netlify.com) → Your Site → Site Settings → Environment Variables
2. Add variable:
   - **Key:** `ANTHROPIC_API_KEY`
   - **Value:** Your API key from [console.anthropic.com](https://console.anthropic.com/settings/keys)
3. Check "Secret" to hide the value

### Step 5: Deploy

```bash
# Deploy to production
netlify deploy --prod
```

---

## Local Development

### Run Locally with Netlify Dev

```bash
# This runs the site with serverless functions locally
netlify dev
```

The site will be available at `http://localhost:8888`

### Testing the Chatbot Locally

For local development, create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
```

**Note:** Never commit the `.env` file to Git.

---

## Customization Guide

### Updating the Chatbot Knowledge Base

Edit the `SITE_KNOWLEDGE` object in `netlify/functions/chat.js` to update:
- Department information
- Contact details
- Office hours
- Service descriptions
- Quick links

### Changing Quick Prompts

Edit the `CONFIG.quickPrompts` array in `js/chatbot.js`:

```javascript
quickPrompts: [
    { text: 'Pay my bill', message: 'How do I pay my tuition bill?' },
    { text: 'Office hours', message: 'What are the Business & Finance office hours?' },
    // Add more prompts here
]
```

### Styling the Chatbot

Edit CSS variables in `css/chatbot.css`:

```css
:root {
    --chatbot-primary: #4a2c6a;      /* Main color */
    --chatbot-secondary: #6b4190;    /* Accent color */
    --chatbot-accent: #d4af37;       /* Highlight color */
}
```

---

## Brand Colors

| Color | Hex Code | Usage |
|-------|----------|-------|
| Wildcat Purple | `#3D2C68` | Primary brand color |
| Wiley Purple | `#65538F` | Secondary/accent color |
| Chatbot Purple | `#4a2c6a` | Chatbot primary |
| Gold Accent | `#d4af37` | Highlights, focus states |
| Gray | `#595959` | Body text |
| Carbon | `#414042` | Headers |
| Silver | `#B1B6C1` | Borders, dividers |
| Light Stone | `#E2E2E2` | Backgrounds |

---

## API Costs

The chatbot uses Claude 3.5 Sonnet. Estimated costs:

| Credits | Approximate Requests |
|---------|---------------------|
| $5 | 300-500 conversations |
| $10 | 600-1000 conversations |
| $20 | 1200-2000 conversations |

Monitor usage at [console.anthropic.com](https://console.anthropic.com)

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Claude API key for chatbot functionality |

---

## Netlify Configuration

The `netlify.toml` file configures:

```toml
[build]
  publish = "."
  functions = "netlify/functions"

[functions]
  node_bundler = "esbuild"

[build.processing.forms]
  enable = true
```

---

## Troubleshooting

### Chatbot shows "Error" message
1. Check that `ANTHROPIC_API_KEY` is set in Netlify environment variables
2. Verify your Anthropic account has credits
3. Check function logs: Netlify Dashboard → Functions → chat → Logs

### Forms not submitting
1. Ensure `data-netlify="true"` is on the form element
2. Check Netlify Forms dashboard for submissions
3. Verify the form has a unique `name` attribute

### Styles not loading on some pages
1. Check the relative path to CSS files matches the page depth
2. Root pages: `css/styles.css`
3. Department pages: `../css/styles.css`
4. Online forms: `../../css/styles.css`

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -m "Add new feature"`)
4. Push to branch (`git push origin feature/new-feature`)
5. Open a Pull Request

---

## Contact

**Wiley University Business & Finance**
711 Wiley Avenue
Marshall, Texas 75670
Phone: (903) 927-3300
Email: businessoffice@wileyc.edu

---

## License

This project is proprietary to Wiley University. All rights reserved.

---

*Founded in 1873, Wiley University is a premier liberal arts institution in Marshall, Texas.*

*Go Forth Inspired.*
