/**
 * Tailwind CSS v3 configuration — Bouchonnage IA dashboard.
 *
 * content: liste explicite des apps Django pour éviter le scan de node_modules.
 * JS scanning inclus pour les classes injectées dynamiquement dans gauges.js.
 */

const path = require('path');

module.exports = {
    content: [
        /* Templates du theme app */
        path.resolve(__dirname, '../templates/**/*.html'),

        /* Templates des apps Django — chemins explicites */
        path.resolve(__dirname, '../../dashboard/templates/**/*.html'),
        path.resolve(__dirname, '../../api/templates/**/*.html'),
        path.resolve(__dirname, '../../machine/templates/**/*.html'),
        path.resolve(__dirname, '../../maintenance/templates/**/*.html'),
        path.resolve(__dirname, '../../simulation/templates/**/*.html'),
        path.resolve(__dirname, '../../predictive/templates/**/*.html'),
        path.resolve(__dirname, '../../ml/templates/**/*.html'),

        /* Fichiers JS qui injectent des classes Tailwind dynamiquement */
        path.resolve(__dirname, '../../dashboard/static/js/**/*.js'),
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
