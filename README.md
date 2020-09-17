# rickandmorty Test


<!-- TABLE OF CONTENTS -->
## Table of Contents
* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)



<!-- ABOUT THE PROJECT -->
## About The Project
This project creates a Flask application to fetch characters from Rick and Morty API. [Rick and Morty API Docs](https://rickandmortyapi.com/documentation/#introduction)  .  
The app fetches all characters that meets the following conditions:
* Species is “Human”
* Status is “Alive”
* Origin is “Earth”

Each character that meets the conditions will be saved and include:
* Name.
* Location.
* Image link.



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

`** Assumed that the env of the test is mac (minikube config limitations) **`

`** The project was developed and tested with python 3.8 version. other versions were not tested **`


* make
* python 3.8
* docker
* minikube

### Installation

1\. Clone the repo
```sh
git clone https://github.com/shm-rickandmorty/rickandmorty.git
cd rickandmorty
```

2\. To start locally on your host run from the repo path:
```sh
pip install -r requirements.txt
python app.py
```

3\. To start app on a docker:
```sh
docker build -t rickandmorty .
docker run --rm --name rickandmorty -p 5000:5000 rickandmorty
```

4\. To Start on a minikube server:
```sh
minikube start --driver=hyperkit --insecure-registry=localhost:5000
eval $(minikube docker-env)
minikube addons enable registry
docker run --rm -it --network=host alpine ash -c "apk add socat && socat TCP-LISTEN:5000,reuseaddr,fork TCP:$(minikube ip):5000"
minikube addons enable ingress
echo  "# minikube rickandmorty test\n$(minikube ip)  rickandmorty.info" | sudo tee -a /etc/hosts
docker build -t localhost:5000/rickandmorty .
docker push localhost:5000/rickandmorty
kubectl apply -f yamls/
```


<!-- USAGE EXAMPLES -->

# Usage
```
The First query can take some time (up to few minutes). 
In the first time query the app fetches all characters, and save them locally (in csv file). 
The second query will fetch the data from the file.
```

* On local env (Docker or on the host directly):
    * health check: curl "localhost:5000/healthcheck"
    ```sh 
    curl "localhost:5000/healthcheck"
    ```
    * fetch all characters: 
    ```sh 
    curl "localhost:5000/all"
    ```
    * fetch characters with a specific names: 
    ```sh 
    curl "localhost:5000/characters?name=Veterinary%20Nurse&name=Tricia%20Lange"
    ```
    * fetch characters with a specific location: 
    ```sh 
    curl "localhost:5000/locations?location=Earth%20(Replacement%20Dimension)"
    ```

* On minikube env replace `localhost:5000` to `rickandmorty.info`
    ```
    e.g:
    
    curl "rickandmorty.info/all"
    ```
  
* Use the make file. The option are given:
    ```sh
    make help
    ``` 
 
 
  


