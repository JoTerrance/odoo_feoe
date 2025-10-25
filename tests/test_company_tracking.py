# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo import fields


class TestCompanyTracking(TransactionCase):
    """Test cases for company.tracking model"""

    def setUp(self):
        super(TestCompanyTracking, self).setUp()
        self.CompanyTracking = self.env['company.tracking']
        self.CompanyInfo = self.env['company.info']
        
        # Create a test company
        self.test_company = self.CompanyInfo.create({
            'name': 'Test Company',
            'cif': 'TRACK123',
        })
        
    def test_create_tracking_basic(self):
        """Test creating a basic tracking record"""
        tracking = self.CompanyTracking.create({
            'company_id': self.test_company.id,
            'contact_date': '2024-01-01',
            'subject': 'Initial Contact',
            'topics_discussed': 'Discussed FCT opportunities',
            'contact_type': 'call',
        })
        self.assertTrue(tracking)
        self.assertEqual(tracking.company_id, self.test_company)
        self.assertEqual(tracking.subject, 'Initial Contact')
        self.assertEqual(tracking.contact_type, 'call')
        self.assertEqual(tracking.outcome, 'neutral')

    def test_create_tracking_full(self):
        """Test creating a tracking record with all fields"""
        tracking = self.CompanyTracking.create({
            'company_id': self.test_company.id,
            'contact_date': '2024-01-15',
            'contact_time': 14.5,
            'subject': 'Follow-up Meeting',
            'topics_discussed': 'Discussed student placement details',
            'contact_type': 'meeting',
            'outcome': 'positive',
            'next_action': 'Send documentation',
            'next_contact_date': '2024-02-01',
            'duration': 60,
            'notes': 'Very productive meeting',
        })
        self.assertEqual(tracking.contact_type, 'meeting')
        self.assertEqual(tracking.outcome, 'positive')
        self.assertEqual(tracking.duration, 60)
        self.assertEqual(tracking.contact_time, 14.5)

    def test_tracking_default_date(self):
        """Test that default contact date is today"""
        tracking = self.CompanyTracking.create({
            'company_id': self.test_company.id,
            'subject': 'Test',
            'topics_discussed': 'Test topics',
            'contact_type': 'call',
        })
        self.assertEqual(str(tracking.contact_date), str(fields.Date.today()))

    def test_name_get(self):
        """Test custom name_get method"""
        tracking = self.CompanyTracking.create({
            'company_id': self.test_company.id,
            'contact_date': '2024-01-01',
            'subject': 'Test Subject',
            'topics_discussed': 'Topics',
            'contact_type': 'email',
        })
        name = tracking.name_get()[0][1]
        self.assertIn('Test Company', name)
        self.assertIn('2024-01-01', name)
        self.assertIn('Test Subject', name)

    def test_related_fields(self):
        """Test related fields for company name and stage"""
        tracking = self.CompanyTracking.create({
            'company_id': self.test_company.id,
            'contact_date': '2024-01-01',
            'subject': 'Test',
            'topics_discussed': 'Topics',
            'contact_type': 'call',
        })
        self.assertEqual(tracking.company_name, 'Test Company')
        self.assertEqual(tracking.company_stage, 'new')

    def test_contact_type_selection(self):
        """Test different contact types"""
        contact_types = ['call', 'email', 'meeting', 'video', 'whatsapp', 'other']
        for contact_type in contact_types:
            tracking = self.CompanyTracking.create({
                'company_id': self.test_company.id,
                'contact_date': '2024-01-01',
                'subject': f'Test {contact_type}',
                'topics_discussed': 'Topics',
                'contact_type': contact_type,
            })
            self.assertEqual(tracking.contact_type, contact_type)

    def test_outcome_selection(self):
        """Test different outcome types"""
        outcomes = ['positive', 'neutral', 'negative', 'pending']
        for outcome in outcomes:
            tracking = self.CompanyTracking.create({
                'company_id': self.test_company.id,
                'contact_date': '2024-01-01',
                'subject': f'Test {outcome}',
                'topics_discussed': 'Topics',
                'contact_type': 'call',
                'outcome': outcome,
            })
            self.assertEqual(tracking.outcome, outcome)

    def test_tracking_order(self):
        """Test that trackings are ordered by date and time desc"""
        tracking1 = self.CompanyTracking.create({
            'company_id': self.test_company.id,
            'contact_date': '2024-01-01',
            'contact_time': 10.0,
            'subject': 'First',
            'topics_discussed': 'Topics',
            'contact_type': 'call',
        })
        tracking2 = self.CompanyTracking.create({
            'company_id': self.test_company.id,
            'contact_date': '2024-01-15',
            'contact_time': 14.0,
            'subject': 'Second',
            'topics_discussed': 'Topics',
            'contact_type': 'call',
        })
        
        trackings = self.CompanyTracking.search([
            ('company_id', '=', self.test_company.id)
        ])
        self.assertEqual(trackings[0], tracking2)
        self.assertEqual(trackings[1], tracking1)

    def test_required_fields(self):
        """Test that required fields are enforced"""
        with self.assertRaises(Exception):
            self.CompanyTracking.create({
                'contact_date': '2024-01-01',
                'subject': 'Test',
                'topics_discussed': 'Topics',
            })

    def test_attachment_relation(self):
        """Test that attachment_ids field exists"""
        tracking = self.CompanyTracking.create({
            'company_id': self.test_company.id,
            'contact_date': '2024-01-01',
            'subject': 'Test',
            'topics_discussed': 'Topics',
            'contact_type': 'call',
        })
        self.assertTrue(hasattr(tracking, 'attachment_ids'))
