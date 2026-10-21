const { app, BrowserWindow, protocol, shell } = require('electron');
const fs = require('node:fs');
const path = require('node:path');

protocol.registerSchemesAsPrivileged([
  {
    scheme: 'servidorbr',
    privileges: { standard: true, secure: true, supportFetchAPI: true },
  },
]);

const mimeTypes = {
  '.css': 'text/css; charset=utf-8',
  '.html': 'text/html; charset=utf-8',
  '.ico': 'image/x-icon',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.webp': 'image/webp',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
};

const contentSecurityPolicy = [
  "default-src 'self'",
  "script-src 'self'",
  "style-src 'self' 'unsafe-inline'",
  "img-src 'self' data:",
  "font-src 'self' data:",
  "connect-src 'self'",
  "object-src 'none'",
  "base-uri 'self'",
  "frame-ancestors 'none'",
].join('; ');

function apiBaseUrl() {
  const configured = new URL(process.env.SERVIDORBR_API_URL || 'http://127.0.0.1:8000');
  const localHosts = new Set(['127.0.0.1', 'localhost', '[::1]']);
  if (!['http:', 'https:'].includes(configured.protocol) || !localHosts.has(configured.hostname)) {
    throw new Error('SERVIDORBR_API_URL precisa apontar para localhost.');
  }
  return configured;
}

const backendUrl = apiBaseUrl();
const webRoot = path.join(app.getAppPath(), 'web-dist');

function response(body, status, headers = {}) {
  return new Response(body, {
    status,
    headers: {
      'Content-Security-Policy': contentSecurityPolicy,
      'X-Content-Type-Options': 'nosniff',
      ...headers,
    },
  });
}

protocol.handle('servidorbr', async (request) => {
  const url = new URL(request.url);
  if (url.hostname !== 'app') return response('Not found', 404);

  if (url.pathname === '/api' || url.pathname.startsWith('/api/')) {
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return response('Method not allowed', 405, { Allow: 'GET, HEAD' });
    }
    try {
      const upstream = await fetch(new URL(`${url.pathname}${url.search}`, backendUrl), {
        method: request.method,
        headers: { Accept: request.headers.get('accept') || 'application/json' },
      });
      const body = request.method === 'HEAD' ? null : await upstream.arrayBuffer();
      return response(body, upstream.status, {
        'Content-Type': upstream.headers.get('content-type') || 'application/json; charset=utf-8',
        'Cache-Control': 'no-store',
      });
    } catch {
      return response(
        JSON.stringify({
          error: {
            code: 'BACKEND_UNAVAILABLE',
            message: 'API local indisponível. Inicie o banco e o backend com docker compose up -d db backend.',
          },
        }),
        503,
        { 'Content-Type': 'application/json; charset=utf-8' },
      );
    }
  }

  if (request.method !== 'GET' && request.method !== 'HEAD') {
    return response('Method not allowed', 405, { Allow: 'GET, HEAD' });
  }

  let requestedPath;
  try {
    requestedPath = decodeURIComponent(url.pathname);
  } catch {
    return response('Bad request', 400);
  }
  const relativePath = requestedPath === '/' ? 'index.html' : requestedPath.replace(/^\/+/, '');
  const filePath = path.resolve(webRoot, relativePath);
  if (filePath !== webRoot && !filePath.startsWith(`${webRoot}${path.sep}`)) {
    return response('Forbidden', 403);
  }

  let contentPath = filePath;
  try {
    if (!fs.statSync(contentPath).isFile()) throw new Error('Not a file');
  } catch {
    contentPath = path.join(webRoot, 'index.html');
  }
  try {
    const content = fs.readFileSync(contentPath);
    const body = request.method === 'HEAD' ? null : content;
    return response(body, 200, {
      'Content-Type': mimeTypes[path.extname(contentPath).toLowerCase()] || 'application/octet-stream',
      'Cache-Control': contentPath.endsWith('index.html') ? 'no-cache' : 'public, max-age=31536000, immutable',
    });
  } catch {
    return response('Desktop assets are missing. Run npm run build:web first.', 500);
  }
});

function isApprovedExternalUrl(value) {
  try {
    const url = new URL(value);
    return url.protocol === 'https:' && ['dados.gov.br', 'repositorio.dados.gov.br'].includes(url.hostname);
  } catch {
    return false;
  }
}

async function createWindow() {
  const window = new BrowserWindow({
    width: 1280,
    height: 860,
    minWidth: 900,
    minHeight: 640,
    autoHideMenuBar: true,
    backgroundColor: '#f5f7f4',
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
    },
  });

  window.webContents.setWindowOpenHandler(({ url }) => {
    if (isApprovedExternalUrl(url)) shell.openExternal(url);
    return { action: 'deny' };
  });
  window.webContents.on('will-navigate', (event, url) => {
    if (!url.startsWith('servidorbr://app/')) event.preventDefault();
  });
  await window.loadURL('servidorbr://app/index.html');
}

app.whenReady().then(async () => {
  await createWindow();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => app.quit());
