document.addEventListener("DOMContentLoaded", () => {
    const currencyFormat = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        maximumFractionDigits: 0,
    });

    // Fetch TV show details
    fetch(`/api/v1/tv/${tvId}`)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("tv-detail");

            const poster = data.poster_path
                ? `<img src="https://image.tmdb.org/t/p/w500${data.poster_path}" alt="${data.name}" style="max-width: 300px; border-radius: 8px;">`
                : `<div>No Image</div>`;

            const genres = data.genres?.map(g => g.name).join(", ") || "N/A";
            const spokenLanguages = data.spoken_languages?.map(l => l.english_name).join(", ") || "N/A";
            const countries = data.origin_country?.join(", ") || "N/A";
            const homepage = data.homepage ? `<a href="${data.homepage}" target="_blank">${data.homepage}</a>` : "N/A";

            container.innerHTML = `
                <h2>${data.name}</h2>
                ${poster}
                <p><strong>Status:</strong> ${data.status}</p>
                <p><strong>First Air Date:</strong> ${data.first_air_date}</p>
                <p><strong>Genres:</strong> ${genres}</p>
                <p><strong>Overview:</strong> ${data.overview}</p>
                <p><strong>Rating:</strong> ⭐ ${Math.round(data.vote_average * 10)}% (${data.vote_count} votes)</p>
                <p><strong>Homepage:</strong> ${homepage}</p>
                <p><strong>Original Language:</strong> ${data.original_language}</p>
                <p><strong>Spoken Languages:</strong> ${spokenLanguages}</p>
                <p><strong>Origin Country:</strong> ${countries}</p>
            `;
        });

    // Fetch TV credits
    fetch(`/api/v1/tv/${tvId}/credits`)
        .then(response => response.json())
        .then(data => {
            const cast = data.cast?.slice(0, 20) || [];
            const container = document.getElementById("tv-credits-container");

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
});
