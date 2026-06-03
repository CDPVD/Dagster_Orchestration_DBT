# Dagster_Orchestration_DBT
Projet Dagster permettant l'exécution automatique des transformations

## Prérequis
Avant de commencer, assurez-vous d’avoir installé :
•	Python
•	Poetry
•	Driver ODBC 17 ou 18
•	Votre fichier pyproject.toml doit avoir les mêmes versions de dépendances que le repo CDPVD (important).

## Préparation des dépôts
1.	Clonez le projet Dagster depuis GitHub.
2.  Voisin de ce projet, assurez vous d'avoir votre repos CSS
    Exemple : cssdc.data.tbe
    ![alt text](doc_images\image.png)
3.  D'autres étapes devront être faite suite à la configuration du projet.

## Configuration du projet
### globalConfigs.cfg

La section de base est obligatoire!
Assurez vous de mettre à jours le nom du dossier contenant votre projet DBT:

![alt text](doc_images\image-1.png)

Les autres sections correspondent aux features additionnel pouvant être activé, mais nécéssitant une configuration. Voir à la fin de ce fichier pour plus de détails.

### profiles.yml

Vous devez remplacer votre adapteur fabric (adapteur par défaut de la CDPVD au moment d'écrire ces lignes) par l'adapteur sqlserver
Exemple de configuration sous windows:

![Windows](doc_images\image-2.png)

Exemple de configuration sous Linux:

![Linux](doc_images\image-3.png)

### Override du stamper
Permet de bypasser Fabric. Le fichier est disponible dans le projet Dagster et doit être ajouter à votre projet DBT CSS

![alt text](doc_images\image-4.png)

### Variable d'environnement
Pour fonctionner, Dagster a besoin d'une variable d'environnement nommée `DAGSTER_HOME`.

- Linux :
    + Ouvrir le fichier de configuration du shell : `nano ~/.bashrc`
    + Ajouter la ligne suivante en adaptant le chemin à votre environnement :
      `export DAGSTER_HOME="/home/theriaultp/Dagster_Orchestration_DBT"`
    + Enregistrer le fichier puis recharger la configuration :
      `source ~/.bashrc`

- Windows :
    + Ouvrir **Paramètres système avancés** puis **Variables d'environnement**.
    + Dans **Variables utilisateur**, cliquer sur **Nouveau**.
    + Renseigner :
        - Nom de la variable : `DAGSTER_HOME`
        - Valeur de la variable : `C:\Users\alluardj\10_projets\tbe\Dagster_Orchestration_DBT`
    + Valider avec **OK**.

### Préparation des environnements Poetry
#### Dans votre dossier CSS
1. Faire un poetry shell ainsi qu'un poetry install pour installer les dépendances (adapteur sqlserver entre autre)
2. Faire un ``` dbt clean ```
3. Faire un ``` dbt deps ```
4. Faire un ``` dbt parse ```
5. Faire un ``` dbt debug ```

Toutes ces commandes sont nécessaire pour s'assurer que vous avez un environnement fonctionnel

#### Dans votre dossier Dagster
Faire un poetry shell ainsi qu'un poetry install pour installer les dépendances.

## Test
Dans votre dossier dagster:
1. Lancer votre shell poetry
2. Faire ``` dagster dev ```:

    ![alt text](doc_images\image-5.png)
    
3. Allez à http://localhost:3000 pour valider que votre Dagster est démarrer.
4. Note: Il est parfois plus simple de passer directement en mode production, car certain accès sont requis pour l'écriture des fichiers temporaire lors d'un dagster dev.
5. Arrêtez votre dagster dev (CTRL + C)

## Passer en mode production
1. Dans un terminal, dans le dossier de dagster
2. Lancer: ``` poetry run dagster-webserver -h 0.0.0.0 -p 3000 ```
3. Attendre quelques secondes que le projet démarre

4. Dans un autre terminal, dans le dossier de dagster
5. Lancer: ``` poetry run dagster-daemon run ```

6. Allez à http://localhost:3000
7. Faire les étapes de Recharger le projet en production

## Recharger le projet en production
Dans l’interface web → rechargez l’ensemble du projet:

![alt text](doc_images\image-6.png)

## Tester une exécution
Lancez manuellement une exécution pour valider que tout fonctionne:

![alt text](doc_images\image-7.png)

## Activer la tâche automatique
Activez la planification pour générer automatiquement votre comptoir de données:

![alt text](doc_images\image-8.png)

## Félicitation 
Votre orchestrateur Dagster + DBT est maintenant fonctionnel 🎊
Il s’exécutera automatiquement selon votre horaire configuré.
Vous pouvez consulter :
•	Overview → vision globale des exécutions
•	Runs → historique détaillé
•	Assets → état des modèles et suivi précis

## Mettre à jours votre repos DBT
À chaque fois que vous voulez automatiser une nouvelle version de votre code, il requis de faire les étapes suivantes pour s'assurer que Dagster exécute toujours la nouvelle version de votre projet.
1. Dans votre repos CSS suite à votre git pull ou autre changement
2. Faire ``` dbt clean ```
3. Faire ``` dbt deps ```
4. Faire ``` dbt parse ```
5. Faire les étapes de **Recharger le projet en production** (dans l'interface de Dagster)

## Configuration des fonctionnalités additionnelles
### ALERTE COURRIEL
1. mettre enabled a: true
2. inscrire votre serveur smtp interne 
3. inscrire le/les destinataire des alertes
4. Faire les étapes de **Recharger le projet en production**:

![alt text](doc_images\image-9.png)

### DFONDATION
1. Aller sur https://app.snowflake.com/grics/dfondation/#/homepage
    |--> Dans Governance & Security --> Users & roles --> trouver votre utilisateur
        |--> Cliquer sur Generate token (Programmatic access tokens), remplir le forms et choisir __All of this user's roles__ ce sera important pour pouvoir changer de role "on the fly" pendant l'extraction de différent schéma
2. Mettre enabled a: true
3. Changer pathPreFix pour le chemin d'accès au dossier contenant les seeds de votre projet DBT
4. Changer le user pour celui pour lequel vous avez générer le token.
5. Créer la variable d'environnement dFondation_key pour y mettre le token que vous avez générez. Sinon vous pouvez le mettre directement dans la config à vos risques et péril
6. Faire les étapes de Recharger le projet en production

#### Ajouter d'autres tables de DFONDATION
Vous pouvez ajouter d'autre table à extraire de dFondation en respectant la structure de la config:
```
"Nom de l'extraction" : {
        "role": "Role requis pour l'accès",
        "schema": "Schéma de dFondation",
        "tables": {
            "Nom de la table" : "Colonne voulu",
            "Nom de la table 2 du même schéma au besoin" : "..."  
        }
    }
```