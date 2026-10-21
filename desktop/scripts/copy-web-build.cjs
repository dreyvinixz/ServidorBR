const fs = require('node:fs');
const path = require('node:path');

const source = path.resolve(__dirname, '../../frontend/dist');
const destination = path.resolve(__dirname, '../web-dist');
if (!fs.existsSync(path.join(source, 'index.html'))) {
  throw new Error('Frontend não compilado. Execute npm run build em frontend antes.');
}

fs.mkdirSync(destination, { recursive: true });
fs.cpSync(source, destination, { recursive: true, force: true });
console.log(`Frontend copiado de ${source} para ${destination}`);
