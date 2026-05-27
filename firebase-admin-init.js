/**
 * Firebase Admin SDK initialization (Node.js)
 *
 * Equivalent to requested setup:
 * var admin = require("firebase-admin");
 * var serviceAccount = require("path/to/serviceAccountKey.json");
 * admin.initializeApp({ credential: admin.credential.cert(serviceAccount) });
 */

const admin = require("firebase-admin");
const path = require("path");

const serviceAccountPath = process.env.FIREBASE_SERVICE_ACCOUNT || "serviceAccountKey.json";
const serviceAccount = require(path.resolve(serviceAccountPath));

if (!admin.apps.length) {
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
  });
}

const db = admin.firestore();

module.exports = { admin, db };
