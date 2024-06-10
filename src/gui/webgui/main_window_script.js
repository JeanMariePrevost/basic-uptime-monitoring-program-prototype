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
      <div class="monitor-title">Monitore Title</div>
      <div class="monitor-url"><a href="https://google.com">https://google.com</a></div>
      <div class="monitor-status">Status unknown</div>
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


/**
 * Save the content of all monitor cards to a local JSON file
 */
async function saveMonitorCardsToFile() {
  // Get all the monitor cards
  const cards = document.querySelectorAll('.card');

  // Extract the content of each card
  const cardContents = Array.from(cards).map(card => card.textContent);

  // Convert the contents to JSON
  const json = JSON.stringify(cardContents, null, 2);

  // Use the File System API to write the JSON to a file
  // Note: This API is not available in all environments
  // In a Node.js environment, you would use the fs module
  // In a browser environment, you might use the File System Access API
  // This example assumes a Node.js environment
  const fs = require('fs');
  fs.writeFile('monitorCards.json', json, (err) => {
    if (err) throw err;
    console.log('The file has been saved!');
  });
}