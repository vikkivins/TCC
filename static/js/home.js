document.addEventListener('DOMContentLoaded', function() {
    const mainAddButton = document.getElementById('mainAddButton');
    const optionButtons = document.getElementById('optionButtons');

    mainAddButton.addEventListener('click', function() {
        this.classList.toggle('active');
        optionButtons.classList.toggle('active');
    });

    // Carousel functionality
    const carouselContainer = document.querySelector('.book-carousel-container');
    const carousel = carouselContainer.querySelector('.book-carousel');
    const prevButton = carouselContainer.querySelector('.carousel-button.prev');
    const nextButton = carouselContainer.querySelector('.carousel-button.next');

    prevButton.addEventListener('click', () => {
        carousel.scrollBy({ left: -200, behavior: 'smooth' });
    });

    nextButton.addEventListener('click', () => {
        carousel.scrollBy({ left: 200, behavior: 'smooth' });
    });
});