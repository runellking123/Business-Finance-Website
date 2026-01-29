#!/usr/bin/env python3
"""
Wiley University - Business & Finance Forms Generator
Creates fillable PDF forms following brand guidelines
"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfform
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont

# Wiley University Brand Colors
WILDCAT_PURPLE = colors.HexColor('#3D2C68')
WILEY_PURPLE = colors.HexColor('#65538F')
GRAY = colors.HexColor('#595959')
CARBON = colors.HexColor('#414042')
SILVER = colors.HexColor('#B1B6C1')
LIGHT_STONE = colors.HexColor('#E2E2E2')

# Forms directory
FORMS_DIR = '/Users/runellking/Desktop/wiley-business-finance-website/forms'

# Ensure forms directory exists
os.makedirs(FORMS_DIR, exist_ok=True)

class WileyFormGenerator:
    def __init__(self):
        self.width, self.height = letter
        self.margin = 0.75 * inch

    def create_form(self, filename, title, department, fields, instructions=None):
        """Create a branded fillable PDF form"""
        filepath = os.path.join(FORMS_DIR, filename)
        c = canvas.Canvas(filepath, pagesize=letter)

        # Draw header
        self._draw_header(c, title, department)

        # Draw instructions if provided
        y_position = self.height - 2 * inch
        if instructions:
            y_position = self._draw_instructions(c, instructions, y_position)

        # Draw form fields
        self._draw_fields(c, fields, y_position)

        # Draw footer
        self._draw_footer(c)

        c.save()
        print(f"Created: {filename}")

    def _draw_header(self, c, title, department):
        """Draw the form header with Wiley branding"""
        # Purple header bar
        c.setFillColor(WILDCAT_PURPLE)
        c.rect(0, self.height - 1.2 * inch, self.width, 1.2 * inch, fill=1, stroke=0)

        # University name
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(self.margin, self.height - 0.5 * inch, "WILEY")
        c.setFont("Helvetica", 10)
        c.drawString(self.margin, self.height - 0.7 * inch, "UNIVERSITY")

        # Divider line
        c.setStrokeColor(colors.white)
        c.setLineWidth(1)
        c.line(self.margin + 1.2 * inch, self.height - 0.35 * inch,
               self.margin + 1.2 * inch, self.height - 0.85 * inch)

        # Department name
        c.setFont("Helvetica", 9)
        c.drawString(self.margin + 1.4 * inch, self.height - 0.55 * inch, "BUSINESS & FINANCE")
        c.setFont("Helvetica-Bold", 9)
        c.drawString(self.margin + 1.4 * inch, self.height - 0.75 * inch, department.upper())

        # Form title below header
        c.setFillColor(WILDCAT_PURPLE)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(self.margin, self.height - 1.6 * inch, title)

        # Accent line under title
        c.setStrokeColor(WILEY_PURPLE)
        c.setLineWidth(2)
        c.line(self.margin, self.height - 1.7 * inch,
               self.margin + 2.5 * inch, self.height - 1.7 * inch)

    def _draw_instructions(self, c, instructions, y_start):
        """Draw instruction text"""
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 9)

        # Word wrap instructions
        max_width = self.width - 2 * self.margin
        words = instructions.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            if c.stringWidth(test_line, "Helvetica", 9) < max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))

        y = y_start
        for line in lines:
            c.drawString(self.margin, y, line)
            y -= 14

        return y - 10

    def _draw_fields(self, c, fields, y_start):
        """Draw form fields"""
        y = y_start - 20
        field_num = 0

        for field in fields:
            if y < 1.5 * inch:
                # New page needed
                c.showPage()
                self._draw_header_minimal(c)
                y = self.height - 1.5 * inch

            field_type = field.get('type', 'text')
            label = field.get('label', '')
            width = field.get('width', 4) * inch
            height = field.get('height', 0.3) * inch
            required = field.get('required', False)
            options = field.get('options', [])

            # Draw label (skip for section and row types which handle their own labels)
            if field_type not in ('section', 'row'):
                c.setFillColor(CARBON)
                c.setFont("Helvetica-Bold", 10)
                label_text = label + (" *" if required else "")
                c.drawString(self.margin, y, label_text)

            field_y = y - height - 5
            field_name = f"field_{field_num}"

            if field_type == 'text':
                # Text input field
                c.setStrokeColor(SILVER)
                c.setFillColor(colors.white)
                c.rect(self.margin, field_y, width, height, fill=1, stroke=1)

                # Add fillable field
                form = c.acroForm
                form.textfield(
                    name=field_name,
                    x=self.margin + 2,
                    y=field_y + 2,
                    width=width - 4,
                    height=height - 4,
                    borderWidth=0,
                    fontSize=10,
                    textColor=CARBON,
                )

            elif field_type == 'textarea':
                # Multi-line text area
                text_height = field.get('height', 1) * inch
                c.setStrokeColor(SILVER)
                c.setFillColor(colors.white)
                c.rect(self.margin, field_y - text_height + height, width, text_height, fill=1, stroke=1)

                form = c.acroForm
                form.textfield(
                    name=field_name,
                    x=self.margin + 2,
                    y=field_y - text_height + height + 2,
                    width=width - 4,
                    height=text_height - 4,
                    borderWidth=0,
                    fontSize=10,
                    textColor=CARBON,
                    fieldFlags='multiline',
                )
                field_y = field_y - text_height + height

            elif field_type == 'checkbox':
                # Checkbox
                form = c.acroForm
                form.checkbox(
                    name=field_name,
                    x=self.margin,
                    y=field_y + 5,
                    size=12,
                    borderColor=SILVER,
                    fillColor=colors.white,
                    textColor=WILDCAT_PURPLE,
                    checked=False,
                )

            elif field_type == 'radio':
                # Radio buttons
                for i, option in enumerate(options):
                    opt_y = field_y - (i * 20)
                    form = c.acroForm
                    form.radio(
                        name=field_name,
                        value=option,
                        x=self.margin,
                        y=opt_y + 5,
                        size=12,
                        borderColor=SILVER,
                        fillColor=colors.white,
                        textColor=WILDCAT_PURPLE,
                        selected=(i == 0),
                    )
                    c.setFillColor(GRAY)
                    c.setFont("Helvetica", 9)
                    c.drawString(self.margin + 20, opt_y + 7, option)
                field_y = field_y - (len(options) * 20)

            elif field_type == 'date':
                # Date field with format hint
                c.setStrokeColor(SILVER)
                c.setFillColor(colors.white)
                c.rect(self.margin, field_y, 1.5 * inch, height, fill=1, stroke=1)

                c.setFillColor(GRAY)
                c.setFont("Helvetica", 8)
                c.drawString(self.margin + 1.6 * inch, field_y + 8, "(MM/DD/YYYY)")

                form = c.acroForm
                form.textfield(
                    name=field_name,
                    x=self.margin + 2,
                    y=field_y + 2,
                    width=1.5 * inch - 4,
                    height=height - 4,
                    borderWidth=0,
                    fontSize=10,
                    textColor=CARBON,
                )

            elif field_type == 'signature':
                # Signature line
                sig_width = 3 * inch
                c.setStrokeColor(CARBON)
                c.setLineWidth(1)
                c.line(self.margin, field_y + 10, self.margin + sig_width, field_y + 10)
                c.setFillColor(GRAY)
                c.setFont("Helvetica", 8)
                c.drawString(self.margin, field_y - 5, "Sign above")

                # Date next to signature
                c.drawString(self.margin + sig_width + 0.5 * inch, field_y + 15, "Date:")
                c.line(self.margin + sig_width + 0.9 * inch, field_y + 10,
                       self.margin + sig_width + 2.5 * inch, field_y + 10)

            elif field_type == 'section':
                # Section header
                c.setFillColor(WILEY_PURPLE)
                c.setFont("Helvetica-Bold", 11)
                c.drawString(self.margin, y, label)
                c.setStrokeColor(WILEY_PURPLE)
                c.setLineWidth(1)
                c.line(self.margin, y - 3, self.width - self.margin, y - 3)
                field_y = y - 10

            elif field_type == 'row':
                # Multiple fields in a row
                row_fields = field.get('fields', [])
                x_offset = self.margin
                for rf in row_fields:
                    rf_label = rf.get('label', '')
                    rf_width = rf.get('width', 2) * inch

                    c.setFillColor(CARBON)
                    c.setFont("Helvetica-Bold", 9)
                    c.drawString(x_offset, y, rf_label)

                    c.setStrokeColor(SILVER)
                    c.setFillColor(colors.white)
                    c.rect(x_offset, field_y, rf_width - 10, height, fill=1, stroke=1)

                    form = c.acroForm
                    form.textfield(
                        name=f"{field_name}_{rf_label.replace(' ', '_')}",
                        x=x_offset + 2,
                        y=field_y + 2,
                        width=rf_width - 14,
                        height=height - 4,
                        borderWidth=0,
                        fontSize=10,
                        textColor=CARBON,
                    )
                    x_offset += rf_width

            y = field_y - 30
            field_num += 1

    def _draw_header_minimal(self, c):
        """Draw minimal header for continuation pages"""
        c.setFillColor(WILDCAT_PURPLE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(self.margin, self.height - 0.5 * inch, "WILEY UNIVERSITY - Business & Finance")
        c.setStrokeColor(WILEY_PURPLE)
        c.setLineWidth(1)
        c.line(self.margin, self.height - 0.6 * inch, self.width - self.margin, self.height - 0.6 * inch)

    def _draw_footer(self, c):
        """Draw form footer"""
        # Footer line
        c.setStrokeColor(LIGHT_STONE)
        c.setLineWidth(1)
        c.line(self.margin, 0.75 * inch, self.width - self.margin, 0.75 * inch)

        # Footer text
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 8)
        c.drawString(self.margin, 0.5 * inch, "Wiley University | 711 Wiley Avenue, Marshall, Texas 75670")
        c.drawString(self.margin, 0.35 * inch, "Phone: (903) 927-3300 | Email: businessoffice@wileyc.edu")

        # Page number (right aligned)
        c.drawRightString(self.width - self.margin, 0.5 * inch, "Page 1 of 1")

        # Required fields note
        c.setFillColor(WILEY_PURPLE)
        c.setFont("Helvetica-Oblique", 8)
        c.drawRightString(self.width - self.margin, 0.35 * inch, "* Required fields")


def create_all_forms():
    """Generate all Business & Finance forms"""
    generator = WileyFormGenerator()

    # ==================== BUSINESS OFFICE FORMS ====================

    # 1. Direct Deposit Authorization
    generator.create_form(
        "direct-deposit-authorization.pdf",
        "Direct Deposit Authorization",
        "Business Office",
        [
            {'type': 'section', 'label': 'Employee Information'},
            {'type': 'row', 'fields': [
                {'label': 'First Name', 'width': 2.5},
                {'label': 'Last Name', 'width': 2.5},
                {'label': 'Employee ID', 'width': 2}
            ]},
            {'type': 'text', 'label': 'Department', 'width': 4, 'required': True},
            {'type': 'text', 'label': 'Email Address', 'width': 4, 'required': True},
            {'type': 'text', 'label': 'Phone Number', 'width': 2.5},
            {'type': 'section', 'label': 'Bank Account Information'},
            {'type': 'text', 'label': 'Bank Name', 'width': 4, 'required': True},
            {'type': 'text', 'label': 'Routing Number (9 digits)', 'width': 3, 'required': True},
            {'type': 'text', 'label': 'Account Number', 'width': 3, 'required': True},
            {'type': 'radio', 'label': 'Account Type', 'options': ['Checking', 'Savings'], 'required': True},
            {'type': 'section', 'label': 'Authorization'},
            {'type': 'checkbox', 'label': 'I authorize Wiley University to deposit my pay directly to the account listed above.'},
            {'type': 'signature', 'label': 'Employee Signature'},
        ],
        "Complete this form to enroll in or change your direct deposit settings. Please attach a voided check or bank letter verifying your account information."
    )

    # 2. Travel Reimbursement Request
    generator.create_form(
        "travel-reimbursement-request.pdf",
        "Travel Reimbursement Request",
        "Business Office",
        [
            {'type': 'section', 'label': 'Employee Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'Employee ID', 'width': 2},
                {'label': 'Department', 'width': 2}
            ]},
            {'type': 'section', 'label': 'Trip Details'},
            {'type': 'text', 'label': 'Purpose of Travel', 'width': 6, 'required': True},
            {'type': 'text', 'label': 'Destination', 'width': 4, 'required': True},
            {'type': 'row', 'fields': [
                {'label': 'Departure Date', 'width': 2},
                {'label': 'Return Date', 'width': 2},
            ]},
            {'type': 'section', 'label': 'Expense Details'},
            {'type': 'row', 'fields': [
                {'label': 'Airfare/Transportation', 'width': 2},
                {'label': 'Lodging', 'width': 2},
                {'label': 'Meals', 'width': 1.5}
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Mileage (miles)', 'width': 1.5},
                {'label': 'Parking/Tolls', 'width': 1.5},
                {'label': 'Other', 'width': 1.5}
            ]},
            {'type': 'text', 'label': 'TOTAL REIMBURSEMENT REQUESTED', 'width': 2.5, 'required': True},
            {'type': 'textarea', 'label': 'Additional Notes/Explanation', 'width': 6, 'height': 0.8},
            {'type': 'section', 'label': 'Approvals'},
            {'type': 'signature', 'label': 'Employee Signature'},
            {'type': 'signature', 'label': 'Supervisor Approval'},
        ],
        "Submit this form with original receipts for all expenses over $25. Allow 2-3 weeks for processing."
    )

    # 3. Expense Report
    generator.create_form(
        "expense-report.pdf",
        "Expense Report",
        "Business Office",
        [
            {'type': 'section', 'label': 'Employee Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'Employee ID', 'width': 2},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Department', 'width': 3},
                {'label': 'Budget Code', 'width': 2},
            ]},
            {'type': 'section', 'label': 'Expense Details'},
            {'type': 'text', 'label': 'Business Purpose', 'width': 6, 'required': True},
            {'type': 'date', 'label': 'Report Period From', 'required': True},
            {'type': 'date', 'label': 'Report Period To', 'required': True},
            {'type': 'section', 'label': 'Itemized Expenses'},
            {'type': 'text', 'label': 'Item 1: Description', 'width': 4},
            {'type': 'row', 'fields': [
                {'label': 'Date', 'width': 1.5},
                {'label': 'Amount', 'width': 1.5},
            ]},
            {'type': 'text', 'label': 'Item 2: Description', 'width': 4},
            {'type': 'row', 'fields': [
                {'label': 'Date', 'width': 1.5},
                {'label': 'Amount', 'width': 1.5},
            ]},
            {'type': 'text', 'label': 'Item 3: Description', 'width': 4},
            {'type': 'row', 'fields': [
                {'label': 'Date', 'width': 1.5},
                {'label': 'Amount', 'width': 1.5},
            ]},
            {'type': 'text', 'label': 'TOTAL EXPENSES', 'width': 2, 'required': True},
            {'type': 'section', 'label': 'Certification'},
            {'type': 'checkbox', 'label': 'I certify that these expenses are accurate and were incurred for university business.'},
            {'type': 'signature', 'label': 'Employee Signature'},
            {'type': 'signature', 'label': 'Supervisor Approval'},
        ],
        "Attach all original receipts. Expenses over $75 require itemized receipts."
    )

    # 4. Vendor Payment Request
    generator.create_form(
        "vendor-payment-request.pdf",
        "Vendor Payment Request",
        "Business Office",
        [
            {'type': 'section', 'label': 'Requestor Information'},
            {'type': 'row', 'fields': [
                {'label': 'Requested By', 'width': 3},
                {'label': 'Department', 'width': 2.5},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Phone', 'width': 2},
                {'label': 'Email', 'width': 3},
            ]},
            {'type': 'section', 'label': 'Vendor Information'},
            {'type': 'text', 'label': 'Vendor Name', 'width': 5, 'required': True},
            {'type': 'text', 'label': 'Vendor Address', 'width': 5, 'required': True},
            {'type': 'row', 'fields': [
                {'label': 'City', 'width': 2.5},
                {'label': 'State', 'width': 1},
                {'label': 'ZIP', 'width': 1.5},
            ]},
            {'type': 'section', 'label': 'Payment Details'},
            {'type': 'text', 'label': 'Invoice Number', 'width': 2.5},
            {'type': 'date', 'label': 'Invoice Date'},
            {'type': 'text', 'label': 'Description of Goods/Services', 'width': 6, 'required': True},
            {'type': 'text', 'label': 'Amount to Pay', 'width': 2, 'required': True},
            {'type': 'text', 'label': 'Budget Code', 'width': 2.5, 'required': True},
            {'type': 'checkbox', 'label': 'W-9 on file'},
            {'type': 'section', 'label': 'Approvals'},
            {'type': 'signature', 'label': 'Requestor Signature'},
            {'type': 'signature', 'label': 'Budget Manager Approval'},
        ],
        "Attach invoice and any supporting documentation. W-9 must be on file before payment can be processed."
    )

    # 5. Petty Cash Request
    generator.create_form(
        "petty-cash-request.pdf",
        "Petty Cash Request",
        "Business Office",
        [
            {'type': 'section', 'label': 'Requestor Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'Department', 'width': 2.5},
            ]},
            {'type': 'text', 'label': 'Budget Code', 'width': 2.5, 'required': True},
            {'type': 'section', 'label': 'Request Details'},
            {'type': 'date', 'label': 'Date of Request', 'required': True},
            {'type': 'text', 'label': 'Amount Requested', 'width': 2, 'required': True},
            {'type': 'text', 'label': 'Purpose/Description', 'width': 6, 'required': True},
            {'type': 'textarea', 'label': 'Itemized List of Expenses', 'width': 6, 'height': 1},
            {'type': 'section', 'label': 'Reimbursement (Office Use Only)'},
            {'type': 'text', 'label': 'Amount Reimbursed', 'width': 2},
            {'type': 'text', 'label': 'Change Returned', 'width': 2},
            {'type': 'section', 'label': 'Signatures'},
            {'type': 'signature', 'label': 'Requestor Signature'},
            {'type': 'signature', 'label': 'Supervisor Approval'},
            {'type': 'signature', 'label': 'Business Office'},
        ],
        "Petty cash requests are limited to $100. Attach all receipts. Unused funds must be returned within 5 business days."
    )

    # 6. W-9 Request Cover Sheet (actual W-9 is IRS form)
    generator.create_form(
        "w9-request-form.pdf",
        "W-9 Submission Cover Sheet",
        "Business Office",
        [
            {'type': 'section', 'label': 'Vendor/Payee Information'},
            {'type': 'text', 'label': 'Name (as shown on tax return)', 'width': 5, 'required': True},
            {'type': 'text', 'label': 'Business Name (if different)', 'width': 5},
            {'type': 'text', 'label': 'Address', 'width': 5, 'required': True},
            {'type': 'row', 'fields': [
                {'label': 'City', 'width': 2.5},
                {'label': 'State', 'width': 1},
                {'label': 'ZIP', 'width': 1.5},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Phone', 'width': 2.5},
                {'label': 'Email', 'width': 3},
            ]},
            {'type': 'section', 'label': 'Tax Classification'},
            {'type': 'radio', 'label': 'Entity Type', 'options': ['Individual/Sole Proprietor', 'Corporation', 'Partnership', 'LLC', 'Other']},
            {'type': 'section', 'label': 'Department Contact'},
            {'type': 'text', 'label': 'Wiley Contact Name', 'width': 3},
            {'type': 'text', 'label': 'Department', 'width': 3},
            {'type': 'section', 'label': 'Submission'},
            {'type': 'checkbox', 'label': 'IRS Form W-9 attached (required)'},
            {'type': 'date', 'label': 'Date Submitted'},
        ],
        "Attach completed IRS Form W-9. The W-9 must be signed and dated. Download W-9 from www.irs.gov."
    )

    # ==================== FACILITIES MANAGEMENT FORMS ====================

    # 7. Work Order Request
    generator.create_form(
        "work-order-request.pdf",
        "Work Order Request Form",
        "Facilities Management",
        [
            {'type': 'section', 'label': 'Requestor Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'Phone', 'width': 2},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Email', 'width': 3},
                {'label': 'Department', 'width': 2.5},
            ]},
            {'type': 'section', 'label': 'Location'},
            {'type': 'row', 'fields': [
                {'label': 'Building', 'width': 3},
                {'label': 'Room Number', 'width': 1.5},
            ]},
            {'type': 'text', 'label': 'Specific Location Details', 'width': 5},
            {'type': 'section', 'label': 'Service Request'},
            {'type': 'radio', 'label': 'Request Type', 'options': ['Maintenance/Repair', 'Custodial', 'Grounds', 'HVAC', 'Electrical', 'Plumbing', 'Other']},
            {'type': 'radio', 'label': 'Priority', 'options': ['Emergency', 'Urgent (24-48 hrs)', 'Standard (1-2 weeks)', 'Low Priority']},
            {'type': 'textarea', 'label': 'Description of Problem or Request', 'width': 6, 'height': 1.2, 'required': True},
            {'type': 'text', 'label': 'Best Time for Service', 'width': 3},
            {'type': 'section', 'label': 'Approval'},
            {'type': 'signature', 'label': 'Requestor Signature'},
            {'type': 'date', 'label': 'Date Submitted'},
        ],
        "For emergencies (flooding, no heat/AC, safety hazards), call (903) 927-3300 immediately."
    )

    # 8. Key Request Form
    generator.create_form(
        "key-request-form.pdf",
        "Key Request Form",
        "Facilities Management",
        [
            {'type': 'section', 'label': 'Employee Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'Employee ID', 'width': 2},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Department', 'width': 3},
                {'label': 'Position/Title', 'width': 2.5},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Phone', 'width': 2.5},
                {'label': 'Email', 'width': 3},
            ]},
            {'type': 'section', 'label': 'Key Request Details'},
            {'type': 'radio', 'label': 'Request Type', 'options': ['New Key', 'Replacement Key', 'Additional Key', 'Return Key']},
            {'type': 'text', 'label': 'Building Name', 'width': 4, 'required': True},
            {'type': 'text', 'label': 'Room Number(s)', 'width': 3, 'required': True},
            {'type': 'textarea', 'label': 'Justification for Access', 'width': 6, 'height': 0.8, 'required': True},
            {'type': 'section', 'label': 'Approvals'},
            {'type': 'signature', 'label': 'Employee Signature'},
            {'type': 'signature', 'label': 'Department Head/Supervisor Approval'},
            {'type': 'section', 'label': 'Facilities Use Only'},
            {'type': 'text', 'label': 'Key Number Issued', 'width': 2},
            {'type': 'date', 'label': 'Date Issued'},
            {'type': 'signature', 'label': 'Issued By'},
        ],
        "Keys remain property of Wiley University and must be returned upon separation. Lost keys may result in a $50 replacement fee."
    )

    # 9. Space Setup Request
    generator.create_form(
        "space-setup-request.pdf",
        "Space/Room Setup Request",
        "Facilities Management",
        [
            {'type': 'section', 'label': 'Event/Requestor Information'},
            {'type': 'text', 'label': 'Event Name', 'width': 5, 'required': True},
            {'type': 'row', 'fields': [
                {'label': 'Contact Name', 'width': 3},
                {'label': 'Phone', 'width': 2},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Department', 'width': 3},
                {'label': 'Email', 'width': 2.5},
            ]},
            {'type': 'section', 'label': 'Event Details'},
            {'type': 'row', 'fields': [
                {'label': 'Building', 'width': 3},
                {'label': 'Room', 'width': 2},
            ]},
            {'type': 'date', 'label': 'Event Date', 'required': True},
            {'type': 'row', 'fields': [
                {'label': 'Start Time', 'width': 1.5},
                {'label': 'End Time', 'width': 1.5},
            ]},
            {'type': 'text', 'label': 'Expected Attendance', 'width': 1.5},
            {'type': 'section', 'label': 'Setup Requirements'},
            {'type': 'row', 'fields': [
                {'label': 'Chairs Needed', 'width': 1.5},
                {'label': 'Tables Needed', 'width': 1.5},
            ]},
            {'type': 'radio', 'label': 'Table Arrangement', 'options': ['Classroom Style', 'Conference Style', 'Banquet/Rounds', 'Theater Style', 'U-Shape', 'Other']},
            {'type': 'textarea', 'label': 'Special Setup Instructions', 'width': 6, 'height': 0.8},
            {'type': 'checkbox', 'label': 'Podium/Lectern needed'},
            {'type': 'checkbox', 'label': 'AV Equipment needed (contact IT separately)'},
            {'type': 'section', 'label': 'Approval'},
            {'type': 'signature', 'label': 'Requestor Signature'},
            {'type': 'date', 'label': 'Date Submitted'},
        ],
        "Submit requests at least 5 business days before the event. Large events may require additional lead time."
    )

    # 10. Moving Request Form
    generator.create_form(
        "moving-request-form.pdf",
        "Moving/Relocation Request",
        "Facilities Management",
        [
            {'type': 'section', 'label': 'Requestor Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'Phone', 'width': 2},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Department', 'width': 3},
                {'label': 'Email', 'width': 2.5},
            ]},
            {'type': 'section', 'label': 'Move Details'},
            {'type': 'text', 'label': 'Current Location (Building/Room)', 'width': 4, 'required': True},
            {'type': 'text', 'label': 'New Location (Building/Room)', 'width': 4, 'required': True},
            {'type': 'date', 'label': 'Requested Move Date', 'required': True},
            {'type': 'section', 'label': 'Items to be Moved'},
            {'type': 'checkbox', 'label': 'Desk/Workstation'},
            {'type': 'checkbox', 'label': 'File Cabinets'},
            {'type': 'checkbox', 'label': 'Bookcases'},
            {'type': 'checkbox', 'label': 'Computer Equipment (coordinate with IT)'},
            {'type': 'checkbox', 'label': 'Boxes/Personal Items'},
            {'type': 'textarea', 'label': 'Other Items (please list)', 'width': 6, 'height': 0.6},
            {'type': 'textarea', 'label': 'Special Instructions', 'width': 6, 'height': 0.6},
            {'type': 'section', 'label': 'Approvals'},
            {'type': 'signature', 'label': 'Requestor Signature'},
            {'type': 'signature', 'label': 'Current Location Supervisor'},
            {'type': 'signature', 'label': 'New Location Supervisor'},
        ],
        "Submit requests at least 2 weeks in advance. Computer/phone moves must be coordinated with IT."
    )

    # ==================== FINANCIAL AID FORMS ====================

    # 11. Verification Worksheet
    generator.create_form(
        "verification-worksheet.pdf",
        "Verification Worksheet",
        "Financial Aid",
        [
            {'type': 'section', 'label': 'Student Information'},
            {'type': 'row', 'fields': [
                {'label': 'Student Name', 'width': 3},
                {'label': 'Student ID', 'width': 2},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Date of Birth', 'width': 2},
                {'label': 'Phone', 'width': 2},
            ]},
            {'type': 'text', 'label': 'Email Address', 'width': 4, 'required': True},
            {'type': 'section', 'label': 'Household Information'},
            {'type': 'text', 'label': 'Number in Household', 'width': 1.5, 'required': True},
            {'type': 'text', 'label': 'Number in College (at least half-time)', 'width': 2, 'required': True},
            {'type': 'textarea', 'label': 'List all household members', 'width': 6, 'height': 1},
            {'type': 'section', 'label': 'Income Information'},
            {'type': 'text', 'label': "Student's AGI (from tax return)", 'width': 2.5},
            {'type': 'text', 'label': "Parent's AGI (if dependent)", 'width': 2.5},
            {'type': 'text', 'label': 'Income Earned from Work (Student)', 'width': 2.5},
            {'type': 'text', 'label': 'Income Earned from Work (Spouse)', 'width': 2.5},
            {'type': 'section', 'label': 'Required Documents'},
            {'type': 'checkbox', 'label': 'IRS Tax Return Transcript or signed tax return'},
            {'type': 'checkbox', 'label': 'W-2 forms for all employers'},
            {'type': 'checkbox', 'label': 'Proof of other untaxed income'},
            {'type': 'section', 'label': 'Certification'},
            {'type': 'checkbox', 'label': 'I certify that all information is true and complete.'},
            {'type': 'signature', 'label': 'Student Signature'},
            {'type': 'signature', 'label': 'Parent Signature (if dependent)'},
        ],
        "You have been selected for verification. Complete this form and submit all required documents within 30 days."
    )

    # 12. Dependency Override Appeal
    generator.create_form(
        "dependency-override-appeal.pdf",
        "Dependency Override Appeal",
        "Financial Aid",
        [
            {'type': 'section', 'label': 'Student Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'Student ID', 'width': 2},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Date of Birth', 'width': 2},
                {'label': 'Phone', 'width': 2},
            ]},
            {'type': 'text', 'label': 'Current Address', 'width': 5},
            {'type': 'text', 'label': 'Email', 'width': 4, 'required': True},
            {'type': 'section', 'label': 'Reason for Appeal'},
            {'type': 'radio', 'label': 'Primary Reason', 'options': ['Parental abandonment', 'Abusive family situation', 'Unable to locate parents', 'Other unusual circumstances']},
            {'type': 'textarea', 'label': 'Detailed Explanation of Circumstances', 'width': 6, 'height': 1.5, 'required': True},
            {'type': 'section', 'label': 'Supporting Documentation (Required)'},
            {'type': 'checkbox', 'label': 'Third-party statement (counselor, clergy, social worker, etc.)'},
            {'type': 'checkbox', 'label': 'Court documents (if applicable)'},
            {'type': 'checkbox', 'label': 'Other documentation (describe):'},
            {'type': 'text', 'label': 'Other Documentation Description', 'width': 5},
            {'type': 'section', 'label': 'Certification'},
            {'type': 'checkbox', 'label': 'I certify all information is true and accurate.'},
            {'type': 'signature', 'label': 'Student Signature'},
            {'type': 'date', 'label': 'Date'},
        ],
        "This form is for students seeking independent status due to unusual circumstances. All appeals require documentation."
    )

    # 13. SAP Appeal Form
    generator.create_form(
        "sap-appeal-form.pdf",
        "Satisfactory Academic Progress (SAP) Appeal",
        "Financial Aid",
        [
            {'type': 'section', 'label': 'Student Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'Student ID', 'width': 2},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Phone', 'width': 2},
                {'label': 'Email', 'width': 3},
            ]},
            {'type': 'text', 'label': 'Major/Program', 'width': 4},
            {'type': 'section', 'label': 'SAP Status'},
            {'type': 'radio', 'label': 'Reason for SAP Failure', 'options': ['GPA below 2.0', 'Completion rate below 67%', 'Maximum timeframe exceeded', 'Multiple reasons']},
            {'type': 'section', 'label': 'Extenuating Circumstances'},
            {'type': 'textarea', 'label': 'Explain the circumstances that led to your academic difficulty', 'width': 6, 'height': 1.2, 'required': True},
            {'type': 'textarea', 'label': 'What has changed that will allow you to succeed?', 'width': 6, 'height': 1, 'required': True},
            {'type': 'section', 'label': 'Documentation Required'},
            {'type': 'checkbox', 'label': 'Medical documentation (illness or injury)'},
            {'type': 'checkbox', 'label': 'Death certificate (family death)'},
            {'type': 'checkbox', 'label': 'Other supporting documentation'},
            {'type': 'section', 'label': 'Academic Plan'},
            {'type': 'checkbox', 'label': 'I agree to meet with an academic advisor'},
            {'type': 'checkbox', 'label': 'I commit to following my academic improvement plan'},
            {'type': 'signature', 'label': 'Student Signature'},
            {'type': 'date', 'label': 'Date'},
        ],
        "Complete this form if you have lost financial aid eligibility due to not meeting SAP requirements."
    )

    # 14. Special Circumstances Form
    generator.create_form(
        "special-circumstances-form.pdf",
        "Special Circumstances Form",
        "Financial Aid",
        [
            {'type': 'section', 'label': 'Student Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'Student ID', 'width': 2},
            ]},
            {'type': 'text', 'label': 'Email', 'width': 4, 'required': True},
            {'type': 'text', 'label': 'Phone', 'width': 2.5},
            {'type': 'section', 'label': 'Reason for Request'},
            {'type': 'checkbox', 'label': 'Loss of employment'},
            {'type': 'checkbox', 'label': 'Reduction in income'},
            {'type': 'checkbox', 'label': 'Divorce or separation'},
            {'type': 'checkbox', 'label': 'Death of parent or spouse'},
            {'type': 'checkbox', 'label': 'Unusually high medical expenses'},
            {'type': 'checkbox', 'label': 'One-time income on tax return'},
            {'type': 'checkbox', 'label': 'Other (explain below)'},
            {'type': 'section', 'label': 'Explanation'},
            {'type': 'textarea', 'label': 'Describe your special circumstances in detail', 'width': 6, 'height': 1.5, 'required': True},
            {'type': 'section', 'label': 'Income Changes'},
            {'type': 'text', 'label': 'Previous Annual Income', 'width': 2.5},
            {'type': 'text', 'label': 'Current/Expected Annual Income', 'width': 2.5},
            {'type': 'section', 'label': 'Required Documentation'},
            {'type': 'checkbox', 'label': 'Tax returns/transcripts'},
            {'type': 'checkbox', 'label': 'Termination letter or unemployment documentation'},
            {'type': 'checkbox', 'label': 'Divorce decree or separation agreement'},
            {'type': 'checkbox', 'label': 'Death certificate'},
            {'type': 'checkbox', 'label': 'Medical bills/documentation'},
            {'type': 'signature', 'label': 'Student Signature'},
            {'type': 'date', 'label': 'Date'},
        ],
        "Submit this form if your family's financial situation has changed significantly since filing the FAFSA."
    )

    # 15. Scholarship Application
    generator.create_form(
        "scholarship-application.pdf",
        "Institutional Scholarship Application",
        "Financial Aid",
        [
            {'type': 'section', 'label': 'Student Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'Student ID', 'width': 2},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Date of Birth', 'width': 2},
                {'label': 'Classification', 'width': 2},
            ]},
            {'type': 'text', 'label': 'Major', 'width': 3, 'required': True},
            {'type': 'text', 'label': 'Email', 'width': 4, 'required': True},
            {'type': 'text', 'label': 'Current GPA', 'width': 1.5, 'required': True},
            {'type': 'section', 'label': 'Scholarship Selection'},
            {'type': 'checkbox', 'label': 'Academic Excellence Scholarship'},
            {'type': 'checkbox', 'label': 'Leadership Scholarship'},
            {'type': 'checkbox', 'label': 'Community Service Scholarship'},
            {'type': 'checkbox', 'label': 'Departmental Scholarship'},
            {'type': 'checkbox', 'label': 'Need-Based Scholarship'},
            {'type': 'section', 'label': 'Essay (500 words or less)'},
            {'type': 'textarea', 'label': 'Describe your academic goals and why you deserve this scholarship', 'width': 6, 'height': 2, 'required': True},
            {'type': 'section', 'label': 'Activities and Leadership'},
            {'type': 'textarea', 'label': 'List extracurricular activities, leadership roles, and community service', 'width': 6, 'height': 1.2},
            {'type': 'section', 'label': 'Certification'},
            {'type': 'checkbox', 'label': 'I certify all information is accurate', 'required': True},
            {'type': 'checkbox', 'label': 'I have filed a FAFSA for the current year', 'required': True},
            {'type': 'signature', 'label': 'Student Signature'},
            {'type': 'date', 'label': 'Date'},
        ],
        "Complete FAFSA before applying. Include two letters of recommendation and official transcripts."
    )

    # ==================== STUDENT ACCOUNTS FORMS ====================

    # 16. Payment Plan Enrollment
    generator.create_form(
        "payment-plan-enrollment.pdf",
        "Payment Plan Enrollment",
        "Student Accounts",
        [
            {'type': 'section', 'label': 'Student Information'},
            {'type': 'row', 'fields': [
                {'label': 'Student Name', 'width': 3},
                {'label': 'Student ID', 'width': 2},
            ]},
            {'type': 'text', 'label': 'Email', 'width': 4, 'required': True},
            {'type': 'text', 'label': 'Phone', 'width': 2.5, 'required': True},
            {'type': 'section', 'label': 'Semester'},
            {'type': 'radio', 'label': 'Enrollment Term', 'options': ['Fall', 'Spring', 'Summer']},
            {'type': 'text', 'label': 'Academic Year', 'width': 1.5},
            {'type': 'section', 'label': 'Payment Plan Selection'},
            {'type': 'radio', 'label': 'Plan Type', 'options': ['3-Month Plan ($50 enrollment fee)', '4-Month Plan ($50 enrollment fee)', '5-Month Plan ($75 enrollment fee)']},
            {'type': 'text', 'label': 'Total Balance to be Financed', 'width': 2.5, 'required': True},
            {'type': 'section', 'label': 'Payment Method'},
            {'type': 'radio', 'label': 'Auto-Pay Method', 'options': ['Credit/Debit Card', 'Bank Account (ACH)', 'Manual Payment Each Month']},
            {'type': 'section', 'label': 'Agreement'},
            {'type': 'checkbox', 'label': 'I understand a $50-$75 non-refundable enrollment fee is required'},
            {'type': 'checkbox', 'label': 'I understand late payments may result in a $25 late fee'},
            {'type': 'checkbox', 'label': 'I understand failure to pay may result in holds on my account'},
            {'type': 'checkbox', 'label': 'I agree to the payment plan terms and conditions'},
            {'type': 'signature', 'label': 'Student Signature'},
            {'type': 'date', 'label': 'Date'},
        ],
        "Payment plans must be established before classes begin. A non-refundable enrollment fee applies."
    )

    # 17. Third-Party Billing Authorization
    generator.create_form(
        "third-party-billing.pdf",
        "Third-Party Billing Authorization",
        "Student Accounts",
        [
            {'type': 'section', 'label': 'Student Information'},
            {'type': 'row', 'fields': [
                {'label': 'Student Name', 'width': 3},
                {'label': 'Student ID', 'width': 2},
            ]},
            {'type': 'text', 'label': 'Email', 'width': 4, 'required': True},
            {'type': 'text', 'label': 'Phone', 'width': 2.5},
            {'type': 'section', 'label': 'Third-Party Sponsor Information'},
            {'type': 'text', 'label': 'Company/Organization Name', 'width': 5, 'required': True},
            {'type': 'text', 'label': 'Billing Contact Name', 'width': 4},
            {'type': 'text', 'label': 'Address', 'width': 5, 'required': True},
            {'type': 'row', 'fields': [
                {'label': 'City', 'width': 2.5},
                {'label': 'State', 'width': 1},
                {'label': 'ZIP', 'width': 1.5},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Phone', 'width': 2.5},
                {'label': 'Email', 'width': 3},
            ]},
            {'type': 'section', 'label': 'Billing Details'},
            {'type': 'text', 'label': 'Authorization/Voucher Number', 'width': 3},
            {'type': 'text', 'label': 'Maximum Amount Authorized', 'width': 2.5, 'required': True},
            {'type': 'checkbox', 'label': 'Tuition'},
            {'type': 'checkbox', 'label': 'Fees'},
            {'type': 'checkbox', 'label': 'Books'},
            {'type': 'checkbox', 'label': 'Housing'},
            {'type': 'checkbox', 'label': 'Meal Plan'},
            {'type': 'section', 'label': 'Student Responsibility'},
            {'type': 'checkbox', 'label': 'I understand I am responsible for any balance not covered by the sponsor'},
            {'type': 'signature', 'label': 'Student Signature'},
            {'type': 'date', 'label': 'Date'},
        ],
        "Attach the official authorization letter or voucher from your sponsor. Submit before the payment deadline."
    )

    # 18. Tuition Appeal Form
    generator.create_form(
        "tuition-appeal-form.pdf",
        "Tuition/Fee Appeal Form",
        "Student Accounts",
        [
            {'type': 'section', 'label': 'Student Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'Student ID', 'width': 2},
            ]},
            {'type': 'text', 'label': 'Email', 'width': 4, 'required': True},
            {'type': 'text', 'label': 'Phone', 'width': 2.5},
            {'type': 'section', 'label': 'Appeal Details'},
            {'type': 'text', 'label': 'Semester/Term', 'width': 2, 'required': True},
            {'type': 'text', 'label': 'Amount in Dispute', 'width': 2, 'required': True},
            {'type': 'radio', 'label': 'Type of Appeal', 'options': ['Late fee', 'Tuition charges', 'Course fees', 'Housing charges', 'Other fees']},
            {'type': 'textarea', 'label': 'Explanation of Appeal', 'width': 6, 'height': 1.5, 'required': True},
            {'type': 'section', 'label': 'Documentation'},
            {'type': 'checkbox', 'label': 'Medical documentation'},
            {'type': 'checkbox', 'label': 'Military orders'},
            {'type': 'checkbox', 'label': 'Employer documentation'},
            {'type': 'checkbox', 'label': 'Other (describe):'},
            {'type': 'text', 'label': 'Other Documentation', 'width': 4},
            {'type': 'section', 'label': 'Certification'},
            {'type': 'checkbox', 'label': 'I certify all information is accurate and complete'},
            {'type': 'signature', 'label': 'Student Signature'},
            {'type': 'date', 'label': 'Date'},
        ],
        "Appeals must be submitted within 30 days of the charge. Include all supporting documentation."
    )

    # 19. 1098-T Consent Form
    generator.create_form(
        "1098t-consent-form.pdf",
        "1098-T Electronic Consent Form",
        "Student Accounts",
        [
            {'type': 'section', 'label': 'Student Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'Student ID', 'width': 2},
            ]},
            {'type': 'text', 'label': 'Social Security Number (last 4 digits)', 'width': 2},
            {'type': 'text', 'label': 'Email', 'width': 4, 'required': True},
            {'type': 'section', 'label': 'Consent Selection'},
            {'type': 'radio', 'label': 'I elect to', 'options': ['Receive my 1098-T electronically', 'Receive my 1098-T by mail', 'Withdraw previous consent for electronic delivery']},
            {'type': 'section', 'label': 'Electronic Delivery Agreement'},
            {'type': 'checkbox', 'label': 'I understand the 1098-T will be available through MyWiley Portal'},
            {'type': 'checkbox', 'label': 'I will receive an email notification when the form is available'},
            {'type': 'checkbox', 'label': 'I can withdraw consent at any time'},
            {'type': 'checkbox', 'label': 'I understand I need software to view/print PDF documents'},
            {'type': 'section', 'label': 'Certification'},
            {'type': 'checkbox', 'label': 'I certify this is my valid email address and I consent to electronic delivery', 'required': True},
            {'type': 'signature', 'label': 'Student Signature'},
            {'type': 'date', 'label': 'Date'},
        ],
        "The 1098-T reports qualified tuition and related expenses for tax purposes. Forms are available by January 31."
    )

    # ==================== RISK MANAGEMENT FORMS ====================

    # 20. Incident/Accident Report
    generator.create_form(
        "incident-accident-report.pdf",
        "Incident/Accident Report",
        "Risk Management",
        [
            {'type': 'section', 'label': 'Report Information'},
            {'type': 'date', 'label': 'Date of Incident', 'required': True},
            {'type': 'text', 'label': 'Time of Incident', 'width': 1.5, 'required': True},
            {'type': 'text', 'label': 'Location (Building/Room/Area)', 'width': 5, 'required': True},
            {'type': 'section', 'label': 'Person Reporting'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'Phone', 'width': 2},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Department', 'width': 3},
                {'label': 'Email', 'width': 2.5},
            ]},
            {'type': 'section', 'label': 'Person(s) Involved'},
            {'type': 'text', 'label': 'Name', 'width': 3},
            {'type': 'radio', 'label': 'Status', 'options': ['Student', 'Employee', 'Visitor', 'Contractor']},
            {'type': 'text', 'label': 'Contact Phone', 'width': 2.5},
            {'type': 'section', 'label': 'Incident Details'},
            {'type': 'radio', 'label': 'Type of Incident', 'options': ['Injury/Accident', 'Property Damage', 'Near Miss', 'Theft', 'Other']},
            {'type': 'textarea', 'label': 'Description of Incident', 'width': 6, 'height': 1.5, 'required': True},
            {'type': 'section', 'label': 'Injury Information (if applicable)'},
            {'type': 'textarea', 'label': 'Describe injuries sustained', 'width': 6, 'height': 0.8},
            {'type': 'radio', 'label': 'Medical Treatment', 'options': ['None', 'First Aid', 'Doctor/Clinic', 'Emergency Room', 'Hospitalized']},
            {'type': 'section', 'label': 'Witnesses'},
            {'type': 'text', 'label': 'Witness 1 Name and Phone', 'width': 5},
            {'type': 'text', 'label': 'Witness 2 Name and Phone', 'width': 5},
            {'type': 'signature', 'label': 'Signature of Person Reporting'},
            {'type': 'date', 'label': 'Date Reported'},
        ],
        "Report all incidents within 24 hours. For emergencies, call 911 first, then Campus Security at (903) 927-3310."
    )

    # 21. Vehicle Use Request
    generator.create_form(
        "vehicle-use-request.pdf",
        "University Vehicle Use Request",
        "Risk Management",
        [
            {'type': 'section', 'label': 'Driver Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'Employee ID', 'width': 2},
            ]},
            {'type': 'text', 'label': 'Department', 'width': 3, 'required': True},
            {'type': 'row', 'fields': [
                {'label': "Driver's License Number", 'width': 2.5},
                {'label': 'State', 'width': 1},
                {'label': 'Expiration', 'width': 1.5},
            ]},
            {'type': 'section', 'label': 'Trip Details'},
            {'type': 'text', 'label': 'Purpose of Trip', 'width': 5, 'required': True},
            {'type': 'text', 'label': 'Destination', 'width': 4, 'required': True},
            {'type': 'date', 'label': 'Departure Date', 'required': True},
            {'type': 'date', 'label': 'Return Date', 'required': True},
            {'type': 'text', 'label': 'Number of Passengers', 'width': 1.5},
            {'type': 'section', 'label': 'Vehicle Preference'},
            {'type': 'radio', 'label': 'Vehicle Type', 'options': ['Sedan', 'SUV', 'Van (7 passengers)', 'Van (15 passengers)', 'No Preference']},
            {'type': 'section', 'label': 'Driver Certification'},
            {'type': 'checkbox', 'label': 'I have a valid driver license'},
            {'type': 'checkbox', 'label': 'I have completed driver authorization training'},
            {'type': 'checkbox', 'label': 'I have no DUI/DWI convictions in the past 5 years'},
            {'type': 'checkbox', 'label': 'I agree to follow all university vehicle policies'},
            {'type': 'signature', 'label': 'Driver Signature'},
            {'type': 'signature', 'label': 'Supervisor Approval'},
        ],
        "Requests must be submitted at least 3 business days in advance. Driver must be authorized."
    )

    # 22. Insurance Certificate Request
    generator.create_form(
        "insurance-certificate-request.pdf",
        "Certificate of Insurance Request",
        "Risk Management",
        [
            {'type': 'section', 'label': 'Requestor Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'Department', 'width': 2.5},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Phone', 'width': 2},
                {'label': 'Email', 'width': 3},
            ]},
            {'type': 'section', 'label': 'Certificate Holder Information'},
            {'type': 'text', 'label': 'Organization/Company Name', 'width': 5, 'required': True},
            {'type': 'text', 'label': 'Contact Name', 'width': 4},
            {'type': 'text', 'label': 'Address', 'width': 5, 'required': True},
            {'type': 'row', 'fields': [
                {'label': 'City', 'width': 2.5},
                {'label': 'State', 'width': 1},
                {'label': 'ZIP', 'width': 1.5},
            ]},
            {'type': 'text', 'label': 'Email (for delivery)', 'width': 4},
            {'type': 'section', 'label': 'Certificate Details'},
            {'type': 'text', 'label': 'Purpose/Event Name', 'width': 5, 'required': True},
            {'type': 'text', 'label': 'Event Location', 'width': 4},
            {'type': 'row', 'fields': [
                {'label': 'Event Date', 'width': 2},
                {'label': 'Date Needed By', 'width': 2},
            ]},
            {'type': 'checkbox', 'label': 'Additional Insured status required'},
            {'type': 'textarea', 'label': 'Special Requirements or Coverage Needed', 'width': 6, 'height': 0.8},
            {'type': 'signature', 'label': 'Requestor Signature'},
            {'type': 'date', 'label': 'Date'},
        ],
        "Allow 5-7 business days for processing. Rush requests may require additional approval."
    )

    # 23. Liability Waiver Template
    generator.create_form(
        "liability-waiver.pdf",
        "Liability Waiver and Release",
        "Risk Management",
        [
            {'type': 'section', 'label': 'Event Information'},
            {'type': 'text', 'label': 'Event/Activity Name', 'width': 5, 'required': True},
            {'type': 'date', 'label': 'Event Date', 'required': True},
            {'type': 'text', 'label': 'Location', 'width': 4},
            {'type': 'text', 'label': 'Sponsoring Department', 'width': 4},
            {'type': 'section', 'label': 'Participant Information'},
            {'type': 'text', 'label': 'Participant Name (Print)', 'width': 4, 'required': True},
            {'type': 'date', 'label': 'Date of Birth'},
            {'type': 'text', 'label': 'Address', 'width': 5},
            {'type': 'row', 'fields': [
                {'label': 'City', 'width': 2.5},
                {'label': 'State', 'width': 1},
                {'label': 'ZIP', 'width': 1.5},
            ]},
            {'type': 'text', 'label': 'Emergency Contact Name', 'width': 3, 'required': True},
            {'type': 'text', 'label': 'Emergency Contact Phone', 'width': 2.5, 'required': True},
            {'type': 'section', 'label': 'Waiver and Release'},
            {'type': 'checkbox', 'label': 'I understand and acknowledge the risks associated with this activity'},
            {'type': 'checkbox', 'label': 'I release Wiley University from liability for injuries'},
            {'type': 'checkbox', 'label': 'I consent to emergency medical treatment if necessary'},
            {'type': 'checkbox', 'label': 'I grant permission for photos/videos to be used for university purposes'},
            {'type': 'section', 'label': 'Signature'},
            {'type': 'signature', 'label': 'Participant Signature (or Parent/Guardian if under 18)'},
            {'type': 'date', 'label': 'Date'},
            {'type': 'text', 'label': 'Printed Name of Parent/Guardian (if minor)', 'width': 4},
        ],
        "Read carefully before signing. Participants under 18 require parent/guardian signature."
    )

    # ==================== TRANSPORTATION & FLEET FORMS ====================

    # 24. Parking Permit Application
    generator.create_form(
        "parking-permit-application.pdf",
        "Parking Permit Application",
        "Transportation & Fleet",
        [
            {'type': 'section', 'label': 'Applicant Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'ID Number', 'width': 2},
            ]},
            {'type': 'radio', 'label': 'Status', 'options': ['Student', 'Faculty', 'Staff']},
            {'type': 'row', 'fields': [
                {'label': 'Phone', 'width': 2.5},
                {'label': 'Email', 'width': 3},
            ]},
            {'type': 'section', 'label': 'Vehicle Information'},
            {'type': 'row', 'fields': [
                {'label': 'Make', 'width': 2},
                {'label': 'Model', 'width': 2},
                {'label': 'Year', 'width': 1},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Color', 'width': 1.5},
                {'label': 'License Plate', 'width': 2},
                {'label': 'State', 'width': 1},
            ]},
            {'type': 'section', 'label': 'Permit Type'},
            {'type': 'radio', 'label': 'Select Permit', 'options': ['Student General ($100/year)', 'Student Resident ($150/year)', 'Faculty/Staff ($75/year)', 'Motorcycle ($50/year)']},
            {'type': 'section', 'label': 'Agreement'},
            {'type': 'checkbox', 'label': 'I have read and agree to the parking rules and regulations'},
            {'type': 'checkbox', 'label': 'I understand parking citations are my responsibility'},
            {'type': 'checkbox', 'label': 'I understand the permit must be displayed at all times'},
            {'type': 'signature', 'label': 'Applicant Signature'},
            {'type': 'date', 'label': 'Date'},
        ],
        "Permits are valid for the academic year (Aug-May). Vehicle registration required."
    )

    # 25. Citation Appeal Form
    generator.create_form(
        "citation-appeal-form.pdf",
        "Parking Citation Appeal Form",
        "Transportation & Fleet",
        [
            {'type': 'section', 'label': 'Citation Information'},
            {'type': 'text', 'label': 'Citation Number', 'width': 2.5, 'required': True},
            {'type': 'date', 'label': 'Citation Date', 'required': True},
            {'type': 'text', 'label': 'License Plate Number', 'width': 2.5},
            {'type': 'text', 'label': 'Citation Amount', 'width': 1.5},
            {'type': 'section', 'label': 'Appellant Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'ID Number', 'width': 2},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Phone', 'width': 2.5},
                {'label': 'Email', 'width': 3},
            ]},
            {'type': 'section', 'label': 'Reason for Appeal'},
            {'type': 'checkbox', 'label': 'Valid permit was displayed'},
            {'type': 'checkbox', 'label': 'Signage was unclear or missing'},
            {'type': 'checkbox', 'label': 'Vehicle was broken down/emergency'},
            {'type': 'checkbox', 'label': 'Citation was issued in error'},
            {'type': 'checkbox', 'label': 'Medical emergency'},
            {'type': 'checkbox', 'label': 'Other'},
            {'type': 'textarea', 'label': 'Detailed Explanation', 'width': 6, 'height': 1.2, 'required': True},
            {'type': 'section', 'label': 'Supporting Documentation'},
            {'type': 'checkbox', 'label': 'Photos attached'},
            {'type': 'checkbox', 'label': 'Medical documentation attached'},
            {'type': 'checkbox', 'label': 'Other documentation attached'},
            {'type': 'signature', 'label': 'Appellant Signature'},
            {'type': 'date', 'label': 'Date'},
        ],
        "Appeals must be submitted within 14 days of citation. Attach any supporting documentation."
    )

    # 26. Vehicle Reservation Request
    generator.create_form(
        "vehicle-reservation-request.pdf",
        "Fleet Vehicle Reservation Request",
        "Transportation & Fleet",
        [
            {'type': 'section', 'label': 'Requestor Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'Employee ID', 'width': 2},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Department', 'width': 3},
                {'label': 'Phone', 'width': 2},
            ]},
            {'type': 'text', 'label': 'Email', 'width': 4, 'required': True},
            {'type': 'section', 'label': 'Trip Details'},
            {'type': 'text', 'label': 'Purpose of Trip', 'width': 5, 'required': True},
            {'type': 'text', 'label': 'Destination', 'width': 4, 'required': True},
            {'type': 'row', 'fields': [
                {'label': 'Departure Date', 'width': 2},
                {'label': 'Departure Time', 'width': 1.5},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Return Date', 'width': 2},
                {'label': 'Return Time', 'width': 1.5},
            ]},
            {'type': 'text', 'label': 'Number of Passengers', 'width': 1.5},
            {'type': 'text', 'label': 'Estimated Miles', 'width': 1.5},
            {'type': 'section', 'label': 'Vehicle Type Requested'},
            {'type': 'radio', 'label': 'Vehicle Preference', 'options': ['Sedan (4 passengers)', 'SUV (6 passengers)', '8-Passenger Van', '12-Passenger Van', '15-Passenger Van']},
            {'type': 'section', 'label': 'Driver Information'},
            {'type': 'text', 'label': 'Primary Driver Name', 'width': 4, 'required': True},
            {'type': 'checkbox', 'label': 'Driver is authorized (completed training)'},
            {'type': 'text', 'label': 'Additional Driver Name', 'width': 4},
            {'type': 'section', 'label': 'Approvals'},
            {'type': 'signature', 'label': 'Requestor Signature'},
            {'type': 'signature', 'label': 'Supervisor Approval'},
        ],
        "Request vehicles at least 5 business days in advance. All drivers must be pre-authorized."
    )

    # 27. Driver Authorization Form
    generator.create_form(
        "driver-authorization-form.pdf",
        "Driver Authorization Form",
        "Transportation & Fleet",
        [
            {'type': 'section', 'label': 'Employee Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'Employee ID', 'width': 2},
            ]},
            {'type': 'text', 'label': 'Department', 'width': 3, 'required': True},
            {'type': 'row', 'fields': [
                {'label': 'Phone', 'width': 2},
                {'label': 'Email', 'width': 3},
            ]},
            {'type': 'section', 'label': "Driver's License Information"},
            {'type': 'text', 'label': "Driver's License Number", 'width': 3, 'required': True},
            {'type': 'row', 'fields': [
                {'label': 'State Issued', 'width': 1.5},
                {'label': 'Expiration Date', 'width': 2},
            ]},
            {'type': 'text', 'label': 'License Class', 'width': 1.5},
            {'type': 'section', 'label': 'Driving Record Certification'},
            {'type': 'checkbox', 'label': 'I have a valid driver license'},
            {'type': 'checkbox', 'label': 'I have NOT had my license suspended/revoked in the past 3 years'},
            {'type': 'checkbox', 'label': 'I have NOT had a DUI/DWI conviction in the past 5 years'},
            {'type': 'checkbox', 'label': 'I have NOT had more than 2 moving violations in the past 3 years'},
            {'type': 'checkbox', 'label': 'I have NOT been at fault in more than 1 accident in the past 3 years'},
            {'type': 'section', 'label': 'Training'},
            {'type': 'checkbox', 'label': 'I have completed defensive driving training'},
            {'type': 'date', 'label': 'Training Completion Date'},
            {'type': 'checkbox', 'label': 'I have read and understand the University Vehicle Policy'},
            {'type': 'section', 'label': 'Agreement'},
            {'type': 'checkbox', 'label': 'I authorize Wiley University to obtain my driving record', 'required': True},
            {'type': 'checkbox', 'label': 'I agree to notify Risk Management of any changes to my driving status'},
            {'type': 'signature', 'label': 'Employee Signature'},
            {'type': 'date', 'label': 'Date'},
            {'type': 'signature', 'label': 'Supervisor Approval'},
        ],
        "Complete this form annually to maintain driver authorization. Driving record check is required."
    )

    # ==================== INFORMATION TECHNOLOGY FORMS ====================

    # 28. Equipment Checkout Request
    generator.create_form(
        "equipment-checkout-request.pdf",
        "IT Equipment Checkout Request",
        "Information Technology",
        [
            {'type': 'section', 'label': 'Requestor Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'ID Number', 'width': 2},
            ]},
            {'type': 'radio', 'label': 'Status', 'options': ['Student', 'Faculty', 'Staff']},
            {'type': 'row', 'fields': [
                {'label': 'Department', 'width': 3},
                {'label': 'Phone', 'width': 2},
            ]},
            {'type': 'text', 'label': 'Email', 'width': 4, 'required': True},
            {'type': 'section', 'label': 'Equipment Requested'},
            {'type': 'checkbox', 'label': 'Laptop'},
            {'type': 'checkbox', 'label': 'Projector'},
            {'type': 'checkbox', 'label': 'Camera/Video Camera'},
            {'type': 'checkbox', 'label': 'Audio Equipment'},
            {'type': 'checkbox', 'label': 'Presentation Remote'},
            {'type': 'checkbox', 'label': 'Other (specify):'},
            {'type': 'text', 'label': 'Other Equipment', 'width': 4},
            {'type': 'section', 'label': 'Checkout Details'},
            {'type': 'date', 'label': 'Pickup Date', 'required': True},
            {'type': 'date', 'label': 'Return Date', 'required': True},
            {'type': 'text', 'label': 'Purpose/Event', 'width': 5, 'required': True},
            {'type': 'section', 'label': 'Agreement'},
            {'type': 'checkbox', 'label': 'I accept responsibility for the equipment while in my possession'},
            {'type': 'checkbox', 'label': 'I will return equipment by the due date'},
            {'type': 'checkbox', 'label': 'I understand I may be charged for lost/damaged equipment'},
            {'type': 'signature', 'label': 'Signature'},
            {'type': 'date', 'label': 'Date'},
            {'type': 'section', 'label': 'IT Use Only'},
            {'type': 'text', 'label': 'Equipment Tag Number', 'width': 2.5},
            {'type': 'signature', 'label': 'Checked Out By'},
        ],
        "Equipment must be returned by 5:00 PM on the return date. Late returns may result in restricted borrowing privileges."
    )

    # 29. Software Request
    generator.create_form(
        "software-request.pdf",
        "Software Request Form",
        "Information Technology",
        [
            {'type': 'section', 'label': 'Requestor Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'Employee ID', 'width': 2},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Department', 'width': 3},
                {'label': 'Phone', 'width': 2},
            ]},
            {'type': 'text', 'label': 'Email', 'width': 4, 'required': True},
            {'type': 'section', 'label': 'Computer Information'},
            {'type': 'text', 'label': 'Computer Name/Asset Tag', 'width': 3},
            {'type': 'text', 'label': 'Location (Building/Room)', 'width': 3},
            {'type': 'section', 'label': 'Software Requested'},
            {'type': 'text', 'label': 'Software Name', 'width': 4, 'required': True},
            {'type': 'text', 'label': 'Version (if specific)', 'width': 2},
            {'type': 'text', 'label': 'Vendor/Publisher', 'width': 3},
            {'type': 'radio', 'label': 'License Type', 'options': ['Free/Open Source', 'University-Licensed', 'Needs Purchase', 'Unknown']},
            {'type': 'textarea', 'label': 'Business Justification', 'width': 6, 'height': 1, 'required': True},
            {'type': 'section', 'label': 'Funding (if purchase required)'},
            {'type': 'text', 'label': 'Budget Code', 'width': 2.5},
            {'type': 'text', 'label': 'Estimated Cost', 'width': 2},
            {'type': 'section', 'label': 'Approvals'},
            {'type': 'signature', 'label': 'Requestor Signature'},
            {'type': 'signature', 'label': 'Supervisor Approval'},
            {'type': 'signature', 'label': 'Budget Manager (if purchase)'},
        ],
        "Allow 3-5 business days for software installation. Purchases require budget manager approval."
    )

    # 30. Account Access Request
    generator.create_form(
        "account-access-request.pdf",
        "System/Account Access Request",
        "Information Technology",
        [
            {'type': 'section', 'label': 'Employee Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'Employee ID', 'width': 2},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Department', 'width': 3},
                {'label': 'Position/Title', 'width': 2.5},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Phone', 'width': 2},
                {'label': 'Email', 'width': 3},
            ]},
            {'type': 'date', 'label': 'Start Date', 'required': True},
            {'type': 'section', 'label': 'Access Requested'},
            {'type': 'checkbox', 'label': 'Banner (Student Information System)'},
            {'type': 'checkbox', 'label': 'Canvas (Learning Management)'},
            {'type': 'checkbox', 'label': 'Financial System'},
            {'type': 'checkbox', 'label': 'HR/Payroll System'},
            {'type': 'checkbox', 'label': 'Email/Office 365'},
            {'type': 'checkbox', 'label': 'Network Drive Access'},
            {'type': 'checkbox', 'label': 'Other:'},
            {'type': 'text', 'label': 'Other System', 'width': 4},
            {'type': 'textarea', 'label': 'Specific Access/Permissions Needed', 'width': 6, 'height': 0.8, 'required': True},
            {'type': 'text', 'label': 'Similar to Existing User (if applicable)', 'width': 4},
            {'type': 'section', 'label': 'Justification'},
            {'type': 'textarea', 'label': 'Business Reason for Access', 'width': 6, 'height': 0.8, 'required': True},
            {'type': 'section', 'label': 'Approvals'},
            {'type': 'signature', 'label': 'Employee Signature'},
            {'type': 'signature', 'label': 'Supervisor Approval'},
            {'type': 'signature', 'label': 'Data Owner Approval (for sensitive systems)'},
        ],
        "Access is granted based on job responsibilities. Annual review of access rights is required."
    )

    # ==================== AUXILIARY SERVICES FORMS ====================

    # 31. Meal Plan Change Request
    generator.create_form(
        "meal-plan-change-request.pdf",
        "Meal Plan Change Request",
        "Auxiliary Services",
        [
            {'type': 'section', 'label': 'Student Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'Student ID', 'width': 2},
            ]},
            {'type': 'text', 'label': 'Email', 'width': 4, 'required': True},
            {'type': 'text', 'label': 'Phone', 'width': 2.5},
            {'type': 'text', 'label': 'Residence Hall/Room', 'width': 3},
            {'type': 'section', 'label': 'Current Meal Plan'},
            {'type': 'radio', 'label': 'Current Plan', 'options': ['Unlimited', '19 Meals/Week', '14 Meals/Week', '10 Meals/Week', 'Commuter Plan']},
            {'type': 'section', 'label': 'Requested Meal Plan'},
            {'type': 'radio', 'label': 'New Plan', 'options': ['Unlimited ($2,500/semester)', '19 Meals/Week ($2,200/semester)', '14 Meals/Week ($1,900/semester)', '10 Meals/Week ($1,600/semester)', 'Commuter Plan ($500/semester)']},
            {'type': 'section', 'label': 'Reason for Change'},
            {'type': 'textarea', 'label': 'Please explain why you are requesting this change', 'width': 6, 'height': 1, 'required': True},
            {'type': 'section', 'label': 'Agreement'},
            {'type': 'checkbox', 'label': 'I understand changes are only allowed during the first 2 weeks of the semester'},
            {'type': 'checkbox', 'label': 'I understand my student account will be adjusted accordingly'},
            {'type': 'signature', 'label': 'Student Signature'},
            {'type': 'date', 'label': 'Date'},
        ],
        "Meal plan changes are only permitted during the first two weeks of each semester."
    )

    # 32. ID Card Replacement Request
    generator.create_form(
        "id-card-replacement.pdf",
        "Wildcat ID Card Replacement Request",
        "Auxiliary Services",
        [
            {'type': 'section', 'label': 'Student/Employee Information'},
            {'type': 'row', 'fields': [
                {'label': 'Name', 'width': 3},
                {'label': 'ID Number', 'width': 2},
            ]},
            {'type': 'radio', 'label': 'Status', 'options': ['Student', 'Faculty', 'Staff']},
            {'type': 'row', 'fields': [
                {'label': 'Phone', 'width': 2.5},
                {'label': 'Email', 'width': 3},
            ]},
            {'type': 'section', 'label': 'Reason for Replacement'},
            {'type': 'radio', 'label': 'Reason', 'options': ['Lost', 'Stolen', 'Damaged', 'Name Change', 'Photo Update']},
            {'type': 'textarea', 'label': 'Additional Details (if lost/stolen, where/when)', 'width': 6, 'height': 0.8},
            {'type': 'section', 'label': 'Fee Information'},
            {'type': 'checkbox', 'label': 'I understand a $25 replacement fee applies'},
            {'type': 'radio', 'label': 'Payment Method', 'options': ['Charge to Student Account', 'Payroll Deduction (Employees)', 'Cash/Card at ID Office']},
            {'type': 'section', 'label': 'Agreement'},
            {'type': 'checkbox', 'label': 'I understand my old card will be deactivated'},
            {'type': 'checkbox', 'label': 'I will surrender my damaged card (if applicable)'},
            {'type': 'signature', 'label': 'Signature'},
            {'type': 'date', 'label': 'Date'},
            {'type': 'section', 'label': 'Office Use Only'},
            {'type': 'text', 'label': 'New Card Number', 'width': 2.5},
            {'type': 'date', 'label': 'Date Issued'},
            {'type': 'signature', 'label': 'Issued By'},
        ],
        "Bring a valid government-issued photo ID. Cards are typically ready same day."
    )

    # 33. Vendor Application
    generator.create_form(
        "vendor-application.pdf",
        "Campus Vendor Application",
        "Auxiliary Services",
        [
            {'type': 'section', 'label': 'Business Information'},
            {'type': 'text', 'label': 'Business Name', 'width': 5, 'required': True},
            {'type': 'text', 'label': 'Contact Person', 'width': 4, 'required': True},
            {'type': 'text', 'label': 'Address', 'width': 5},
            {'type': 'row', 'fields': [
                {'label': 'City', 'width': 2.5},
                {'label': 'State', 'width': 1},
                {'label': 'ZIP', 'width': 1.5},
            ]},
            {'type': 'row', 'fields': [
                {'label': 'Phone', 'width': 2.5},
                {'label': 'Email', 'width': 3},
            ]},
            {'type': 'text', 'label': 'Website', 'width': 4},
            {'type': 'section', 'label': 'Business Details'},
            {'type': 'radio', 'label': 'Type of Business', 'options': ['Food/Beverage', 'Merchandise/Retail', 'Services', 'Entertainment', 'Other']},
            {'type': 'textarea', 'label': 'Description of Products/Services', 'width': 6, 'height': 1, 'required': True},
            {'type': 'section', 'label': 'Event Information'},
            {'type': 'text', 'label': 'Event/Location Requested', 'width': 4},
            {'type': 'date', 'label': 'Requested Date(s)'},
            {'type': 'section', 'label': 'Requirements'},
            {'type': 'checkbox', 'label': 'Electricity needed'},
            {'type': 'checkbox', 'label': 'Tables/chairs needed'},
            {'type': 'checkbox', 'label': 'Water access needed'},
            {'type': 'textarea', 'label': 'Other Requirements', 'width': 6, 'height': 0.6},
            {'type': 'section', 'label': 'Certifications'},
            {'type': 'checkbox', 'label': 'Valid business license (attach copy)'},
            {'type': 'checkbox', 'label': 'Certificate of Insurance (attach copy)'},
            {'type': 'checkbox', 'label': 'Food handler permit (if applicable)'},
            {'type': 'section', 'label': 'Agreement'},
            {'type': 'checkbox', 'label': 'I agree to comply with all university policies'},
            {'type': 'checkbox', 'label': 'I understand approval is subject to university review'},
            {'type': 'signature', 'label': 'Authorized Signature'},
            {'type': 'date', 'label': 'Date'},
        ],
        "Submit application at least 3 weeks before event. All vendors must provide proof of insurance."
    )

    print("\n" + "="*50)
    print("All 33 forms have been created successfully!")
    print("="*50)
    print(f"\nForms are located in: {FORMS_DIR}")
    print("\nForms created by department:")
    print("- Business Office: 6 forms")
    print("- Facilities Management: 4 forms")
    print("- Financial Aid: 5 forms")
    print("- Student Accounts: 4 forms")
    print("- Risk Management: 4 forms")
    print("- Transportation & Fleet: 4 forms")
    print("- Information Technology: 3 forms")
    print("- Auxiliary Services: 3 forms")


if __name__ == "__main__":
    create_all_forms()
