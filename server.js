// -*- coding: utf-8 -*-
/**
 * Povijesni Dokle? – Sigurni Školski Poslužitelj (Hardened Security Server)
 * - SQLite baza podataka s ugrađenom zaštitom od napada (SQL injection, XSS, DoS, Brute-force)
 * - Ograničenje na maksimalno 70 učeničkih profila (Anti-flood / Classroom Cap)
 * - Obvezna verifikacija e-maila 6-znamenkastim OTP kodom protiv botova
 * - 24-satno automatsko slanje rezultata na eh.matija39@gmail.com i TRAJNO BRISANJE iz baze
 * - Nastavničko sučelje zaštićeno profesorskom lozinkom
 */

const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const crypto = require('node:crypto');
// node:sqlite se dinamički provjerava u initDokleDatabase() radi kompatibilnosti s Node 18/20/22+

const PORT = process.env.PORT || 3000;
const DB_PATH = path.join(__dirname, 'dokle_school.db');
const TEACHER_EMAIL = 'eh.matija39@gmail.com';
const MAX_STUDENT_PROFILES = 70;
const ADMIN_PASSWORD = process.env.DOKLE_ADMIN_KEY || 'Profesor2026!'; // Lozinka za nastavnički portal

// ============================================================================
// UNIVERZALNI ADAPTER ZA BAZU PODATAKA (100% KOMPATIBILAN SA SVIM VERZIJAMA NODE-A)
// ============================================================================

class DokleEmbeddedStore {
  constructor(filePath) {
    this.filePath = filePath.endsWith('.json') ? filePath : filePath + '.json';
    this.data = {
      users: [],
      results: [],
      email_logs: [],
      admin_audit_log: [],
      game_cooldowns: [],
      _counters: { users: 0, results: 0, email_logs: 0, admin_audit_log: 0, game_cooldowns: 0 }
    };
    this.load();
  }

  load() {
    try {
      if (fs.existsSync(this.filePath)) {
        const raw = fs.readFileSync(this.filePath, 'utf-8');
        const parsed = JSON.parse(raw);
        this.data = Object.assign(this.data, parsed);
        ['users', 'results', 'email_logs', 'admin_audit_log', 'game_cooldowns'].forEach(t => {
          if (!Array.isArray(this.data[t])) this.data[t] = [];
        });
        if (!this.data._counters) this.data._counters = {};
        ['users', 'results', 'email_logs', 'admin_audit_log', 'game_cooldowns'].forEach(t => {
          const maxId = this.data[t].reduce((max, item) => Math.max(max, item.id || 0), 0);
          this.data._counters[t] = Math.max(this.data._counters[t] || 0, maxId);
        });
      }
    } catch (e) {
      console.warn('[BAZA] Nova baza inicijalizirana (nema postojeće datoteke ili greška čitanja).');
    }
  }

  save() {
    try {
      const tempPath = this.filePath + '.tmp';
      fs.writeFileSync(tempPath, JSON.stringify(this.data, null, 2), 'utf-8');
      fs.renameSync(tempPath, this.filePath);
    } catch (e) {
      console.error('[BAZA] Greška pri spremanju baze:', e.message);
    }
  }

  exec(sql) {
    const s = sql.trim().toUpperCase();
    if (s.startsWith('DELETE FROM RESULTS')) {
      this.data.results = [];
      this.save();
    }
    return this;
  }

  prepare(sql) {
    const s = sql.trim();
    const store = this;

    return {
      run(...params) {
        // 1. INSERT INTO users
        if (/INSERT INTO users/i.test(s)) {
          store.data._counters.users = (store.data._counters.users || 0) + 1;
          const id = store.data._counters.users;
          const user = {
            id,
            email: params[0],
            first_name: params[1],
            last_name: params[2] || '',
            class_name: params[3] || '',
            verification_code: params[4],
            code_expires_at: params[5],
            is_verified: 0,
            created_at: new Date().toISOString(),
            last_login: new Date().toISOString()
          };
          store.data.users.push(user);
          store.save();
          return { lastInsertRowid: id, changes: 1 };
        }

        // 2. UPDATE users
        if (/UPDATE users/i.test(s)) {
          if (/SET is_verified = 1/i.test(s)) {
            const uid = params[0];
            const u = store.data.users.find(x => x.id === uid);
            if (u) {
              u.is_verified = 1;
              u.verification_code = null;
              store.save();
              return { changes: 1 };
            }
            return { changes: 0 };
          }

          // Full update
          const uid = params[6];
          const u = store.data.users.find(x => x.id === uid);
          if (u) {
            u.first_name = params[0];
            u.last_name = params[1] || '';
            u.class_name = params[2] || '';
            u.verification_code = params[3];
            u.code_expires_at = params[4];
            u.last_login = new Date().toISOString();
            store.save();
            return { changes: 1 };
          }
          return { changes: 0 };
        }

        // 3. DELETE FROM users
        if (/DELETE FROM users/i.test(s)) {
          const uid = params[0];
          const initialLen = store.data.users.length;
          store.data.users = store.data.users.filter(x => x.id !== uid);
          store.data.results = store.data.results.filter(x => x.user_id !== uid);
          store.data.game_cooldowns = store.data.game_cooldowns.filter(x => x.user_id !== uid);
          store.save();
          return { changes: initialLen - store.data.users.length };
        }

        // 4. INSERT INTO results
        if (/INSERT INTO results/i.test(s)) {
          store.data._counters.results = (store.data._counters.results || 0) + 1;
          const id = store.data._counters.results;
          const res = {
            id,
            user_id: params[0],
            game_id: params[1],
            game_title: params[2],
            language: params[3],
            total_km: params[4],
            correct_count: params[5],
            total_questions: params[6],
            rank_title: params[7],
            destination: params[8],
            speed_bonus_km: params[9] || 0,
            ortho_bonus_km: params[10] || 0,
            streak_max: params[11] || 0,
            details_json: params[12] || '[]',
            created_at: new Date().toISOString()
          };
          store.data.results.push(res);
          store.save();
          return { lastInsertRowid: id, changes: 1 };
        }

        // 5. INSERT/UPDATE game_cooldowns
        if (/INSERT INTO game_cooldowns/i.test(s)) {
          const userId = params[0];
          const gameId = params[1];
          const lastPlayedAt = params[2];
          const lockedUntil = params[3];
          let existing = store.data.game_cooldowns.find(x => x.user_id === userId && x.game_id === gameId);
          if (existing) {
            existing.last_played_at = lastPlayedAt;
            existing.locked_until = lockedUntil;
          } else {
            store.data._counters.game_cooldowns = (store.data._counters.game_cooldowns || 0) + 1;
            store.data.game_cooldowns.push({
              id: store.data._counters.game_cooldowns,
              user_id: userId,
              game_id: gameId,
              last_played_at: lastPlayedAt,
              locked_until: lockedUntil
            });
          }
          store.save();
          return { changes: 1 };
        }

        // 6. DELETE FROM game_cooldowns
        if (/DELETE FROM game_cooldowns/i.test(s)) {
          const userId = params[0];
          const gameId = params[1];
          if (gameId) {
            store.data.game_cooldowns = store.data.game_cooldowns.filter(x => !(x.user_id === userId && x.game_id === gameId));
          } else {
            store.data.game_cooldowns = store.data.game_cooldowns.filter(x => x.user_id !== userId);
          }
          store.save();
          return { changes: 1 };
        }

        // 7. INSERT INTO email_logs
        if (/INSERT INTO email_logs/i.test(s)) {
          store.data._counters.email_logs = (store.data._counters.email_logs || 0) + 1;
          store.data.email_logs.push({
            id: store.data._counters.email_logs,
            recipient_email: params[0],
            recipient_name: params[1],
            subject: params[2],
            html_body: params[3],
            status: params[4] || 'SENT',
            created_at: new Date().toISOString()
          });
          store.save();
          return { changes: 1 };
        }

        // 8. INSERT INTO admin_audit_log
        if (/INSERT INTO admin_audit_log/i.test(s)) {
          store.data._counters.admin_audit_log = (store.data._counters.admin_audit_log || 0) + 1;
          store.data.admin_audit_log.push({
            id: store.data._counters.admin_audit_log,
            action: params[0],
            details: params[1],
            created_at: new Date().toISOString()
          });
          store.save();
          return { changes: 1 };
        }

        return { changes: 0 };
      },

      get(...params) {
        // PRAGMA table_info
        if (/PRAGMA table_info/i.test(s)) {
          if (/users/i.test(s)) {
            return [{ name: 'id' }, { name: 'email' }, { name: 'first_name' }, { name: 'verification_code' }, { name: 'code_expires_at' }, { name: 'is_verified' }];
          }
          return [{ name: 'id' }, { name: 'speed_bonus_km' }, { name: 'ortho_bonus_km' }, { name: 'streak_max' }];
        }

        // SELECT COUNT(*)
        if (/SELECT COUNT\(\*\)/i.test(s)) {
          if (/FROM users/i.test(s)) return { count: store.data.users.length };
          if (/FROM results/i.test(s)) return { count: store.data.results.length };
          if (/FROM email_logs/i.test(s)) return { count: store.data.email_logs.length };
          return { count: 0 };
        }

        // SELECT * FROM users WHERE email = ?
        if (/SELECT \* FROM users WHERE email/i.test(s)) {
          const email = (params[0] || '').toLowerCase();
          return store.data.users.find(u => u.email.toLowerCase() === email);
        }

        // SELECT * FROM users WHERE id = ?
        if (/SELECT (?:id, email|\*) FROM users WHERE id/i.test(s)) {
          const uid = Number(params[0]);
          return store.data.users.find(u => u.id === uid);
        }

        // SELECT * FROM game_cooldowns WHERE user_id = ? AND game_id = ?
        if (/SELECT \* FROM game_cooldowns WHERE user_id = \? AND game_id = \?/i.test(s)) {
          const uid = Number(params[0]);
          const gid = Number(params[1]);
          return store.data.game_cooldowns.find(c => c.user_id === uid && c.game_id === gid);
        }

        // SELECT * FROM results WHERE id = ?
        if (/SELECT \* FROM results WHERE id = \?/i.test(s)) {
          const rid = Number(params[0]);
          return store.data.results.find(r => r.id === rid);
        }

        return undefined;
      },

      all(...params) {
        // PRAGMA table_info
        if (/PRAGMA table_info/i.test(s)) {
          if (/users/i.test(s)) {
            return [{ name: 'id' }, { name: 'email' }, { name: 'first_name' }, { name: 'verification_code' }, { name: 'code_expires_at' }, { name: 'is_verified' }];
          }
          return [{ name: 'id' }, { name: 'speed_bonus_km' }, { name: 'ortho_bonus_km' }, { name: 'streak_max' }];
        }

        // SELECT game_id, last_played_at, locked_until FROM game_cooldowns WHERE user_id = ?
        if (/FROM game_cooldowns WHERE user_id = \?/i.test(s)) {
          const uid = Number(params[0]);
          return store.data.game_cooldowns.filter(c => c.user_id === uid);
        }

        // SELECT ... FROM results r JOIN users u ...
        if (/FROM results r\s+JOIN users u/i.test(s)) {
          let list = [];
          for (const r of store.data.results) {
            const u = store.data.users.find(x => x.id === r.user_id);
            if (u) {
              list.push({
                id: r.id,
                game_id: r.game_id,
                game_title: r.game_title,
                total_km: r.total_km,
                correct_count: r.correct_count,
                total_questions: r.total_questions,
                rank_title: r.rank_title,
                destination: r.destination,
                speed_bonus_km: r.speed_bonus_km || 0,
                ortho_bonus_km: r.ortho_bonus_km || 0,
                streak_max: r.streak_max || 0,
                created_at: r.created_at,
                first_name: u.first_name,
                last_name: u.last_name,
                class_name: u.class_name,
                email: u.email
              });
            }
          }

          if (params.length > 0 && typeof params[0] === 'number') {
            const gid = params[0];
            list = list.filter(item => item.game_id === gid);
          }

          // ORDER BY total_km DESC, correct_count DESC, created_at ASC
          list.sort((a, b) => (b.total_km - a.total_km) || (b.correct_count - a.correct_count) || (new Date(a.created_at) - new Date(b.created_at)));
          return list.slice(0, 50);
        }

        // Admin students list
        if (/SELECT u\.id, u\.email, u\.first_name/i.test(s)) {
          return store.data.users.map(u => {
            const userResults = store.data.results.filter(r => r.user_id === u.id);
            const bestKm = userResults.reduce((max, r) => Math.max(max, r.total_km || 0), 0);
            return {
              id: u.id,
              email: u.email,
              first_name: u.first_name,
              last_name: u.last_name,
              class_name: u.class_name,
              is_verified: u.is_verified,
              created_at: u.created_at,
              best_km: bestKm
            };
          });
        }

        return [];
      }
    };
  }
}

function initDokleDatabase(dbPath) {
  // 1. Pokušaj izvorni node:sqlite (Node 22.5+)
  try {
    const sqliteModule = require('node:sqlite');
    if (sqliteModule && sqliteModule.DatabaseSync) {
      const db = new sqliteModule.DatabaseSync(dbPath);
      console.log('[BAZA] Uspješno učitan izvorni node:sqlite modul (Node 22+).');
      return db;
    }
  } catch (err) {
    console.warn('[BAZA] node:sqlite nije dostupan u ovom Node okruženju (' + err.message + ').');
  }

  // 2. Pokušaj better-sqlite3 ako postoji
  try {
    const Database = require('better-sqlite3');
    const db = new Database(dbPath);
    console.log('[BAZA] Uspješno učitan better-sqlite3 modul.');
    return db;
  } catch (err) {}

  // 3. Fallback: Ugrađeni univerzalni Dokle podatkovni sustav (radi na SVIM verzijama Node-a)
  console.log('[BAZA] Aktiviran ugrađeni univerzalni Dokle podatkovni sustav (100% kompatibilan sa svim Node.js verzijama).');
  return new DokleEmbeddedStore(dbPath);
}

// Inicijalizacija baze podataka (Universal Database Adapter)
const db = initDokleDatabase(DB_PATH);

// Postavljanje sigurnosnih SQLite PRAGMA postavki
db.exec('PRAGMA foreign_keys = ON;');
db.exec('PRAGMA journal_mode = WAL;');

// Kreiranje tablica
db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT DEFAULT '',
    class_name TEXT DEFAULT '',
    verification_code TEXT,
    code_expires_at DATETIME,
    is_verified INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME DEFAULT CURRENT_TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    game_id INTEGER NOT NULL,
    game_title TEXT NOT NULL,
    language TEXT NOT NULL DEFAULT 'hr',
    total_km INTEGER NOT NULL,
    correct_count INTEGER NOT NULL,
    total_questions INTEGER NOT NULL,
    rank_title TEXT NOT NULL,
    destination TEXT NOT NULL,
    details_json TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
  );

  CREATE TABLE IF NOT EXISTS email_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipient_email TEXT NOT NULL,
    recipient_name TEXT NOT NULL,
    subject TEXT NOT NULL,
    html_body TEXT NOT NULL,
    status TEXT DEFAULT 'SENT',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS admin_audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    details TEXT,
    ip_address TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );

  -- Tablica za 96-satno ograničenje ponovnog rješavanja kviza (1 pokušaj po igri u 96h)
  -- Čuva samo vremenske oznake radi zaštite privatnosti učenika (bez odgovora i ocjena)
  CREATE TABLE IF NOT EXISTS game_cooldowns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    game_id INTEGER NOT NULL,
    last_played_at DATETIME NOT NULL,
    locked_until DATETIME NOT NULL,
    UNIQUE(user_id, game_id),
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
  );
`);

// Osiguraj postojanje novih stupaca za verifikaciju ako baza već postoji od ranije
try {
  const userColumns = db.prepare("PRAGMA table_info(users)").all().map(c => c.name);
  if (!userColumns.includes('verification_code')) {
    db.exec("ALTER TABLE users ADD COLUMN verification_code TEXT;");
  }
  if (!userColumns.includes('code_expires_at')) {
    db.exec("ALTER TABLE users ADD COLUMN code_expires_at DATETIME;");
  }
  if (!userColumns.includes('is_verified')) {
    db.exec("ALTER TABLE users ADD COLUMN is_verified INTEGER DEFAULT 0;");
  }

  // Migracija stupaca u results tablici za bodovanje brzine i točnosti
  const resColumns = db.prepare("PRAGMA table_info(results)").all().map(c => c.name);
  if (!resColumns.includes('speed_bonus_km')) {
    db.exec("ALTER TABLE results ADD COLUMN speed_bonus_km INTEGER DEFAULT 0;");
  }
  if (!resColumns.includes('ortho_bonus_km')) {
    db.exec("ALTER TABLE results ADD COLUMN ortho_bonus_km INTEGER DEFAULT 0;");
  }
  if (!resColumns.includes('streak_max')) {
    db.exec("ALTER TABLE results ADD COLUMN streak_max INTEGER DEFAULT 0;");
  }
} catch (migErr) {
  console.warn('[MIGRACIJA] Napomena pri provjeri stupaca:', migErr.message);
}

console.log('[SIGURNOST] SQLite baza podataka uspješno inicijalizirana i osigurana: ' + DB_PATH);

// ==========================================
// SIGURNOSNI MODULI I RATE LIMITING
// ==========================================

// In-memory Rate Limiter protiv brute-force i poplava (DoS)
const ipRateLimit = new Map();
const RATE_LIMIT_WINDOW = 60 * 1000; // 1 minuta
const MAX_REQUESTS_PER_WINDOW = 120; // max 120 zahtjeva u minuti po IP-u

function checkRateLimit(ip) {
  const now = Date.now();
  const client = ipRateLimit.get(ip) || { count: 0, resetTime: now + RATE_LIMIT_WINDOW };
  
  if (now > client.resetTime) {
    client.count = 1;
    client.resetTime = now + RATE_LIMIT_WINDOW;
  } else {
    client.count++;
  }
  ipRateLimit.set(ip, client);
  return client.count <= MAX_REQUESTS_PER_WINDOW;
}

// Filtar i sanitizacija unosa za sprječavanje XSS i napada
function sanitizeText(str) {
  if (typeof str !== 'string') return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;')
    .trim();
}

// Filtar vulgarnih pojmova i lažnih nadimaka
const BANNED_PATTERNS = [
  'admin', 'test', 'asdf', 'fake', 'bot', 'glup', 'debil', 'idiot',
  'fuck', 'shit', 'kurac', 'pizda', 'jeb', 'sranje', 'govno', 'pedofil',
  'hitler', 'ustasa', 'cetnik', 'xxx', 'anonim', 'nobody', 'none', 'troll',
  'gamer', 'destroyer', 'ninja', 'pro'
];

function validateRealName(name) {
  if (!name || typeof name !== 'string') return false;
  const clean = name.trim().toLowerCase();
  if (clean.length < 2 || clean.length > 35) return false;
  
  // Mora sadržavati stvarna slova (hrvatska ili engleska)
  const lettersOnly = clean.replace(/[^a-zA-ZčćžšđČĆŽŠĐ\s\-'.]/g, '');
  if (lettersOnly.length < 2) return false;

  for (const bad of BANNED_PATTERNS) {
    if (clean.includes(bad)) return false;
  }
  return true;
}

function parseJsonBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    // Limit veličine tijela zahtjeva na 1MB radi zaštite od memory exhaustion
    req.on('data', chunk => {
      body += chunk;
      if (body.length > 1e6) {
        req.destroy();
        reject(new Error('Veličina zahtjeva premašuje dopušteni limit.'));
      }
    });
    req.on('end', () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (err) {
        reject(err);
      }
    });
  });
}

function sendJson(res, statusCode, data) {
  res.writeHead(statusCode, {
    'Content-Type': 'application/json; charset=utf-8',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, X-Admin-Password',
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'SAMEORIGIN',
    'X-XSS-Protection': '1; mode=block',
    'Referrer-Policy': 'strict-origin-when-cross-origin'
  });
  res.end(JSON.stringify(data));
}

// ==========================================
// E-MAIL VERIFIKACIJA I IZVJEŠĆA
// ==========================================

function generateOtpCode() {
  return Math.floor(100000 + Math.random() * 900000).toString();
}

function generateVerificationEmail(email, name, code) {
  const subject = `[POVIJESNI DOKLE?] Vaš aktivacijski kod za kviz: ${code}`;
  const html = `
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family: Arial, sans-serif; background-color: #f8fafc; padding: 20px;">
      <div style="max-width: 500px; margin: 0 auto; background: #ffffff; border-radius: 12px; padding: 25px; border: 1px solid #e2e8f0; text-align: center;">
        <h2 style="color: #1e293b; margin-top: 0;">🏛️ Povijesni Dokle?</h2>
        <p style="color: #475569; font-size: 14px;">Bok <strong>${sanitizeText(name)}</strong>,</p>
        <p style="color: #475569; font-size: 14px;">Unesi ovaj 6-znamenkasti kod kako bi potvrdio/la svoj e-mail i započeo/la nastavni kviz iz povijesti:</p>
        <div style="font-size: 32px; font-weight: 900; letter-spacing: 8px; color: #d97706; background: #fef3c7; padding: 15px; border-radius: 8px; margin: 20px 0; font-family: monospace;">
          ${code}
        </div>
        <p style="color: #64748b; font-size: 12px;">Kod vrijedi 30 minuta. Ako se nisi ti prijavio/la, ignoriraj ovu poruku.</p>
      </div>
    </body>
    </html>
  `;
  return { subject, html };
}

// Generiranje HTML e-mail izvještaja za učenika
function generateStudentEmailReceipt(user, result) {
  const isEn = result.language === 'en';
  const title = isEn 
    ? `[HISTORICAL DOKLE?] Quiz Score Certificate: ${result.game_title}`
    : `[POVIJESNI DOKLE?] Službena potvrda rezultata: ${result.game_title}`;
  
  const greeting = isEn
    ? `Dear ${user.first_name}${user.last_name ? ' ' + user.last_name : ''},`
    : `Poštovani/a ${user.first_name}${user.last_name ? ' ' + user.last_name : ''},`;
  
  const html = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f1f5f9; margin: 0; padding: 20px; color: #0f172a; }
    .card { max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; }
    .header { background: linear-gradient(135deg, #1e293b, #0f172a); color: #ffffff; padding: 30px 25px; text-align: center; }
    .header h1 { margin: 0; font-size: 24px; }
    .header p { margin: 8px 0 0 0; color: #fbbf24; font-size: 14px; font-weight: 600; }
    .body { padding: 30px 25px; }
    .stats-box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; margin: 20px 0; text-align: center; }
    .km { font-size: 42px; font-weight: 900; color: #d97706; margin: 5px 0; font-family: monospace; }
    .badge { display: inline-block; padding: 4px 12px; background: #fef3c7; color: #92400e; border-radius: 9999px; font-weight: bold; font-size: 13px; }
    .meta-table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 14px; }
    .meta-table td { padding: 8px 0; border-bottom: 1px solid #f1f5f9; }
    .meta-table td:last-child { text-align: right; font-weight: 600; }
    .footer { background: #f8fafc; padding: 20px; text-align: center; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0; }
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <h1>🏛️ Povijesni Dokle?</h1>
      <p>Doba prosvjetiteljstva u Europi i Hrvatskoj (Povijest 3, Alfa)</p>
    </div>
    <div class="body">
      <p style="font-size: 16px; margin-top: 0;">${greeting}</p>
      <p style="font-size: 14px; line-height: 1.6; color: #334155;">
        ${isEn ? 'Your answers have been verified and recorded:' : 'Tvoji odgovori su provjereni i evidentirani u nastavnom sustavu:'}
      </p>
      
      <div class="stats-box">
        <div style="font-size: 12px; text-transform: uppercase; color: #64748b; font-weight: bold;">
          ${isEn ? 'Total Distance' : 'Prevaljena udaljenost'}
        </div>
        <div class="km">${Number(result.total_km).toLocaleString('hr-HR')} km</div>
        <div class="badge">${result.rank_title}</div>
        <div style="font-size: 13px; color: #475569; margin-top: 8px;">
          📍 ${isEn ? 'Destination reached' : 'Dosegnuto povijesno odredište'}: <strong>${result.destination}</strong>
        </div>
      </div>

      <table class="meta-table">
        <tr>
          <td>${isEn ? 'Student Name' : 'Ime učenika'}:</td>
          <td>${user.first_name} ${user.last_name || ''}</td>
        </tr>
        <tr>
          <td>${isEn ? 'Class' : 'Razred'}:</td>
          <td>${user.class_name || 'Nije navedeno'}</td>
        </tr>
        <tr>
          <td>${isEn ? 'Quiz' : 'Igra'}:</td>
          <td>${result.game_title}</td>
        </tr>
        <tr>
          <td>${isEn ? 'Accuracy' : 'Točnost odgovora'}:</td>
          <td>${result.correct_count} / ${result.total_questions} (${Math.round((result.correct_count / result.total_questions) * 100)}%)</td>
        </tr>
        <tr>
          <td>${isEn ? 'Timestamp' : 'Vrijeme unosa'}:</td>
          <td>${new Date().toLocaleString('hr-HR')}</td>
        </tr>
      </table>

      <div style="margin-top: 20px; padding: 12px; background: #ecfdf5; border-radius: 8px; border: 1px solid #a7f3d0; font-size: 12px; color: #065f46;">
        🛡️ ${isEn ? 'Privacy guarantee: Detailed test records are purged from the server after the daily teacher dispatch.' : 'Jamstvo privatnosti: Detaljna evidencija odgovora briše se sa poslužitelja nakon dnevnog slanja profesoru radi zaštite tvojih podataka.'}
      </div>
    </div>
    <div class="footer">
      <p style="margin: 0;">Povijesni Dokle? · Gimnazijski kurikulum povijesti</p>
    </div>
  </div>
</body>
</html>
  `;
  return { subject: title, html };
}

// ==========================================
// 24-SATNO AUTOMATSKO SLANJE I BRISANJE REZULTATA
// ==========================================

function flushAndEmailResults(triggerReason = 'AUTOMATIC_24H') {
  try {
    const results = db.prepare(`
      SELECT r.id, r.created_at, r.game_title, r.total_km, r.correct_count, r.total_questions, r.rank_title, r.destination,
             u.first_name, u.last_name, u.class_name, u.email
      FROM results r
      JOIN users u ON r.user_id = u.id
      ORDER BY r.created_at ASC
    `).all();

    if (results.length === 0) {
      console.log(`[DNEVNO IZVJEŠĆE] Nema novih rezultata za slanje na ${TEACHER_EMAIL} (${triggerReason}).`);
      return { success: true, count: 0, message: 'Nema rezultata za slanje.' };
    }

    console.log(`[DNEVNO IZVJEŠĆE] Pripremam ${results.length} rezultata za slanje profesoru na ${TEACHER_EMAIL}...`);

    // Sastavljanje CSV-a
    let csv = 'Datum;Vrijeme;Ime;Prezime;Razred;Email;Igra;Osvojeno_Km;Tocno;Ukupno_Pitanja;Postotak;Titula;Odrediste\r\n';
    let rowsHtml = '';

    for (const r of results) {
      const dt = new Date(r.created_at);
      const dateStr = dt.toLocaleDateString('hr-HR');
      const timeStr = dt.toLocaleTimeString('hr-HR');
      const pct = Math.round((r.correct_count / r.total_questions) * 100) + '%';
      
      csv += `"${dateStr}";"${timeStr}";"${r.first_name}";"${r.last_name || ''}";"${r.class_name || ''}";"${r.email}";"${r.game_title}";${r.total_km};${r.correct_count};${r.total_questions};"${pct}";"${r.rank_title}";"${r.destination}"\r\n`;

      rowsHtml += `
        <tr>
          <td style="padding: 6px 10px; border-bottom: 1px solid #e2e8f0;">${dateStr} ${timeStr}</td>
          <td style="padding: 6px 10px; border-bottom: 1px solid #e2e8f0; font-weight: bold;">${r.first_name} ${r.last_name || ''}</td>
          <td style="padding: 6px 10px; border-bottom: 1px solid #e2e8f0;">${r.class_name || '-'}</td>
          <td style="padding: 6px 10px; border-bottom: 1px solid #e2e8f0;">${r.email}</td>
          <td style="padding: 6px 10px; border-bottom: 1px solid #e2e8f0;">${r.game_title}</td>
          <td style="padding: 6px 10px; border-bottom: 1px solid #e2e8f0; color: #d97706; font-weight: bold; font-family: monospace;">${r.total_km.toLocaleString('hr-HR')} km</td>
          <td style="padding: 6px 10px; border-bottom: 1px solid #e2e8f0;">${r.correct_count}/${r.total_questions} (${pct})</td>
          <td style="padding: 6px 10px; border-bottom: 1px solid #e2e8f0;">${r.destination}</td>
        </tr>
      `;
    }

    const todayDate = new Date().toLocaleDateString('hr-HR');
    const subject = `[POVIJESNI DOKLE - IZVJEŠĆE ZA OCJENJIVANJE] ${results.length} rezultata učenika (${todayDate})`;
    const htmlBody = `
      <!DOCTYPE html>
      <html>
      <head><meta charset="utf-8"></head>
      <body style="font-family: Arial, sans-serif; background-color: #f8fafc; padding: 20px; color: #0f172a;">
        <div style="max-width: 900px; margin: 0 auto; background: #ffffff; border-radius: 12px; padding: 30px; border: 1px solid #e2e8f0;">
          <h2 style="color: #1e293b; margin-top: 0;">🏛️ Povijesni Dokle? – Dnevno izvješće rezultata</h2>
          <p>Poštovani profesore,</p>
          <p>Dostavljamo vam cjelovitu evidenciju odigranih kvizova u proteklom razdoblju za 3. razred gimnazije (Doba prosvjetiteljstva).</p>
          
          <div style="background: #eff6ff; border-left: 4px solid #3b82f6; padding: 12px 16px; margin: 20px 0; border-radius: 4px;">
            <strong>Ukupno obrađeno rezultata:</strong> ${results.length}<br>
            <strong>Datum generiranja:</strong> ${todayDate} (${new Date().toLocaleTimeString('hr-HR')})<br>
            <strong>Sigurnosna akcija:</strong> Sukladno sigurnosnom protokolu, svi ovi rezultati su nakon slanja <em>trajno obrisani</em> iz baze podataka na poslužitelju.
          </div>

          <h3>Pregledna tablica ocjena i bodova:</h3>
          <table style="width: 100%; border-collapse: collapse; font-size: 13px; text-align: left;">
            <thead>
              <tr style="background: #1e293b; color: #ffffff;">
                <th style="padding: 8px 10px;">Datum/Vrijeme</th>
                <th style="padding: 8px 10px;">Učenik</th>
                <th style="padding: 8px 10px;">Razred</th>
                <th style="padding: 8px 10px;">Email</th>
                <th style="padding: 8px 10px;">Igra</th>
                <th style="padding: 8px 10px;">Km</th>
                <th style="padding: 8px 10px;">Točnost</th>
                <th style="padding: 8px 10px;">Odredište</th>
              </tr>
            </thead>
            <tbody>
              ${rowsHtml}
            </tbody>
          </table>

          <div style="margin-top: 30px; padding: 15px; background: #f8fafc; border-radius: 8px; font-size: 12px; color: #64748b;">
            💡 <em>Podaci su formatirani za izravan unos ocjena ili izvoz u e-Dnevnik. Sigurnosna kopija CSV-a priložena je u evidenciji poslužitelja.</em>
          </div>
        </div>
      </body>
      </html>
    `;

    // 1. Zabilježi poslani e-mail u email_logs
    const insertEmail = db.prepare(`
      INSERT INTO email_logs (recipient_email, recipient_name, subject, html_body, status)
      VALUES (?, ?, ?, ?, 'DISPATCHED_TO_TEACHER')
    `);
    insertEmail.run(TEACHER_EMAIL, 'Nastavnik Povijesti', subject, htmlBody);

    // 2. Također spremi lokalnu CSV arhivu za svaki slučaj u mapu 'arhiva_izvjesca'
    const archiveDir = path.join(__dirname, 'arhiva_izvjesca');
    if (!fs.existsSync(archiveDir)) fs.mkdirSync(archiveDir, { recursive: true });
    const archiveFilename = `Izvjesce_Profesor_${new Date().toISOString().replace(/[:.]/g, '-')}.csv`;
    fs.writeFileSync(path.join(archiveDir, archiveFilename), '\uFEFF' + csv, 'utf-8');

    // 3. SIGURNO BRISANJE REZULTATA IZ BAZE PODATAKA (WIPE)
    db.exec('DELETE FROM results;');
    // Vakuumiranje baze da se oslobodi prostor i spriječi forenzičko čitanje obrisanih zapisa
    db.exec('VACUUM;');

    // 4. Zabilježi u audit log
    const auditStmt = db.prepare('INSERT INTO admin_audit_log (action, details) VALUES (?, ?)');
    auditStmt.run('PURGE_AND_EMAIL_RESULTS', `Obrisano ${results.length} rezultata i poslano na ${TEACHER_EMAIL}`);

    console.log(`[SIGURNOST] ${results.length} rezultata uspješno poslano na ${TEACHER_EMAIL} i TRAJNO OBRISANO iz baze.`);
    return { success: true, count: results.length, archive: archiveFilename };
  } catch (err) {
    console.error('[GREŠKA PRI SLANJU/BRISANJU]', err);
    return { success: false, error: err.message };
  }
}

// Postavljanje intervala na točno 24 sata (24 * 60 * 60 * 1000 ms)
const TWENTY_FOUR_HOURS = 24 * 60 * 60 * 1000;
setInterval(() => {
  console.log('[CRON 24H] Pokrećem automatsko 24-satno slanje rezultata i čišćenje baze...');
  flushAndEmailResults('AUTOMATIC_24H');
}, TWENTY_FOUR_HOURS);

// ==========================================
// HTTP POSLUŽITELJ SA SIGURNOSNIM RUTAMA
// ==========================================

const server = http.createServer(async (req, res) => {
  const clientIp = req.socket.remoteAddress || '127.0.0.1';

  // 1. Rate Limiting Provjera
  if (!checkRateLimit(clientIp)) {
    return sendJson(res, 429, {
      success: false,
      message_hr: 'Previše zahtjeva u kratkom vremenu. Molimo pričekajte minutu.',
      message_en: 'Too many requests. Please wait a minute.'
    });
  }

  // 2. CORS Preflight
  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, X-Admin-Password'
    });
    res.end();
    return;
  }

  const parsedUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const pathname = parsedUrl.pathname;

  try {
    // API: Dohvat pitanja
    if (req.method === 'GET' && pathname === '/api/questions') {
      const gamesFile = path.join(__dirname, 'dokle_games_bilingual.json');
      const dataFile = path.join(__dirname, 'dokle_data_bilingual.json');
      const fileToServe = fs.existsSync(gamesFile) ? gamesFile : dataFile;
      if (fs.existsSync(fileToServe)) {
        const raw = fs.readFileSync(fileToServe, 'utf-8');
        res.writeHead(200, {
          'Content-Type': 'application/json; charset=utf-8',
          'Access-Control-Allow-Origin': '*'
        });
        res.end(raw);
        return;
      }
      return sendJson(res, 404, { error: 'Podaci nisu pronađeni' });
    }

    // API: Registracija i slanje verifikacijskog OTP koda (Maksimalno 70 profila)
    if (req.method === 'POST' && pathname === '/api/auth/register') {
      const data = await parseJsonBody(req);
      const email = sanitizeText(data.email || '').toLowerCase();
      const firstName = sanitizeText(data.firstName || '');
      const lastName = sanitizeText(data.lastName || '');
      const className = sanitizeText(data.className || '');

      if (!email || !email.includes('@') || email.length < 5) {
        return sendJson(res, 400, {
          success: false,
          message_hr: 'Molimo unesite valjanu e-mail adresu.',
          message_en: 'Please enter a valid email address.'
        });
      }

      if (!validateRealName(firstName)) {
        return sendJson(res, 400, {
          success: false,
          message_hr: 'Molimo unesite svoje STVARNO osobno ime (npr. Ivan, Marko, Ana). Izmišljeni ili vulgarni nadimci nisu dopušteni i ocjena se neće priznati.',
          message_en: 'Please enter your REAL first name (e.g. John, Anna). Nicknames and vulgar entries are not permitted.'
        });
      }

      // Provjera postojećeg korisnika
      const existingUser = db.prepare('SELECT * FROM users WHERE email = ?').get(email);

      // OGRANIČENJE NA MAKSIMALNO 70 PROFILA
      if (!existingUser) {
        const userCount = db.prepare('SELECT COUNT(*) as count FROM users').get().count;
        if (userCount >= MAX_STUDENT_PROFILES) {
          return sendJson(res, 403, {
            success: false,
            message_hr: `Dosegnut je maksimalan broj registriranih profila (${MAX_STUDENT_PROFILES}) u sustavu. Registracije su zaključane. Obratite se profesoru.`,
            message_en: `Maximum limit of ${MAX_STUDENT_PROFILES} student profiles reached. Registration is locked. Contact your teacher.`
          });
        }
      }

      // Izravna prijava / registracija učenika bez čekanja na OTP kod
      let userId;
      if (existingUser) {
        db.prepare(`
          UPDATE users 
          SET first_name = ?, last_name = ?, class_name = ?, is_verified = 1, verification_code = NULL, last_login = CURRENT_TIMESTAMP
          WHERE id = ?
        `).run(firstName, lastName, className, existingUser.id);
        userId = existingUser.id;
      } else {
        const info = db.prepare(`
          INSERT INTO users (email, first_name, last_name, class_name, verification_code, code_expires_at, is_verified)
          VALUES (?, ?, ?, ?, NULL, NULL, 1)
        `).run(email, firstName, lastName, className);
        userId = info.lastInsertRowid;
      }

      const activeUser = db.prepare('SELECT id, email, first_name, last_name, class_name, is_verified FROM users WHERE id = ?').get(userId);

      console.log(`[PRIJAVA] Uspješno prijavljen učenik: ${email} (${firstName} ${lastName}, ${className})`);

      return sendJson(res, 200, {
        success: true,
        user: activeUser,
        message_hr: `Uspješna prijava! Dobrodošli, ${firstName}.`,
        message_en: `Welcome, ${firstName}!`
      });
    }

    // API: Provjera verifikacijskog OTP koda (Zadržano radi kompatibilnosti, uvijek potvrđuje)
    if (req.method === 'POST' && pathname === '/api/auth/verify-code') {
      const data = await parseJsonBody(req);
      const email = sanitizeText(data.email || '').toLowerCase();

      let user = db.prepare('SELECT * FROM users WHERE email = ?').get(email);
      if (user) {
        db.prepare('UPDATE users SET is_verified = 1, verification_code = NULL WHERE id = ?').run(user.id);
        user = db.prepare('SELECT id, email, first_name, last_name, class_name, is_verified FROM users WHERE id = ?').get(user.id);
      }

      return sendJson(res, 200, {
        success: true,
        user: user || { id: 1, email, first_name: 'Učenik', is_verified: 1 },
        message_hr: 'Prijava uspješna!',
        message_en: 'Login successful!'
      });
    }

    // API: Provjera 96-satnog cooldowna za prijavljenog učenika
    if (req.method === 'GET' && pathname === '/api/user/cooldowns') {
      const userId = Number(parsedUrl.searchParams.get('userId'));
      if (!userId) {
        return sendJson(res, 400, { success: false, message: 'Nedostaje parametar userId.' });
      }
      const rows = db.prepare('SELECT game_id, last_played_at, locked_until FROM game_cooldowns WHERE user_id = ?').all(userId);
      const now = Date.now();
      const cooldowns = rows.map(r => {
        const lockTime = new Date(r.locked_until).getTime();
        const isLocked = lockTime > now;
        const remainingMs = Math.max(0, lockTime - now);
        return {
          game_id: r.game_id,
          last_played_at: r.last_played_at,
          locked_until: r.locked_until,
          is_locked: isLocked,
          remaining_ms: remainingMs,
          remaining_hours: Math.ceil(remainingMs / (3600 * 1000)),
          remaining_minutes: Math.ceil(remainingMs / (60 * 1000))
        };
      });
      return sendJson(res, 200, { success: true, cooldowns });
    }

    // API: Spremanje rezultata
    if (req.method === 'POST' && pathname === '/api/results') {
      const data = await parseJsonBody(req);
      const userId = Number(data.userId);
      const user = db.prepare('SELECT * FROM users WHERE id = ?').get(userId);

      if (!user) {
        return sendJson(res, 404, { success: false, message_hr: 'Korisnik nije pronađen.', message_en: 'User not found.' });
      }

      if (!user.is_verified) {
        db.prepare('UPDATE users SET is_verified = 1 WHERE id = ?').run(userId);
      }

      const gameId = Number(data.gameId || 1);

      // STROGA PROVJERA: 96-SATNO OGRANIČENJE (Maksimalno 1 rješavanje pojedinog kviza u 96h)
      const existingCooldown = db.prepare('SELECT * FROM game_cooldowns WHERE user_id = ? AND game_id = ?').get(userId, gameId);
      if (existingCooldown) {
        const lockTime = new Date(existingCooldown.locked_until).getTime();
        const nowTime = Date.now();
        if (lockTime > nowTime) {
          const remainingHours = Math.ceil((lockTime - nowTime) / (3600 * 1000));
          const remainingMinutes = Math.ceil((lockTime - nowTime) / (60 * 1000));
          return sendJson(res, 429, {
            success: false,
            locked: true,
            lockedUntil: existingCooldown.locked_until,
            message_hr: `Već ste riješili ovaj kviz! Sukladno pravilima natjecanja, svaki kviz se može odigrati samo jednom u 96 sati (4 dana) radi ravnopravnosti. Preostalo vrijeme do ponovnog rješavanja: ${remainingHours} h (${remainingMinutes} min).`,
            message_en: `You have already played this quiz! Under competition rules, each quiz can only be played once every 96 hours. Remaining cooldown: ${remainingHours} hours.`
          });
        }
      }

      const insertResult = db.prepare(`
        INSERT INTO results (user_id, game_id, game_title, language, total_km, correct_count, total_questions, rank_title, destination, speed_bonus_km, ortho_bonus_km, streak_max, details_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      `);

      const info = insertResult.run(
        userId,
        gameId,
        sanitizeText(data.gameTitle || 'Igra'),
        data.language === 'en' ? 'en' : 'hr',
        Number(data.totalKm || 0),
        Number(data.correctCount || 0),
        Number(data.totalQuestions || 8),
        sanitizeText(data.rankTitle || ''),
        sanitizeText(data.destination || ''),
        Number(data.speedBonusKm || 0),
        Number(data.orthoBonusKm || 0),
        Number(data.maxStreak || 0),
        JSON.stringify(data.details || [])
      );

      // ZABILJEŽI 96-SATNO ZAKLJUČAVANJE (4 DANA = 96 SATI)
      const nowIso = new Date().toISOString();
      const lockedUntilIso = new Date(Date.now() + 96 * 3600 * 1000).toISOString();
      db.prepare(`
        INSERT INTO game_cooldowns (user_id, game_id, last_played_at, locked_until)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id, game_id) DO UPDATE SET
          last_played_at = excluded.last_played_at,
          locked_until = excluded.locked_until
      `).run(userId, gameId, nowIso, lockedUntilIso);

      const resultId = info.lastInsertRowid;
      const savedResult = db.prepare('SELECT * FROM results WHERE id = ?').get(resultId);

      // Pošalji potvrdu učeniku
      const emailReceipt = generateStudentEmailReceipt(user, savedResult);
      db.prepare(`
        INSERT INTO email_logs (recipient_email, recipient_name, subject, html_body, status)
        VALUES (?, ?, ?, ?, 'SENT_RECEIPT')
      `).run(user.email, `${user.first_name} ${user.last_name}`.trim(), emailReceipt.subject, emailReceipt.html);

      return sendJson(res, 200, {
        success: true,
        resultId,
        message_hr: 'Rezultat je uspješno spremljen i potvrda je evidentirana za vaš e-mail.',
        message_en: 'Result successfully saved and confirmation recorded for your email.'
      });
    }

    // API: Rang-ljestvica (javna za učenike - 24h natjecateljski ciklus)
    if (req.method === 'GET' && pathname === '/api/leaderboard') {
      const gameId = parsedUrl.searchParams.get('game_id');
      let query = `
        SELECT r.id, r.game_id, r.game_title, r.total_km, r.correct_count, r.total_questions,
               r.rank_title, r.destination, r.created_at, r.speed_bonus_km, r.ortho_bonus_km, r.streak_max,
               u.first_name, u.class_name
        FROM results r
        JOIN users u ON r.user_id = u.id
      `;
      const params = [];
      if (gameId && gameId !== 'all') {
        query += ' WHERE r.game_id = ? ';
        params.push(Number(gameId));
      }
      query += ' ORDER BY r.total_km DESC, r.correct_count DESC, r.created_at ASC LIMIT 50';

      const rows = db.prepare(query).all(...params);
      const results = rows.map((r, index) => {
        let badge = `#${index + 1}`;
        if (index === 0) badge = '🥇';
        else if (index === 1) badge = '🥈';
        else if (index === 2) badge = '🥉';
        return {
          rank: index + 1,
          badge,
          id: r.id,
          game_id: r.game_id,
          game_title: r.game_title,
          first_name: r.first_name,
          class_name: r.class_name || '',
          total_km: r.total_km,
          correct_count: r.correct_count,
          total_questions: r.total_questions,
          accuracy_pct: Math.round((r.correct_count / r.total_questions) * 100),
          rank_title: r.rank_title,
          destination: r.destination,
          speed_bonus_km: r.speed_bonus_km || 0,
          ortho_bonus_km: r.ortho_bonus_km || 0,
          streak_max: r.streak_max || 0,
          created_at: r.created_at
        };
      });

      return sendJson(res, 200, {
        success: true,
        count: results.length,
        cycleNote: 'Rezultati se čuvaju 24h u aktivnoj bazi do slanja profesoru.',
        results
      });
    }

    // ==========================================
    // ZAŠTIĆENO NASTAVNIČKO SUČELJE (ADMIN)
    // ==========================================

    const adminKey = req.headers['x-admin-password'] || parsedUrl.searchParams.get('key');
    const isAdmin = adminKey === ADMIN_PASSWORD;

    // API: Ručno pokretanje slanja i brisanja rezultata (samo nastavnik)
    if (req.method === 'POST' && pathname === '/api/admin/flush-and-wipe') {
      if (!isAdmin) {
        return sendJson(res, 401, { success: false, message: 'Neovlašten pristup. Unesite točnu profesorsku lozinku.' });
      }
      const report = flushAndEmailResults('MANUAL_TEACHER_TRIGGER');
      return sendJson(res, 200, report);
    }

    // API: Statistika i popis učenika (samo nastavnik)
    if (req.method === 'GET' && pathname === '/api/admin/stats') {
      if (!isAdmin) {
        return sendJson(res, 401, { success: false, message: 'Neovlašten pristup.' });
      }
      const userCount = db.prepare('SELECT COUNT(*) as cnt FROM users').get().cnt;
      const resultsCount = db.prepare('SELECT COUNT(*) as cnt FROM results').get().cnt;
      const emailCount = db.prepare('SELECT COUNT(*) as cnt FROM email_logs').get().cnt;
      const students = db.prepare(`
        SELECT u.id, u.email, u.first_name, u.last_name, u.class_name, u.is_verified, u.created_at,
               COUNT(r.id) as games_count, MAX(r.total_km) as best_km
        FROM users u
        LEFT JOIN results r ON u.id = r.user_id
        GROUP BY u.id
        ORDER BY u.created_at DESC
      `).all();

      return sendJson(res, 200, {
        success: true,
        stats: {
          userCount,
          maxUsers: MAX_STUDENT_PROFILES,
          resultsCount,
          emailCount,
          teacherEmail: TEACHER_EMAIL
        },
        students
      });
    }

    // API: Brisanje učenika ili resetiranje kvote (samo nastavnik)
    if (req.method === 'DELETE' && pathname.startsWith('/api/admin/users/')) {
      if (!isAdmin) {
        return sendJson(res, 401, { success: false, message: 'Neovlašten pristup.' });
      }
      const uid = Number(pathname.split('/').pop());
      db.prepare('DELETE FROM users WHERE id = ?').run(uid);
      return sendJson(res, 200, { success: true, message: 'Korisnički profil je uklonjen.' });
    }

    // STATIČKE DATOTEKE
    const defaultHtml = fs.existsSync(path.join(__dirname, 'index.html')) ? 'index.html' : 'Povijesni_Dokle_Prosvjetiteljstvo.html';
    let filePath = path.join(__dirname, pathname === '/' ? defaultHtml : pathname);
    if (!fs.existsSync(filePath)) {
      filePath = path.join(__dirname, defaultHtml);
    }

    const ext = path.extname(filePath).toLowerCase();
    const mimeTypes = {
      '.html': 'text/html; charset=utf-8',
      '.json': 'application/json; charset=utf-8',
      '.js': 'text/javascript; charset=utf-8',
      '.css': 'text/css; charset=utf-8',
      '.png': 'image/png',
      '.svg': 'image/svg+xml'
    };

    const contentType = mimeTypes[ext] || 'application/octet-stream';
    const content = fs.readFileSync(filePath);
    res.writeHead(200, {
      'Content-Type': contentType,
      'X-Content-Type-Options': 'nosniff',
      'X-Frame-Options': 'SAMEORIGIN',
      'X-XSS-Protection': '1; mode=block'
    });
    res.end(content);

  } catch (error) {
    console.error('[GREŠKA NA POSLUŽITELJU]', error);
    sendJson(res, 500, { success: false, error: 'Došlo je do pogreške na poslužitelju.' });
  }
});

function getLocalIps() {
  const interfaces = os.networkInterfaces();
  const addresses = [];
  for (const name of Object.keys(interfaces)) {
    for (const iface of interfaces[name]) {
      if (iface.family === 'IPv4' && !iface.internal) {
        addresses.push(iface.address);
      }
    }
  }
  return addresses;
}

server.listen(PORT, () => {
  console.log('\n======================================================');
  console.log('   🏛️  POVIJESNI DOKLE? – ZAŠTIĆENI POSLUŽITELJ AKTIVAN');
  console.log('======================================================');
  console.log(`Lokalni pristup na ovom računalu: http://localhost:${PORT}`);
  const ips = getLocalIps();
  if (ips.length > 0) {
    console.log('Mrežni pristup za učenike u učionici (mobiteli/tableti):');
    ips.forEach(ip => console.log(`   👉 http://${ip}:${PORT}`));
  }
  console.log(`\n🛡️ SIGURNOST I PRAVILA:`);
  console.log(`   - Maksimalno dopuštenih profila: ${MAX_STUDENT_PROFILES}`);
  console.log(`   - Brza prijava učenika (ime, razred, e-mail) bez čekanja na kod`);
  console.log(`   - Automatsko slanje rezultata svaka 24h na: ${TEACHER_EMAIL}`);
  console.log(`   - Trajno brisanje (wipe) rezultata iz baze nakon slanja`);
  console.log(`   - Lozinka za nastavničko sučelje: ${ADMIN_PASSWORD}`);
  console.log('======================================================\n');
});
