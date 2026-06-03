const themeToggle =
document.getElementById(
'themeToggle'
);

themeToggle.addEventListener(
'click',

() => {

    document.body.classList.toggle(
        'light-theme'
    );
});