/* Esto es sólo para la selección xp */

const items=document.querySelectorAll('.small-img');
const big=document.querySelector('.big-img');
for (let item of items){
    item.addEventListener('mouseover', () => {
    big.setAttribute('src', item.getAttribute('src'));
});
}