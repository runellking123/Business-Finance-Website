/**
 * Wiley University Business & Finance - Chat API
 * Netlify Serverless Function for Claude Integration
 */

const Anthropic = require('@anthropic-ai/sdk');

// Site knowledge base - curated content for accurate responses
const SITE_KNOWLEDGE = {
    institution: {
        name: "Wiley University",
        location: "711 Wiley Avenue, Marshall, Texas 75670",
        founded: 1873,
        mainPhone: "(903) 927-3300",
        mainFax: "(903) 927-3301",
        mainEmail: "businessoffice@wileyc.edu",
        website: "https://wiley-business-finance.netlify.app"
    },
    officeHours: {
        regular: "Monday - Friday, 8:00 AM - 5:00 PM",
        weekend: "Closed Saturday and Sunday",
        note: "Hours may vary during holidays and university breaks"
    },
    departments: {
        auxiliaryServices: {
            name: "Auxiliary Services",
            description: "Bookstore, dining services, ID cards, mail services, and vending operations",
            contact: "Mr. Johnny Johnson",
            email: "auxiliary@wileyc.edu",
            phone: "(903) 927-3300",
            page: "/departments/auxiliary-services.html",
            services: ["Wildcat Campus Store (Bookstore)", "Dining Services", "Wiley ID Cards", "Mail Services", "Vending Services"]
        },
        businessOffice: {
            name: "Business Office",
            description: "Accounts payable, payroll, purchasing, travel reimbursement, and vendor management",
            contact: "Shae Bogue, Controller",
            email: "businessoffice@wileyc.edu",
            phone: "(903) 927-3300",
            page: "/departments/business-office.html",
            services: ["Accounts Payable", "Payroll", "Purchasing", "Travel Reimbursement", "Vendor Management", "Budget Management"]
        },
        facilitiesManagement: {
            name: "Facilities Management",
            description: "Building maintenance, custodial services, grounds keeping, and work orders",
            email: "facilities@wileyc.edu",
            phone: "(903) 927-3300",
            page: "/departments/facilities-management.html",
            services: ["Work Orders", "Building Maintenance", "Custodial Services", "Grounds Keeping", "Key Requests", "Space Setup"]
        },
        financialAid: {
            name: "Financial Aid",
            description: "Grants, loans, scholarships, work-study, and financial counseling services",
            director: "Ms. Elisha Warford, Director",
            email: "financialaid@wileyc.edu",
            phone: "(903) 927-3217",
            fax: "(903) 927-3366",
            page: "/departments/financial-aid.html",
            services: ["Federal Pell Grant", "TEXAS Grant", "Federal Direct Loans", "Scholarships", "Work-Study Program", "Financial Aid Counseling"],
            deadlines: {
                fafsa: "Complete FAFSA at studentaid.gov - Priority deadline varies by semester",
                documents: "Submit all required documents within 2 weeks of request"
            }
        },
        informationTechnology: {
            name: "Information Technology",
            description: "Help desk, email, WiFi, computer labs, software, and technical support",
            cto: "Mr. Darren Ashley, CTO",
            helpDesk: "(903) 927-3300",
            email: "helpdesk@wileyc.edu",
            page: "/departments/information-technology.html",
            services: ["Help Desk Support", "Email/Microsoft 365", "WiFi (WileyWiFi)", "Computer Labs", "Software Support", "Classroom Technology"],
            supportForm: "/online-forms/information-technology/it-support-request.html"
        },
        riskManagement: {
            name: "Risk Management",
            description: "Insurance, liability, safety compliance, and incident reporting",
            contact: "Mr. Johnny Johnson",
            email: "riskmanagement@wileyc.edu",
            phone: "(903) 927-3300",
            page: "/departments/risk-management.html",
            services: ["Insurance Certificates", "Contract Review", "Incident Reporting", "Workers Compensation", "Vehicle Use Requests", "Liability Waivers"]
        },
        studentAccounts: {
            name: "Student Accounts",
            description: "Tuition billing, payment plans, refunds, and 1098-T tax forms",
            bursar: "Amia Jones-Richardson, Bursar",
            email: "studentaccounts@wileyc.edu",
            phone: "(903) 927-3300",
            page: "/departments/student-accounts.html",
            services: ["Tuition Billing", "Payment Plans", "Refunds", "1098-T Tax Forms", "Account Balances"],
            paymentLink: "https://www.wileyc.edu/students/payment-options"
        },
        transportationFleet: {
            name: "Transportation & Fleet Management",
            description: "Parking permits, shuttle services, fleet vehicles, and citation appeals",
            email: "transportation@wileyc.edu",
            phone: "(903) 927-3300",
            page: "/departments/transportation-fleet.html",
            services: ["Parking Permits", "Shuttle Services", "Fleet Vehicle Reservations", "Citation Appeals"],
            parkingContact: {
                name: "Chief J. M. Reynolds",
                title: "Director of Campus Safety",
                department: "Department of Public Safety/Police Department",
                phone: "(903) 665-0281"
            }
        }
    },
    leadership: {
        svp: {
            name: "George Stiell",
            title: "Senior Vice President for Business & Finance",
            email: "george.stiell@wileyc.edu"
        },
        controller: {
            name: "Shae Bogue",
            title: "Controller",
            email: "shae.bogue@wileyc.edu"
        },
        bursar: {
            name: "Amia Jones-Richardson",
            title: "Bursar",
            email: "amia.jones@wileyc.edu"
        }
    },
    forms: {
        page: "/forms-resources.html",
        categories: [
            "Business Office Forms (Expense Reports, Travel, Vendor Payments)",
            "Financial Aid Forms (FAFSA, Scholarships, Appeals)",
            "Facilities Forms (Work Orders, Key Requests)",
            "IT Forms (Support Requests, Equipment Checkout)",
            "Risk Management Forms (Incident Reports, Insurance)"
        ]
    },
    quickLinks: {
        payBill: "https://www.wileyc.edu/students/payment-options",
        forms: "/forms-resources.html",
        itHelp: "/departments/information-technology.html",
        financialAid: "/departments/financial-aid.html"
    }
};

// System prompt for Claude
const SYSTEM_PROMPT = `You are Wiley Assistant, a helpful AI assistant for Wiley University's Business & Finance Division website. Your role is to help students, faculty, and staff navigate services, find information, and answer questions about business and financial matters at the university.

## Your Knowledge Base
${JSON.stringify(SITE_KNOWLEDGE, null, 2)}

## Guidelines

1. **Be Helpful and Accurate**: Use the knowledge base above to provide accurate information. Always include relevant links when referencing pages or services.

2. **Format Links Properly**: When mentioning pages, use markdown format: [Link Text](URL). For example: [Financial Aid](/departments/financial-aid.html)

3. **Be Concise**: Keep responses brief but informative. Use bullet points for lists.

4. **Know Your Limits**:
   - For account-specific questions (balance, grades, personal records), direct users to log into MyWiley Portal or contact the appropriate office directly.
   - For legal, tax, or complex financial advice, recommend consulting with the appropriate office or professional.
   - If you're unsure about something, say so and provide contact information for the relevant department.

5. **Privacy First**: Never ask for or attempt to process sensitive personal information (SSN, passwords, account numbers).

6. **Professional Tone**: Be friendly and professional. You represent Wiley University.

7. **Current Page Context**: The user may be viewing a specific page. Use this context to provide more relevant responses.

8. **Contact Information**: When directing users to offices, include phone numbers and emails when available.

## Common Questions to Handle Well
- How to pay tuition/bills
- Financial aid applications and deadlines
- Office hours and contact information
- Where to find forms
- IT support requests
- Parking permits
- Work orders and facilities requests

Always end complex answers by asking if they need more help or have other questions.`;

// Rate limiting (simple in-memory for demo - use Redis in production)
const rateLimit = new Map();
const RATE_LIMIT_WINDOW = 60000; // 1 minute
const RATE_LIMIT_MAX = 20; // 20 requests per minute

function checkRateLimit(ip) {
    const now = Date.now();
    const userLimit = rateLimit.get(ip) || { count: 0, resetTime: now + RATE_LIMIT_WINDOW };

    if (now > userLimit.resetTime) {
        userLimit.count = 0;
        userLimit.resetTime = now + RATE_LIMIT_WINDOW;
    }

    userLimit.count++;
    rateLimit.set(ip, userLimit);

    return userLimit.count <= RATE_LIMIT_MAX;
}

// Input validation
function validateInput(body) {
    if (!body || typeof body !== 'object') {
        return { valid: false, error: 'Invalid request body' };
    }

    if (!body.messages || !Array.isArray(body.messages)) {
        return { valid: false, error: 'Messages array required' };
    }

    // Check message content length
    for (const msg of body.messages) {
        if (!msg.role || !msg.content) {
            return { valid: false, error: 'Invalid message format' };
        }
        if (msg.content.length > 2000) {
            return { valid: false, error: 'Message too long (max 2000 characters)' };
        }
    }

    return { valid: true };
}

// Main handler
exports.handler = async (event, context) => {
    // CORS headers
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    };

    // Handle preflight
    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 204, headers, body: '' };
    }

    // Only allow POST
    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            headers,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    // Check rate limit
    const clientIP = event.headers['x-forwarded-for'] || event.headers['client-ip'] || 'unknown';
    if (!checkRateLimit(clientIP)) {
        return {
            statusCode: 429,
            headers,
            body: JSON.stringify({ error: 'Too many requests. Please wait a moment and try again.' })
        };
    }

    // Parse and validate input
    let body;
    try {
        body = JSON.parse(event.body);
    } catch (e) {
        return {
            statusCode: 400,
            headers,
            body: JSON.stringify({ error: 'Invalid JSON' })
        };
    }

    const validation = validateInput(body);
    if (!validation.valid) {
        return {
            statusCode: 400,
            headers,
            body: JSON.stringify({ error: validation.error })
        };
    }

    // Check for API key
    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) {
        console.error('ANTHROPIC_API_KEY not configured');
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ error: 'Chat service not configured. Please contact support.' })
        };
    }

    try {
        // Initialize Anthropic client
        const anthropic = new Anthropic({ apiKey });

        // Build context from current page
        let pageContext = '';
        if (body.currentPage) {
            pageContext = `\n\nThe user is currently viewing: ${body.currentPage.title || 'Unknown Page'} (${body.currentPage.url || '/'})`;
        }

        // Format messages for Claude
        const messages = body.messages.map(msg => ({
            role: msg.role === 'user' ? 'user' : 'assistant',
            content: msg.content
        }));

        // Call Claude API
        const response = await anthropic.messages.create({
            model: 'claude-3-5-sonnet-20241022',
            max_tokens: 1024,
            system: SYSTEM_PROMPT + pageContext,
            messages: messages
        });

        // Extract response text
        const assistantMessage = response.content[0]?.text || 'I apologize, but I was unable to generate a response. Please try again or contact the Business & Finance office at (903) 927-3300.';

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({
                response: assistantMessage,
                sessionId: body.sessionId || `session_${Date.now()}`
            })
        };

    } catch (error) {
        console.error('Claude API error:', error.message || error);
        console.error('Error details:', JSON.stringify(error, null, 2));

        // Handle specific error types
        if (error.status === 401 || error.message?.includes('401') || error.message?.includes('authentication') || error.message?.includes('invalid_api_key')) {
            return {
                statusCode: 500,
                headers,
                body: JSON.stringify({ error: 'API key error: Please verify your Anthropic API key is correct and starts with sk-ant-' })
            };
        }

        if (error.status === 429) {
            return {
                statusCode: 429,
                headers,
                body: JSON.stringify({ error: 'Service is busy. Please try again in a moment.' })
            };
        }

        if (error.status === 400 || error.message?.includes('400')) {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ error: 'Request error: ' + (error.message || 'Invalid request format') })
            };
        }

        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ error: 'Error: ' + (error.message || 'Unknown error. Please contact (903) 927-3300.') })
        };
    }
};
