import { supabase, isSupabaseConfigured } from "./supabaseClient";

const STORAGE_KEY_USER = "plantvision_user_session";
const STORAGE_KEY_ACCOUNTS = "plantvision_registered_accounts";

export const authService = {
  getCurrentUser() {
    const data = localStorage.getItem(STORAGE_KEY_USER);
    if (!data) return null;
    try {
      return JSON.parse(data);
    } catch {
      return null;
    }
  },

  async register(fullName, username, email, password) {
    const cleanEmail = email.trim().toLowerCase();
    const cleanUsername = username.trim().toLowerCase();

    // 1. SUPABASE AUTH
    if (isSupabaseConfigured() && supabase) {
      try {
        const { data, error } = await supabase.auth.signUp({
          email: cleanEmail,
          password: password,
          options: {
            data: {
              full_name: fullName.trim(),
              username: cleanUsername
            }
          }
        });

        if (error) {
          return { success: false, message: error.message };
        }

        const user = {
          id: data.user?.id || Date.now().toString(),
          fullName: fullName.trim(),
          username: cleanUsername,
          email: cleanEmail,
          createdAt: new Date().toISOString(),
          isSupabase: true
        };

        // Create profile in Supabase profiles table if available
        try {
          await supabase.from("profiles").upsert({
            id: user.id,
            full_name: user.fullName,
            username: user.username,
            updated_at: new Date().toISOString()
          });
        } catch (e) {
          console.warn("Profile table insert skipped:", e);
        }

        localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(user));
        return { success: true, user };
      } catch (err) {
        return { success: false, message: err.message };
      }
    }

    // 2. LOCAL STORAGE FALLBACK (If Supabase not yet configured)
    const users = JSON.parse(localStorage.getItem(STORAGE_KEY_ACCOUNTS) || "[]");
    if (users.find(u => u.username === cleanUsername)) {
      return { success: false, message: "Username is already taken." };
    }
    if (users.find(u => u.email === cleanEmail)) {
      return { success: false, message: "Email is already registered." };
    }

    const newUser = {
      id: Date.now().toString(),
      fullName: fullName.trim(),
      username: cleanUsername,
      email: cleanEmail,
      password: password,
      createdAt: new Date().toISOString(),
      isSupabase: false
    };

    users.push(newUser);
    localStorage.setItem(STORAGE_KEY_ACCOUNTS, JSON.stringify(users));

    const sessionUser = { ...newUser };
    delete sessionUser.password;
    localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(sessionUser));

    return { success: true, user: sessionUser };
  },

  async login(usernameOrEmail, password) {
    const cleanInput = usernameOrEmail.trim().toLowerCase();

    // 1. SUPABASE AUTH (By Email)
    if (isSupabaseConfigured() && supabase && cleanInput.includes("@")) {
      try {
        const { data, error } = await supabase.auth.signInWithPassword({
          email: cleanInput,
          password: password
        });

        if (error) {
          return { success: false, message: error.message };
        }

        const user = {
          id: data.user.id,
          fullName: data.user.user_metadata?.full_name || cleanInput.split("@")[0],
          username: data.user.user_metadata?.username || cleanInput.split("@")[0],
          email: data.user.email,
          isSupabase: true
        };

        localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(user));
        return { success: true, user };
      } catch (err) {
        return { success: false, message: err.message };
      }
    }

    // 2. LOCAL STORAGE FALLBACK
    const users = JSON.parse(localStorage.getItem(STORAGE_KEY_ACCOUNTS) || "[]");
    const found = users.find(
      u => (u.username === cleanInput || u.email === cleanInput) && u.password === password
    );

    if (!found) {
      return { success: false, message: "Invalid credentials. If using Supabase, please sign in with your email." };
    }

    const sessionUser = { ...found };
    delete sessionUser.password;
    localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(sessionUser));
    return { success: true, user: sessionUser };
  },

  guestLogin() {
    const guestUser = {
      id: "guest_farmer",
      fullName: "Guest Agronomist",
      username: "guest",
      email: "guest@plantvision.ai",
      isGuest: true,
      createdAt: new Date().toISOString()
    };
    localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(guestUser));
    return { success: true, user: guestUser };
  },

  async logout() {
    if (isSupabaseConfigured() && supabase) {
      try {
        await supabase.auth.signOut();
      } catch {}
    }
    localStorage.removeItem(STORAGE_KEY_USER);
  }
};
