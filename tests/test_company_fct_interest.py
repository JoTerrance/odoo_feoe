# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestCompanyFCTInterest(TransactionCase):
    """Test cases for company.fct.interest model"""

    def setUp(self):
        super(TestCompanyFCTInterest, self).setUp()
        self.FCTInterest = self.env['company.fct.interest']
        self.CompanyInfo = self.env['company.info']
        self.EducationCycle = self.env['education.cycle']
        
        # Create test company
        self.test_company = self.CompanyInfo.create({
            'name': 'Test Company',
            'cif': 'FCT123',
        })
        
        # Create test cycle
        self.test_cycle = self.EducationCycle.create({
            'name': 'Test Cycle',
            'code': 'TC01',
            'level': 'gs',
        })
        
    def test_create_fct_interest_basic(self):
        """Test creating a basic FCT interest record"""
        interest = self.FCTInterest.create({
            'company_id': self.test_company.id,
            'cycle_id': self.test_cycle.id,
            'course': '1',
            'call': 'first',
            'year': 2024,
        })
        self.assertTrue(interest)
        self.assertEqual(interest.company_id, self.test_company)
        self.assertEqual(interest.cycle_id, self.test_cycle)
        self.assertEqual(interest.course, '1')
        self.assertEqual(interest.call, 'first')
        self.assertEqual(interest.year, 2024)
        self.assertTrue(interest.interested)
        self.assertFalse(interest.knows_number)

    def test_create_fct_interest_with_students(self):
        """Test creating FCT interest with student count"""
        interest = self.FCTInterest.create({
            'company_id': self.test_company.id,
            'cycle_id': self.test_cycle.id,
            'course': '2',
            'call': 'first',
            'year': 2024,
            'knows_number': True,
            'num_students': 5,
        })
        self.assertTrue(interest.knows_number)
        self.assertEqual(interest.num_students, 5)

    def test_negative_students_validation(self):
        """Test that num_students cannot be negative"""
        with self.assertRaises(ValidationError):
            self.FCTInterest.create({
                'company_id': self.test_company.id,
                'cycle_id': self.test_cycle.id,
                'course': '1',
                'call': 'first',
                'year': 2024,
                'num_students': -1,
            })

    def test_onchange_knows_number(self):
        """Test onchange when knows_number is unchecked"""
        interest = self.FCTInterest.create({
            'company_id': self.test_company.id,
            'cycle_id': self.test_cycle.id,
            'course': '1',
            'call': 'first',
            'year': 2024,
            'knows_number': True,
            'num_students': 5,
        })
        interest.knows_number = False
        interest._onchange_knows_number()
        self.assertEqual(interest.num_students, 0)

    def test_onchange_interested(self):
        """Test onchange when interested is unchecked"""
        interest = self.FCTInterest.create({
            'company_id': self.test_company.id,
            'cycle_id': self.test_cycle.id,
            'course': '1',
            'call': 'first',
            'year': 2024,
            'knows_number': True,
            'num_students': 5,
            'interested': True,
        })
        interest.interested = False
        interest._onchange_interested()
        self.assertFalse(interest.knows_number)
        self.assertEqual(interest.num_students, 0)

    def test_name_get_interested(self):
        """Test name_get for interested company"""
        interest = self.FCTInterest.create({
            'company_id': self.test_company.id,
            'cycle_id': self.test_cycle.id,
            'course': '1',
            'call': 'first',
            'year': 2024,
            'interested': True,
            'knows_number': True,
            'num_students': 3,
        })
        name = interest.name_get()[0][1]
        self.assertIn('TC01', name)
        self.assertIn('1', name)
        self.assertIn('2024', name)
        self.assertIn('3 alumnos', name)

    def test_name_get_not_interested(self):
        """Test name_get for not interested company"""
        interest = self.FCTInterest.create({
            'company_id': self.test_company.id,
            'cycle_id': self.test_cycle.id,
            'course': '2',
            'call': 'first',
            'year': 2024,
            'interested': False,
        })
        name = interest.name_get()[0][1]
        self.assertIn('No interesada', name)

    def test_name_get_second_call(self):
        """Test name_get for second call"""
        interest = self.FCTInterest.create({
            'company_id': self.test_company.id,
            'cycle_id': self.test_cycle.id,
            'course': '1',
            'call': 'second',
            'year': 2024,
        })
        name = interest.name_get()[0][1]
        self.assertIn('2ª Conv', name)

    def test_unique_constraint(self):
        """Test unique constraint for company, cycle, course, call and year"""
        self.FCTInterest.create({
            'company_id': self.test_company.id,
            'cycle_id': self.test_cycle.id,
            'course': '1',
            'call': 'first',
            'year': 2024,
        })
        with self.assertRaises(ValidationError):
            self.FCTInterest.create({
                'company_id': self.test_company.id,
                'cycle_id': self.test_cycle.id,
                'course': '1',
                'call': 'first',
                'year': 2024,
            })

    def test_different_courses(self):
        """Test creating records for different courses"""
        courses = ['1', '2', 'dual']
        for course in courses:
            interest = self.FCTInterest.create({
                'company_id': self.test_company.id,
                'cycle_id': self.test_cycle.id,
                'course': course,
                'call': 'first',
                'year': 2024,
            })
            self.assertEqual(interest.course, course)

    def test_related_fields(self):
        """Test related fields"""
        interest = self.FCTInterest.create({
            'company_id': self.test_company.id,
            'cycle_id': self.test_cycle.id,
            'course': '1',
            'call': 'first',
            'year': 2024,
        })
        self.assertEqual(interest.company_name, 'Test Company')
        self.assertEqual(interest.cycle_name, 'Test Cycle')
