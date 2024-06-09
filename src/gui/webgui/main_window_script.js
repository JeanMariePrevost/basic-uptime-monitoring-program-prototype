document.addEventListener("DOMContentLoaded", (event) => {
  document.getElementById("add-card-btn").addEventListener("click", addNewCard);
});

/**
 * Add a new monitor card to the dashboard
 */
function addNewCard() {
  const cardContainer = document.getElementById("dashboard");
  const newCard = createCardElement();

  cardContainer.appendChild(newCard);
  showOrHideNoMonitorsCard();

  addDeleteButtonListener(newCard);
  addEditButtonListener(newCard);
}

/**
 * Creates  a new html element for a card monitor
 * @returns {HTMLDivElement} A new card element for a monitor
 */
function createCardElement() {
  const newCard = document.createElement("div");
  newCard.className = "card";
  newCard.innerHTML = `
      <h2>New Monitor</h2>
      <p>Details about the monitor.</p>
      <button class="edit-btn">Edit</button>
      <button class="delete-btn">Delete</button>
    `;
  return newCard;
}

/**
 * Add a listener to the delete button of the card
 * @param {HTMLDivElement} card - The card element
 */
function addDeleteButtonListener(card) {
  card.querySelector(".delete-btn").addEventListener("click", function () {
    animateAndRemoveCard(this.parentNode);
  });
}

/**
 * Add a listener to the edit button of the card
 * @param {HTMLDivElement} card - The card element
 */
function addEditButtonListener(card) {
  card.querySelector(".edit-btn").addEventListener("click", function () {
    const card = this.parentNode;
    const cardTitle = card.querySelector("h2");
    const cardDetails = card.querySelector("p");
    const cardEditButton = card.querySelector(".edit-btn");

    const newTitle = prompt("Enter the new title", cardTitle.textContent);
    const newDetails = prompt("Enter the new details", cardDetails.textContent);

    if (newTitle && newDetails) {
      cardTitle.textContent = newTitle;
      cardDetails.textContent = newDetails;
    }
  });
}

/**
 * Animate the removal of a card then remove it from the dashboard
 * @param {HTMLDivElement} card - The card element to remove
 */
function animateAndRemoveCard(card) {
  const cardHeight = window.getComputedStyle(card).getPropertyValue("height");
  card.style.height = cardHeight;
  void card.offsetHeight;
  card.classList.add("fade-out");

  card.addEventListener("animationend", () => {
    card.remove();
    showOrHideNoMonitorsCard();
  });
}

/**
 * Show or hide the no monitors card based on whether monitors exist
 */
function showOrHideNoMonitorsCard() {
  const cardContainer = document.getElementById("dashboard");
  const noMonitorsCard = document.getElementById("no-monitors-card");
  const otherCards = cardContainer.getElementsByClassName("card");

  if (otherCards.length === 0) {
    noMonitorsCard.style.display = "block";
  } else if (noMonitorsCard) {
    noMonitorsCard.style.display = "none";
  }
}
