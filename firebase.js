import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-analytics.js";
import {
    getAuth,
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    updateProfile,
    onAuthStateChanged,
    signOut
} from "https://www.gstatic.com/firebasejs/10.12.5/firebase-auth.js";
import {
    getFirestore,
    doc,
    getDoc,
    setDoc,
    updateDoc,
    increment,
    serverTimestamp
} from "https://www.gstatic.com/firebasejs/10.12.5/firebase-firestore.js";

const firebaseConfig = { apiKey: "AIzaSyAdPQDhJB_MDkyK_6DrBYNIDsxeIm_B3hc", authDomain: "guardioescerrado-903ab.firebaseapp.com", projectId: "guardioescerrado-903ab", storageBucket: "guardioescerrado-903ab.firebasestorage.app", messagingSenderId: "416924056556", appId: "1:416924056556:web:0d76d4e7ca592a3d849ec9", measurementId: "G-B3PWG4QYQC" };

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
const db = getFirestore(app);

const feedback = document.getElementById("auth-feedback");
const loginForm = document.getElementById("login-form");
const registerForm = document.getElementById("register-form");

function showMessage(message, type = "info") {
    if (!feedback) return;
    feedback.textContent = message;
    feedback.className = `auth-feedback ${type}`;
}

async function getOrCreateProfile(user) {
    const userRef = doc(db, "usuarios", user.uid);
    const snap = await getDoc(userRef);
    if (!snap.exists()) {
        await setDoc(userRef, {
            nome: user.displayName || user.email,
            email: user.email,
            pontos: 0,
            createdAt: serverTimestamp(),
            unlockedSpecies: ["lobo-guara", "tamandua-bandeira"]
        });
        return { nome: user.displayName || user.email, pontos: 0 };
    }
    return snap.data();
}

if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const email = document.getElementById("login-email").value;
        const senha = document.getElementById("login-senha").value;
        try {
            await signInWithEmailAndPassword(auth, email, senha);
            showMessage("Login realizado com sucesso! Redirecionando...", "success");
            window.location.href = "home.html";
        } catch (error) {
            showMessage(`Erro no login: ${error.message}`, "error");
        }
    });
}

if (registerForm) {
    registerForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const nome = document.getElementById("cadastro-nome").value;
        const email = document.getElementById("cadastro-email").value;
        const senha = document.getElementById("cadastro-senha").value;
        try {
            const credencial = await createUserWithEmailAndPassword(auth, email, senha);
            await updateProfile(credencial.user, { displayName: nome });
            await getOrCreateProfile({ ...credencial.user, displayName: nome });
            showMessage("Conta criada com sucesso! Redirecionando para a home...", "success");
            window.location.href = "home.html";
        } catch (error) {
            showMessage(`Erro no cadastro: ${error.message}`, "error");
        }
    });
}

const userName = document.getElementById("user-name");
const logoutBtn = document.getElementById("logout-btn");
const homeUserName = document.getElementById("home-user-name");
const homeUserPoints = document.getElementById("home-user-points");
const homeUserLevel = document.getElementById("home-user-level");
const homeProgressBar = document.getElementById("home-progress-bar");

onAuthStateChanged(auth, async (user) => {
    const protectedPage = userName || homeUserName;
    if (!user && protectedPage) {
        window.location.href = "login.html";
        return;
    }
    if (!user) return;

    const profile = await getOrCreateProfile(user);

    if (userName) {
        userName.textContent = profile.nome || user.displayName || user.email;
    }

    if (homeUserName) {
        const pontos = Number(profile.pontos || 0);
        const nivel = Math.floor(pontos / 100);
        const progresso = pontos % 100;
        homeUserName.textContent = profile.nome || user.displayName || user.email;
        homeUserPoints.textContent = String(pontos);
        homeUserLevel.textContent = String(nivel);
        homeProgressBar.style.width = `${progresso}%`;
    }
});

if (logoutBtn) {
    logoutBtn.addEventListener("click", async () => {
        await signOut(auth);
        window.location.href = "login.html";
    });
}

window.guardioesDB = {
    async somarPontos(uid, pontos) {
        await updateDoc(doc(db, "usuarios", uid), { pontos: increment(pontos) });
    }
};

export { app, analytics, auth };
