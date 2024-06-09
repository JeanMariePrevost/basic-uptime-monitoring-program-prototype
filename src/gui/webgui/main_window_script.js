document.addEventListener("DOMContentLoaded", (event) => {
  document.querySelector("#dashboard > h1").innerText = "The script is working";
});

function addNewCard() {
  const cardContainer = document.getElementById("dashboard");
  const newCard = document.createElement("div");
  newCard.className = "card";
  newCard.innerHTML = `
        <h2>New Resource</h2>
        <p>Details about the new resource.</p>
        <button class="edit-btn">Edit</button>
        <button class="delete-btn">Delete</button>
    `;
  cardContainer.appendChild(newCard);
  showOrHideNoMonitorsCard();

  newCard.querySelector(".delete-btn").addEventListener("click", function () {
    const card = this.parentNode;
    // HACK - Fix the delete animation by setting the height of the card to be "static
    //Get the current computed height of the card
    const cardHeight = window.getComputedStyle(card).getPropertyValue("height");
    // Set the height of the card to its current computed height
    card.style.height = cardHeight;
    // Force a reflow (redraw) to make sure the new height is applied
    void card.offsetHeight;
    // Add the fade-out class to start the animation
    card.classList.add("fade-out");
    //When done animating, remove
    card.addEventListener("animationend", () => {
      card.remove();
      showOrHideNoMonitorsCard();
    });
  });
}

function showOrHideNoMonitorsCard() {
  const cardContainer = document.getElementById('dashboard');
  const noMonitorsCard = document.getElementById('no-monitors-card');
  const otherCards = cardContainer.getElementsByClassName('card');

  if (otherCards.length === 0) {
    noMonitorsCard.style.display = 'block';
  } else if (otherCards.length > 0 && noMonitorsCard) {
    noMonitorsCard.style.display = 'none';
  }
}

// Attach the event listener to the button
document.getElementById("add-card-btn").addEventListener("click", addNewCard);
