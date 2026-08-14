const fs = require('fs');

const svgContent = `<svg width="800" height="160" viewBox="0 0 800 160" xmlns="http://www.w3.org/2000/svg">
  <style>
    .bg-rect {
      fill: #13141c; 
      rx: 12px;
      stroke: #2a2b3d;
      stroke-width: 2px;
    }
    .text-quote {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 26px;
      font-style: italic;
      font-weight: 500;
      fill: #22d3ee; 
    }
    .text-author {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 19px;
      font-style: italic;
      fill: #f472b6;
    }
    .glow {
      filter: drop-shadow(0px 2px 10px rgba(34, 211, 238, 0.2));
    }
  </style>
  
  <rect class="bg-rect" x="5" y="5" width="790" height="150" />
  
  <!-- Center aligned quote -->
  <text class="text-quote glow" x="400" y="80" text-anchor="middle" dominant-baseline="middle">
    "Success is a journey, not a destination 🚴"
  </text>
</svg>`;

fs.writeFileSync('quote_styled.svg', svgContent);
console.log('quote_styled.svg created successfully!');
