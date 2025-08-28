# API-Driven Mini Web App

A full-stack web application to search external APIs (GitHub & OpenWeather), store results, and display them on a dashboard with timestamps in both UTC and IST. Built with **React** (frontend) and **Flask** (backend), deployed on **Vercel** (frontend) and **Render** (backend).

## Live Demo

- Frontend: [https://api-web-app-sandy.vercel.app/](https://api-web-app-sandy.vercel.app/)  
- Backend: *(Render deployment)*

---

## Features

- Search GitHub repositories or OpenWeather cities directly from the dashboard.
- Store search results in PostgreSQL with timestamps (UTC + IST).
- Display results in a clean, responsive dashboard.
- Supports pagination for stored results.
- RESTful API endpoints for frontend consumption.
- Handles API errors gracefully and logs them for debugging.

---

## Tech Stack

- **Frontend:** React, Axios, HTML/CSS  
- **Backend:** Python, Flask, Flask-Migrate, SQLAlchemy  
- **Database:** PostgreSQL  
- **Deployment:** Vercel (frontend), Render (backend)  
- **Other Tools:** GitHub Actions for CI/CD, dotenv for environment variables

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/vin2075/API-web-app.git
cd API-web-app
