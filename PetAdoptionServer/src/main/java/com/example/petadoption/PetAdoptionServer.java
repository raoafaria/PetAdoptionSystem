package com.example.petadoption;

import io.grpc.Server;
import io.grpc.ServerBuilder;
import io.grpc.stub.StreamObserver;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class PetAdoptionServer {
    private final int port = 50051;  // gRPC default port
    private Server server;
    private static final int THREAD_POOL_SIZE = 15;

    // Start the gRPC server
    private void start() throws IOException {
        ExecutorService threadPool = Executors.newFixedThreadPool(THREAD_POOL_SIZE);
        server = ServerBuilder.forPort(port)
                .addService(new PetAdoptionServiceImpl())  // Attach the service implementation
                .executor(threadPool)
                .build()
                .start();
        System.out.println("Server started, listening on " + port);

        // Add a shutdown hook to handle server shutdown
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.err.println("Shutting down gRPC server...");
            PetAdoptionServer.this.stop();
            System.err.println("Server shut down.");
        }));
    }

    // Stop the gRPC server
    private void stop() {
        if (server != null) {
            server.shutdown();
        }
    }

    // Block until the server is terminated
    private void blockUntilShutdown() throws InterruptedException {
        if (server != null) {
            server.awaitTermination();
        }
    }

    // Main method to start the server
    public static void main(String[] args) throws IOException, InterruptedException {
        final PetAdoptionServer server = new PetAdoptionServer();
        server.start();
        server.blockUntilShutdown();
    }

    // Service implementation (you will implement this)
    static class PetAdoptionServiceImpl extends PetAdoptionGrpc.PetAdoptionImplBase {

        private final List<PetAdoptionProto.Pet> petList = new ArrayList<>();

        @Override
        public void registerPet(PetAdoptionProto.Pet request, StreamObserver<PetAdoptionProto.RegistrationResponse> responseObserver) {
            // Add the pet to the list
            petList.add(request);

            // Send response
            PetAdoptionProto.RegistrationResponse response = PetAdoptionProto.RegistrationResponse.newBuilder()
                    .setSuccess(true)
                    .setMessage("Pet registered successfully!")
                    .build();

            // Send response back to client
            responseObserver.onNext(response);
            responseObserver.onCompleted();
        }

        @Override
        public void searchPet(PetAdoptionProto.SearchRequest request, StreamObserver<PetAdoptionProto.PetList> responseObserver) {
            // Search for pets matching the search criteria
            PetAdoptionProto.PetList.Builder resultBuilder = PetAdoptionProto.PetList.newBuilder();

            for (PetAdoptionProto.Pet pet : petList) {
                if ((request.getName().isEmpty() || pet.getName().equalsIgnoreCase(request.getName())) &&
                        (request.getGender().isEmpty() || pet.getGender().equalsIgnoreCase(request.getGender())) &&
                        (request.getAge() == 0 || pet.getAge() == request.getAge()) &&
                        (request.getBreed().isEmpty() || pet.getBreed().equalsIgnoreCase(request.getBreed()))) {
                    resultBuilder.addPets(pet);
                }
            }

            // Send search results back to client
            responseObserver.onNext(resultBuilder.build());
            responseObserver.onCompleted();
        }
    }
}