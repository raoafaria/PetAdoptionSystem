# PetAdoptionServer

This is created using Java.

## Installation

Setup Pom.xml file. Code this already there. Then run the following command to build the project with all the dependencies. This will also generate the necessary gRPC files in /target folder.
```bash
mvn clean install
```
Then run the following command to start the server.
```bash
mvn exec:java -Dexec.mainClass="com.example.petadoption.PetAdoptionServer"
```

# PetAdoptionClient

This is created using Python.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install necessary packages.

```bash
pip install grpcio grpcio-tools
```
Then run the following command to generate the gRPC files.
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. pet_adoption.proto
```

## Usage
Run the following command.
```bash
python pet_adoption_client.py
```