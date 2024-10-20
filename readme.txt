Client - Python
pip install grpcio grpcio-tools 
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. pet_adoption.proto


Server - Java
Setup Pom.xml file. Code this already there.
mvn clean install
mvn exec:java -Dexec.mainClass="com.example.petadoption.PetAdoptionServer"

