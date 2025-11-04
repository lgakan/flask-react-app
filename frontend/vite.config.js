import path from 'path'
 import { defineConfig } from 'vite'
 import react from '@vitejs/plugin-react'

 // https://vitejs.dev/config/
 export default defineConfig({
     plugins: [react()],
     plugins: [react()],
     resolve: {
         alias: {
             'react': path.resolve(__dirname, './node_modules/react')
         }
     }
 })