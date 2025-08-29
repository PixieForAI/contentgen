# Documentation: ContentGen Django Application

This document provides a technical overview of the `contentgen` web application. It is intended for developers and AI assistants to understand the architecture, data models, and core logic of the project.

## 1\. Project Overview 🎯

**ContentGen** is a web application built with Django that allows users to manage content creation campaigns. Users can register, create campaigns with specific objectives, and add detailed content items for various social media platforms under each campaign.

**Core Functionality:**

  * User authentication (Register, Login, Logout).
  * User profile management for organization details.
  * CRUD (Create, Read, Update, Delete) operations for Campaigns.
  * CRUD operations for Campaign Items nested under campaigns.
  * A dashboard with paginated and searchable lists of a user's campaigns.

-----

## 2\. Tech Stack 🛠️

  * **Backend:** Python 3.11+, Django 5.2
  * **Frontend:** HTML5, Tailwind CSS v3, Alpine.js (for minor interactivity)
  * **Database:** SQLite (for development), compatible with PostgreSQL for production.
  * **Python Packages:** `django-tailwind`, `Pillow`, `python-decouple`, `gunicorn`.
  * **Node.js Packages:** `tailwindcss`.

-----

## 3\. Project Structure 📁

The project is organized into a main configuration directory (`contentgen`) and distinct applications housed within an `apps/` directory to promote modularity and prevent naming conflicts.

```text
contentgen/
├── apps/
│   ├── campaigns/      # Core logic for campaigns and items.
│   └── users/          # Handles user auth and profiles.
├── contentgen/         # Main Django project configuration.
├── templates/          # Global templates (base.html, partials).
├── theme/              # Manages Tailwind CSS assets.
├── manage.py
├── requirements.txt
├── package.json
└── tailwind.config.js
```

-----

## 4\. Core Concepts & Data Models 💾

The application revolves around two primary concepts: Campaigns and Campaign Items, which are linked to a User's Profile.

### 4.1. User & Profile Models (`apps.users`)

  * **`User` (Django Built-in)**: Handles authentication (username, password, email).
  * **`Profile`**: A one-to-one extension of the `User` model to store application-specific data.
      * `user`: **OneToOneField** to `User`. The profile is automatically created via a Django signal when a new user registers.
      * `org_name`: `CharField`
      * `org_objectives`: `TextField`

### 4.2. Campaign & CampaignItem Models (`apps.campaigns`)

  * **`Campaign`**: The top-level container for a content strategy.

      * `user`: **ForeignKey** to `User`. Defines ownership.
      * `title`: `CharField`
      * `objectives`: `TextField`
      * `created_at`: `DateTimeField` (auto-set on creation).
      * `updated_at`: `DateTimeField` (auto-updated on save). This field is critical for sorting the user's dashboard.
      * **Default Ordering**: The model's `Meta` class orders all queries by `-updated_at` by default.

  * **`CampaignItem`**: A single piece of content within a `Campaign`.

      * `campaign`: **ForeignKey** to `Campaign`. Links the item to its parent campaign.
      * `title`: `CharField`
      * `input_content`: `TextField` for the base brief.
      * `*_content`: Multiple `TextField`s for different platforms (LinkedIn, X, Facebook, etc.).
      * `image_prompt`, `video_prompt`: `TextField`s.
      * `image`: `ImageField` for user image uploads.
      * `video`: `FileField` for user video uploads.
      * **Custom `save()` Logic**: The `save()` method is overridden to also trigger the parent `Campaign`'s `save()` method. This ensures that when an item is updated, the parent campaign's `updated_at` timestamp is also updated, causing it to "bubble up" to the top of the campaign list.

-----

## 5\. Application Breakdown 🧩

### 5.1. `users` App

**Responsibility**: Manages user registration, authentication, and profile editing.

  * **Views (`views.py`)**:
      * `RegisterView`: (`CreateView`) Handles new user sign-ups.
      * `CustomLoginView`: (`LoginView`) Handles user login.
      * `LogoutView`: (Django built-in) Handles user logout.
      * `ProfileUpdateView`: (`LoginRequiredMixin`, `UpdateView`) Allows a logged-in user to edit their own profile.
  * **URLs (`urls.py`)**: Prefixed with `/accounts/`. Provides routes for `login/`, `logout/`, `register/`, and `profile/`.

### 5.2. `campaigns` App

**Responsibility**: The core business logic of the application. Manages all CRUD operations for campaigns and their items.

  * **Views (`views.py`)**:
      * **`CampaignListView`**: (`LoginRequiredMixin`, `ListView`) The main user dashboard. It filters campaigns by the logged-in user, includes search logic (on title and objectives), and uses pagination.
      * **`CampaignDetailView`**: (`UserOwnsCampaignMixin`, `DetailView`) Displays a single campaign and lists all of its child `CampaignItem`s.
      * **`CampaignCreateView` / `CampaignUpdateView`**: (`CreateView`/`UpdateView`) Handle creating and editing campaigns. The create view automatically assigns the `request.user`.
      * **`CampaignItemCreateView` / `CampaignItemUpdateView`**: Handle creating and editing individual content items, ensuring they are linked to the correct parent campaign.
  * **Security**: All views use `LoginRequiredMixin`. Detail, Update, and Delete views use custom `UserOwns...Mixin` classes to ensure a user can only interact with their own data.
  * **URLs (`urls.py`)**: Mounted at the project root (`''`). Includes routes for the campaign list, detail, create, update, and delete, as well as nested routes for creating/editing items.

-----

## 6\. Frontend Setup 🎨

The frontend uses **Tailwind CSS**, managed by the `django-tailwind` package.

  * **`theme` App**: A dedicated Django app that serves as the home for frontend assets, as recommended by `django-tailwind`.
  * **Source File**: `theme/static/src/input.css`. This file contains the `@tailwind` directives.
  * **Output File**: `theme/static/css/dist/styles.css`. This is the compiled, production-ready CSS file that is generated by the Tailwind CLI. It is linked in `base.html`.
  * **Configuration**: `tailwind.config.js` is configured to scan all `.html` and `.py` files in the `templates/` and `apps/` directories to purge unused CSS classes.
  * **Templates**: The project uses a main `base.html` template with partials (e.g., `_navbar.html`, `_pagination.html`) for reusable components.
  * **Interactivity**: **Alpine.js** is included for simple, lightweight JavaScript interactivity, such as toggling the mobile navigation menu.

-----

## 7\. Setup & Running the Project 🚀

1.  **Clone the repository** and navigate into the project directory.
2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Install Node.js dependencies**:
    ```bash
    npm install
    ```
5.  **Create a `.env` file** in the root directory for environment variables:
    ```env
    SECRET_KEY='your-strong-secret-key'
    DEBUG=True
    ```
6.  **Run database migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
7.  **Create a superuser** to access the admin panel:
    ```bash
    python manage.py createsuperuser
    ```
8.  **Run the development servers**: Open two terminals.
      * **Terminal 1 (Tailwind Watcher)**:
        ```bash
        npm run watch
        ```
      * **Terminal 2 (Django Server)**:
        ```bash
        python manage.py runserver
        ```