import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, updateProfile, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-auth.js";
import { getFirestore, doc, setDoc, getDoc } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyAdPQDhJB_MDkyK_6DrBYNIDsxeIm_B3hc",
  authDomain: "guardioescerrado-903ab.firebaseapp.com",
  projectId: "guardioescerrado-903ab",
  storageBucket: "guardioescerrado-903ab.firebasestorage.app",
  messagingSenderId: "416924056556",
  appId: "1:416924056556:web:0d76d4e7ca592a3d849ec9"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

async function ensureProfile(user, name) {
  const ref = doc(db, 'usuarios', user.uid);
  const snap = await getDoc(ref);
  if (!snap.exists()) {
    await setDoc(ref, { nome: name || user.displayName || user.email, pontos: 1250, nivel: 4, missoes: 12, medalhas: 5 });
  }
}

async function createServerSession() {
  const token = await auth.currentUser.getIdToken();
  await fetch('/session-login', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ idToken: token })});
}

const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');

if (loginForm) {
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const senha = document.getElementById('login-senha').value;
    const feedback = document.getElementById('login-feedback');
    try {
      await signInWithEmailAndPassword(auth, email, senha);
      await createServerSession();
      feedback.textContent = 'Login realizado com sucesso!';
      feedback.className = 'auth-feedback success';
      window.location.href = '/dashboard';
    } catch (err) {
      feedback.textContent = 'Erro no login. Verifique seus dados.';
      feedback.className = 'auth-feedback error';
    }
  });
}

if (registerForm) {
  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const nome = document.getElementById('cadastro-nome').value;
    const email = document.getElementById('cadastro-email').value;
    const senha = document.getElementById('cadastro-senha').value;
    const feedback = document.getElementById('register-feedback');
    try {
      const cred = await createUserWithEmailAndPassword(auth, email, senha);
      await updateProfile(cred.user, { displayName: nome });
      await ensureProfile(cred.user, nome);
      await createServerSession();
      feedback.textContent = 'Cadastro concluído!';
      feedback.className = 'auth-feedback success';
      window.location.href = '/dashboard';
    } catch (err) {
      feedback.textContent = 'Erro no cadastro. Tente outro e-mail.';
      feedback.className = 'auth-feedback error';
    }
  });
}

const dashName = document.getElementById('dash-user-name');
if (dashName) {
  onAuthStateChanged(auth, async (user) => {
    if (!user) {
      window.location.href = '/login.html';
      return;
    }
    await ensureProfile(user);
    const snap = await getDoc(doc(db, 'usuarios', user.uid));
    const d = snap.data() || {};
    document.getElementById('dash-user-name').textContent = d.nome || user.displayName || user.email;
    document.getElementById('dash-user-level').textContent = `Nível ${d.nivel || 1}`;
    document.getElementById('hero-name').textContent = d.nome || user.displayName || 'Guardião';
    document.getElementById('stat-pontos').textContent = d.pontos || 0;
    document.getElementById('stat-missoes').textContent = d.missoes || 0;
    document.getElementById('stat-medalhas').textContent = d.medalhas || 0;
    document.getElementById('progress-fill').style.width = `${Math.min(100, ((d.pontos || 0) % 500) / 5)}%`;
  });

  const logoutBtn = document.getElementById('logout-btn');
  logoutBtn?.addEventListener('click', async () => {
    await signOut(auth);
    await fetch('/session-logout', { method: 'POST' });
    window.location.href = '/login.html';
  });
}
