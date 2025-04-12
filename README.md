# Log Platform

A scalable logging platform built with FastAPI, Kafka, Prometheus, and Grafana. This system captures application logs, processes them through Kafka, and provides real-time monitoring and visualization capabilities.

## Architecture

![Architecture](https://i.imgur.com/example.png)

The platform consists of the following components:
- **FastAPI Application**: Generates logs for different endpoints
- **Apache Kafka**: Message broker for log processing
- **Kafka Consumer**: Processes logs and exposes metrics
- **Prometheus**: Time-series database for metrics storage
- **Grafana**: Visualization and monitoring dashboard

## Features

- Real-time log processing
- Metrics collection and monitoring
- Authentication logs tracking
- General application logs tracking
- Beautiful visualization with Grafana
- Scalable architecture using Kafka

## Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Git

## Quick Start

1. Clone the repository:
```bash
git clone <your-repo-url>
cd log-platform
```

2. Start the services:
```bash
docker-compose up --build
```

3. Access the services:
- FastAPI Application: http://localhost:8000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (default credentials: admin/admin)

## Generate Test Data

Run the test data generator to simulate log generation:
```bash
python test_data_generator.py
```

## API Endpoints

### General Endpoints
- `GET /`: Welcome message
- `GET /data`: Sample data endpoint

### Authentication Endpoints
- `POST /login`: User login
- `POST /signup`: User registration
- `PUT /profile`: Profile update

## Monitoring

### Available Metrics
- Logs processed by type
- Processing time
- Endpoint hits
- User activity

### Grafana Dashboards
The platform comes with pre-configured dashboards showing:
- Log processing rates
- Total logs by type
- Endpoint usage patterns
- System health metrics

## Project Structure

```
log-platform/
├── app/
│   ├── main.py              # FastAPI application
│   ├── consumer/            # Kafka consumer
│   └── Dockerfile.consumer  # Consumer Dockerfile
├── grafana/
│   └── provisioning/        # Grafana configuration
├── docker-compose.yml       # Service orchestration
├── prometheus.yml          # Prometheus configuration
├── requirements.txt        # Python dependencies
└── test_data_generator.py  # Test data simulation
```

## Configuration

### Kafka
- Bootstrap Server: kafka:9092
- Topics: 
  - general-logs
  - auth-logs

### Prometheus
- Scrape Interval: 15s
- Retention: 15 days

### Grafana
- Default Port: 3000
- Anonymous Access: Enabled
- Default Org Role: Viewer

## Development

To modify or extend the platform:

1. Update FastAPI endpoints in `app/main.py`
2. Modify consumer logic in `app/consumer/log_consumer.py`
3. Add new metrics in the consumer
4. Create custom Grafana dashboards

## Troubleshooting

Common issues and solutions:

1. **Services not starting**
   - Ensure Docker is running
   - Check port conflicts
   - Verify Docker Compose file

2. **No metrics in Grafana**
   - Verify Prometheus connection
   - Check if consumer is processing logs
   - Run test data generator

3. **Kafka connection issues**
   - Ensure Kafka is healthy
   - Check network connectivity
   - Verify topic creation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastAPI
- Apache Kafka
- Prometheus
- Grafana
- Docker 