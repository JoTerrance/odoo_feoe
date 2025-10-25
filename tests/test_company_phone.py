# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestCompanyPhone(TransactionCase):
    """Test cases for company.phone model"""

    def setUp(self):
        super(TestCompanyPhone, self).setUp()
        self.Phone = self.env['company.phone']
        self.CompanyInfo = self.env['company.info']
        
        # Create test company
        self.test_company = self.CompanyInfo.create({
            'name': 'Test Company',
            'cif': 'PHONE123',
        })
        
    def test_create_phone_basic(self):
        """Test creating a basic phone record"""
        phone = self.Phone.create({
            'company_id': self.test_company.id,
            'phone': '912345678',
        })
        self.assertTrue(phone)
        self.assertEqual(phone.phone, '912345678')
        self.assertEqual(phone.company_id, self.test_company)
        self.assertEqual(phone.phone_type, 'principal')
        self.assertTrue(phone.active)
        self.assertEqual(phone.sequence, 10)

    def test_create_phone_full(self):
        """Test creating a phone with all fields"""
        phone = self.Phone.create({
            'company_id': self.test_company.id,
            'phone': '932345678',
            'phone_type': 'alternative',
            'sequence': 5,
            'note': 'Contact during office hours',
        })
        self.assertEqual(phone.phone_type, 'alternative')
        self.assertEqual(phone.sequence, 5)
        self.assertEqual(phone.note, 'Contact during office hours')

    def test_phone_types(self):
        """Test all phone types"""
        phone_types = ['principal', 'alternative', 'mobile', 'fax', 'other']
        for phone_type in phone_types:
            phone = self.Phone.create({
                'company_id': self.test_company.id,
                'phone': f'91234567{phone_types.index(phone_type)}',
                'phone_type': phone_type,
            })
            self.assertEqual(phone.phone_type, phone_type)

    def test_phone_unique_constraint(self):
        """Test that phone must be unique per company"""
        self.Phone.create({
            'company_id': self.test_company.id,
            'phone': '912345678',
        })
        
        with self.assertRaises(ValidationError):
            self.Phone.create({
                'company_id': self.test_company.id,
                'phone': '912345678',
            })

    def test_phone_different_companies(self):
        """Test that same phone can exist in different companies"""
        company2 = self.CompanyInfo.create({
            'name': 'Another Company',
            'cif': 'PHONE456',
        })
        
        phone1 = self.Phone.create({
            'company_id': self.test_company.id,
            'phone': '912345678',
        })
        
        phone2 = self.Phone.create({
            'company_id': company2.id,
            'phone': '912345678',
        })
        
        self.assertEqual(phone1.phone, phone2.phone)
        self.assertNotEqual(phone1.company_id, phone2.company_id)

    def test_name_get(self):
        """Test custom name_get method"""
        phone = self.Phone.create({
            'company_id': self.test_company.id,
            'phone': '912345678',
            'phone_type': 'mobile',
        })
        name = phone.name_get()[0][1]
        self.assertIn('912345678', name)
        self.assertIn('Móvil', name)

    def test_phone_ordering(self):
        """Test phone ordering by sequence and type"""
        phone1 = self.Phone.create({
            'company_id': self.test_company.id,
            'phone': '912345678',
            'phone_type': 'principal',
            'sequence': 20,
        })
        phone2 = self.Phone.create({
            'company_id': self.test_company.id,
            'phone': '932345678',
            'phone_type': 'alternative',
            'sequence': 10,
        })
        
        phones = self.Phone.search([
            ('company_id', '=', self.test_company.id)
        ])
        self.assertEqual(phones[0], phone2)
        self.assertEqual(phones[1], phone1)

    def test_active_flag(self):
        """Test active flag"""
        phone = self.Phone.create({
            'company_id': self.test_company.id,
            'phone': '912345678',
            'active': False,
        })
        self.assertFalse(phone.active)

    def test_required_fields(self):
        """Test that required fields are enforced"""
        with self.assertRaises(Exception):
            self.Phone.create({
                'company_id': self.test_company.id,
            })
        
        with self.assertRaises(Exception):
            self.Phone.create({
                'phone': '912345678',
            })

    def test_cascade_delete(self):
        """Test that phone is deleted when company is deleted"""
        phone = self.Phone.create({
            'company_id': self.test_company.id,
            'phone': '912345678',
        })
        phone_id = phone.id
        self.test_company.unlink()
        
        # Verify phone was deleted
        self.assertFalse(self.Phone.search([('id', '=', phone_id)]))

    def test_phone_with_note(self):
        """Test phone with note"""
        phone = self.Phone.create({
            'company_id': self.test_company.id,
            'phone': '912345678',
            'note': 'Only for emergencies',
        })
        self.assertEqual(phone.note, 'Only for emergencies')

    def test_multiple_phones_per_company(self):
        """Test creating multiple phones for one company"""
        phone1 = self.Phone.create({
            'company_id': self.test_company.id,
            'phone': '912345678',
            'phone_type': 'principal',
        })
        phone2 = self.Phone.create({
            'company_id': self.test_company.id,
            'phone': '932345678',
            'phone_type': 'alternative',
        })
        phone3 = self.Phone.create({
            'company_id': self.test_company.id,
            'phone': '612345678',
            'phone_type': 'mobile',
        })
        
        phones = self.Phone.search([('company_id', '=', self.test_company.id)])
        self.assertEqual(len(phones), 3)
