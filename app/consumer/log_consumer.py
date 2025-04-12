from kafka import KafkaConsumer
import json
import logging
from prometheus_client import start_http_server, Counter, Histogram, Gauge
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prometheus metrics
LOGS_PROCESSED = Counter('logs_processed_total', 'Number of logs processed', ['log_type', 'endpoint'])
PROCESSING_TIME = Histogram('log_processing_seconds', 'Time spent processing logs', ['log_type', 'endpoint'])
LAST_LOG_TIMESTAMP = Gauge('last_log_timestamp', 'Timestamp of last processed log', ['log_type', 'endpoint'])
USER_ACTIVITY = Counter('user_activity_total', 'Number of activities by user', ['username', 'endpoint'])
ENDPOINT_HITS = Counter('endpoint_hits_total', 'Number of hits per endpoint', ['endpoint'])

class LogConsumer:
    def __init__(self):
        # Start Prometheus metrics server
        start_http_server(8000)
        logger.info("Started Prometheus metrics server on port 8000")
        
        self.consumer = KafkaConsumer(
            'general-logs', 'auth-logs',
            bootstrap_servers=['kafka:9092'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            group_id='log_processor_group',
            auto_offset_reset='earliest'
        )
        logger.info("Initialized Kafka consumer")

    def process_general_log(self, log_data):
        start_time = time.time()
        try:
            endpoint = log_data['endpoint']
            timestamp = log_data['timestamp']

            # Update metrics
            LOGS_PROCESSED.labels(log_type='general', endpoint=endpoint).inc()
            ENDPOINT_HITS.labels(endpoint=endpoint).inc()
            LAST_LOG_TIMESTAMP.labels(log_type='general', endpoint=endpoint).set(timestamp)
            
            logger.info(f"Processed general log for endpoint: {endpoint}")
        except Exception as e:
            logger.error(f"Error processing general log: {str(e)}")
        finally:
            PROCESSING_TIME.labels(log_type='general', endpoint=endpoint).observe(time.time() - start_time)

    def process_auth_log(self, log_data):
        start_time = time.time()
        try:
            endpoint = log_data['endpoint']
            username = log_data['user']
            timestamp = log_data['timestamp']

            # Update metrics
            LOGS_PROCESSED.labels(log_type='auth', endpoint=endpoint).inc()
            ENDPOINT_HITS.labels(endpoint=endpoint).inc()
            USER_ACTIVITY.labels(username=username, endpoint=endpoint).inc()
            LAST_LOG_TIMESTAMP.labels(log_type='auth', endpoint=endpoint).set(timestamp)
            
            logger.info(f"Processed auth log for user: {username} on endpoint: {endpoint}")
        except Exception as e:
            logger.error(f"Error processing auth log: {str(e)}")
        finally:
            PROCESSING_TIME.labels(log_type='auth', endpoint=endpoint).observe(time.time() - start_time)

    def start_consuming(self):
        try:
            logger.info("Starting log consumer...")
            for message in self.consumer:
                topic = message.topic
                log_data = message.value

                if topic == 'general-logs':
                    self.process_general_log(log_data)
                elif topic == 'auth-logs':
                    self.process_auth_log(log_data)

        except Exception as e:
            logger.error(f"Error in consumer: {str(e)}")

if __name__ == "__main__":
    consumer = LogConsumer()
    consumer.start_consuming() 