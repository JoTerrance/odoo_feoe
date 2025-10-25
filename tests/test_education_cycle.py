# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestEducationCycle(TransactionCase):
    """Test cases for education.cycle model"""

    def setUp(self):
        super(TestEducationCycle, self).setUp()
        self.EducationCycle = self.env['education.cycle']
        
    def test_create_cycle_basic(self):
        """Test creating a basic education cycle"""
        cycle = self.EducationCycle.create({
            'name': 'Desarrollo de Aplicaciones Web',
            'code': 'DAW',
            'level': 'gs',
        })
        self.assertTrue(cycle)
        self.assertEqual(cycle.name, 'Desarrollo de Aplicaciones Web')
        self.assertEqual(cycle.code, 'DAW')
        self.assertEqual(cycle.level, 'gs')
        self.assertTrue(cycle.active)
        self.assertEqual(cycle.sequence, 10)

    def test_create_cycle_grado_medio(self):
        """Test creating a grado medio cycle"""
        cycle = self.EducationCycle.create({
            'name': 'Sistemas Microinformáticos y Redes',
            'code': 'SMR',
            'level': 'gm',
        })
        self.assertEqual(cycle.level, 'gm')

    def test_create_cycle_grado_superior(self):
        """Test creating a grado superior cycle"""
        cycle = self.EducationCycle.create({
            'name': 'Administración de Sistemas Informáticos en Red',
            'code': 'ASIR',
            'level': 'gs',
        })
        self.assertEqual(cycle.level, 'gs')

    def test_code_unique_constraint(self):
        """Test that code must be unique"""
        self.EducationCycle.create({
            'name': 'First Cycle',
            'code': 'UNIQUE',
            'level': 'gs',
        })
        with self.assertRaises(ValidationError):
            self.EducationCycle.create({
                'name': 'Second Cycle',
                'code': 'UNIQUE',
                'level': 'gm',
            })

    def test_cycle_with_description(self):
        """Test creating a cycle with description"""
        cycle = self.EducationCycle.create({
            'name': 'Test Cycle',
            'code': 'TC01',
            'level': 'gs',
            'description': 'This is a test cycle for testing purposes',
        })
        self.assertEqual(cycle.description, 'This is a test cycle for testing purposes')

    def test_cycle_sequence(self):
        """Test custom sequence"""
        cycle = self.EducationCycle.create({
            'name': 'Test Cycle',
            'code': 'SEQ01',
            'level': 'gs',
            'sequence': 5,
        })
        self.assertEqual(cycle.sequence, 5)

    def test_cycle_active_flag(self):
        """Test active flag"""
        cycle = self.EducationCycle.create({
            'name': 'Test Cycle',
            'code': 'ACT01',
            'level': 'gs',
            'active': False,
        })
        self.assertFalse(cycle.active)

    def test_cycle_ordering(self):
        """Test that cycles are ordered by sequence and name"""
        cycle1 = self.EducationCycle.create({
            'name': 'B Cycle',
            'code': 'BC01',
            'level': 'gs',
            'sequence': 20,
        })
        cycle2 = self.EducationCycle.create({
            'name': 'A Cycle',
            'code': 'AC01',
            'level': 'gs',
            'sequence': 10,
        })
        
        cycles = self.EducationCycle.search([
            ('id', 'in', [cycle1.id, cycle2.id])
        ])
        self.assertEqual(cycles[0], cycle2)
        self.assertEqual(cycles[1], cycle1)

    def test_required_fields(self):
        """Test that required fields are enforced"""
        with self.assertRaises(Exception):
            self.EducationCycle.create({
                'code': 'TEST',
                'level': 'gs',
            })
        
        with self.assertRaises(Exception):
            self.EducationCycle.create({
                'name': 'Test Cycle',
                'level': 'gs',
            })
        
        with self.assertRaises(Exception):
            self.EducationCycle.create({
                'name': 'Test Cycle',
                'code': 'TEST',
            })
