# The test task for ProstoPay

## Steps to run the project:

### Task 1: Implement a hash table

<p>Simplicity and Understandability: My goal was to create a simple and easily understandable class that would be accessible even to programming beginners.

Efficiency of Basic Operations: While this implementation lacks complex collision resolution mechanisms, it ensures efficient performance of basic operations such as insertion, retrieval, and deletion.

Adherence to Python Standards: I preferred to adhere to standard Python practices, such as raising a KeyError exception when a key is not found, which facilitates understanding by other developers.

Minimalistic Functionality: To avoid unnecessary complexity and overhead, I included only a basic set of functionalities without adding unnecessary logic.

Convenient Interface: The interface of my class is designed for convenience, providing clear methods for interacting with the hash table without excessive complexity.
</p>

1. Clone the repository

```bash
git clone https://github.com/vlad-bb/test_task_prostopay.git
```

2. Install the requirements

```bash
pip install -r requirements.txt
```

3. Run the test

```bash
pytest task_1/test_hashtable.py
```

### Task 2: 
<p>
Mocking Database Operations:

I use AsyncMock to mock the behavior of AsyncSession, allowing us to simulate database operations without actually hitting the database.
For simulating database queries, I use MagicMock to mock the return value of session.execute. 
This allows us to control the behavior of the database queries and ensure deterministic test results.
Clear Test Case Names and Descriptions:

Each test case has a descriptive name and docstring, making it easy to understand its purpose and what aspect of the service it is testing.
Isolated Tests:

By utilizing IsolatedAsyncioTestCase, each test case runs in an isolated event loop, preventing interference between tests and ensuring test independence.
Test Scenario Coverage:

The test suite covers various scenarios, including fetching users by email and ID, handling nonexistent users, and creating users with and without existing email addresses. This provides comprehensive coverage of the UserService functionality.
Overall, the chosen implementation ensures that the tests are well-structured, isolated, and cover a wide range of scenarios, enabling thorough testing of the UserService class.
</p>

1. Run the test

```bash
pytest task_2/test_service.py
```