import { defineConfig, searchForWorkspaceRoot } from 'vite';
import react from '@vitejs/plugin-react';

// GitHub Pages project sites are served from /<repository-name>/.
// Set VITE_BASE_PATH to /your-repository-name/ in the Pages workflow.
export default defineConfig(
    {
        plugins: [react()],
        base: process.env.VITE_BASE_PATH || '/',
        server: {
            fs: {
            allow: [
                // Keep Vite's default workspace root detection
                searchForWorkspaceRoot(process.cwd()),
                // Allow access to a specific folder outside the root
                `process.cwd()/..`,
            ],
            },
        },
    }
);
