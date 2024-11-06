// Constants
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
const formElement = document.querySelector('form');

// Eventlisteners
formElement.addEventListener('submit', filterHotelsByCity)

// Functions
async function filterHotelsByCity(event) {
   /**
   * Asynchronous function for making post request with passed in city filter.
   */
   event.preventDefault();
   const formData = new FormData(formElement);

   await fetch('/', {
       method: 'POST',
       headers: {'X-CSRFToken': csrfToken}
       body: formData,
   });
}