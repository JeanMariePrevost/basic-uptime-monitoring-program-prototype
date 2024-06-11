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
 * @param {string} last_result_status - The last result status of the monitor
 * @param {string} last_result_timestamp - The last result timestamp of the monitor
 * @param {string} next_test_timestamp - The next test timestamp of the monitor
 * @param {string} test_interval_in_seconds - The test interval in seconds of the monitor
 * @returns {HTMLDivElement} A new card element for a monitor
 */
function createCardElement(title, url, last_result_status, last_result_timestamp, next_test_timestamp, test_interval_in_seconds) {
  const newCard = document.createElement("div");
  newCard.className = "card";
  newCard.innerHTML = `
      <div class="monitor-info">
        <div class="left-aligned">
          <div class="monitor-title">${title}</div>
          <a class="monitor-url" href="${url}" target="_blank">${url}</a>
        </div>
        <div class="right-aligned">
          <div class="monitor-status" status="${last_result_status}">${last_result_status}</div>
          <div class="monitor-last-result-timestamp">${last_result_timestamp}</div>
          <div class="monitor-next-test-timestamp">${next_test_timestamp}</div>
          <div class="monitor-test-interval">${test_interval_in_seconds}</div>
        </div>
      </div>
      <div class="buttons">
        <button class="edit-btn">Edit</button>
        <button class="delete-btn">Delete</button>
      </div>
    `;
  return newCard;
}




/**
 * Add a listener to the delete button of the card
 * @param {HTMLDivElement} card - The card element
 */
function addDeleteButtonListener(card) {
  card.querySelector(".delete-btn").addEventListener("click", function () {
    let parentCard = this.closest('.card');// Get the relevant card element
    animateAndRemoveCard(parentCard);
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
  console.log("Card removal animation started");

  card.addEventListener("animationend", () => {
    console.log("Card removal animation ended");
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


/**
 * Hook for receiving monitor data from the backend
 * @param {string} jsonMonitorsData - The JSON string of monitor data 
 */
function receiveMonitorsDataFromBackend(jsonMonitorsData) {
  console.log("Received monitor data from backend:");
  console.log(jsonMonitorsData);
  const monitorsData = JSON.parse(jsonMonitorsData);
  for (let monitor of monitorsData) {
    console.log(`title: ${monitor.title}`);
    console.log(`url: ${monitor.url}`);
    console.log(`last_result_status: ${monitor.last_result_status}`);
    console.log(`last_result_timestamp: ${monitor.last_result_timestamp}`);
    console.log(`next_test_timestamp: ${monitor.next_test_timestamp}`);
    console.log(`test_interval_in_seconds: ${monitor.test_interval_in_seconds}`);

    newMonitorCard = createCardElement(monitor.title, monitor.url, monitor.last_result_status, monitor.last_result_timestamp, monitor.next_test_timestamp, monitor.test_interval_in_seconds)
    addCardToDashboard(newMonitorCard);
  }
}
