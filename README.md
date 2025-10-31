# What To Eat — Django + HTMX App

A small Django app that lets you discover meals by category, search by name, view full recipe details (ingredients, instructions, video), and manage a simple favorites list — all with HTMX-powered interactivity, plain CSS, and a bit of vanilla JS.

---

## Routes & Views

### 1) Home (`/`)
- **View:** `index`  
  Loads meal categories from TheMealDB via `list_categories()`. Results are cached for 1 hour under the key `meal_categories`. A random category (if available) is also chosen and sent to the template.
- **Template:** `index.html`  
  Renders a `<select>` with all categories. HTMX automatically triggers a request on **page load** and **change** to fetch meals for the selected category (see `/load-meals/` below). Results are injected into `#results`.

### 2) Fetch meals for a category (`/load-meals/`)
- **View:** `load_meals`  
  Reads the `categories` query param, fetches meals with `filterByCategory(category)`, and renders a **partial** with `meals_partial.html`. It also reads a `favorites` list from the session, extracts `favorite_ids`, and passes them into the template so the partial can show “✓ Favorited” where appropriate.
- **Template (partial):** `meals_partial.html`  
  Displays each meal as a card with image, title, optional chips, and two actions:  
  * “View Recipe” — an HTMX button that loads the **details page** into the whole `<body>` via `hx-target="body"` and `hx-swap="outerHTML"`.  
  * “Add to Favorites” — a normal link to `/favorites/add/?meal_id=...` (or a disabled “✓ Favorited” if it’s already in the session).

### 3) Meal details (`/meal-details/`)
- **View:** `meal_details`  
  Expects `?meal=<name>`; if missing, redirects to the home page. Looks up meals by name via `searchByName`. If none found, returns 404. For the first matched meal, it:
  * Builds a list of **ingredients** by pairing `strIngredient1..20` with `strMeasure1..20`, skipping blanks.  
  * Parses `strYoutube` to extract a clean **YouTube video ID** (supports both `youtu.be` and `youtube.com/watch?v=` forms).  
  * Renders the data in `meal_detail.html`.

- **Template:** `meal_detail.html`  
  Shows:  
  * Meal title and ID  
  * Embedded YouTube video (or image fallback if no video)  
  * Category, area, and tags  
  * Full list of ingredients and measurements  
  * Instructions formatted with preserved line breaks  
  * A “Back to Categories” HTMX button.

### 4) Search (`/search/`)
- **View:** `search_meals`  
  Accepts `?q=<term>` and calls TheMealDB’s search API via `searchByName`. Renders `search_results.html` (partial).  
- **Template:** `search_results.html`  
  Displays a dynamic grid of found meals similar to category results.

### 5) Favorites (`/favorites/`)
- **Views:**  
  * `favorites` — renders all favorite meals saved in the session using `favorites.html`.  
  * `add_to_favorites` — adds a meal (by `meal_id`) to the session favorites list.  
  * `remove_from_favorites` — removes it from the session list.

- **Template:** `favorites.html`  
  Lists all favorites as clickable image cards that can be viewed or removed.

---

## Utilities (`utils.py`)
Contains helper functions that wrap TheMealDB public API:
- `list_categories()` → returns available meal categories.
- `filterByCategory(category)` → returns meals in that category.
- `searchByName(name)` → returns meals matching a name.
Each returns parsed JSON data ready to render.

---

## Templates Summary
| File | Purpose |
|------|----------|
| **base.html** | Shared HTML structure (header, container, script includes). |
| **index.html** | Home page with category dropdown and results section. |
| **meals_partial.html** | HTMX partial to show meals for a selected category. |
| **meal_detail.html** | Shows full meal recipe with embedded video and ingredients. |
| **favorites.html** | Lists favorite meals stored in session. |
| **search_results.html** | Displays search results when using autocomplete. |
| **autocomplete_results.html** | Partial used for live search suggestions. |

---

## How It Works (Flow)
1. User opens the home page. HTMX immediately loads the default category.  
2. Selecting a category triggers an HTMX GET to `/load-meals/`.  
3. Clicking a meal image loads `/meal-details/?meal=<name>` via HTMX, replacing `<body>`.  
4. The detail page shows the video, ingredients, and instructions.  
5. User can favorite meals, view favorites, or search meals by name (autocomplete).

---

## Tech Stack
- **Backend:** Django (Python)
- **Frontend:** HTMX + Vanilla JS + CSS
- **Data Source:** [TheMealDB API](https://www.themealdb.com/api.php)
- **Caching:** Django’s cache for categories
- **Session storage:** Browser session for favorites

---

## Running the Project
```bash
python manage.py runserver
```
Then visit [http://localhost:8000](http://localhost:8000).