# Simple Python script with 20 lines of code

# Function to calculate factorial
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)

# Main program
if __name__ == "__main__":
    # Print welcome message
    print("Welcome to CodeBuddy!")
    
    # Example variables
    name = "User"
    numbers = [1, 2, 3, 4, 5]
    
    # Loop through numbers
    for num in numbers:
        print(f"Number: {num}")
    
    # Calculate factorial
    result = factorial(5)
    print(f"Factorial of 5 is: {result}")
    
    # Dictionary example
    user_data = {"name": name, "age": 30}
    print(f"User data: {user_data}")
    
    # End of program
    print("Program completed!")