
document.addEventListener("DOMContentLoaded", () => {

    // Formatter for currency (USD)
    const currencyFormat = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        maximumFractionDigits: 0,
    });

    // Fetch movie details
    fetch(`/api/v1/movie/${movieId}`)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("movie-detail");

            const poster = data.poster_path
                ? `<img src="https://image.tmdb.org/t/p/w500${data.poster_path}" alt="${data.title}" style="max-width: 300px; border-radius: 8px;">`
                : `<div>No Image</div>`;

            const genres = data.genres?.map(g => g.name).join(", ") || "N/A";
            const spokenLanguages = data.spoken_languages?.map(l => l.english_name).join(", ") || "N/A";
            const countries = data.production_countries?.map(c => c.name).join(", ") || "N/A";
            const homepage = data.homepage ? `<a href="${data.homepage}" target="_blank">${data.homepage}</a>` : "N/A";
            const imdb = data.imdb_id ? `<a href="https://www.imdb.com/title/${data.imdb_id}" target="_blank">${data.imdb_id}</a>` : "N/A";
            const budget = data.budget ? currencyFormat.format(data.budget) : "N/A";
            const revenue = data.revenue ? currencyFormat.format(data.revenue) : "N/A";

            container.innerHTML = `
                <h2>${data.title}</h2>
                ${poster}
                <p><strong>Status:</strong> ${data.status}</p>
                <p><strong>Release Date:</strong> ${data.release_date}</p>
                <p><strong>Genres:</strong> ${genres}</p>
                <p><strong>Overview:</strong> ${data.overview}</p>
                <p><strong>Rating:</strong> ⭐ ${Math.round(data.vote_average * 10)}% (${data.vote_count} votes)</p>
                <p><strong>Runtime:</strong> ${data.runtime} minutes</p>
                <p><strong>Budget:</strong> ${budget}</p>
                <p><strong>Revenue:</strong> ${revenue}</p>
                <p><strong>Homepage:</strong> ${homepage}</p>
                <p><strong>IMDb:</strong> ${imdb}</p>
                <p><strong>Original Language:</strong> ${data.original_language}</p>
                <p><strong>Spoken Languages:</strong> ${spokenLanguages}</p>
                <p><strong>Production Countries:</strong> ${countries}</p>
            `;
        });

    // Fetch movie credits
    fetch(`/api/v1/movie/${movieId}/credits`)
        .then(response => response.json())
        .then(data => {
            const cast = data.cast?.slice(0, 20) || [];
            const container = document.getElementById("credits-container");

            if (cast.length === 0) {
                container.innerHTML = "<p>No cast data available.</p>";
                return;
            }

            cast.forEach(person => {
                const profile = person.profile_path
                    ? `<img src="https://image.tmdb.org/t/p/w185${person.profile_path}" alt="${person.name}">`
                    : `<div style="width:100%;height:0;padding-bottom:100%;background:#ccc;border-radius:50%;"></div>`;

                const card = document.createElement("div");
                card.className = "credit-card";
                card.innerHTML = `
                    ${profile}
                    <strong>${person.name}</strong><br>
                    <span>${person.character || person.job || ''}</span>
                `;
                container.appendChild(card);
            });
        });

    // Fetch movie video
    fetch(`/api/v1/movie/${movieId}/videos`)
        .then(response => response.json())
        .then(data => {
            const trailer = data.find(
                v => v.type === "Trailer" && v.site === "YouTube"
            );

            if (trailer) {
                const trailerContainer = document.getElementById("trailer-container");
                const button = document.createElement("button");
                button.textContent = "▶ Play Trailer";
                button.style.margin = "1rem 0";
                button.onclick = () => {
                    const modal = document.getElementById("trailer-modal");
                    const iframe = document.getElementById("trailer-frame");
                    if (modal && iframe) {
                        modal.style.display = "flex";
                        iframe.src = `https://www.youtube.com/embed/${trailer.key}?autoplay=1`;
                    }
                };
                trailerContainer.appendChild(button);
            }
    });

    const closeBtn = document.getElementById("close-trailer");
    if (closeBtn) {
        closeBtn.onclick = () => {
            document.getElementById("trailer-modal").style.display = "none";
            document.getElementById("trailer-frame").src = ""; // Stop video
        };
    }
});
