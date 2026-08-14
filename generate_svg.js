const fs = require('fs');

const imgPath = '../logo.png';
if (!fs.existsSync(imgPath)) {
  console.error("logo.png not found here, searching in original download location or falling back.");
}
const imgBuff = fs.readFileSync(imgPath);
const base64 = imgBuff.toString('base64');
const ext = 'png';
const dataUrl = `data:image/${ext};base64,${base64}`;

const svgContent = `<svg width="450" height="450" viewBox="0 0 450 450" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <style>
    /* Futuristic HUD Rings Animations */
    .ring1 { animation: spin 15s linear infinite; transform-origin: 225px 225px; }
    .ring2 { animation: spinReverse 20s linear infinite; transform-origin: 225px 225px; }
    .ring3 { animation: spin 25s linear infinite; transform-origin: 225px 225px; }
    
    @keyframes spin { 100% { transform: rotate(360deg); } }
    @keyframes spinReverse { 100% { transform: rotate(-360deg); } }

    /* New Generation Logo Levitation & Pulse */
    @keyframes modernFloat {
      0% {
        transform: translateY(0px) scale(1);
        filter: drop-shadow(0 0 10px rgba(0, 210, 255, 0.6)) drop-shadow(0 0 20px rgba(58, 123, 213, 0.4));
      }
      50% {
        transform: translateY(-20px) scale(1.05);
        filter: drop-shadow(0 0 25px rgba(0, 255, 255, 1)) drop-shadow(0 0 45px rgba(0, 150, 255, 0.8));
      }
      100% {
        transform: translateY(0px) scale(1);
        filter: drop-shadow(0 0 10px rgba(0, 210, 255, 0.6)) drop-shadow(0 0 20px rgba(58, 123, 213, 0.4));
      }
    }
    .animated-logo {
      animation: modernFloat 4s ease-in-out infinite;
      transform-origin: center;
    }
  </style>

  <!-- Futuristic Background Rings -->
  <circle cx="225" cy="225" r="160" fill="none" stroke="rgba(0, 255, 255, 0.4)" stroke-width="2" stroke-dasharray="15 15" class="ring1" />
  <circle cx="225" cy="225" r="175" fill="none" stroke="rgba(100, 200, 255, 0.6)" stroke-width="1.5" stroke-dasharray="30 10 5 10" class="ring2" />
  <circle cx="225" cy="225" r="190" fill="none" stroke="rgba(0, 150, 255, 0.3)" stroke-width="3" stroke-dasharray="5 20" class="ring3" />

  <!-- Main Logo Image -->
  <g class="animated-logo">
    <image xlink:href="${dataUrl}" href="${dataUrl}" width="280" height="280" x="85" y="85" />
  </g>
</svg>`;

fs.writeFileSync('animated_logo.svg', svgContent);
console.log('Futuristic animated_logo.svg created successfully!');
