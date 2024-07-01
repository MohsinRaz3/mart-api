# Mart API Project

The Mart API project is an advanced product management system built using FastAPI and SQLModel. It incorporates several technologies to ensure robust and efficient operations. Key features and technologies include:

- **FastAPI:** Provides a high-performance web framework for building APIs.
- **SQLModel:** Utilized for ORM capabilities to interact with the PostgreSQL database.
- **PostgreSQL:** Serves as the database for storing product information securely and efficiently.
- **Docker:** Containerizes the application for consistent and isolated development and deployment environments.
- **Kafka:** Used for event streaming to handle real-time data processing and communication between services.

## Architecture

### Microservices

- **User Service:** Manages user authentication, registration, and profiles.
- **Product Service:** Manages product catalog, including CRUD operations for products.
- **Order Service:** Handles order creation, updating, and tracking.
- **Inventory Service:** Manages stock levels and inventory updates.
- **Notification Service:** Sends notifications (email, SMS) to users about order statuses and other updates.
- **Payment Service:** Processes payments and manages transaction records.
