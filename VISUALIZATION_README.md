# 🎭 Curb Your Enthusiasm Episodes - Interactive Visualization

An interactive web-based visualization of all 120 episodes of Curb Your Enthusiasm, showing ratings across all 12 seasons with unique shapes per season and rating-based color coding. Features dual view modes for analyzing individual episodes or season averages.

## 🚀 Quick Start

### Option 1: Using Python Server (Recommended)
```bash
python3 start_server.py
```
This will automatically:
- Start a local web server on port 8000
- Open the visualization in your browser
- Load all episode data from the CSV file

### Option 2: Direct File Opening
Simply open `curb_episodes_visualization.html` in your browser (note: may have CORS issues loading the CSV).

## 📊 Features

### Interactive Chart
- **Scatter Plot**: Each shape represents an episode positioned by season (x-axis) and rating (y-axis)
- **Season Grouping**: Episodes are grouped by season with slight horizontal jittering to avoid overlap
- **Unique Shapes**: Each season has a distinct shape (circle, square, triangle, diamond, pentagon, hexagon, star, heart, cross, arrow, oval, octagon)
- **Rating-Based Colors**: Colors represent episode ratings (red = low, yellow = medium, green = high)
- **Hover Tooltips**: Click on any episode to see:
  - Episode title and season/episode number
  - Rating and vote count
  - Director name
  - Air date
  - Shape type

### Season Filtering
- **One-Click Toggle Buttons**: Click season buttons to show/hide specific seasons
- **Shape Icons**: Each filter button shows the actual shape used in the visualization
- **Blue Button Design**: Consistent blue styling that doesn't interfere with rating colors
- **Select All/Deselect All**: One-click button to toggle all seasons
- **Real-time Updates**: Chart updates instantly when filters change

### Episode/Season View Toggle
- **Dual View Modes**: Switch between individual episodes and season averages
- **Episode Mode**: Shows all 120 individual episodes with ratings spread across each season
- **Season Average Mode**: Shows one data point per season representing the average rating
- **Larger Points**: Season averages display with larger shapes for better visibility
- **Dynamic Statistics**: Stats panel updates to show either episode or season-level data

### Live Statistics
- **Total Episodes**: Count of currently visible episodes
- **Average Rating**: Mean rating of visible episodes
- **Highest Rated**: Best episode currently visible
- **Lowest Rated**: Worst episode currently visible

### Visual Encoding System
- **Shapes by Season**: 
  - Season 1: Circle ○
  - Season 2: Square ■
  - Season 3: Triangle △
  - Season 4: Diamond ◆
  - Season 5: Pentagon ⬟
  - Season 6: Hexagon ⬢
  - Season 7: Star ★
  - Season 8: Heart ♥
  - Season 9: Cross ✚
  - Season 10: Arrow ↑
  - Season 11: Oval ⬭
  - Season 12: Octagon ⬣
- **Colors by Rating**: Red (7.0) → Yellow (8.25) → Green (9.5)

## 🎨 Visual Design

- **Modern UI**: Clean, professional interface with responsive design
- **Dual Visual System**: Shapes identify seasons, colors indicate ratings
- **Shape-Based Rating Scale**: Visual legend using actual season shapes to demonstrate color progression
- **Clean Interface**: Removed redundant chart legend to reduce clutter
- **Accessible**: High contrast shapes and clear typography
- **Mobile-Friendly**: Responsive layout that works on all devices

## 📈 What You Can Discover

- **Season Comparisons**: Easily compare overall performance between seasons with grouped visualization
- **Season Consistency**: See how ratings are distributed within each season using color intensity
- **Rating Patterns**: Identify high-rated episodes (green) vs lower-rated episodes (red/yellow)
- **Shape Recognition**: Quickly identify episodes from specific seasons by their unique shapes
- **Outliers**: Spot exceptional episodes that stand out from their season's typical performance
- **Director Impact**: Hover over shapes to see director information
- **Evolution**: Track how the show's quality changed over 12 seasons with clear season separation and rating colors

## 🔧 Technical Details

- **Framework**: Vanilla JavaScript with Chart.js for visualization
- **Data Source**: `curb_episodes_with_credits.csv` (120 episodes)
- **Libraries**: 
  - Chart.js for interactive charts
  - Papa Parse for CSV parsing
- **No Dependencies**: Everything runs in the browser

## 📱 Usage Tips

1. **Start with all seasons** to see the complete picture
2. **Toggle view mode** - Use the "Show Season Averages" switch to compare overall season performance
3. **Click blue filter buttons** to toggle specific seasons on/off
4. **Use "Select All/Deselect All"** for quick bulk toggling
5. **Hover over shapes** to get detailed episode/season information
6. **Watch the statistics** update as you change filters and view modes
7. **Use the color legend** to interpret rating levels (red = low, green = high)
8. **Look for patterns** - do later seasons rate higher? Which seasons are most consistent?
9. **Identify seasons by shape** - each season has a unique geometric shape

## 🎯 Perfect For

- **Data Analysis**: Compare episode performance across seasons
- **Fan Discussions**: Reference specific episodes and their ratings
- **Pattern Recognition**: Identify trends in the show's quality
- **Research**: Academic or journalistic analysis of the series

---

**Data Source**: IMDB ratings for all 120 episodes across 12 seasons (2000-2024)
**Last Updated**: Based on episode data scraped from IMDB 