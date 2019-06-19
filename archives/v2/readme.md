
# LibLSC Analyzer (version 2)

> Ce projet regroupe des scripts pour réaliser l'analyse des expériences réalisées via la LibLSC

## Organisation du projet

### Base du projet

- **/archives** : dossier contenant les anciennes versions du projet qui peuvent être nécessaire pour l'analyse d'anciens résultats
- **/parser** : dossier contenant les classes de base permettant de lire les différents fichiers relatifs aux expérience et de manipuler les différentes données qu'ils contiennent
  - **operation.py** : classe qui permet de formater et manipuler les lignes du fichier de résultat
  - **manage_manip.py** : classe permettant de formater et manipuler les différents fichiers résultats d'une expérience
- **/plotter** : dossier contenant le module permettant de faire de l'affichage de données variées (matrices, nuage de point, histogramme...) de manière dynamique ou statique
  - **plotter.py** : classe qui permet de réaliser l'affichage des données
  - **test_plotter.py** : script qui permet de tester la classe *Plotter* et sert en même temps d'exemple d'utilisation

### Analyse simple

> Permet de voir les opérations réalisées lors de la cartographie

- **print_done_ope.py** : affiche les opérations qui ont déjà été exécutées
- **trace_carto.py** : affiche en temps réel la matrice des différentes positions déjà exécutées par une cartographie

### Analyse cartographique

> Chaque dossier correspond à un DUT testé

- **/raspi3** : dossier contenant les scripts d'analyse des cartographies sur le Raspberry Pi 3 
  - **print_faulted_ope.py** : affiche les opérations qui ont été fautées
  - **analyze_carto_raspi_loop(_old).py** : affiche une matrice représentant les effets obtenus lors d'une cartographie (la version *old* correspond aux premières versions de firmware du Raspberry Pi 3)
  - **analyze_carto_delay.py** : affiche sur un graphe l'ensemble des valeurs de `cnt`, `i` et `j` ainsi que leur distribution en fonction du delay
  - **trace_and_faults_carto.py** : affiche en temps réel sur la même figure les positions déjà exécutées par une cartographie, les reboots qui ont eu lieu et les fautes
  
- **/zoro** : dossier contenant les scripts d'analyse des cartographies du projet *Zoro*
  - **analyze_carto.py** : affiche une matrice représentant les effets obtenus lors d'une cartographie
