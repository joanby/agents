# Come inviare una Pull Request (PR) al repository del corso

**Guida completa per studenti che lavorano su Windows o Mac, usando Cursor, Python (.py e .ipynb), uv per i pacchetti e un repository pubblico su GitHub.**

---

## Parte 1 – Concetti preliminari

### Cos'è una Pull Request (PR) e perché si usa

Una **Pull Request** è una richiesta formale per proporre le tue modifiche al repository principale del corso.

In pratica stai dicendo:

> "Ho migliorato / aggiunto qualcosa: puoi controllarlo e, se va bene, integrarlo nel progetto?"

Le PR servono a:

- ✅ Permettere la revisione del codice o dei notebook
- ✅ Mantenere il repository principale ordinato e stabile
- ✅ Collaborare senza rischiare di rompere il lavoro degli altri

### Cos'è un Git remote e perché è importante

Un **remote** è una versione del repository che vive online (di solito su GitHub).

Nel nostro caso ne userai due:

- **`origin`** → il tuo fork del repository (dove puoi scrivere e fare push)
- **`upstream`** → il repository ufficiale del corso (da cui fare pull)

Questo è fondamentale perché:

- ✅ Pushi le modifiche sul tuo fork
- ✅ Pulli gli aggiornamenti dal repo ufficiale

---

## Parte 2 – Fork del repository e configurazione dei remotes

### 1. Fork del repository

1. Vai al repository del corso su GitHub
2. Clicca su **Fork** (in alto a destra)
3. Seleziona il tuo account GitHub

GitHub creerà una copia del repo sotto il tuo profilo.

### 2. Clona il tuo fork in locale

Apri il terminale (in Cursor o sistema):

```bash
git clone https://github.com/tuo-username/nome-repo.git
cd nome-repo
```

### 3. Aggiungi il repository del corso come upstream

```bash
git remote add upstream https://github.com/organizzazione/nome-repo.git
```

**Verifica:**

```bash
git remote -v
```

Dovresti vedere qualcosa tipo:

```
origin    https://github.com/tuo-username/nome-repo.git (fetch)
origin    https://github.com/tuo-username/nome-repo.git (push)
upstream  https://github.com/organizzazione/nome-repo.git (fetch)
upstream  https://github.com/organizzazione/nome-repo.git (push)
```

---

## Parte 3 – Preparare correttamente la PR

### Dove fare le modifiche

Ogni sezione del corso ha una cartella:

```
community_contributions/
```

**Regola d'oro:**
👉 **Le tue modifiche dovrebbero stare solo lì.**

**Esempio:**

```
03-embeddings/
└── community_contributions/
    └── mio_notebook.ipynb
```

### Notebook: pulizia obbligatoria degli output

Prima di inviare la PR:

- ✅ **Tutti gli output devono essere cancellati**
- ✅ In Cursor: tasto destro sul notebook → **Clear All Outputs**
- ✅ Il notebook deve:
  - aprirsi senza output
  - poter essere eseguito dall'alto verso il basso senza errori

Questo è fondamentale per mantenere il repo leggero e leggibile.

### Controllo finale prima del commit

**Checklist rapida:**

- [ ] File nella cartella `community_contributions`
- [ ] Notebook senza output
- [ ] Nessun file extra (cache, `.venv`, `.DS_Store`, ecc.)
- [ ] Hai incluso solo ciò che vuoi davvero proporre

**Per controllare:**

```bash
git status
```

---

## Parte 4 – Creare e inviare la Pull Request

### 1. Crea un branch dedicato

**Mai lavorare direttamente su `main`.**

```bash
git checkout -b nome-del-tuo-branch
```

**Esempio:**

```bash
git checkout -b notebook-section-3
```

### 2. Commit delle modifiche

```bash
git add .
git commit -m "Aggiunto notebook su XYZ nella sezione 3"
```

**Suggerimento:** Usa messaggi di commit chiari e descrittivi.

### 3. Push sul tuo fork

```bash
git push origin nome-del-tuo-branch
```

**Se è la prima volta che pushi questo branch:**

```bash
git push --set-upstream origin nome-del-tuo-branch
```

### 4. Apri la Pull Request su GitHub

1. Vai sul tuo fork su GitHub
2. Comparirà il pulsante **"Compare & Pull Request"**
3. Scrivi:
   - cosa hai aggiunto
   - per quale sezione
4. Invia la PR

**Fine 🎉**

---

## Parte 5 – Workflow corretto: pull dal corso, push sul fork

### Aggiornare il tuo main dal repo ufficiale

```bash
git checkout main
git pull upstream main
```

**(Opzionale ma consigliato) aggiornare anche il tuo fork:**

```bash
git push origin main
```

### Riepilogo dei comandi principali

| Operazione | Comando |
|------------|---------|
| Clonare il fork | `git clone URL` |
| Aggiungere upstream | `git remote add upstream URL` |
| Nuovo branch | `git checkout -b nome-branch` |
| Commit | `git add .` + `git commit -m "msg"` |
| Push al fork | `git push origin nome-branch` |
| Pull dal corso | `git pull upstream main` |

---

## Parte 6 – Aggiornare una PR dopo il feedback (opzionale)

Se ricevi feedback tipo:

- "Per favore rimuovi gli output"
- "Hai incluso file non necessari"

**Nessun problema.**

### 1. Fai le modifiche richieste

Sistema i file in locale.

### 2. Nuovo commit

```bash
git add .
git commit -m "Correzioni dopo feedback PR"
```

### 3. Push sullo stesso branch

```bash
git push origin nome-del-tuo-branch
```

**La Pull Request si aggiorna automaticamente.**
Non serve crearne una nuova.

---

## In sintesi

Pensa alla PR come a una conversazione educata:

> "Ehi, ho preparato qualcosa di utile, l'ho pulita bene, sta nel posto giusto — dai un'occhiata!"

---

## Troubleshooting

### "Permission denied" quando fai push

- Verifica di essere sul tuo fork (`origin`), non sul repo originale
- Usa un **Personal Access Token** invece della password:
  1. Vai su: https://github.com/settings/tokens
  2. "Generate new token (classic)"
  3. Scope: `repo`
  4. Usa il token come password quando Git lo chiede

### "Branch not found" quando fai push

- Assicurati di aver fatto `git checkout -b nome-branch` prima
- Verifica su quale branch sei: `git branch`

### "Repository not found"

- Verifica l'URL del remote: `git remote -v`
- Assicurati di aver fatto il fork correttamente

---

## Risorse utili

- [Documentazione ufficiale GitHub su Pull Requests](https://docs.github.com/en/pull-requests)
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

---

**Buon lavoro! 🚀**
