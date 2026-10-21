# Aplicativo desktop

O ServidorBR Desktop é um aplicativo gráfico para Windows que reutiliza a interface React do projeto. O processo principal do Electron serve os arquivos locais pelo protocolo `servidorbr://` e encaminha `/api` para a API local em `127.0.0.1:8000`.

## Uso

1. Inicie PostgreSQL e API: `docker compose up -d db backend`.
2. Gere a pasta portátil: em `desktop`, execute `npm ci` e `npm run package:win`.
3. Abra `desktop/release/ServidorBR-win32-x64/ServidorBR.exe`.

O app não empacota banco, API ou dados; esses serviços precisam estar ativos no mesmo computador. Se a API não responder, a interface apresenta a orientação de inicialização. Para desenvolvimento, `npm start` compila o frontend e inicia a janela Electron.

## Implementação e segurança

- Electron 44, Node.js e Electron Packager geram o executável Windows x64 portátil.
- A API é chamada por um handler do protocolo local, evitando CORS e URL fixa no frontend.
- O renderer usa sandbox, `contextIsolation` e `nodeIntegration: false`; não recebe APIs do processo principal.
- A política de conteúdo restringe scripts, objetos e conexões à origem local. Apenas links HTTPS para os domínios oficiais de dados abrem no navegador padrão.
- CI compila e empacota o app em Windows e publica a pasta executável como artefato do workflow.

## Limitações

- O pacote requer uma instalação local da stack ServidorBR e dados importados no PostgreSQL.
- O executável não é assinado digitalmente; o Windows pode exibir um aviso de editor desconhecido.
- A inspeção visual automatizada depende de navegador/desktop disponível no ambiente.

Consulte [desktop/README.md](../desktop/README.md) para os comandos detalhados de desenvolvimento e empacotamento.
