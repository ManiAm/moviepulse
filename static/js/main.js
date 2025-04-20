
function debounce(fn, delay) {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => fn(...args), delay);
    };
}

const favoriteList = new Set();

function loadFavorites() {
    fetch('/api/v1/favorites')
        .then(res => res.json())
        .then(favs => {
            favs.forEach(f => {
                favoriteList.add(`${f.media_type}:${f.tmdb_id}`);
                const card = document.querySelector(`.movie-card[data-id="${f.tmdb_id}"][data-type="${f.media_type}"]`);
                if (card) card.querySelector(".favorite-heart").textContent = "❤️";
            });
        });
}

// clicking on the heart
function toggleFavorite(el) {
    const card = el.closest(".movie-card");
    const tmdb_id = card.dataset.id;
    const media_type = card.dataset.type;
    const key = `${media_type}:${tmdb_id}`;

    const isFavorite = favoriteList.has(key);

    fetch('/api/v1/favorites', {
        method: isFavorite ? 'DELETE' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tmdb_id, media_type })
    }).then(() => {
        if (isFavorite) {
            favoriteList.delete(key);
            el.textContent = "🤍";
        } else {
            favoriteList.add(key);
            el.textContent = "❤️";
        }
    });
}


document.addEventListener("DOMContentLoaded", () => {

    // Restore scroll position and highlight clicked card
    const savedScroll = sessionStorage.getItem("scrollPosition");
    const restoreToTop = sessionStorage.getItem("restoreToTop");
    
    if (savedScroll !== null && restoreToTop === "false") {
        window.scrollTo(0, parseInt(savedScroll));
        sessionStorage.removeItem("scrollPosition");
        sessionStorage.removeItem("restoreToTop");
    }    

    const clickedCardId = sessionStorage.getItem("clickedCardId");

    if (clickedCardId) {
        const clickedCard = document.getElementById(clickedCardId);
        if (clickedCard) {
            clickedCard.classList.add("highlighted-card");
        }
        sessionStorage.removeItem("clickedCardId");
    }

    //////////////////////////////////////////////////////////////

    document.getElementById("search-input").addEventListener("input", debounce(async (e) => {
        const query = e.target.value.trim();
        const resultsContainer = document.getElementById("search-results");
        resultsContainer.innerHTML = ""; // Clear previous
    
        if (query.length < 2) return;
    
        const response = await fetch(`/api/v1/search?query=${encodeURIComponent(query)}`);
        const data = await response.json();
    
        data
            .filter(item => item.media_type !== "person")
            .forEach(item => {
            if (!item.poster_path && !item.profile_path) return;
    
            const card = document.createElement("div");
            card.className = "movie-card";

            const image = item.poster_path || item.profile_path;
            const title = item.title || item.name;
            const type = item.media_type;
    
            card.id = `search-${item.id}`;
            card.setAttribute("data-id", item.id);
            card.setAttribute("data-type", type);

            const poster = `<img src="https://image.tmdb.org/t/p/w500${image}" alt="${title}">`;
    
            let href = "#";
            if (type === "movie") href = `/movie/${item.id}`;
            else if (type === "tv") href = `/tv/${item.id}`;
    
            card.innerHTML = `
                <span class="favorite-heart" onclick="toggleFavorite(this)">🤍</span>
                <a href="${href}" style="text-decoration: none; color: inherit;">
                    ${poster}
                    <h3>${title}</h3>
                    <p>Type: ${type}</p>
                </a>
            `;
    
            // Scroll memory
            card.addEventListener("click", () => {
                sessionStorage.setItem("scrollPosition", window.scrollY);
                sessionStorage.setItem("clickedCardId", `search-${item.id}`);
            });
    
            resultsContainer.appendChild(card);
        });

        loadFavorites();

    }, 400)); // debounce to avoid API spamming

    //////////////////////////////////////////////////////////////

    fetch("/api/v1/trending/movies")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("movies-container");

            data.forEach(movie => {
                const card = document.createElement("div");
                card.className = "movie-card";
                card.id = `movie-${movie.id}`;
                card.setAttribute("data-id", movie.id);
                card.setAttribute("data-type", "movie");

                const poster = movie.poster_path 
                    ? `<img src="https://image.tmdb.org/t/p/w500${movie.poster_path}" alt="${movie.title}">`
                    : `<div>No Image</div>`;

                card.innerHTML = `
                <span class="favorite-heart" onclick="toggleFavorite(this)">🤍</span>
                <a href="/movie/${movie.id}" style="text-decoration: none; color: inherit;">
                    ${poster}
                    <h3>${movie.title}</h3>
                    <p>${movie.release_date}</p>
                    <p>⭐ ${Math.round(movie.vote_average * 10)}%</p>
                </a>
                `;

                // Save scroll position before navigating
                card.addEventListener("click", () => {
                    sessionStorage.setItem("scrollPosition", window.scrollY);
                    sessionStorage.setItem("clickedCardId", `movie-${movie.id}`);
                });

                container.appendChild(card);
            });
        })
        .catch(err => {
            console.error("Failed to fetch trending movies", err);
        });

    // Trending TV Shows
    fetch("/api/v1/trending/tv")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("tv-container");

            data.forEach(tv => {
                const card = document.createElement("div");
                card.className = "movie-card";
                card.id = `tv-${tv.id}`;
                card.setAttribute("data-id", tv.id);
                card.setAttribute("data-type", "tv");

                const poster = tv.poster_path
                    ? `<img src="https://image.tmdb.org/t/p/w500${tv.poster_path}" alt="${tv.name}">`
                    : `<div>No Image</div>`;

                card.innerHTML = `
                    <span class="favorite-heart" onclick="toggleFavorite(this)">🤍</span>
                    <a href="/tv/${tv.id}" style="text-decoration: none; color: inherit;">
                        ${poster}
                        <h3>${tv.name}</h3>
                        <p>${tv.first_air_date}</p>
                        <p>⭐ ${Math.round(tv.vote_average * 10)}%</p>
                    </a>
                `;                

                card.addEventListener("click", () => {
                    sessionStorage.setItem("scrollPosition", window.scrollY);
                    sessionStorage.setItem("clickedCardId", `tv-${tv.id}`);
                });

                container.appendChild(card);
            });
        });

    //////////////////////////////////////////////////////////////

    fetch("/api/v1/discover/upcoming")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("movies-upcoming");

            data.forEach(movie => {
                const card = document.createElement("div");
                card.className = "movie-card";
                card.id = `movie-upcoming-${movie.id}`;
                card.setAttribute("data-id", movie.id);
                card.setAttribute("data-type", "movie");

                const poster = movie.poster_path 
                    ? `<img src="https://image.tmdb.org/t/p/w500${movie.poster_path}" alt="${movie.title}">`
                    : `<div>No Image</div>`;

                card.innerHTML = `
                <span class="favorite-heart" onclick="toggleFavorite(this)">🤍</span>
                <a href="/movie/${movie.id}" style="text-decoration: none; color: inherit;">
                    ${poster}
                    <h3>${movie.title}</h3>
                    <p>${movie.release_date}</p>
                    <p>⭐ ${Math.round(movie.vote_average * 10)}%</p>
                </a>
                `;

                // Save scroll position before navigating
                card.addEventListener("click", () => {
                    sessionStorage.setItem("scrollPosition", window.scrollY);
                    sessionStorage.setItem("clickedCardId", `movie-upcoming-${movie.id}`);
                });

                container.appendChild(card);
            });
        })
        .catch(err => {
            console.error("Failed to fetch trending movies", err);
        });

    //////////////////////////////////////////////////////////////

    const choicesInstances = {};  // Store initialized instances

    async function populateFilters(genreSelectId, languageSelectId, regionSelectId) {

      const genreSelect = document.getElementById(genreSelectId);
      const languageSelect = document.getElementById(languageSelectId);
      const regionSelect = document.getElementById(regionSelectId);
    
      // Initialize Choices.js
      const genreChoices = new Choices(genreSelect, {
        removeItemButton: true,
        placeholder: true,
        placeholderValue: "Select genres",
        shouldSort: false,
      });

      const languageChoices = new Choices(languageSelect, {
        removeItemButton: true,
        placeholder: true,
        placeholderValue: "Select languages",
        shouldSort: true,
      });

      const regionChoices = new Choices(regionSelect, {
        removeItemButton: true,
        placeholder: true,
        placeholderValue: "Select regions",
        shouldSort: true,
      });
    
      // Save for later use
      choicesInstances[genreSelectId] = genreChoices;
      choicesInstances[languageSelectId] = languageChoices;
      choicesInstances[regionSelectId] = regionChoices;
    
      try {
        const genreRes = await fetch("/api/v1/genres");
        const genreData = await genreRes.json();
        genreChoices.setChoices(
          genreData.genres.map(g => ({ value: g.id, label: g.name })),
          'value',
          'label',
          false
        );

        const languageRes = await fetch("/api/v1/languages");
        const languageData = await languageRes.json();
        languageChoices.setChoices(
          languageData.map(g => ({ value: g.iso_639_1, label: g.english_name })),
          'value',
          'label',
          false
        );

        const regionRes = await fetch("/api/v1/regions");
        const regionData = await regionRes.json();
        regionChoices.setChoices(
          regionData.map(r => ({ value: r.iso_3166_1, label: r.english_name })),
          'value',
          'label',
          false
        );
      } catch (error) {
        console.error("Failed to load filter", error);
      }
    }

    //////////////////////////////////////////////////////////////

    function setupPopularFilters() {
        const genreChoices = choicesInstances["popular-genre-select"];
        const languageChoices = choicesInstances["popular-language-select"];
        const regionChoices = choicesInstances["popular-region-select"];
        const yearInput = document.getElementById("popular-year-input");
    
        function applyPopularFilters() {
            const genres = genreChoices.getValue(true).join("|");
            const language = languageChoices.getValue(true).join("|");
            const regions = regionChoices.getValue(true).join("|");
            const year = yearInput.value;
    
            const params = new URLSearchParams({
                with_genres: genres,
                language: language,
                region: regions,
                year: year
            });
    
            fetchAndRenderMovies(`/api/v1/discover/popular?${params}`, "movies-popular", "movie-popular");
        }
    
        genreChoices.passedElement.element.addEventListener("change", applyPopularFilters);
        languageChoices.passedElement.element.addEventListener("change", applyPopularFilters);
        regionChoices.passedElement.element.addEventListener("change", applyPopularFilters);

        yearInput.addEventListener("input", applyPopularFilters);
    }        

    //////////////////////////////////////////////////////////////

    function setupTopRatedFilters() {
        const genreChoices = choicesInstances["top-rated-genre-select"];
        const languageChoices = choicesInstances["top-rated-language-select"];
        const regionChoices = choicesInstances["top-rated-region-select"];
        const yearInput = document.getElementById("top-rated-year-input");
    
        function applyTopRatedFilters() {
            const genres = genreChoices.getValue(true).join("|");
            const language = languageChoices.getValue(true).join("|");
            const regions = regionChoices.getValue(true).join("|");
            const year = yearInput.value;
    
            const params = new URLSearchParams({
                with_genres: genres,
                language: language,
                region: regions,
                year: year
            });
    
            fetchAndRenderMovies(`/api/v1/discover/top_rated?${params}`, "movies-top-rated", "movie-top-rated");
        }
    
        genreChoices.passedElement.element.addEventListener("change", applyTopRatedFilters);
        languageChoices.passedElement.element.addEventListener("change", applyTopRatedFilters);
        regionChoices.passedElement.element.addEventListener("change", applyTopRatedFilters);

        yearInput.addEventListener("input", applyTopRatedFilters);
    }    

    //////////////////////////////////////////////////////////////

    function fetchAndRenderMovies(endpointUrl, containerId, cardIdPrefix) {
        fetch(endpointUrl)
          .then(response => response.json())
          .then(data => {
            const container = document.getElementById(containerId);
            container.innerHTML = "";  // Clear previous results
      
            data.forEach(movie => {
              const card = document.createElement("div");
              card.className = "movie-card";
              card.id = `${cardIdPrefix}-${movie.id}`;
              card.setAttribute("data-id", movie.id);
              card.setAttribute("data-type", "movie");

              const poster = movie.poster_path 
                ? `<img src="https://image.tmdb.org/t/p/w500${movie.poster_path}" alt="${movie.title}">`
                : `<div>No Image</div>`;
      
              card.innerHTML = `
                <span class="favorite-heart" onclick="toggleFavorite(this)">🤍</span>
                <a href="/movie/${movie.id}" style="text-decoration: none; color: inherit;">
                    ${poster}
                    <h3>${movie.title}</h3>
                    <p>${movie.release_date}</p>
                    <p>⭐ ${Math.round(movie.vote_average * 10)}%</p>
                </a>
              `;
      
              card.addEventListener("click", () => {
                sessionStorage.setItem("scrollPosition", window.scrollY);
                sessionStorage.setItem("clickedCardId", `${cardIdPrefix}-${movie.id}`);
              });
      
              container.appendChild(card);
            });
          })
          .catch(err => {
            console.error(`Failed to fetch from ${endpointUrl}`, err);
          });
    }

    //////////////////////////////////////////////////////////////

    populateFilters("popular-genre-select", "popular-language-select", "popular-region-select");
    populateFilters("top-rated-genre-select", "top-rated-language-select", "top-rated-region-select");

    setupPopularFilters();
    setupTopRatedFilters();

    fetchAndRenderMovies("/api/v1/discover/popular", "movies-popular", "movie-popular");
    fetchAndRenderMovies("/api/v1/discover/top_rated", "movies-top-rated", "movie-top-rated");

    //////////////////////////////////////////////////////////////

    fetch("/api/v1/discover/horror")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("movies-horror");

            data.forEach(movie => {
                const card = document.createElement("div");
                card.className = "movie-card";
                card.id = `movie-horror-${movie.id}`;
                card.setAttribute("data-id", movie.id);
                card.setAttribute("data-type", "movie");

                const poster = movie.poster_path 
                    ? `<img src="https://image.tmdb.org/t/p/w500${movie.poster_path}" alt="${movie.title}">`
                    : `<div>No Image</div>`;

                card.innerHTML = `
                <span class="favorite-heart" onclick="toggleFavorite(this)">🤍</span>
                <a href="/movie/${movie.id}" style="text-decoration: none; color: inherit;">
                    ${poster}
                    <h3>${movie.title}</h3>
                    <p>${movie.release_date}</p>
                    <p>⭐ ${Math.round(movie.vote_average * 10)}%</p>
                </a>
                `;

                // Save scroll position before navigating
                card.addEventListener("click", () => {
                    sessionStorage.setItem("scrollPosition", window.scrollY);
                    sessionStorage.setItem("clickedCardId", `movie-horror-${movie.id}`);
                });

                container.appendChild(card);
            });
        })
        .catch(err => {
            console.error("Failed to fetch trending movies", err);
        });

    //////////////////////////////////////////////////////////////

    fetch("/api/v1/discover/family_animation")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("movies-family-animation");

            data.forEach(movie => {
                const card = document.createElement("div");
                card.className = "movie-card";
                card.id = `movie-family-animation-${movie.id}`;
                card.setAttribute("data-id", movie.id);
                card.setAttribute("data-type", "movie");

                const poster = movie.poster_path 
                    ? `<img src="https://image.tmdb.org/t/p/w500${movie.poster_path}" alt="${movie.title}">`
                    : `<div>No Image</div>`;

                card.innerHTML = `
                <span class="favorite-heart" onclick="toggleFavorite(this)">🤍</span>
                <a href="/movie/${movie.id}" style="text-decoration: none; color: inherit;">
                    ${poster}
                    <h3>${movie.title}</h3>
                    <p>${movie.release_date}</p>
                    <p>⭐ ${Math.round(movie.vote_average * 10)}%</p>
                </a>
                `;

                // Save scroll position before navigating
                card.addEventListener("click", () => {
                    sessionStorage.setItem("scrollPosition", window.scrollY);
                    sessionStorage.setItem("clickedCardId", `movie-family-animation-${movie.id}`);
                });

                container.appendChild(card);
            });
        })
        .catch(err => {
            console.error("Failed to fetch trending movies", err);
        });

    //////////////////////////////////////////////////////////////

    loadFavorites();

});
