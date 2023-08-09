document.addEventListener('DOMContentLoaded', function() {
  // Define toggleLock function
  function toggleLock(icon) {
    const lockIcon = 'static/img/lock_icon.png';
    const unlockIcon = 'static/img/unlock_icon.png';
    
    if (icon.src.includes(lockIcon)) {
      icon.src = icon.src.replace(lockIcon, unlockIcon);
    } else if (icon.src.includes(unlockIcon)) {
      icon.src = icon.src.replace(unlockIcon, lockIcon);
    }
  }
  
  // Add event listener to lock icons
  const lockIcons = document.querySelectorAll('.icons.lock');
  lockIcons.forEach(icon => {
    icon.addEventListener('click', function() {
      toggleLock(icon);
    });
  });
});

import './firebase-config.mjs'

    // firestore.js
const db = firebase.firestore();

// Example: Get all documents from the "users" collection
db.collection('users').get()
  .then((querySnapshot) => {
    querySnapshot.forEach((doc) => {
      console.log(doc.id, ' => ', doc.data());
    });
  })
  .catch((error) => {
    console.log('Error getting documents: ', error);
  });
