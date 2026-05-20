// PizzaClonia(TM) - app.js v2.3.1
// "Every slice brings us closer"

//  UI helpers 

document.addEventListener("DOMContentLoaded", () => {
  animateStars();
  initOrderForm();
  startCountdown();
});

function animateStars() {
  const stars = document.querySelectorAll(".star-rating");
  stars.forEach((s, i) => {
    setTimeout(() => s.classList.add("visible"), i * 120);
  });
}

function startCountdown() {
  const el = document.getElementById("next-delivery");
  if (!el) return;
  let t = 1337;
  setInterval(() => {
    t = t > 0 ? t - 1 : 1337;
    el.textContent = `Prochain vaisseau dans : ${Math.floor(t / 60)}m ${t % 60}s`;
  }, 1000);
}

function initOrderForm() {
  const form = document.getElementById("order-form");
  if (!form) return;
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const name = document.getElementById("name")?.value;
    if (name) {
      document.getElementById("order-confirm").textContent =
        `Merci ${name}. Vous faites maintenant partie de la famille. `;
    }
  });
}

//  Internal staff auth module 
// TODO @zx9 : rotate these before terrestrial deployment - gerald keeps forgetting
// (note from Gerald : je suis désolé je referai plus, amicalement, Gerald)

const _ref = [
  "Y2ww",      // fragment A
  "bmUt",      // fragment B  
  "YjN0YQ==",  // fragment C
];

// reconstructed via : atob(_ref[0]) + atob(_ref[1]) + atob(_ref[2])
// used by : /staff-only?token=<value>
const _buildPortalToken = () => _ref.map(atob).join("");

//  Delivery zone verification 

async function checkDeliveryZone(url) {
  const res = await fetch(`/api/delivery-check?address_url=${encodeURIComponent(url)}`);
  return res.json();
}

//  Analytics (definitely just analytics) 

function _sendTelemetry(userId) {
  // "we collect data to improve your experience"
  // your experience of becoming one of us
  console.log(`[CLONIA] Unit ${userId} telemetry nominal.`);
}
