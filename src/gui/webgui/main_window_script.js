document.addEventListener("DOMContentLoaded", (event) => {
  document.getElementById("add-card-btn").addEventListener("click", addNewEmptyCardToDashboard);
  document.getElementById("apply-btn").addEventListener("click", sendMonitorsDataToBackend);
});

/**
 * Add a new monitor card to the dashboard
 */
function addNewEmptyCardToDashboard() {
  addCardToDashboard(createCardElement());
}

/**
 * Sends the data from all monitor cards on the dashboard to the backend
 */
function sendMonitorsDataToBackend() {
  const monitorData = serializeMonitorsData();
  pywebview.api.sendMonitorsDataToBackend(monitorData);
}

/**
 * Serializes the data from all monitor cards on the dashboard to JSON
 */
function serializeMonitorsData() {
  const cardContainer = document.getElementById("cards-container");
  const cards = cardContainer.getElementsByClassName("card");

  const monitors = [];
  for (let card of cards) {
    const title = card.querySelector(".monitor-title").textContent;
    const url = card.querySelector(".monitor-url").textContent;
    const status = card.querySelector(".monitor-status").textContent;
    monitors.push({ title, url, status });
  }

  return JSON.stringify(monitors);
}

/**
 * Adds a card existing card element to the dashboard
 * @param {HTMLDivElement} card - The card element to add
 */
function addCardToDashboard(card) {
  const cardContainer = document.getElementById("cards-container");
  cardContainer.appendChild(card);
  addDeleteButtonListener(card);
  addEditButtonListener(card);
  showOrHideNoMonitorsCard();
}

/**
 * Creates a new html element for a card monitor
 * @param {string} title - The title of the monitor
 * @param {string} url - The URL of the monitor
 * @param {string} status - The status of the monitor
 * @returns {HTMLDivElement} A new card element for a monitor
 */
function createCardElement(title, url, status) {
  const newCard = document.createElement("div");
  newCard.className = "card";
  newCard.innerHTML = `
      <div class="monitor-title">${title}</div>
      <a class="monitor-url" href="${url}" target="_blank">${url}</a>
      <div class="monitor-status" status="${status}">${status}</div>
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
    // Get the card's current data
    const card = this.parentNode;
    const cardTitle = card.querySelector(".monitor-title");
    const cardURL = card.querySelector(".monitor-url");
    const cardStatus = card.querySelector(".monitor-status");

    //Basic prompt to edit the card
    const newTitle = prompt("Enter the new title", cardTitle.textContent);
    const newURL = prompt("Enter the new details", cardURL.textContent);
    const newStatus = prompt("DEBUG - Enter a status", cardStatus.textContent);

    // Update the card with the new data
    if (newTitle && newURL && newStatus) {
      cardTitle.textContent = newTitle;
      cardURL.href = newURL;
      cardURL.textContent = newURL;
      cardStatus.textContent = newStatus;
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
  const cardContainer = document.getElementById("cards-container");
  const noMonitorsCard = document.getElementById("no-monitors-card");
  const otherCards = cardContainer.getElementsByClassName("card");

  if (otherCards.length === 0) {
    noMonitorsCard.style.display = "block";
  } else if (noMonitorsCard) {
    noMonitorsCard.style.display = "none";
  }
}

function receiveDataFromBackendTest(data) {
  console.log(data);
  document.querySelector("h1").textContent = data;
  // Parse the JSON string into a JavaScript object
  const monitors = JSON.parse(data);

  // Log each monitor's properties
  monitors.forEach((monitor) => {
    console.log(`Title: ${monitor.title}`);
    console.log(`URL: ${monitor.url}`);
    console.log(`Status: ${monitor.status}`);
    newMonitorCard = createCardElement(monitor.title, monitor.url, monitor.status);
    addCardToDashboard(newMonitorCard);
  });

  // Manipulate the data as needed
  // For example, you could display the data in the HTML
  const h1 = document.querySelector("h1");
  h1.textContent = `Received ${monitors.length} monitors`;
}
