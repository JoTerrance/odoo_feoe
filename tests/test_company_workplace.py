# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase


class TestCompanyWorkplace(TransactionCase):
    """Test cases for company.workplace model"""

    def setUp(self):
        super(TestCompanyWorkplace, self).setUp()
        self.Workplace = self.env['company.workplace']
        self.CompanyInfo = self.env['company.info']
        
        # Create test company
        self.test_company = self.CompanyInfo.create({
            'name': 'Test Company',
            'cif': 'WP123',
        })
        
    def test_create_workplace_basic(self):
        """Test creating a basic workplace"""
        workplace = self.Workplace.create({
            'name': 'Main Office',
            'company_id': self.test_company.id,
        })
        self.assertTrue(workplace)
        self.assertEqual(workplace.name, 'Main Office')
        self.assertEqual(workplace.company_id, self.test_company)
        self.assertTrue(workplace.active)
        self.assertEqual(workplace.sequence, 10)
        self.assertEqual(workplace.country, 'España')

    def test_create_workplace_full(self):
        """Test creating a workplace with all fields"""
        workplace = self.Workplace.create({
            'name': 'Branch Office',
            'company_id': self.test_company.id,
            'street': 'Main Street 123',
            'city': 'Barcelona',
            'state': 'Barcelona',
            'zip': '08001',
            'country': 'España',
            'phone': '932345678',
            'email': 'branch@company.com',
            'company_schedule': '9:00 - 18:00',
            'student_schedule': '9:00 - 14:00',
            'observations': 'This is the main branch',
            'sequence': 5,
        })
        self.assertEqual(workplace.city, 'Barcelona')
        self.assertEqual(workplace.phone, '932345678')
        self.assertEqual(workplace.company_schedule, '9:00 - 18:00')
        self.assertEqual(workplace.sequence, 5)

    def test_name_get_without_city(self):
        """Test name_get without city"""
        workplace = self.Workplace.create({
            'name': 'Office',
            'company_id': self.test_company.id,
        })
        name = workplace.name_get()[0][1]
        self.assertEqual(name, 'Office')

    def test_name_get_with_city(self):
        """Test name_get with city"""
        workplace = self.Workplace.create({
            'name': 'Office',
            'company_id': self.test_company.id,
            'city': 'Madrid',
        })
        name = workplace.name_get()[0][1]
        self.assertEqual(name, 'Office (Madrid)')

    def test_workplace_ordering(self):
        """Test workplace ordering by sequence and name"""
        wp1 = self.Workplace.create({
            'name': 'B Office',
            'company_id': self.test_company.id,
            'sequence': 20,
        })
        wp2 = self.Workplace.create({
            'name': 'A Office',
            'company_id': self.test_company.id,
            'sequence': 10,
        })
        
        workplaces = self.Workplace.search([
            ('company_id', '=', self.test_company.id)
        ])
        self.assertEqual(workplaces[0], wp2)
        self.assertEqual(workplaces[1], wp1)

    def test_tutor_relationship(self):
        """Test many2many relationship with tutors"""
        workplace = self.Workplace.create({
            'name': 'Office',
            'company_id': self.test_company.id,
        })
        
        tutor = self.env['company.tutor'].create({
            'name': 'John Tutor',
            'company_id': self.test_company.id,
        })
        
        workplace.tutor_ids = [(4, tutor.id)]
        self.assertIn(tutor, workplace.tutor_ids)

    def test_active_flag(self):
        """Test active flag"""
        workplace = self.Workplace.create({
            'name': 'Inactive Office',
            'company_id': self.test_company.id,
            'active': False,
        })
        self.assertFalse(workplace.active)

    def test_required_fields(self):
        """Test that required fields are enforced"""
        with self.assertRaises(Exception):
            self.Workplace.create({
                'company_id': self.test_company.id,
            })
        
        with self.assertRaises(Exception):
            self.Workplace.create({
                'name': 'Office',
            })

    def test_cascade_delete(self):
        """Test that workplace is deleted when company is deleted"""
        workplace = self.Workplace.create({
            'name': 'Office',
            'company_id': self.test_company.id,
        })
        workplace_id = workplace.id
        self.test_company.unlink()
        
        # Verify workplace was deleted
        self.assertFalse(self.Workplace.search([('id', '=', workplace_id)]))
