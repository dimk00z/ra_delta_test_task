# International Delivery Service

## Task

You can find the task details in the [Google Doc](https://docs.google.com/document/d/1rmbGprfekLIdAdEJtaw2lhw5qdaHF-f770qmdRBgyP8/edit?usp=sharing).

## Solution Overview

This project is a microservice designed to manage international delivery services. It includes API endpoints for managing parcels, checking currency rates, and ensuring the system’s health.

## Environment Setup

1.Clone the Repository

git clone [<repository_url>](https://github.com/dimk00z/ra_delta_test_task)
cd ra_delta_test_task

2.Copy and Configure the Environment File

```bash
cp .env.example .env
```

Edit the .env file with your desired configuration.

3.Start the Services

Build and run the application:

```bash
make build
make migrate
make up
```

Technologies Used

- Python 3.13+
- Database: MySQL (SQLite for testing)
- Cache: Redis (FakeRedis for testing)
- Message Broker: RabbitMQ
- Framework: FastAPI
- ORM: SQLModel(SQLAlchemy under the hood)
- Validation: Pydantic
- Dependency Injection: Dishka
- Code Quality Tools:
- Package Manager: uv
- Linting and Formatting: ruff

API Documentation

Interactive API documentation is available via Swagger:

- `GET /docs`

Core API Endpoints

Delivery API

- `GET /api/v1/currency/{currency}` Retrieve the exchange rate for a given currency.
- `GET /api/v1/delivery/parcels/types` Fetch all available parcel types.
- `GET /api/v1/delivery/parcels` Retrieve parcels associated with a user.
- `POST /api/v1/delivery/parcels/background` Register a parcel asynchronously using RabbitMQ.
- `POST /api/v1/delivery/parcels` Register a parcel synchronously. Useful for testing business logic.
- `GET /api/v1/delivery/parcels/{parcel_id}` Fetch details of a specific parcel.

Health Check API

- `GET /api/v1/health/ping` Simple health check endpoint.
- `GET /api/v1/health/check` Detailed health check endpoint.

Development

Running Locally
1.Install dependencies:

`uv sync`

2.Run the server:

`export PYTHONPATH=. && uv run app.main`

Testing

Run the tests with:

`export PYTHONPATH=. && uv run pytest ./tests`

Test results:

```bash
export PYTHONPATH=. && uv run pytest ./tests
==================================== test session starts =====================================
platform darwin -- Python 3.13.0, pytest-8.3.4, pluggy-1.5.0
configfile: pyproject.toml
plugins: Faker-33.1.0, asyncio-0.25.0, anyio-4.7.0
asyncio: mode=Mode.STRICT, asyncio_default_fixture_loop_scope=session
collected 10 items                                                                           

tests/app/currency/test_currency.py .                                                  [ 10%]
tests/app/delivery/test_get_parcel.py ..                                               [ 30%]
tests/app/delivery/test_get_parcels.py ..                                              [ 50%]
tests/app/delivery/test_parcel_creation.py ..                                          [ 70%]
tests/app/delivery/test_parcels_types.py .                                             [ 80%]
tests/app/health/test_health.py ..                                                     [100%]

===================================== 10 passed in 0.12s =====================================
```

Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

License

This project is licensed under the MIT License. See the LICENSE file for details.
