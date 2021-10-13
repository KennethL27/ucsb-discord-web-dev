const navslide = () => {
    const navburger = document.querySelector('.navburger');
    const nav = document.querySelector('.mobilenav');
    const navs = document.querySelectorAll('.mobilenav li');

    navburger.addEventListener('click', () => {
        nav.classList.toggle('navburger-active');

        navs.forEach((tab, index) => {
            if (tab.style.animation) {
                tab.style.animation = '';
            }
            else {
                tab.style.animation = `navFade 0.5s ease forwards ${index / 7+0.5}s`;
            }
        });
    });
}

navslide();