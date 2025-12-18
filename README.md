# Tennis Nerds League

A robust full-stack solution designed to automate the management of competitive tennis "box leagues." This project handles dynamic player assignments, automated scoring logic, and real-time standings calculation using a relational database backend.

The application is deployed and can be viewed here: [www.tennisnerds.org ](https://www.tennisnerds.org/)

## System Architecture

The application follows a modular architecture, separating data persistence from the presentation layer to ensure scalability and maintainability.

### Front-End Development

- _User Interface:_ A responsive web interface designed for mobile-first score and data visualization.
- _Dynamic Templating:_ Utilizes Python-based rendering (like Jinja2) to dynamically inject SQL View data into the UI, ensuring real-time leaderboard updates.

### Back-End & Database

- _Data Processing:_ Python scripts manage the business logic for HTML Reports.
- _Relational Schema:_ A normalized Microsoft SQL Server backend with optimized Views for analytical reporting.

## Database Design & Logic

The core of this project is a highly normalized MS SQL database designed for data integrity.

- _Complex View Logic:_ Utilizes Common Table Expressions (CTEs) and Window Functions (ROW*NUMBER() OVER) to calculate real-time rankings within isolated \_Boxes*
- _Automated Metrics:_ The active_hours_summary view calculates player engagement by aggregating time spent in social sessions (150m/session) vs. formal matches (120m/match).
- _Constraints:_ Strict use of FOREIGN KEY and UNIQUE constraints to prevent logical errors, such as duplicate player assignments in a single round.

## Repository Structure

While the live site is the primary interface, this repository contains the core logic:

- _/docs/schema.sql:_ The complete blueprint used to initialize the production database.
- _/_.py:\* Python logic for processing league data and generating reports.
