# Firebase Admin SDK (Node) - Configuração do Banco

Este projeto agora inclui a configuração do banco via SDK conforme solicitado.

## Arquivo
- `firebase-admin-init.js`

## Trecho equivalente solicitado
```js
var admin = require("firebase-admin");

var serviceAccount = require("path/to/serviceAccountKey.json");

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});
```

## Como usar
1. Coloque sua chave de serviço em:
   - `serviceAccountKey.json` (raiz do projeto)
   - **ou** configure a variável `FIREBASE_SERVICE_ACCOUNT` com caminho do arquivo.
2. Importe no seu código Node:
```js
const { admin, db } = require('./firebase-admin-init');
```

## Exemplo de leitura/gravação
```js
await db.collection('usuarios').doc('uid_teste').set({ nome: 'Guardião', pontos: 10 });
const snap = await db.collection('usuarios').doc('uid_teste').get();
console.log(snap.data());
```
