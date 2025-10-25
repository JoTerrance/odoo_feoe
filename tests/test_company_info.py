# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestCompanyInfo(TransactionCase):
    """Test cases for company.info model"""

    def setUp(self):
        super(TestCompanyInfo, self).setUp()
        self.CompanyInfo = self.env['company.info']
        self.country_spain = self.env.ref('base.es')
        
    def test_create_company_basic(self):
        """Test creating a basic company record"""
        company = self.CompanyInfo.create({
            'name': 'Test Company',
            'cif': '12345678A',
        })
        self.assertTrue(company)
        self.assertEqual(company.name, 'Test Company')
        self.assertEqual(company.cif, '12345678A')
        self.assertEqual(company.stage, 'new')
        self.assertEqual(company.priority, '1')
        self.assertTrue(company.active)

    def test_create_company_full(self):
        """Test creating a company with all fields"""
        company = self.CompanyInfo.create({
            'name': 'Full Test Company',
            'cif': '87654321B',
            'email': 'test@company.com',
            'phone': '912345678',
            'mobile': '612345678',
            'website': 'www.testcompany.com',
            'street': 'Test Street 123',
            'city': 'Madrid',
            'zip': '28001',
            'country_id': self.country_spain.id,
            'sector': 'Technology',
            'num_employees': 50,
            'contact_person': 'John Doe',
            'contact_position': 'Manager',
            'stage': 'contacted',
            'priority': '2',
        })
        self.assertEqual(company.name, 'Full Test Company')
        self.assertEqual(company.email, 'test@company.com')
        self.assertEqual(company.city, 'Madrid')
        self.assertEqual(company.stage, 'contacted')
        
    def test_cif_unique_constraint(self):
        """Test that CIF must be unique"""
        self.CompanyInfo.create({
            'name': 'Company One',
            'cif': 'UNIQUE123',
        })
        with self.assertRaises(ValidationError):
            self.CompanyInfo.create({
                'name': 'Company Two',
                'cif': 'UNIQUE123',
            })

    def test_compute_tracking_count(self):
        """Test tracking count computation"""
        company = self.CompanyInfo.create({
            'name': 'Test Company',
            'cif': 'COUNT123',
        })
        self.assertEqual(company.tracking_count, 0)
        
        # Create a tracking record
        self.env['company.tracking'].create({
            'company_id': company.id,
            'contact_date': '2024-01-01',
            'subject': 'Test Contact',
            'topics_discussed': 'Discussion topics',
            'contact_type': 'call',
        })
        company._compute_tracking_count()
        self.assertEqual(company.tracking_count, 1)

    def test_compute_last_contact_date(self):
        """Test last contact date computation"""
        company = self.CompanyInfo.create({
            'name': 'Test Company',
            'cif': 'LASTDATE123',
        })
        self.assertFalse(company.last_contact_date)
        
        # Create tracking records with different dates
        self.env['company.tracking'].create({
            'company_id': company.id,
            'contact_date': '2024-01-01',
            'subject': 'First Contact',
            'topics_discussed': 'Topics',
            'contact_type': 'call',
        })
        self.env['company.tracking'].create({
            'company_id': company.id,
            'contact_date': '2024-01-15',
            'subject': 'Second Contact',
            'topics_discussed': 'Topics',
            'contact_type': 'email',
        })
        company._compute_last_contact_date()
        self.assertEqual(str(company.last_contact_date), '2024-01-15')

    def test_compute_fct_interest_count(self):
        """Test FCT interest count computation"""
        company = self.CompanyInfo.create({
            'name': 'Test Company',
            'cif': 'FCT123',
        })
        
        # Create education cycle
        cycle = self.env['education.cycle'].create({
            'name': 'Test Cycle',
            'code': 'TC01',
            'level': 'gs',
        })
        
        # Create interested FCT record
        self.env['company.fct.interest'].create({
            'company_id': company.id,
            'cycle_id': cycle.id,
            'course': '1',
            'call': 'first',
            'year': 2024,
            'interested': True,
        })
        
        company._compute_fct_interest_count()
        self.assertEqual(company.fct_interest_count, 1)

    def test_action_view_trackings(self):
        """Test action to view trackings"""
        company = self.CompanyInfo.create({
            'name': 'Test Company',
            'cif': 'ACTION123',
        })
        action = company.action_view_trackings()
        self.assertEqual(action['type'], 'ir.actions.act_window')
        self.assertEqual(action['res_model'], 'company.tracking')
        self.assertIn(('company_id', '=', company.id), action['domain'])

    def test_action_view_fct_interests(self):
        """Test action to view FCT interests"""
        company = self.CompanyInfo.create({
            'name': 'Test Company',
            'cif': 'FCTACTION123',
        })
        action = company.action_view_fct_interests()
        self.assertEqual(action['type'], 'ir.actions.act_window')
        self.assertEqual(action['res_model'], 'company.fct.interest')
        
    def test_action_view_workplaces(self):
        """Test action to view workplaces"""
        company = self.CompanyInfo.create({
            'name': 'Test Company',
            'cif': 'WORKPLACE123',
        })
        action = company.action_view_workplaces()
        self.assertEqual(action['type'], 'ir.actions.act_window')
        self.assertEqual(action['res_model'], 'company.workplace')

    def test_action_view_tutors(self):
        """Test action to view tutors"""
        company = self.CompanyInfo.create({
            'name': 'Test Company',
            'cif': 'TUTOR123',
        })
        action = company.action_view_tutors()
        self.assertEqual(action['type'], 'ir.actions.act_window')
        self.assertEqual(action['res_model'], 'company.tutor')

    def test_default_country(self):
        """Test that default country is Spain"""
        company = self.CompanyInfo.create({
            'name': 'Test Company',
            'cif': 'COUNTRY123',
        })
        self.assertEqual(company.country_id, self.country_spain)

    def test_compute_workplace_count(self):
        """Test workplace count computation"""
        company = self.CompanyInfo.create({
            'name': 'Test Company',
            'cif': 'WPCOUNT123',
        })
        self.assertEqual(company.workplace_count, 0)
        
        self.env['company.workplace'].create({
            'name': 'Main Office',
            'company_id': company.id,
        })
        company._compute_workplace_count()
        self.assertEqual(company.workplace_count, 1)

    def test_compute_tutor_count(self):
        """Test tutor count computation"""
        company = self.CompanyInfo.create({
            'name': 'Test Company',
            'cif': 'TUTCOUNT123',
        })
        self.assertEqual(company.tutor_count, 0)
        
        self.env['company.tutor'].create({
            'name': 'John Tutor',
            'company_id': company.id,
        })
        company._compute_tutor_count()
        self.assertEqual(company.tutor_count, 1)
