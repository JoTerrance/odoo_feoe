# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestCompanyTutor(TransactionCase):
    """Test cases for company.tutor model"""

    def setUp(self):
        super(TestCompanyTutor, self).setUp()
        self.Tutor = self.env['company.tutor']
        self.CompanyInfo = self.env['company.info']
        
        # Create test company
        self.test_company = self.CompanyInfo.create({
            'name': 'Test Company',
            'cif': 'TUT123',
        })
        
    def test_create_tutor_basic(self):
        """Test creating a basic tutor"""
        tutor = self.Tutor.create({
            'name': 'John Doe',
            'company_id': self.test_company.id,
        })
        self.assertTrue(tutor)
        self.assertEqual(tutor.name, 'John Doe')
        self.assertEqual(tutor.company_id, self.test_company)
        self.assertTrue(tutor.active)

    def test_create_tutor_full(self):
        """Test creating a tutor with all fields"""
        tutor = self.Tutor.create({
            'name': 'Jane Smith',
            'company_id': self.test_company.id,
            'dni': '12345678A',
            'phone': '612345678',
            'email': 'jane@company.com',
            'schedule': '9:00 - 17:00',
            'position': 'Technical Manager',
            'observations': 'Available for morning sessions',
        })
        self.assertEqual(tutor.dni, '12345678A')
        self.assertEqual(tutor.phone, '612345678')
        self.assertEqual(tutor.email, 'jane@company.com')
        self.assertEqual(tutor.position, 'Technical Manager')

    def test_dni_unique_constraint(self):
        """Test that DNI must be unique per company"""
        self.Tutor.create({
            'name': 'John Doe',
            'company_id': self.test_company.id,
            'dni': '12345678A',
        })
        
        with self.assertRaises(ValidationError):
            self.Tutor.create({
                'name': 'Jane Doe',
                'company_id': self.test_company.id,
                'dni': '12345678A',
            })

    def test_dni_different_companies(self):
        """Test that same DNI can exist in different companies"""
        company2 = self.CompanyInfo.create({
            'name': 'Another Company',
            'cif': 'TUT456',
        })
        
        tutor1 = self.Tutor.create({
            'name': 'John Doe',
            'company_id': self.test_company.id,
            'dni': '12345678A',
        })
        
        tutor2 = self.Tutor.create({
            'name': 'John Doe',
            'company_id': company2.id,
            'dni': '12345678A',
        })
        
        self.assertEqual(tutor1.dni, tutor2.dni)
        self.assertNotEqual(tutor1.company_id, tutor2.company_id)

    def test_workplace_relationship(self):
        """Test many2many relationship with workplaces"""
        tutor = self.Tutor.create({
            'name': 'John Tutor',
            'company_id': self.test_company.id,
        })
        
        workplace = self.env['company.workplace'].create({
            'name': 'Main Office',
            'company_id': self.test_company.id,
        })
        
        tutor.workplace_ids = [(4, workplace.id)]
        self.assertIn(workplace, tutor.workplace_ids)

    def test_tutor_ordering(self):
        """Test tutor ordering by name"""
        tutor1 = self.Tutor.create({
            'name': 'Zebra Tutor',
            'company_id': self.test_company.id,
        })
        tutor2 = self.Tutor.create({
            'name': 'Alpha Tutor',
            'company_id': self.test_company.id,
        })
        
        tutors = self.Tutor.search([
            ('company_id', '=', self.test_company.id)
        ])
        self.assertEqual(tutors[0], tutor2)
        self.assertEqual(tutors[1], tutor1)

    def test_active_flag(self):
        """Test active flag"""
        tutor = self.Tutor.create({
            'name': 'Inactive Tutor',
            'company_id': self.test_company.id,
            'active': False,
        })
        self.assertFalse(tutor.active)

    def test_required_fields(self):
        """Test that required fields are enforced"""
        with self.assertRaises(Exception):
            self.Tutor.create({
                'company_id': self.test_company.id,
            })
        
        with self.assertRaises(Exception):
            self.Tutor.create({
                'name': 'John Doe',
            })

    def test_cascade_delete(self):
        """Test that tutor is deleted when company is deleted"""
        tutor = self.Tutor.create({
            'name': 'John Doe',
            'company_id': self.test_company.id,
        })
        tutor_id = tutor.id
        self.test_company.unlink()
        
        # Verify tutor was deleted
        self.assertFalse(self.Tutor.search([('id', '=', tutor_id)]))

    def test_tutor_without_dni(self):
        """Test creating tutor without DNI (not required)"""
        tutor = self.Tutor.create({
            'name': 'John Doe',
            'company_id': self.test_company.id,
        })
        self.assertFalse(tutor.dni)
