
document.addEventListener("DOMContentLoaded", () => {

    // Fetch TV show details
    fetch(`/api/v1/tv/${tvId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("tv-title").textContent = data.name;
            const infoContainer = document.getElementById("tv-info-container");

            const poster = data.poster_path
                ? `<img src="https://image.tmdb.org/t/p/w500${data.poster_path}" alt="${data.name}" style="max-width: 300px; border-radius: 8px;">`
                : `<div>No Image</div>`;

            const genres = data.genres?.map(g => g.name).join(", ") || "N/A";
            const countries = data.origin_country?.join(", ") || "N/A";
            const homepage = data.homepage ? `<a href="${data.homepage}" target="_blank">${data.homepage}</a>` : "N/A";

            const networks = data.networks?.map(n => {
                const logo = n.logo_path ? `<img src="https://image.tmdb.org/t/p/w92${n.logo_path}" alt="${n.name}" style="height: 20px;">` : n.name;
                return `<div style="display: flex; align-items: center; gap: 0.5rem;">${logo}<span>${n.name}</span></div>`;
            }).join("") || "N/A";

            const seasonsHTML = data.seasons?.map(season => {
                const seasonPoster = season.poster_path
                    ? `<img src="https://image.tmdb.org/t/p/w185${season.poster_path}" alt="${season.name}" class="season-poster">`
                    : `<div class="season-poster-placeholder"></div>`;

                return `
                    <div class="season-card">
                        ${seasonPoster}
                        <div>
                            <h4>${season.name}</h4>
                            <p><strong>Air Date:</strong> ${season.air_date || 'N/A'}</p>
                            <p><strong>Episodes:</strong> ${season.episode_count}</p>
                            <p>${season.overview || ''}</p>
                        </div>
                    </div>
                `;
            }).join("") || "<p>No seasons info available.</p>";

            infoContainer.innerHTML = `
                ${poster}
                <p><strong>Status:</strong> ${data.status}</p>
                <p><strong>First Air Date:</strong> ${data.first_air_date}</p>
                <p><strong>Genres:</strong> ${genres}</p>
                <p><strong>Overview:</strong> ${data.overview}</p>
                <p><strong>Seasons:</strong> ${data.number_of_seasons}, <strong>Total Episodes:</strong> ${data.number_of_episodes}</p>
                <p><strong>Rating:</strong> ⭐ ${Math.round(data.vote_average * 10)}% (${data.vote_count} votes)</p>
                <p><strong>Original Language:</strong> ${data.original_language}</p>
                <p><strong>Networks:</strong><br/> ${networks}</p>
                <p><strong>Homepage:</strong> ${homepage}</p>
                <p><strong>Origin Country:</strong> ${countries}</p>
                <hr/>
                <h3>Seasons</h3>
                ${seasonsHTML}
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

    ////////////////////////////////////////

    const favoriteList = new Set();
    const media_type = "tv";
    const favoriteKey = `${media_type}:${tvId}`;

    const heartEl = document.getElementById("favorite-heart");

    fetch('/api/v1/favorites')
        .then(res => res.json())
        .then(favs => {
            favs.forEach(f => favoriteList.add(`${f.media_type}:${f.tmdb_id}`));
            updateHeartIcon();
        });

    function updateHeartIcon() {
        heartEl.textContent = favoriteList.has(favoriteKey) ? "❤️" : "🤍";
    }

    heartEl.addEventListener("click", () => {
        const isFavorite = favoriteList.has(favoriteKey);

        fetch("/api/v1/favorites", {
            method: isFavorite ? "DELETE" : "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ tmdb_id: tvId, media_type })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                if (isFavorite) favoriteList.delete(favoriteKey);
                else favoriteList.add(favoriteKey);
                updateHeartIcon();
            }
        });
    });

});
