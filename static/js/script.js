// // active class menu and navbar
// document.addEventListener("DOMContentLoaded", function () {
//   let sections = document.querySelectorAll('section');
//   let navLinks = document.querySelectorAll('header nav a');
//   let navMenuLinks = document.querySelectorAll('header nav ul li a');
//   window.onscroll = () => {
//     sections.forEach(sec => {
//       let top = window.scrollY;
//       let offset = sec.offsetTop - 10;
//       let height = sec.offsetHeight;
//       let id = sec.getAttribute('id');
//       if (top >= offset && top < offset + height) {
//         navLinks.forEach(links => {
//           links.classList.remove('active');
//           document.querySelector('header nav a[href*=' + id + ']').classList.add('active');
//         });
//         navMenuLinks.forEach(links => {
//           links.classList.remove('active');
//           document.querySelector('header nav ul li a[href*=' + id + ']').classList.add('active');
//         });
//       };
//     });
//   };
// })



document.addEventListener("DOMContentLoaded", function () {
  var header = document.querySelector('header');

  // Set initial style based on the scroll position
  if (window.scrollY > 10) {
    header.classList.add('scrolled');
  } else {
    header.classList.remove('scrolled');
  }

  window.addEventListener('scroll', function () {
    if (window.scrollY > 10) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });
});


// function smoothScroll(targetId) {
//   const targetSection = document.querySelector(targetId);
//   if (targetSection) {
//     window.scrollTo({
//       top: targetSection.offsetTop,
//       behavior: 'smooth'
//     });
//   }
// }

// Apply smooth scrolling to all anchor tags with href starting with '#'
// document.querySelectorAll('a[href^="#"]').forEach(anchor => {
//   anchor.addEventListener('click', function (e) {
//     e.preventDefault();
//     const targetId = this.getAttribute('href');
//     smoothScroll(targetId);
//   });
// });

// Counter section
// $(document).ready(function () {
//   $('.counter').counterUp({
//     delay: 10,
//     time: 1200
//   });
// });

var owl = $('.owl-carousel-car');
owl.owlCarousel({
  items: 4,
  loop: false,
  rewind: true,
  margin: -16,
  autoplay: true,
  autoplayTimeout: 4000,
  autoplayHoverPause: true,
  responsive: {
    0: {
      items: 1  // Show 1 item on mobile devices
    },
    600: {
      items: 2  // Show 2 items on devices with screen width 600px or more
    },
    1000: {
      items: 4  // Show 4 items on devices with screen width 1000px or more
    }
  }
});

var owl_brand = $('.owl-carousel-brand');
owl_brand.owlCarousel({
  items: 6,
  loop: true,
  margin: -16,
  autoplay: true,
  autoplayTimeout: 4000,
  autoplayHoverPause: true,
  responsive: {
    0: {
      items: 2  // Show 1 item on mobile devices
    },
    600: {
      items: 4  // Show 2 items on devices with screen width 600px or more
    },
    1000: {
      items: 6  // Show 4 items on devices with screen width 1000px or more
    }
  }
});

var owl_review = $('.owl-carousel-review');
owl_review.owlCarousel({
  items: 1,
  loop: true,
  autoplay: true,
  autoplayTimeout: 3000,
  autoplayHoverPause: true,
});

var owl_price = $('.owl-carousel-price');
owl_price.owlCarousel({
  items: 1,
  loop: false,
  rewind: true,
  autoplay: true,
  autoplayTimeout: 3000,
  autoplayHoverPause: true,
});

document.getElementById("dateInput").min = new Date().toISOString().split("T")[0];

// Set up the interval
setInterval(price_change_function, 2000);

function notification_badge() {
  var notiElement = document.getElementById("noti");

    // Check if the noti element exists
  if (notiElement) {
      // Remove the noti element
    notiElement.remove();
  }
}

imgInp.onchange = evt => {
  const [file] = imgInp.files
  if (file) {
    blah.src = URL.createObjectURL(file)
  }
}
