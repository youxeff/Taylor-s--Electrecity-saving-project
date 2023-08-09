import { firebaseConfig } from './firebase-config.mjs';
// Constants
const ROWS_PER_PAGE = 6;
let currentPage = 1;

// Firestore initialization
firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

// Function to fetch billing data for the current page
const fetchBillingData = () => {
  const billingTable = document.querySelector('table');
  const currentPageElement = document.getElementById('currentPage');

  // Clear the table
  while (billingTable.rows.length > 1) {
    billingTable.deleteRow(1);
  }

  // Fetch the billing data
   db.collection
    .orderBy('id')
    .limit(ROWS_PER_PAGE)
    .offset((currentPage - 1) * ROWS_PER_PAGE)
    .get()
    .then((querySnapshot) => {
      querySnapshot.forEach((doc) => {
        const billing = doc.data();
        const row = billingTable.insertRow(-1);
        row.insertCell().textContent = billing.address;
        row.insertCell().textContent = billing.billingType;
        row.insertCell().textContent = billing.electricAccount;
        row.insertCell().textContent = billing.Name;
        row.insertCell().textContent = billing.id;
        row.insertCell().textContent = billing.numOfAirConUnits;
        row.insertCell().textContent = billing.numOfLightingUnits;
        row.insertCell().textContent = billing.numOfOccupants;
        row.insertCell().textContent = billing.numOfRefrigeratorUnits;
      });
    
      // Update the current page element
      currentPageElement.textContent = currentPage;
    })

    .catch((error) => {
      console.log('Error getting documents: ', error);
    });
};

// Function to navigate to the previous page
const goToPreviousPage = () => {
  if (currentPage > 1) {
    currentPage--;
    fetchBillingData();
    updatePaginationButtons();
  }
};

// Function to navigate to the next page
const goToNextPage = () => {
  currentPage++;
  fetchBillingData();
  updatePaginationButtons();
};

// Function to update the state of pagination buttons
const updatePaginationButtons = () => {
  const prevPageBtn = document.getElementById('prevPageBtn');
  const nextPageBtn = document.getElementById('nextPageBtn');

  // Enable or disable buttons based on current page
  prevPageBtn.disabled = currentPage === 1;
  nextPageBtn.disabled = false; // Assuming there is always more data to load

  // Update the page number display
  const currentPageElement = document.getElementById('currentPage');
  currentPageElement.textContent = currentPage;
};

// Attach event listeners to pagination buttons
document.getElementById('prevPageBtn').addEventListener('click', goToPreviousPage);
document.getElementById('nextPageBtn').addEventListener('click', goToNextPage);

// Fetch initial billing data
fetchBillingData();
