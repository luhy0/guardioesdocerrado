const map = L.map('cerrado-map').setView([-16.3, -49.3], 6);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 18,
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

const pontos = [
  {
    tipo: 'Queimada',
    cor: '#e76f51',
    nome: 'Região de Pirenópolis (GO)',
    coords: [-15.85, -48.96],
    mensagem: 'Essa área sofre com queimadas frequentes durante a estação seca.',
    imagem: 'https://images.unsplash.com/photo-1475776408506-9a5371e7a068'
  },
  {
    tipo: 'Área Preservada',
    cor: '#2a9d8f',
    nome: 'Parque Estadual da Serra de Caldas',
    coords: [-17.74, -48.68],
    mensagem: 'Área com vegetação preservada e ações de recuperação ambiental.',
    imagem: 'https://images.unsplash.com/photo-1448375240586-882707db888b'
  },
  {
    tipo: 'Animais do Cerrado',
    cor: '#f4a261',
    nome: 'Entorno do Parque Nacional das Emas',
    coords: [-18.34, -52.95],
    mensagem: 'Ponto de observação de espécies como lobo-guará e tamanduá-bandeira.',
    imagem: 'https://upload.wikimedia.org/wikipedia/commons/5/58/Chrysocyon_brachyurus.jpg'
  }
];

const cards = document.getElementById('mapa-cards');

function addInfoCard(ponto) {
  const article = document.createElement('article');
  article.className = 'info-card fade-in-up is-visible';
  article.innerHTML = `
    <span class="info-badge" style="background:${ponto.cor}">${ponto.tipo}</span>
    <h3>${ponto.nome}</h3>
    <img src="${ponto.imagem}" alt="${ponto.nome}">
    <p>${ponto.mensagem}</p>
  `;
  cards.prepend(article);
}

pontos.forEach((ponto) => {
  const marker = L.circleMarker(ponto.coords, {
    radius: 10,
    color: ponto.cor,
    fillColor: ponto.cor,
    fillOpacity: 0.85
  }).addTo(map);

  marker.bindPopup(`<strong>${ponto.tipo}</strong><br>${ponto.nome}`);
  marker.on('click', () => addInfoCard(ponto));
});
