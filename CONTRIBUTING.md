# Guide de Contribution à Linklet

Merci de votre intérêt pour contribuer à Linklet ! Ce document fournit les lignes directrices pour contribuer au projet.

## 🌟 Comment Contribuer

1. **Fork & Clone**
   ```powershell
   git clone https://github.com/votre-username/linklet.git
   cd linklet
   git remote add upstream https://github.com/original/linklet.git
   ```

2. **Créer une Branche**
   ```powershell
   git checkout -b feature/nom-de-votre-fonctionnalite
   ```

3. **Configuration de l'Environnement**
   ```powershell
   python -m venv env
   .\env\Scripts\Activate.ps1
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   pip install -e .
   ```

## 💻 Standards de Code

- Utiliser **Black** pour le formatage
- Utiliser **isort** pour les imports
- Suivre PEP 8
- Docstrings pour toutes les fonctions publiques
- Type hints pour tous les paramètres

## ✅ Tests

- Écrire des tests pour chaque nouvelle fonctionnalité
- Les tests doivent passer avant le commit
- Vérifier la couverture de code
  ```powershell
  pytest --cov=src tests/
  ```

## 📝 Messages de Commit

Format : `type(scope): description`

Types :
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `style`: Formatage
- `refactor`: Refactoring
- `test`: Tests
- `chore`: Maintenance

Exemple : `feat(bot): ajouter commande /help`

## 🔄 Processus de Pull Request

1. **Mettre à Jour votre Fork**
   ```powershell
   git fetch upstream
   git rebase upstream/main
   ```

2. **Vérifier votre Code**
   ```powershell
   # Formatter le code
   black src/ tests/
   isort src/ tests/
   
   # Lancer les tests
   pytest
   ```

3. **Créer la Pull Request**
   - Titre clair et descriptif
   - Description détaillée des changements
   - Référencer les issues concernées
   - Screenshots/GIFs si pertinent

## 📚 Documentation

- Mettre à jour le README.md si nécessaire
- Documenter les nouvelles fonctionnalités
- Ajouter des exemples d'utilisation

## 🚫 À Éviter

- Breaking changes sans discussion préalable
- Commits directs sur main
- Code non testé
- Modifications de style dans les commits fonctionnels

## 🤝 Code de Conduite

- Soyez respectueux et bienveillant
- Acceptez les critiques constructives
- Focus sur ce qui est le mieux pour la communauté

## 📫 Questions & Support

- Ouvrir une issue pour les bugs
- Discussions GitHub pour les questions
- Pull Requests pour les corrections

---

N'hésitez pas à proposer des améliorations à ce guide !
