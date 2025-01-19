interface ImportMetaEnv {
  VITE_API_URL: string;
  // Add other env variables here
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
