# Use an official GCC image as the base image
FROM gcc:latest

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the C program to the container
COPY hello.c .

# Compile the C program inside the container
RUN gcc -o hello hello.c

# Command to run the program when the container starts
CMD ["./hello"]
