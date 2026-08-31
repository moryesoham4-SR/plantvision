import { createClient } from "@supabase/supabase-js";

// Retrieve keys from environment or localStorage runtime settings
const envUrl = import.meta.env.VITE_SUPABASE_URL;
const envKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

const localConfig = JSON.parse(localStorage.getItem("plantvision_supabase_config") || "{}");

export const SUPABASE_URL = localConfig.supabaseUrl || envUrl || "";
export const SUPABASE_ANON_KEY = localConfig.supabaseAnonKey || envKey || "";

export const isSupabaseConfigured = () => {
  return Boolean(SUPABASE_URL && SUPABASE_ANON_KEY && !SUPABASE_URL.includes("your-project-url"));
};

export const supabase = isSupabaseConfigured()
  ? createClient(SUPABASE_URL, SUPABASE_ANON_KEY)
  : null;

