let _monitors = []; //Array of Monitor data objects

document.addEventListener("DOMContentLoaded", (event) => {
  document.getElementById("add-card-btn").addEventListener("click", onAddMonitorClicked);
  // document.getElementById("apply-btn").addEventListener("click", updateMonitorsDataInBackend);
});

/**
 * Disables all interaction with the window and blurs it
 */
function disableWindow() {
  const body = document.querySelector("body");
  body.style.pointerEvents = "none";
  body.style.filter = "blur(5px)";
  body.style.userSelect = "none";
}

/**
 * Re-enables interactions with the window and removes the blur
 */
function enableWindow() {
  console.log("Enabling window");
  const body = document.querySelector("body");
  body.style.pointerEvents = "auto";
  body.style.filter = "none";
  body.style.userSelect = "auto";
}

/**
 * Add a new monitor card to the dashboard
 */
function onAddMonitorClicked() {
  pywebview.api.on_new_monitor_button_clicked();
}

/**
 * Sends the data from all monitor cards on the dashboard to the backend
 */
function updateMonitorsDataInBackend() {
  const monitorData = JSON.stringify(_monitors);
  pywebview.api.send_monitors_data_to_backend(monitorData);
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
  addCheckStatusButtonListener(card);
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
function createCardElement(monitorDataObject) {
  let display_title = monitorDataObject.title;
  let display_url = monitorDataObject.url;
  let display_last_result_status = monitorDataObject.last_result_status;
  let display_last_result_error = monitorDataObject.last_result_error;
  let display_last_result_timestamp = monitorDataObject.last_result_timestamp;
  let display_next_test_timestamp = monitorDataObject.next_test_timestamp;
  let display_test_interval_in_seconds = monitorDataObject.test_interval_in_seconds;
  let toolTipText = "";

  //Replace null/"falsy" strings with user-friendly display values
  if (display_last_result_status === null || display_last_result_status === "" || display_last_result_status === "null") {
    display_last_result_status = "Unknown";
  }else if (display_last_result_status === "down" && display_last_result_error !== null && display_last_result_error !== "") {
    display_last_result_status = "Error";
    toolTipText = display_last_result_error;
  }

  if (display_last_result_timestamp === null || display_last_result_timestamp === "" || display_last_result_timestamp === "null") {
    display_last_result_timestamp = "Never tested";
  }
  if (display_next_test_timestamp === null || display_next_test_timestamp === "" || display_next_test_timestamp === "null") {
    display_next_test_timestamp = "No upcoming test scheduled";
  }

  const newCard = document.createElement("div");
  newCard.className = "card";
  newCard.innerHTML = `
      <div class="monitor-info">
        <div class="left-aligned">
          <div class="monitor-title">${display_title}</div>
          <a class="monitor-url" href="${display_url}" target="_blank">${display_url}</a>
        </div>
        <div class="right-aligned">
          <div class="monitor-status" status="${monitorDataObject.last_result_status}" title="${toolTipText}">${display_last_result_status}</div>
          <div class="monitor-last-result-timestamp">Last checked: ${display_last_result_timestamp}</div>
          <div class="monitor-next-test-timestamp">Next check: ${display_next_test_timestamp}</div>
          <div class="monitor-test-interval">Check frenquency: ${display_test_interval_in_seconds}s</div>
        </div>
      </div>
      <div class="buttons">
        <button class="edit-btn">Edit</button>
        <button class="delete-btn">Delete</button>
        <button class="check-status-btn">Check Status</button>
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
    let parentCard = this.closest(".card"); // Get the relevant card element
    let cardTitle = parentCard.querySelector(".monitor-title").textContent;
    const confirmed = confirm(`Are you sure you want to delete the following monitor?\n"${cardTitle}"\n\nThis action cannot be undone.`);
    if (confirmed) {
      animateAndRemoveCard(parentCard);
    }
  });
}

/**
 * Add a listener to the edit button of the card
 * @param {HTMLDivElement} card - The card element
 */
function addEditButtonListener(card) {
  card.querySelector(".edit-btn").addEventListener("click", function () {
    // Get the card's current data
    const monitor = getMonitorByCard(card);
    const title = monitor.title;
    const url = monitor.url;
    const testInterval = monitor.test_interval_in_seconds;

    //Basic prompt to edit the card
    const newTitle = prompt("Enter the new title", title);
    if (!newTitle) return; //If the user cancels the prompt, do nothing
    const newURL = prompt("Enter the new details", url);
    if (!newURL) return; //If the user cancels the prompt, do nothing
    const newTestInterval = prompt("Enter the new test interval", testInterval);
    if (!newTestInterval) return; //If the user cancels the prompt, do nothing

    //Update the Monitor object in the array
    monitor.title = newTitle;
    monitor.url = newURL;
    monitor.test_interval_in_seconds = newTestInterval;

    // Update the card with the new data
    const titleElement = card.querySelector(".monitor-title");
    const urlElement = card.querySelector(".monitor-url");
    const testIntervalElement = card.querySelector(".monitor-test-interval");
    
    titleElement.textContent = newTitle;
    urlElement.href = newURL;
    urlElement.textContent = newURL;
    testIntervalElement.textContent = newTestInterval;

    updateMonitorsDataInBackend();
  });
}

/**
 * Add a listener to the check status button of the card
 * @param {HTMLDivElement} card - The card element
 */
function addCheckStatusButtonListener(card) {
  card.querySelector(".check-status-btn").addEventListener("click", function () {
    const title = card.querySelector(".monitor-title").textContent;
    pywebview.api.on_check_status_button_clicked(title);
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
    // Remove the Monitor object from the _monitors array
    const monitor = getMonitorByCard(card);
    const index = _monitors.indexOf(monitor);
    if (index > -1) {
      _monitors.splice(index, 1);
    }
    //Remove the card element from the DOM
    card.remove();

    updateMonitorsDataInBackend(); //Apply the changes to the backend immediately
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

  console.log(`Number of cards: ${otherCards.length}`);

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
  //DEBUG
  console.log("Received monitor data from backend:");
  console.log(jsonMonitorsData);

  //Update the data
  updateMonitorsArray(jsonMonitorsData);

  //Rebuild the visuals
  refreshMonitorCards();
}

/**
 * Removes all monitor card elements from the dashboard
 */
function removeAllMonitorCardElements() {
  const cardContainer = document.getElementById("cards-container");
  const cards = cardContainer.getElementsByClassName("card");
  for (let i = cards.length - 1; i >= 0; i--) {
    const card = cards[i];
    if (card.id !== "no-monitors-card") {
      card.remove();
    }
  }
}

/**
 * Rebuilds the monitor cards from the current monitor data array
 */
function refreshMonitorCards() {
  removeAllMonitorCardElements();
  for (let monitor of _monitors) {
    const newMonitorCard = createCardElement(monitor);
    addCardToDashboard(newMonitorCard);
  }
}

/**
 * Rebuilds the array of monitors data objects from a JSON string
 * @param {string} jsonMonitorsData - The JSON string of monitor data
 */
function updateMonitorsArray(jsonMonitorsData) {
  const monitorsData = JSON.parse(jsonMonitorsData);
  _monitors = monitorsData.map(
    (monitor) => new Monitor(monitor.title, monitor.url, monitor.last_result_status, monitor.last_result_error, monitor.last_result_timestamp, monitor.next_test_timestamp, monitor.test_interval_in_seconds)
  );
}

/**
 * Monitor data object to hold the data separate from their visual representation
 */
class Monitor {
  /**
   * Create a new Monitor object
   * @param {string} title - The title of the monitor
   * @param {string} url - The URL of the monitor
   * @param {string} last_result_status - The last result status of the monitor
   * @param {string} last_result_error - The last result error of the monitor
   * @param {string} last_result_timestamp - The last result timestamp of the monitor
   * @param {string} next_test_timestamp - The next test timestamp of the monitor
   * @param {string} test_interval_in_seconds - The test interval in seconds of the monitor
   */
  constructor(title, url, last_result_status, last_result_error, last_result_timestamp, next_test_timestamp, test_interval_in_seconds) {
    this.title = title;
    this.url = url;
    this.last_result_status = last_result_status;
    this.last_result_error = last_result_error;
    this.last_result_timestamp = last_result_timestamp;
    this.next_test_timestamp = next_test_timestamp;
    this.test_interval_in_seconds = test_interval_in_seconds;
  }
}

/**
 * Get the Monitor object from the array of monitors by its title
 * @param {string} title - The title of the monitor
 */
function getMonitorByTitle(title) {
  return _monitors.find((monitor) => monitor.title === title);
}

/**
 * Get the Monitor object from the array of monitors by its card element
 * @param {HTMLDivElement} card - The card element of the monitor
 * @returns {Monitor} The Monitor object
 */
function getMonitorByCard(card) {
  return getMonitorByTitle(getCardTitle(card));
}

function getCardTitle(card) {
  return card.querySelector(".monitor-title").textContent;
}