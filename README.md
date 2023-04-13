# Python Security

Python Security est un projet réalisé par notre groupe de 4 étudiants dans le cadre du cours de sécurité Python à l'EPITA. 

Consulter la [==> documentation Sphinx <==](https://sazard.github.io/python_security/_build/html/)

## Fonctionnalités

* ✅ Analyse réseau
* ✅ Scan de chaque machine du réseau
* ✅ Génération de rapport (HTML, JSON, CSV)
* ✅ Scan de port multithread
* ✅ Environnement Docker pour tests et exécution
* ✅ Simulation d'attaques avec `src/tools/pirate.py`

## Dépendances
* `python 3.x` et le contenu de `requirements.txt`
* `docker`
* `docker-compose`

## Installation

* Clonez le dépôt :

```
git clone https://github.com/Sazard/python_security
cd python_security
```

## Installez les dépendances

```
pip install -r requirements.txt
```

## Utilisation sans docker

Lancer directement `python3 src/main.py --help` pour voir les options.

```
python3 src/main.py --help
usage: main.py [-h] [-i ip] [-n netmask] [-1 single_ip] [-f output_format] [-a analyse]

Basic network scanner

options:
  -h, --help            show this help message and exit
  -i ip, --ip ip        Host IP address
  -n netmask, --netmask netmask
                        Subnet mask
  -1 single_ip, --single-ip single_ip
                        Single IP address to scan
  -f output_format, --output-format output_format
                        Output format
  -a analyze, --analyse analyse
                        Analyse network traffic
```

Explication des options :
* -h, --help : Affiche l'aide et la liste des options disponibles.
* -i ip, --ip ip : Spécifie l'adresse IP de l'hôte.
* -n netmask, --netmask netmask : Spécifie le masque de sous-réseau.
* -1 single_ip, --single-ip single_ip : Spécifie une seule adresse IP à analyser.
* -f output_format, --output-format output_format : Choisissez le format de sortie pour les rapports ("html", "json", "csv").
* -a analyse, --analyse analyse : Analyse le trafic réseau. Utilisez -a "*" pour analyser toutes les interfaces réseau de la machine.

## Utilisation avec docker
Pour lancer le projet dans un environnement Docker interactif, exécutez le script `build_and_run.sh` :

```
./build_and_run.sh
... création des environnements réseau et build de l'image ...
```

![image](https://user-images.githubusercontent.com/44167150/231593068-ff22d444-e301-40c4-a85f-6fee5a6416ba.png)


Cela lancera un shell Bash dans l'image Docker, avec un environnement réseau créé automatiquement.

## Utilisation du mode scan de port

**1. Avec docker : lancera un shell interactif dans un docker ayant l'IP 172.18.1.10 dans un réseau dédié**
```
./build_and_run.sh
... création des environnements réseau et build de l'image ...

python3 src/main.py --help
usage: main.py [-h] [-i ip] [-n netmask] [-1 single_ip] [-f output_format] [-a analyse]

Basic network scanner

options:
  -h, --help            show this help message and exit
  -i ip, --ip ip        Host IP address
  -n netmask, --netmask netmask
                        Subnet mask
  -1 single_ip, --single-ip single_ip
                        Single IP address to scan
  -f output_format, --output-format output_format
                        Output format
  -a analyse, --analyse analyse
                        Analyse network traffic

python3 src/main.py --single-ip 172.18.1.3 -f <format>
```

Les rapports peuvent être générés aux formats nommés "html", "json", "csv" avec l'option "-f", "--format"

**2. Sans docker : lancer le script directement sans docker**
```
python3 src/main.py --help
usage: main.py [-h] [-i ip] [-n netmask] [-1 single_ip] [-f output_format] [-a analyse]

Basic network scanner

options:
  -h, --help            show this help message and exit
  -i ip, --ip ip        Host IP address
  -n netmask, --netmask netmask
                        Subnet mask
  -1 single_ip, --single-ip single_ip
                        Single IP address to scan
  -f output_format, --output-format output_format
                        Output format
  -a analyse, --analyse analyse
                        Analyse network traffic

python3 src/main.py --single-ip 65.21.239.190 -f <format>
```

## Utilisation du mode analyse réseau

Lancer dans deux consoles séparées - avec ou sans docker - si docker est utilisé il faut lancer deux instances différentes à partir de la commande `docker run` et changer l'IP, par exemple : 

**1. Lancer un shell interactif automatiquement dans le conteneur 1 avec l'IP 172.18.1.10**
```
./build_and_run.sh 
... création des environnements réseau et build de l'image ...
```

* Première console dans le conteneur 1 (celui lancé avec `build_and_run.sh`):
```
python3 src/main.py -a "*"
```

*Le script `main.py` avec le mode "-a" (pour analyse réseau) sera en écoute sur toutes les interfaces réseau de la machine.*

**2. Lancer un shell interactif dans le conteneur 2 avec l'IP 172.18.1.12 en lançant la commande suivante :**

```
docker run -v "$PWD/:/opt/python-securite" --name python-securite2 -it --ip 172.18.1.12 --network test_network python-securite:dev
```  

![image](https://user-images.githubusercontent.com/44167150/231593265-e3e2f653-5e1d-4204-8c98-a611827d7ede.png)

* Deuxième console dans le conteneur 2 (celui lancé avec la commande):
```
python3 src/tools/pirate.py --target <target> --host <host>
```

Le script `pirate.py` génère tout un tas d'attaques qui apparaitrons dans la première console. Etant donné que le docker est en `root` il n'y a pas besoin de sudo pour lancer le script d'attaque.

Cela devrait être ainsi :

![image](https://user-images.githubusercontent.com/44167150/231594159-21b2b501-ca3a-4e21-847c-bcca6e5e2842.png)

⚠️ Sans docker, il faut simplement lancer deux consoles séparées. Ne pas oublier d'installer les dépendances avec sudo.
L'avantage d'utiliser le docker est qu'il est directement en `root`.

Utilisation sans docker :
```
sudo pip install -r requirements.txt # sinon problème d'import python
sudo python3 src/tools/pirate.py --target <target> --host <host>
```

# Tests 

⚠️ attention c'est très long, regardez plutôt la trace dans GitHub Actions

Pour lancer les tests, exécutez le script `tests/non_interactive_run.sh` :

```
./tests/non_interactive_run.sh
```

Ce script appelle directement `pytest` et effectue le tout dans docker.

# Documentation

La documentation est générée à partir du code Python à l'aide de Sphinx et du thème Read the Docs. Pour générer la documentation, exécutez les commandes suivantes :

```
cd docs
make html
```

Vous pouvez ensuite accéder à la documentation en ouvrant le fichier `docs/_build/html/index.html` dans votre navigateur ou y accéder via [ce lien](https://sazard.github.io/python_security/_build/html/).

# Jalons
- Premier jalon (05/04/2023) :
    - POC fonctionnalités de base (sniffing : parseur de paquet, scan de port : finger printing) ✅ 
    - Revue de code ✅ 

- Second jalon (07/04/2023) :
    - Documentation ✅ 
    - Amélioration des fonctionnalités ✅ 
    - Vérification du pipeline et des tests unitaires ✅ 

- Troisième jalon (15/04/2023) :
    - Revue documentation ✅ 
    - Export des données dans les formats convenus ✅ 
    - Environnement Docker complet pour les tests ✅ 

- Quatrième jalon (20/04/2023) :
    - PoC complet
    - Documentation de run complète

# Contributeurs

* Stanislas MEDRANO
* Clément MILISAVLJEVIC
* Antoine REMY
* Nicolas SUTTER

Ce projet est réalisé dans le cadre du cours de sécurité Python à l'EPITA.
