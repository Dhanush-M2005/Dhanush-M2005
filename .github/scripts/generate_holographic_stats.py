import os
import json
import urllib.request
import datetime

username = "Dhanush-M2005"
token = os.environ.get("GITHUB_TOKEN")

def fetch_data(url):
    req = urllib.request.Request(url)
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())

try:
    user_data = fetch_data(f"https://api.github.com/users/{username}")
    repos_data = fetch_data(f"https://api.github.com/users/{username}/repos?per_page=100")
    
    total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_data)
    public_repos = user_data.get('public_repos', 0)
    followers = user_data.get('followers', 0)
    created_at = datetime.datetime.strptime(user_data.get('created_at', '2020-01-01T00:00:00Z'), "%Y-%m-%dT%H:%M:%SZ")
    years_active = datetime.datetime.now().year - created_at.year
    if years_active == 0:
        years_active = 1
        
except Exception as e:
    total_stars, public_repos, followers, years_active = "Error", "Error", "Error", "Error"

svg_template = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 200" width="500" height="200">
  <defs>
    <radialGradient id="hologram-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#0ff" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="#f0f" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="neon-border" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0ff"/>
      <stop offset="50%" stop-color="#f0f"/>
      <stop offset="100%" stop-color="#0ff"/>
    </linearGradient>
    <linearGradient id="text-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#fff"/>
      <stop offset="100%" stop-color="#a5f3fc"/>
    </linearGradient>
    <filter id="neon-glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <style>
    @keyframes rotateRing {{
      0% {{ transform: rotate(0deg); }}
      100% {{ transform: rotate(360deg); }}
    }}
    @keyframes reverseRotate {{
      0% {{ transform: rotate(360deg); }}
      100% {{ transform: rotate(0deg); }}
    }}
    @keyframes floatBox {{
      0%, 100% {{ transform: translateY(0); }}
      50% {{ transform: translateY(-5px); }}
    }}
    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateX(-10px); }}
      to {{ opacity: 1; transform: translateX(0); }}
    }}
    @keyframes pulseGlow {{
      0%, 100% {{ opacity: 0.6; transform: scale(1); }}
      50% {{ opacity: 1; transform: scale(1.02); }}
    }}
    .bg-rect {{ fill: #0f172a; rx: 15; ry: 15; stroke: url(#neon-border); stroke-width: 2; }}
    .ring {{ fill: none; stroke-width: 1.5; opacity: 0.6; transform-origin: 390px 100px; }}
    .ring1 {{ stroke: #0ff; stroke-dasharray: 4 4; animation: rotateRing 10s linear infinite; }}
    .ring2 {{ stroke: #f0f; stroke-dasharray: 8 4; animation: reverseRotate 15s linear infinite; }}
    .ring3 {{ stroke: #3b82f6; stroke-dasharray: 12 8; animation: rotateRing 20s linear infinite; }}
    
    .data-text {{ font-family: 'Segoe UI', -apple-system, sans-serif; font-size: 15px; font-weight: 600; fill: url(#text-grad); }}
    .title-text {{ font-family: 'Segoe UI', -apple-system, sans-serif; font-size: 20px; font-weight: 800; fill: #0ff; filter: url(#neon-glow); opacity: 0; animation: fadeIn 0.8s ease-out forwards; animation-delay: 0.1s; }}
    
    .fade-in {{ opacity: 0; animation: fadeIn 0.8s ease-out forwards; }}
    .delay-1 {{ animation-delay: 0.3s; }}
    .delay-2 {{ animation-delay: 0.5s; }}
    .delay-3 {{ animation-delay: 0.7s; }}
    .delay-4 {{ animation-delay: 0.9s; }}
    
    .wrapper {{ animation: floatBox 4s ease-in-out infinite; transform-origin: center; }}
    .glow-layer {{ animation: pulseGlow 3s ease-in-out infinite; transform-origin: center; }}
  </style>

  <g class="wrapper">
    <!-- Glow -->
    <rect class="glow-layer" fill="url(#hologram-glow)" x="10" y="10" width="480" height="180" rx="15" ry="15"/>
    
    <!-- Main Box -->
    <rect class="bg-rect" x="10" y="10" width="480" height="180" />

    <!-- Animated Holographic Core on the right -->
    <g>
      <circle class="ring ring1" cx="390" cy="100" r="50"/>
      <circle class="ring ring2" cx="390" cy="100" r="65"/>
      <circle class="ring ring3" cx="390" cy="100" r="80"/>
      <text x="390" y="110" font-family="'Segoe UI', sans-serif" font-size="34" font-weight="bold" fill="#0ff" text-anchor="middle" filter="url(#neon-glow)">{username[0]}</text>
    </g>

    <!-- Data -->
    <text x="35" y="45" class="title-text">HOLOGRAPHIC LIVE STATS</text>
    
    <g class="fade-in delay-1">
      <text x="35" y="85" class="data-text">⭐ Total Stars Earned:</text>
      <text x="220" y="85" class="data-text" fill="#f0f">{total_stars}</text>
    </g>

    <g class="fade-in delay-2">
      <text x="35" y="115" class="data-text">📦 Public Repositories:</text>
      <text x="220" y="115" class="data-text" fill="#f0f">{public_repos}</text>
    </g>

    <g class="fade-in delay-3">
      <text x="35" y="145" class="data-text">👥 GitHub Followers:</text>
      <text x="220" y="145" class="data-text" fill="#f0f">{followers}</text>
    </g>

    <g class="fade-in delay-4">
      <text x="35" y="175" class="data-text">⏳ Years Active:</text>
      <text x="220" y="175" class="data-text" fill="#f0f">{years_active} Years</text>
    </g>
  </g>
</svg>
"""

os.makedirs("dist", exist_ok=True)
with open("dist/holographic-stats.svg", "w", encoding="utf-8") as f:
    f.write(svg_template)
