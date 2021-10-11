
# Mobilityhouse
  
This project captures, stores and retrieves test data on AMQP.
  
## Installation  
  
Prior to install the package, it is expected to have docker installed.  [Docker](https://docs.docker.com/engine/install/).
  
```bash  
## Building the containers  
sudo docker-compose build
## Starting the containers  
sudo docker-compose up
```  
  
## Using  
After the installation of all docker images and containers the application will be available on the following address.   
Web: 				127.0.0.1:8008  
RabbitMQ: 	127.0.0.1:15673   (username and password are in docker-compose.yml)

The saved data will be stored in the media folder.


##   Implementation

The test data, is handled using celery and beat. Each 10 seconds a beat sends a signal to the celery (worker). The worker is responsible for creating a RabbitMQ connection and sending a random data from 0-9000. The frequency of the data can be modified in the `celery.py`
The worker is also responsible for listening to the random data service. This service gets called when the system initiates  `@celeryd_init`. 

##   Future considerations
First thing that is needed to be implemented, is the feature to monitor the live data. This requirement can be fulfilled using web-socket and a buffer handler.

