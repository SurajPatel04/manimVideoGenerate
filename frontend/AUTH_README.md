# Authentication System

This project includes a complete authentication system with signup and login functionality.

## Features

- 🔐 **Toggle between Login and Signup** - Switch between forms with a single click
- 👁️ **Password visibility toggle** - Show/hide password fields
- ✅ **Form validation** - Client-side validation for all fields
- 🎨 **Beautiful UI** - Modern design with background animations
- 💾 **State persistence** - User session persists across browser refreshes
- 📱 **Responsive design** - Works on all screen sizes
- 🌙 **Dark mode support** - Automatic dark/light theme switching

## Usage

### Running the Application

```bash
cd frontend
npm install
npm run dev
```

The application will be available at `http://localhost:5173`

### Authentication Flow

1. **Signup Process:**
   - Fill in first name, last name, email, and password
   - Confirm password (must match)
   - Click "Sign Up" button
   - Upon successful signup, you'll be redirected to the dashboard

2. **Login Process:**
   - Enter your email and password
   - Optionally check "Remember me"
   - Click "Sign In" button
   - Upon successful login, you'll be redirected to the dashboard

3. **Switching Forms:**
   - Click the "Sign in" link at the bottom to switch from signup to login
   - Click the "Sign up" link at the bottom to switch from login to signup

4. **Dashboard:**
   - View your profile information
   - Access quick actions
   - Sign out when done

### Component Structure

```
src/
├── components/
│   ├── AuthForm.tsx          # Main authentication form with toggle
│   ├── Dashboard.tsx         # User dashboard after login
│   └── ui/                   # Reusable UI components
├── contexts/
│   └── AuthContext.tsx       # Authentication state management
└── App.tsx                   # Main app component
```

### Key Components

- **AuthForm**: Handles both signup and login with form switching
- **Dashboard**: Shows user information and logout functionality
- **AuthContext**: Manages authentication state globally
- **Background Beams**: Animated background component

### Social Login

The form includes buttons for:
- GitHub authentication
- Google authentication

*Note: These are currently placeholders. To implement actual OAuth, you would need to integrate with your chosen authentication provider.*

### Customization

You can easily customize:
- Form fields and validation
- Styling and themes
- Authentication providers
- API endpoints (currently using mock data)

### Security Features

- Password visibility toggle
- Form validation
- Session persistence
- Secure password handling (ready for backend integration)

## Backend Integration

To connect this to a real backend:

1. Update the `login` and `signup` functions in `AuthContext.tsx`
2. Replace mock API calls with actual HTTP requests
3. Handle JWT tokens or session cookies
4. Add proper error handling for network requests

Example API integration:

```typescript
const login = async (email: string, password: string) => {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  
  if (response.ok) {
    const user = await response.json();
    setUser(user);
    return true;
  }
  return false;
};
```

## Technologies Used

- **React 19** with TypeScript
- **Tailwind CSS** for styling
- **Vite** for build tooling
- **Radix UI** for accessible components
- **Tabler Icons** for iconography
- **Motion** for animations
