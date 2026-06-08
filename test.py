# Simple Python script with 20 lines of code

# Function to calculate factorial
def factorial(n: object) -> int:
    """Calculate factorial for non-negative integers."""
    # Essential input validation to prevent invalid or unsafe recursion-like behavior.
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be a non-negative integer")

    # Iterative implementation avoids recursion depth limits and improves stability.
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def main():
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


# Main program
if __name__ == "__main__":
    main()
