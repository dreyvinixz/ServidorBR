# ServidorBR Desktop

Aplicativo gráfico para Windows que abre a interface React existente em uma janela Electron. Os arquivos da interface são empacotados no instalador; a busca continua usando a API ServidorBR e o banco PostgreSQL local.

## Iniciar em desenvolvimento

Requisitos: Windows, Node.js 22 ou superior e Docker Desktop.

Na raiz do repositório, inicie banco e API:

```powershell
docker compose up -d db backend
```

Depois instale e abra o desktop:

```powershell
cd desktop
npm ci
npm start
```

`npm start` compila o frontend e abre uma janela nativa. O backend deve responder em `http://127.0.0.1:8000`; se não estiver ativo, o app mostra uma mensagem com o comando para iniciá-lo.

## Gerar pacote portátil para Windows

```powershell
cd desktop
npm ci
npm run package:win
```

O pacote fica em `desktop/release/ServidorBR-win32-x64/`; execute `ServidorBR.exe`. A pasta contém o runtime do aplicativo e pode ser compactada para entrega. O usuário não precisa instalar Node.js; o backend e o banco precisam estar ativos no computador. Para apontar a API a outra porta local, defina `SERVIDORBR_API_URL` antes de abrir o app.

## Segurança e escopo

- A interface roda sob o protocolo local seguro `servidorbr://`; a requisição à API é encaminhada pelo processo principal do Electron.
- O renderer usa `contextIsolation`, sandbox e `nodeIntegration: false`; nenhum objeto privilegiado é exposto à página.
- Apenas links HTTPS para os domínios oficiais de dados são abertos no navegador padrão.
- O pacote contém a interface, não uma cópia do banco nem dos arquivos oficiais. Os dados ficam no serviço PostgreSQL local.
