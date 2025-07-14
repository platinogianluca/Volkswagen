# Gianluca Giuffrida Izquierdo

## Technical Decisions & Architecture

The project is built using Python and structured following the principles of **Hexagonal Architecture** (also known as Ports and Adapters) and **Domain-Driven Design (DDD)**.

### Hexagonal Architecture

The core logic of the application is completely independent of external services and frameworks. This is achieved by separating the code into three main layers:

-   **Domain**: Contains the core business logic, rules, and entities. This layer is the heart of the application and has no dependencies on any other layer. It includes entities like `Robot` and `WorkSpace`, and value objects like `Position` and `Orientation`.
-   **Application**: Orchestrates the application's use cases (application logic). It directs the domain objects to fulfill tasks according to a specific workflow, but the core business rules themselves are encapsulated within the domain. This layer defines the interfaces (ports) required to interact with the outside world, such as `RobotRepository` and `WorkSpaceRepository`.
-   **Infrastructure**: Provides the concrete implementations (adapters) for the ports defined in the application layer. This layer is responsible for all external communication, such as reading from a file, interacting with a database, or exposing an API.

**Benefits of this approach:**

-   **Framework Independence**: The core logic is not tied to any specific framework or technology.
-   **Testability**: The domain and application layers can be tested in isolation without needing external dependencies like databases or web servers.
-   **Maintainability & Flexibility**: By decoupling the core logic from external concerns, the system becomes easier to maintain. For example, if we need to change the input source from a text file to a REST API, we would only need to create a new adapter in the infrastructure layer without modifying the core application.

### Domain-Driven Design (DDD)

DDD principles were applied to create a rich and expressive domain model that accurately reflects the business requirements.

-   **Ubiquitous Language**: The names used in the domain model (`Robot`, `WorkSpace`, `Position`, `Orientation`) are taken directly from the problem description. This creates a shared, unambiguous language between the code and the problem domain.
-   **Rich Domain Model**: Business logic and rules are encapsulated within the domain entities themselves. For instance, the `Robot` entity is responsible for executing instructions and updating its own state (`Position` and `Orientation`), ensuring that all operations are valid and consistent. This contrasts with an anemic domain model where logic is handled by external service classes, leading to scattered and less cohesive code.

**Benefits of this approach:**

-   **Cohesion**: Business logic is located close to the data it manipulates, making the system more modular and easier to understand.
-   **Robustness**: Domain rules and constraints are consistently enforced within the entities, reducing the risk of errors.
-   **Maintainability**: A clear and expressive domain model makes the system easier to reason about and evolve over time.

## Assumptions

During the development of this solution, a few assumptions were made based on the interpretation of the challenge:

1.  **Input Source**: I have assumed that the input is provided via a text file (`input.txt`). The application reads this file to get the workspace dimensions and the robot instructions.
2.  **Output Destination**: The final positions of the robots are printed to the standard output console.
3.  **Input Formatting**: The input file is expected to have space-separated values. For a robot's initial position like `12 N`, a space is required between `1`, `2` and `N`. This allows the parser to correctly handle


## How to Run the Project

To get the project running on your local machine, follow these steps.

### Prerequisites

-   Python 3.8+
-   pip

### Installation & Execution

1.  **Clone the repository** (or use your local copy):
    ````sh
    git clone <your-repository-url>
    cd Volkswagen
    ````

2.  **Install dependencies** from the `requirements.txt` file:
    ````sh
    pip install -r requirements.txt
    ````

3.  **Prepare the input file**:
    Make sure the `input.txt` file is present in the root directory and contains the data in the specified format.

4.  **Run the application**:
    ````sh
    python main.py
    ````
    The output with the final positions of the robots will be printed to the console.

### Running Tests

To run the full test suite and ensure everything is working as expected, use `pytest`:
````sh
pytest
````

## Project Structure

````
.
├── src/
│        │ 
│        ├── application/      # Application layer (use cases, ports)
│        ├── domain/           # Domain layer (entities, value objects, business logic)
│        └── infrastructure/   # Infrastructure layer (adapters for files, APIs, etc.)
├── tests/                    # Test suite for all layers
├── .gitignore
├── input.txt                 # Default input file for the application
├── main.py                   # Main entry point of the application
├── README.md                 # This file
└── requirements.txt          # Project dependencies