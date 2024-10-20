import unittest
from unittest.mock import MagicMock, patch
import pet_adoption_pb2
import pet_adoption_pb2_grpc
from pet_adoption_client import PetAdoptionClient  # Make sure to import your PetAdoptionClient class

class TestPetAdoptionClient(unittest.TestCase):
    @patch('pet_adoption_pb2_grpc.PetAdoptionStub')
    def setUp(self, mock_stub):
        # Mock the gRPC stub
        self.client = PetAdoptionClient()
        self.client.stub = mock_stub()

    def test_register_pet_success(self):
        # Arrange
        mock_response = pet_adoption_pb2.RegistrationResponse(success=True, message="Pet registered successfully.")
        self.client.stub.RegisterPet = MagicMock(return_value=mock_response)

        # Act
        success, message = self.client.register_pet("Buddy", "Male", 5, "Golden Retriever", "http://example.com/pic.jpg")

        # Assert
        self.assertTrue(success)
        self.assertEqual(message, "Pet registered successfully.")

    def test_register_pet_failure(self):
        # Arrange
        mock_response = pet_adoption_pb2.RegistrationResponse(success=False, message="Registration failed.")
        self.client.stub.RegisterPet = MagicMock(return_value=mock_response)

        # Act
        success, message = self.client.register_pet("Buddy", "Male", 5, "Golden Retriever", "http://example.com/pic.jpg")

        # Assert
        self.assertFalse(success)
        self.assertEqual(message, "Registration failed.")

    def test_search_pet_found(self):
        # Arrange
        pet_list = pet_adoption_pb2.PetList(pets=[pet_adoption_pb2.Pet(name="Buddy", gender="Male", age=5, breed="Golden Retriever")])
        self.client.stub.SearchPet = MagicMock(return_value=pet_list)

        # Act
        pets = self.client.search_pet(name="Buddy")

        # Assert
        self.assertEqual(len(pets), 1)
        self.assertEqual(pets[0].name, "Buddy")

    def test_search_pet_not_found(self):
        # Arrange
        pet_list = pet_adoption_pb2.PetList(pets=[])
        self.client.stub.SearchPet = MagicMock(return_value=pet_list)

        # Act
        pets = self.client.search_pet(name="Nonexistent")

        # Assert
        self.assertEqual(len(pets), 0)

    def test_search_pet_with_empty_parameters(self):
        # Arrange
        pet_list = pet_adoption_pb2.PetList(pets=[
            pet_adoption_pb2.Pet(name="Buddy", gender="Male", age=5, breed="Golden Retriever"),
            pet_adoption_pb2.Pet(name="Mittens", gender="Female", age=3, breed="Siamese")
        ])
        self.client.stub.SearchPet = MagicMock(return_value=pet_list)

        # Act
        pets = self.client.search_pet()

        # Assert
        self.assertEqual(len(pets), 2)

if __name__ == '__main__':
    unittest.main()
