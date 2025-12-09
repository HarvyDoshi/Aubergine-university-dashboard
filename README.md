# University Search Dashboard 

A full-stack web application that allows users to search for universities worldwide, filter by state/province, view analytics, and download university details as JPEG cards.

[cite_start]This project was built as part of the **Practical Test - Placement 2026** assignment[cite: 1].

##  Features Implemented

### [cite_start]Level 1: Database Ingestion [cite: 8-11]
* Automatically fetches data from the [University Domains List API](https://github.com/Hipo/university-domains-list).
* Stores data efficiently in a **SQLite** database (`university.db`).
* Prevents duplicate data entry and supports data refreshing.

### [cite_start]Level 2: Basic Search Functionality [cite: 12-18]
* **Search by Country:** Users can input a country name (e.g., "India", "Turkey") to filter universities.
* **University Cards:** Displays results in a grid layout with the university name and country.
* **Website Links:** Each card includes a direct link to the university's official website.

### [cite_start]Level 3: Enhanced Search with Province Filtering [cite: 19-26]
* **Dynamic Dropdown:** After entering a country, a dropdown automatically populates with available states/provinces for that country.
* **Refined Filtering:** Selecting a state updates the grid to show only universities from that specific region.

### [cite_start]Level 4: Download as JPEG [cite: 27-32]
* **One-Click Download:** Each university card has a download button (⬇️).
* **Image Generation:** Uses `html2canvas` to generate a high-quality JPEG image of the card containing the university name, location, and website indicator.

### Bonus Features (Analytics)
* **Dashboard Stats:** A "Stats" modal (📊) that displays:
    * Total number of universities in the database.
    * Total number of unique countries.
    * A bar chart showing the top 5 countries by number of universities.

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask, SQLAlchemy
* **Database:** SQLite (Auto-generated)
* **Frontend:** HTML5, Tailwind CSS (for styling)
* **Tools:** `html2canvas` (for image generation), `requests` (for API ingestion)

---

## 📸 Snapshots

[cite_start]*(As required by Level 1 Task: "Add snapshots of your Data visualized in any UI handle into the backend github repo" [cite: 11])*

### 1. Dashboard Overview & Country Search
![Dashboard Screenshot](https://via.placeholder.com/800x400?text=Upload+Your+Dashboard+Screenshot+Here)

### 2. State/Province Filtering
![Filter Screenshot](https://via.placeholder.com/800x400?text=Upload+Filter+Screenshot+Here)

### 3. Downloaded University Card (JPEG)
![Card Screenshot](https://via.placeholder.com/300x200?text=Upload+Card+JPEG+Here)

---

## ⚙️ Setup & Installation

Follow these steps to run the project locally.

### 1. Clone the Repository
```bash
git clone <YOUR_REPOSITORY_URL>
cd university-dashboard
2. Install DependenciesMake sure you have Python installed. Then run:Bashpip install -r requirements.txt
3. Run the ApplicationBashpython app.py
4. Access the DashboardOpen your web browser and go to:http://127.0.0.1:9090Note: The first time you search, the application will take a few seconds to download the dataset and build the local database.📡 API EndpointsThe backend provides the following JSON endpoints:EndpointMethodDescription/searchGETSearch universities by name, country, or state-province./provincesGETReturns a list of states for a specific country./statsGETReturns global analytics (total count, top countries)./updateGETForces a refresh of the dataset from the remote source.📄 LicenseData provided by Hipo/university-domains-list.Project structure based on "Practical Test - Placement 2026" requirements.
### **Instructions to finish:**
1.  **Take Screenshots:** Run your app, take screenshots of the dashboard and a downloaded card.
2.  **Upload Images:** Upload these images to your GitHub repository (you can drag and drop them into an "images" folder on GitHub or upload them in an issue comment to get a URL).
3.  **Update Links:** Replace the `https://via.placeholder.com...` links in the README above
