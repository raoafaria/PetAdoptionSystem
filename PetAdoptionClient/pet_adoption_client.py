import threading
import time

import grpc
import pet_adoption_pb2
import pet_adoption_pb2_grpc

class PetAdoptionClient:
    def __init__(self, server_address='localhost:50051'):
        self.channel = grpc.insecure_channel(server_address)
        self.stub = pet_adoption_pb2_grpc.PetAdoptionStub(self.channel)

    def register_pet(self, name, gender, age, breed, picture_url):
        pet = pet_adoption_pb2.Pet(
            name=name,
            gender=gender,
            age=age,
            breed=breed,
            picture_url=picture_url
        )
        response = self.stub.RegisterPet(pet)
        return response.success, response.message

    def search_pet(self, name=None, gender=None, age=None, breed=None):
        search_request = pet_adoption_pb2.SearchRequest(
            name=name if name else "",
            gender=gender if gender else "",
            age=age if age else 0,
            breed=breed if breed else ""
        )
        pet_list = self.stub.SearchPet(search_request)
        return pet_list.pets

    def close(self):
        self.channel.close()

def send_registration_request(client, name, gender, age, breed, picture_url):
    success, message = client.register_pet(name, gender, age, breed, picture_url)
    print(f"Response for {name}: Success: {success}, Message: {message}")

def send_search_request(client, name):
    if name:
        pets = client.search_pet(name=name)
        if pets:
            for pet in pets:
                print(f"Search Response: Found Pet: {pet.name}, Breed: {pet.breed}")
        else:
            print(f"Search Response: No Pets Found with name: {name}")
    else:
        print(f"Search Response: No name provided")

def main():
    client = PetAdoptionClient()

    threads = []
    pet_date = [
        ("Buddy", "Male", 5, "Golden Retriever", "http://example.com/buddy.jpg"),
        ("Mittens", "Female", 3, "Siamese", "http://example.com/mittens.jpg"),
        ("Rex", "Male", 2, "Beagle", "http://example.com/rex.jpg"),
        ("Luna", "Female", 4, "Poodle", "http://example.com/luna.jpg"),
        ("Max", "Male", 1, "Bulldog", "http://example.com/max.jpg"),
    ]

    for name, gender, age, breed, picture_url in pet_date:
        thread = threading.Thread(target=send_registration_request, args=(client, name, gender, age, breed, picture_url))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    search_names = ["Buddy", "Mittens", "None"]
    search_threads = []

    for name in search_names:
        print(f"Searching {name}")
        thread = threading.Thread(target=send_search_request, args=(client, name))
        search_threads.append(thread)
        thread.start()

    for thread in search_threads:
        thread.join()

    client.close()

if __name__ == "__main__":
    main()
