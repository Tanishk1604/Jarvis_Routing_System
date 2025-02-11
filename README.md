# Jarvis Routing System

## Overview

The *Jarvis Routing System* is an advanced Dynamic Route Optimization System designed to address key challenges in logistics and transportation. By leveraging real-time data from multiple APIs, the system optimizes delivery routes, estimates vehicle emissions, and promotes environmentally conscious decision-making. With a focus on efficiency and scalability, it offers actionable insights to reduce costs and emissions, supporting both small and large-scale logistics operations.

## Features


- *Dynamic Route Optimization :* Generates optimized routes based on real-time traffic, distance, and user preferences.
- *Real-Time Traffic Data :* Displays live traffic updates and incidents along the route to ensure efficiency.
- *Weather Integration :* Incorporates real-time weather data from the OpenWeatherMap API for enhanced route planning during disruptions.
- *CO₂ Emission Calculations :* Provides detailed CO₂ emission estimates for selected routes based on vehicle type and fuel efficiency.
- *Air Quality Insights :* Offers AQI data for both the origin and destination to aid eco-friendly decision-making.
- *Interactive and User-Friendly Interface :* Intuitive web interface with an interactive map for seamless navigation and route selection.
- *Scalability :* Designed to handle complex operations, including large fleets and multi-destination routing (planned as a future enhancement)

## Technologies Used

- *Backend*: Flask
- *Frontend*: HTML, CSS , JS
- *Python*: For core logic, API integrations, and emissions calculations.
  
 
## APIs Used

- Google Maps API: For route generation and distance calculations.
- TomTom API: For real-time traffic incident data.
- AQICN API: For air quality data.
- OSRM: For alternative route optimization (future integration).
- OpenWeatherMap API: For live weather data integration to improve route planning.


## Project Structure


├── templates/  
│       ├── base.html        # Base template for UI structure  
│       ├── index.html       # Home page with user input form  
│       ├── result.html      # Results page with route, emissions, and weather data  
│       ├── map.html         # Interactive map display for route visualization  
│       ├── about.html       # About page providing details on the project and team  
│       ├── contact.html     # Contact page for user queries or feedback  
├── static/  
│       ├── style.css        # Stylesheet for the project  
├── app.py               # Main application file containing logic and API integrations  
├── README.md            # Project documentation  


*Follow this Structure to run this project*

## Screenshots 


- ![Screenshot 2025-01-23 203803](https://github.com/user-attachments/assets/e3bed5a1-de83-44d1-b017-d6d2659a6d01)
- ![Screenshot 2025-01-23 203836](https://github.com/user-attachments/assets/e698ac57-00e2-4712-a374-dd6b4c858f26)
- ![Screenshot 2025-01-23 203859](https://github.com/user-attachments/assets/886c8c39-7d4a-4e8c-a7cc-9eceef274f0a)
- ![Screenshot 2025-01-23 203916](https://github.com/user-attachments/assets/1274bc82-d8dd-42ca-bbe7-e4eddfd9f6b4)
- ![Screenshot 2025-01-23 203954](https://github.com/user-attachments/assets/9585d77a-9fa8-4a3d-bfa8-d47a060e48a0)
