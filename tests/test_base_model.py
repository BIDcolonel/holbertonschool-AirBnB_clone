#!/usr/bin/python3
"""Unittest for BaseModel"""
import unittest
from models.base_model import BaseModel
from datetime import datetime


class testBaseModel(unittest.TestCase):
    """Test class for BaseModel"""

    def setUp(self):
        """Set up for the test"""
        self.model = BaseModel()

    def test_init(self):
        """Test the initialization"""
        self.assertIsInstance(self.model, BaseModel)

    def test_id_is_string(self):
        """Test if 'id' is a string"""
        self.assertIsInstance(self.model.id, str)

    def test_created_at_is_datetime(self):
        """Test if 'created_at' is a datetime object"""
        self.assertIsInstance(self.model.created_at, datetime)

    def test_updated_at_is_datetime(self):
        """Test if 'updated_at' is a datetime object"""
        self.assertIsInstance(self.model.updated_at, datetime)

    def test_created_and_updated_at_are_equal_on_init(self):
        """Test if 'created_at' and 'updated_at' are equal on initialization"""
        self.assertEqual(self.model.created_at, self.model.updated_at)

    def test_str_representation(self):
        """Test the string representation"""
        expected_str = f"[BaseModel] ({self.model.id}) {self.model.__dict__}"
        self.assertEqual(str(self.model), expected_str)

    def test_save_method_updates_updated_at(self):
        """Test if the 'save' method updates 'updated_at'"""
        old_updated_at = self.model.updated_at
        self.model.save()
        self.assertNotEqual(old_updated_at, self.model.updated_at)

    def test_to_dict_method(self):
        """Test the 'to_dict' method"""
        model_dict = self.model.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertEqual(model_dict['__class__'], 'BaseModel')
        self.assertEqual(model_dict['created_at'],
                         self.model.created_at.isoformat())
        self.assertEqual(model_dict['updated_at'],
                         self.model.updated_at.isoformat())

    def test_id_unique_for_each_instance(self):
        """Test if 'id' is unique for each instance"""
        model1 = BaseModel()
        model2 = BaseModel()
        self.assertNotEqual(model1.id, model2.id)

    def test_created_at_and_updated_at_format(self):
        """Test if 'created_at' and 'updated_at' are in the correct format"""
        iso_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.assertEqual(
            self.model.created_at.strftime(iso_format),
            self.model.created_at.isoformat())
        self.assertEqual(
            self.model.updated_at.strftime(iso_format),
            self.model.updated_at.isoformat())

    def test_to_dict_method_includes_id(self):
        """Test if 'to_dict' method includes 'id' key"""
        model_dict = self.model.to_dict()
        self.assertIn('id', model_dict)

    def test_to_dict_method_includes_class_key(self):
        """Test if 'to_dict' method includes '__class__' key"""
        model_dict = self.model.to_dict()
        self.assertIn('__class__', model_dict)

    def test_to_dict_method_includes_created_at_key(self):
        """Test if 'to_dict' method includes 'created_at' key"""
        model_dict = self.model.to_dict()
        self.assertIn('created_at', model_dict)

    def test_to_dict_method_includes_updated_at_key(self):
        """Test if 'to_dict' method includes 'updated_at' key"""
        model_dict = self.model.to_dict()
        self.assertIn('updated_at', model_dict)

    def test_init_with_kwargs_removes_class_key(self):
        """Test if '__class__' key is removed from kwargs"""
        kwargs = {"__class__": "SomeClass", "name": "TestObject"}
        model = BaseModel(**kwargs)
        self.assertNotIn('__class__', model.__dict__)

    def test_init_with_kwargs_sets_attributes_correctly(self):
        """Test if attributes are set correctly from kwargs"""
        kwargs = {"name": "TestObject", "created_at":
                  "2023-01-01T00:00:00.123456", "value": 42}
        model = BaseModel(**kwargs)
        self.assertEqual(model.name, "TestObject")
        self.assertEqual(model.value, 42)
        self.assertIsInstance(model.created_at, datetime)
        self.assertEqual(model.created_at.isoformat(),
                         "2023-01-01T00:00:00.123456")

    def test_init_with_kwargs_handles_datetime_format(self):
        """Test if 'created_at' and 'updated_at' are parsed
        from kwargs correctly"""
        kwargs = {"created_at": "2023-01-01T00:00:00.123456",
                  "updated_at": "2023-02-02T01:01:01.654321"}
        model = BaseModel(**kwargs)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)
        self.assertEqual(model.created_at.isoformat(),
                         "2023-01-01T00:00:00.123456")
        self.assertEqual(model.updated_at.isoformat(),
                         "2023-02-02T01:01:01.654321")

    def test_init_with_id(self):
        """Test if 'id' is correctly initialized when provided"""
        custom_id = "custom_id"
        model = BaseModel(id=custom_id)
        self.assertEqual(model.id, custom_id)

    def test_init_with_invalid_created_at(self):
        """Test if an invalid 'created_at' format raises an exception"""
        with self.assertRaises(ValueError):
            BaseModel(created_at="invalid_format")

    def test_init_with_invalid_updated_at(self):
        """Test if an invalid 'updated_at' format raises an exception"""
        with self.assertRaises(ValueError):
            BaseModel(updated_at="invalid_format")

    def test_str_representation_with_custom_attributes(self):
        """Test the string representation when custom attributes are added"""
        model = BaseModel(name="TestObject", value=42)
        expected_str = f"[BaseModel] ({model.id}) {{'name': 'TestObject', 'value': 42}}"
        self.assertEqual(str(model), expected_str)

    def test_save_method_updates_updated_at(self):
        """Test if the 'save' method updates 'updated_at' correctly"""
        old_updated_at = self.model.updated_at.timestamp()
        self.model.save()
        self.assertGreater(self.model.updated_at.timestamp(), old_updated_at)

    def test_to_dict_method_includes_custom_attributes(self):
        """Test if 'to_dict' method includes custom attributes"""
        model = BaseModel(name="TestObject", value=42)
        model_dict = model.to_dict()
        self.assertIn('name', model_dict)
        self.assertIn('value', model_dict)
        self.assertEqual(model_dict['name'], "TestObject")
        self.assertEqual(model_dict['value'], 42)

    def test_to_dict_method_includes_custom_attributes_type(self):
        """Test if 'to_dict' method includes the correct type
        for custom attributes"""
        model = BaseModel(name="TestObject", value=42)
        model_dict = model.to_dict()
        self.assertEqual(type(model_dict['name']), str)
        self.assertEqual(type(model_dict['value']), int)

    def test_to_dict_method_includes_custom_attributes_type_list(self):
        """Test if 'to_dict' method includes the correct type
        for custom attributes in a list"""
        model = BaseModel(name="TestObject", values=[42, 43, 44])
        model_dict = model.to_dict()
        self.assertEqual(type(model_dict['values']), list)
        self.assertEqual(type(model_dict['values'][0]), int)
        self.assertEqual(type(model_dict['values'][1]), int)
        self.assertEqual(type(model_dict['values'][2]), int)


if __name__ == '__main__':
    unittest.main()