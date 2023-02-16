document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();
    document.querySelector('#message').innerHTML = 'Thank you for your message!';
  });