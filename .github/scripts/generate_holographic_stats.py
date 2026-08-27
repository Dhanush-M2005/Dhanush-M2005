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
    events_data = fetch_data(f"https://api.github.com/users/{username}/events?per_page=100")
    
    total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_data)
    public_repos = user_data.get('public_repos', 0)
    followers = user_data.get('followers', 0)
    created_at = datetime.datetime.strptime(user_data.get('created_at', '2020-01-01T00:00:00Z'), "%Y-%m-%dT%H:%M:%SZ")
    years_active = datetime.datetime.now().year - created_at.year
    if years_active == 0:
        years_active = 1
        
    # Build Graph Data from Events (Last 14 days of activity)
    activity = {}
    for event in events_data:
        date_str = event['created_at'][:10]
        activity[date_str] = activity.get(date_str, 0) + 1
        
    # Sort dates and pick the most recent 14 active days
    sorted_dates = sorted(list(activity.keys()))[-14:]
    if not sorted_dates:
        sorted_dates = [datetime.datetime.now().strftime("%Y-%m-%d")]
        activity[sorted_dates[0]] = 1
        
    # Normalize data for SVG chart (Y range: 0 to 60)
    max_activity = max([activity[d] for d in sorted_dates]) or 1
    graph_points = []
    width_step = 280 / max(len(sorted_dates) - 1, 1)
    
    for i, date_str in enumerate(sorted_dates):
        x = i * width_step
        # Invert Y to draw upwards (Height max is 60)
        y = 60 - ((activity[date_str] / max_activity) * 50) 
        graph_points.append(f"{x},{y}")
        
    path_data = " ".join(graph_points)
    area_path = f"0,60 {path_data} 280,60"

except Exception as e:
    total_stars, public_repos, followers, years_active = "Err", "Err", "Err", "Err"
    path_data = "0,60 140,20 280,60"
    area_path = "0,60 140,20 280,60"

svg_template = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 250" width="500" height="250">
  <defs>
    <radialGradient id="hologram-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#0ff" stop-opacity="0.15"/>
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
    <linearGradient id="area-grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0ff" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#f0f" stop-opacity="0.1"/>
    </linearGradient>
    <filter id="neon-glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <style>
    @keyframes rotateRing {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
    @keyframes reverseRotate {{ 0% {{ transform: rotate(360deg); }} 100% {{ transform: rotate(0deg); }} }}
    @keyframes pulseGlow {{ 0%, 100% {{ opacity: 0.7; transform: scale(1); }} 50% {{ opacity: 1; transform: scale(1.02); }} }}
    @keyframes drawLine {{ from {{ stroke-dashoffset: 400; }} to {{ stroke-dashoffset: 0; }} }}
    @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    
    .bg-rect {{ fill: #0a0f1d; rx: 15; ry: 15; stroke: url(#neon-border); stroke-width: 2; }}
    .glow-layer {{ animation: pulseGlow 4s ease-in-out infinite; transform-origin: center; }}
    
    .data-text {{ font-family: 'Segoe UI', sans-serif; font-size: 15px; font-weight: 600; fill: url(#text-grad); }}
    .title-text {{ font-family: 'Segoe UI', sans-serif; font-size: 19px; font-weight: 800; fill: #0ff; filter: url(#neon-glow); }}
    
    .ring {{ fill: none; stroke-width: 1.5; opacity: 0.6; transform-origin: 400px 100px; }}
    .ring1 {{ stroke: #0ff; stroke-dasharray: 4 4; animation: rotateRing 10s linear infinite; }}
    .ring2 {{ stroke: #f0f; stroke-dasharray: 8 4; animation: reverseRotate 15s linear infinite; }}
    
    .fade-in {{ opacity: 0; animation: fadeIn 0.8s ease-out forwards; }}
    .d1 {{ animation-delay: 0.3s; }} .d2 {{ animation-delay: 0.5s; }}
    
    .graph-line {{ fill: none; stroke: #0ff; stroke-width: 3; stroke-linejoin: round; stroke-linecap: round; filter: url(#neon-glow); stroke-dasharray: 400; stroke-dashoffset: 400; animation: drawLine 2s ease-out forwards; animation-delay: 0.8s; }}
    .graph-area {{ fill: url(#area-grad); opacity: 0; animation: fadeIn 1s ease-out forwards; animation-delay: 1.5s; }}
  </style>

  <!-- Glow and Background -->
  <rect class="glow-layer" fill="url(#hologram-glow)" x="10" y="10" width="480" height="230" rx="15" ry="15"/>
  <rect class="bg-rect" x="10" y="10" width="480" height="230" />

  <!-- Holographic Core -->
  <g>
    <circle class="ring ring1" cx="400" cy="100" r="50"/>
    <circle class="ring ring2" cx="400" cy="100" r="65"/>
    <text x="400" y="112" font-family="'Segoe UI', sans-serif" font-size="36" font-weight="bold" fill="#0ff" text-anchor="middle" filter="url(#neon-glow)">{username[0]}</text>
  </g>

  <!-- Text Stats -->
  <text x="35" y="45" class="title-text">HOLOGRAPHIC LIVE STATS</text>
  <g class="fade-in d1">
    <text x="35" y="80" class="data-text">⭐ Stars: <tspan fill="#f0f">{total_stars}</tspan></text>
    <text x="35" y="105" class="data-text">📦 Repos: <tspan fill="#f0f">{public_repos}</tspan></text>
  </g>
  <g class="fade-in d2">
    <text x="180" y="80" class="data-text">👥 Followers: <tspan fill="#f0f">{followers}</tspan></text>
    <text x="180" y="105" class="data-text">⏳ Active: <tspan fill="#f0f">{years_active} Yrs</tspan></text>
  </g>

  <!-- Live Animated Event Graph -->
  <g transform="translate(35, 160)">
    <polygon class="graph-area" points="{area_path}" />
    <polyline class="graph-line" points="{path_data}" />
    <!-- Graph Grid Lines -->
    <line x1="0" y1="60" x2="280" y2="60" stroke="#f0f" stroke-width="1" stroke-dasharray="2 2" opacity="0.3"/>
    <text x="290" y="65" font-family="'Segoe UI', sans-serif" font-size="10" fill="#0ff" opacity="0.6">TODAY</text>
    <text x="0" y="-10" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="bold" fill="#f0f" opacity="0.8">RECENT ACTIVITY MOMENTUM</text>
  </g>
</svg>
"""

with open("holographic-stats.svg", "w", encoding="utf-8") as f:
    f.write(svg_template)
