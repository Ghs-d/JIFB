const track = document.querySelector('.carousel-track');
const prevButton = document.querySelector('.prev');
const nextButton = document.querySelector('.next');

let currentIndex = 0;

// Duplicar os cards para criar o efeito infinito
const cards = Array.from(track.children);
cards.forEach(card => {
  const clone = card.cloneNode(true);
  track.appendChild(clone); // Adiciona os clones ao final
});

nextButton.addEventListener('click', () => moveToNext());
prevButton.addEventListener('click', () => moveToPrev());

function moveToNext() {
  currentIndex++;
  track.style.transition = 'transform 0.5s ease-in-out';
  updateCarousel();

  if (currentIndex >= cards.length) {
    setTimeout(() => {
      track.style.transition = 'none';
      currentIndex = 0;
      updateCarousel();
    }, 500); // Tempo igual ao de transição
  }
}

function moveToPrev() {
  currentIndex--;
  if (currentIndex < 0) {
    currentIndex = cards.length - 1;
    track.style.transition = 'none';
    updateCarousel();
  }

  setTimeout(() => {
    track.style.transition = 'transform 0.5s ease-in-out';
    updateCarousel();
  }, 10);
}

function updateCarousel() {
  const cardWidth = track.children[0].getBoundingClientRect().width + 20; // Inclui margens
  track.style.transform = `translateX(-${currentIndex * cardWidth}px)`;
}

// Movimento automático (opcional)
setInterval(() => {
  moveToNext();
}, 3000); // Tempo em milissegundos
